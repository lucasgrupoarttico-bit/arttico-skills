#!/usr/bin/env python3
"""
Relatorio Semanal Tastto - coleta e agregacao (rota de fallback).

A rota preferencial e o MCP oficial da Meta (ver Passo 2 do SKILL.md), que ja
devolve `results` / `cost_per_result` resolvidos por objetivo de campanha. Este
script existe para quando o MCP nao estiver disponivel na sessao.

Puxa insights no nivel de ad, classifica cada linha em ToF/MoF/BoF pelo conta.yaml
e agrega. Puxa tambem a quebra diaria por campanha, que e o que revela parada de
entrega (etapa ativa com R$0 em dias seguidos).

Uso:
    coletar.py                                   # janela padrao: D-7 a D-1
    coletar.py --desde 2026-07-30 --ate 2026-08-05
    coletar.py --saida .cache/semana.json
    coletar.py --descobrir                       # lista campanhas e action_types
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAMPOS_BASE = [
    "campaign_id", "campaign_name",
    "adset_id", "adset_name",
    "ad_id", "ad_name",
    "spend", "impressions", "clicks", "ctr", "cpc", "cpm",
    "reach", "frequency",
    "inline_link_clicks", "inline_link_click_ctr",
    "actions", "cost_per_action_type",
]

ETAPAS_ORDEM = ["ToF", "MoF", "BoF"]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def carregar_config():
    import yaml
    caminho = os.path.join(SKILL_DIR, "conta.yaml")
    if not os.path.exists(caminho):
        erro(f"conta.yaml nao encontrado em {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def carregar_env():
    """Procura o .env do meta-ads-ratos (projeto primeiro, depois home)."""
    candidatos = [
        os.path.join(SKILL_DIR, "..", "meta-ads-ratos", ".env"),
        os.path.expanduser("~/.claude/skills/meta-ads-ratos/.env"),
    ]
    for c in candidatos:
        c = os.path.abspath(c)
        if not os.path.exists(c):
            continue
        valores = {}
        with open(c, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                k, v = linha.split("=", 1)
                valores[k.strip()] = v.strip().strip('"').strip("'")
        if valores.get("META_ADS_TOKEN"):
            return valores, c
    return {}, None


def erro(msg, extra=None):
    payload = {"erro": True, "mensagem": msg}
    if extra:
        payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(1)


def campos_extras(cfg):
    """Campos de topo pedidos pelo conta.yaml (resultado tipo 'campo')."""
    extras = []
    for etapa in ETAPAS_ORDEM:
        r = cfg["etapas"][etapa].get("resultado") or {}
        if r.get("tipo") == "campo" and r.get("valor"):
            extras.append(r["valor"])
    return sorted(set(extras))


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

def puxar_insights(conta_id, desde, ate, token, app_id, campos,
                   nivel="ad", time_increment=None):
    try:
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.adaccount import AdAccount
    except ImportError:
        erro("SDK facebook-business nao instalado. Rode: pip install facebook-business")

    FacebookAdsApi.init(app_id=app_id or None, access_token=token)

    params = {
        "level": nivel,
        "time_range": {"since": desde, "until": ate},
        "limit": 200,
        "action_report_time": "conversion",
    }
    if time_increment:
        params["time_increment"] = time_increment

    try:
        cursor = AdAccount(conta_id).get_insights(fields=campos, params=params)
        linhas = [dict(r) for r in cursor]
        while cursor.load_next_page():
            linhas.extend(dict(r) for r in cursor)
    except Exception as e:
        detalhe = getattr(e, "api_error_message", lambda: str(e))
        msg = detalhe() if callable(detalhe) else str(e)
        codigo = getattr(e, "api_error_code", lambda: None)
        codigo = codigo() if callable(codigo) else None
        dica = {
            190: "Token expirado. Gere um novo no Graph API Explorer e atualize o .env.",
            200: "Token sem permissao ads_read nessa conta.",
            100: ("Parametro ou campo invalido. Se a mensagem citar um campo de "
                  "resultado do conta.yaml, use a rota do MCP - ela resolve "
                  "`results` sozinha, sem depender do nome do campo no SDK."),
        }.get(codigo, "")
        erro(f"Falha ao ler a conta ({nivel}): {msg}", {"codigo": codigo, "dica": dica})

    return linhas


# ---------------------------------------------------------------------------
# Classificacao
# ---------------------------------------------------------------------------

def compilar_padroes(cfg):
    return {e: [re.compile(p, re.IGNORECASE)
                for p in (cfg["etapas"][e].get("padroes") or [])]
            for e in ETAPAS_ORDEM}


def mapa_ids(cfg):
    m = {}
    for etapa in ETAPAS_ORDEM:
        for cid in (cfg["etapas"][etapa].get("campanha_ids") or []):
            m[str(cid)] = etapa
    return m


def classificar(linha, padroes, ids):
    """ID de campanha primeiro; se nao casar, regex por campanha/conjunto/ad."""
    cid = str(linha.get("campaign_id") or "")
    if cid in ids:
        return ids[cid], f"campaign_id={cid}"

    for campo in ("campaign_name", "adset_name", "ad_name"):
        nome = linha.get(campo) or ""
        for etapa in ETAPAS_ORDEM:
            for rx in padroes[etapa]:
                if rx.search(nome):
                    return etapa, f"{campo}~{rx.pattern}"
    return "NAO_CLASSIFICADO", ""


def ler_resultado(linha, spec):
    """Le o Resultado da linha conforme o spec do conta.yaml.

    tipo 'campo' -> campo de topo da linha (ex: total_profile_visits)
    tipo 'acao'  -> soma dentro de actions, tentando valor e depois alternativas
    """
    if not spec:
        return None
    tipo = spec.get("tipo")

    if tipo == "campo":
        v = linha.get(spec.get("valor"))
        return f(v, None) if v is not None else None

    if tipo == "acao":
        acoes = {a.get("action_type"): a.get("value") for a in (linha.get("actions") or [])}
        for chave in [spec.get("valor")] + list(spec.get("alternativas") or []):
            if chave in acoes:
                return f(acoes[chave], 0.0)
        return 0.0 if acoes else None

    return None


def f(v, padrao=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return padrao


def relevante(linha):
    """Descarta linhas zeradas - so poluem o relatorio de nao classificados."""
    return f(linha.get("spend")) > 0 or f(linha.get("impressions")) > 0


# ---------------------------------------------------------------------------
# Agregacao
# ---------------------------------------------------------------------------

def agregar(linhas, cfg, padroes, ids):
    etapas = {e: {
        "rotulo": cfg["etapas"][e]["rotulo"],
        "cor": cfg["etapas"][e]["cor"],
        "resultado_rotulo": cfg["etapas"][e]["resultado_rotulo"],
        "gasto": 0.0, "impressoes": 0, "cliques": 0, "alcance": 0,
        "resultado": 0.0, "resultado_disponivel": False,
        "ads": [],
    } for e in ETAPAS_ORDEM}

    nao_classificados = []

    for linha in linhas:
        if not relevante(linha):
            continue

        etapa, motivo = classificar(linha, padroes, ids)
        if etapa == "NAO_CLASSIFICADO":
            nao_classificados.append({
                "campanha": linha.get("campaign_name"),
                "campanha_id": linha.get("campaign_id"),
                "conjunto": linha.get("adset_name"),
                "ad": linha.get("ad_name"),
                "gasto": round(f(linha.get("spend")), 2),
            })
            continue

        alvo = etapas[etapa]
        gasto = f(linha.get("spend"))
        impressoes = int(f(linha.get("impressions")))
        cliques = int(f(linha.get("clicks")))

        alvo["gasto"] += gasto
        alvo["impressoes"] += impressoes
        alvo["cliques"] += cliques
        alvo["alcance"] += int(f(linha.get("reach")))

        res = ler_resultado(linha, cfg["etapas"][etapa].get("resultado"))
        if res is not None:
            alvo["resultado"] += res
            alvo["resultado_disponivel"] = True

        alvo["ads"].append({
            "ad": linha.get("ad_name"),
            "conjunto": linha.get("adset_name"),
            "gasto": round(gasto, 2),
            "impressoes": impressoes,
            "cliques": cliques,
            "ctr": round(f(linha.get("ctr")), 2),
            "cpm": round(f(linha.get("cpm")), 2),
            "frequencia": round(f(linha.get("frequency")), 2),
            "resultado": res,
            "custo_resultado": round(gasto / res, 2) if res else None,
            "classificado_por": motivo,
        })

    for e in ETAPAS_ORDEM:
        d = etapas[e]
        d["ctr"] = round(d["cliques"] / d["impressoes"] * 100, 2) if d["impressoes"] else None
        d["cpm"] = round(d["gasto"] / d["impressoes"] * 1000, 2) if d["impressoes"] else None
        d["custo"] = (round(d["gasto"] / d["resultado"], 2)
                      if d["resultado_disponivel"] and d["resultado"] else None)
        d["resultado"] = int(d["resultado"]) if d["resultado_disponivel"] else None
        d["gasto"] = round(d["gasto"], 2)
        d["ads"].sort(key=lambda a: a["gasto"], reverse=True)

        # A3 - concentracao do criativo lider, agrupando versoes de mesmo nome
        por_nome = defaultdict(float)
        for a in d["ads"]:
            por_nome[a["ad"] or "(sem nome)"] += a["resultado"] or 0
        total_res = sum(por_nome.values())
        if total_res:
            nome, valor = max(por_nome.items(), key=lambda kv: kv[1])
            d["concentracao_lider"] = {
                "ad": nome,
                "resultado": int(valor),
                "fatia_pct": round(valor / total_res * 100, 1),
            }
        else:
            d["concentracao_lider"] = None

    return etapas, nao_classificados


def agregar_diario(linhas_diarias, cfg, padroes, ids, desde, ate):
    """Gasto por etapa por dia + dias sem entrega (check A8)."""
    d1, d2 = date.fromisoformat(desde), date.fromisoformat(ate)
    todos = [(d1 + timedelta(days=i)).isoformat() for i in range((d2 - d1).days + 1)]

    por_dia = {dia: {e: 0.0 for e in ETAPAS_ORDEM} for dia in todos}
    for linha in linhas_diarias:
        dia = linha.get("date_start")
        if dia not in por_dia:
            continue
        etapa, _ = classificar(linha, padroes, ids)
        if etapa in ETAPAS_ORDEM:
            por_dia[dia][etapa] += f(linha.get("spend"))

    for dia in por_dia:
        for e in ETAPAS_ORDEM:
            por_dia[dia][e] = round(por_dia[dia][e], 2)

    sem_entrega = {
        e: [dia for dia in todos if por_dia[dia][e] == 0]
        for e in ETAPAS_ORDEM
    }
    return por_dia, sem_entrega


def montar_saida(cfg, desde, ate, etapas, nao_classificados, por_dia, sem_entrega, qtd):
    d1, d2 = date.fromisoformat(desde), date.fromisoformat(ate)
    dias = (d2 - d1).days + 1

    gasto_total = round(sum(etapas[e]["gasto"] for e in ETAPAS_ORDEM), 2)
    leads = etapas["BoF"]["resultado"]

    return {
        "conta": cfg["meta"]["conta_anuncio"],
        "nome_conta": cfg["meta"]["nome_conta"],
        "periodo": {"inicio": desde, "fim": ate, "dias": dias, "parcial": dias != 7},
        "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "etapas": etapas,
        "total": {
            "gasto": gasto_total,
            "gasto_diario": round(gasto_total / dias, 2) if dias else None,
            "leads": leads,
            "cpl_bof": round(etapas["BoF"]["gasto"] / leads, 2) if leads else None,
            "cpl_full_funnel": round(gasto_total / leads, 2) if leads else None,
        },
        "entrega_por_dia": por_dia,
        "dias_sem_entrega": sem_entrega,
        "metas": cfg["metas"],
        "nao_classificados": nao_classificados,
        "qtd_linhas_api": qtd,
    }


# ---------------------------------------------------------------------------
# Descoberta
# ---------------------------------------------------------------------------

def descobrir(linhas):
    campanhas = defaultdict(lambda: {"id": None, "gasto": 0.0, "conjuntos": set(), "ads": set()})
    tipos_acao = defaultdict(float)

    for l in linhas:
        if not relevante(l):
            continue
        c = l.get("campaign_name") or "(sem nome)"
        campanhas[c]["id"] = l.get("campaign_id")
        campanhas[c]["gasto"] += f(l.get("spend"))
        campanhas[c]["conjuntos"].add(l.get("adset_name") or "")
        campanhas[c]["ads"].add(l.get("ad_name") or "")
        for a in l.get("actions") or []:
            tipos_acao[a.get("action_type")] += f(a.get("value"))

    return {
        "campanhas": [
            {"nome": n, "id": v["id"], "gasto": round(v["gasto"], 2),
             "conjuntos": sorted(x for x in v["conjuntos"] if x),
             "ads": sorted(x for x in v["ads"] if x)}
            for n, v in sorted(campanhas.items(), key=lambda kv: -kv[1]["gasto"])
        ],
        "action_types": [
            {"action_type": k, "total": round(v, 2)}
            for k, v in sorted(tipos_acao.items(), key=lambda kv: -kv[1])
        ],
        "como_usar": (
            "Copie os IDs de campanha pro bloco campanha_ids do conta.yaml e confira "
            "se o action_type de cada etapa bate com o bloco `resultado`. Em 05/08/2026 "
            "os indicadores da conta eram: ToF total_profile_visits (campo de topo), "
            "MoF omni_landing_page_view (acao), BoF lead / leadgen.other (acao)."
        ),
    }


# ---------------------------------------------------------------------------
# Janela
# ---------------------------------------------------------------------------

def janela_padrao(hoje=None):
    """Sete dias fechados terminando ONTEM (D-7 a D-1).

    A serie roda toda quinta. Gerando em 06/08 (quinta), a janela e 30/07 a 05/08,
    ou seja quinta a quarta.

    Terminar em D-1 e proposital: nenhum dia entra com o dia ainda em curso. Foi
    exatamente esse o erro do relatorio parcial de 31/07, que capturou o ultimo dia
    pela metade e subestimou o ToF em R$6,30.
    """
    hoje = hoje or date.today()
    fim = hoje - timedelta(days=1)
    inicio = fim - timedelta(days=6)
    return inicio.isoformat(), fim.isoformat()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Coleta semanal Tastto")
    p.add_argument("--desde", help="AAAA-MM-DD (default: os 7 dias fechados ate ontem)")
    p.add_argument("--ate", help="AAAA-MM-DD")
    p.add_argument("--conta", help="Sobrescreve a conta do conta.yaml")
    p.add_argument("--saida", help="Caminho do JSON de saida (default: stdout)")
    p.add_argument("--descobrir", action="store_true",
                   help="Lista campanhas, IDs e action_types em vez de agregar")
    args = p.parse_args()

    cfg = carregar_config()

    desde, ate = args.desde, args.ate
    if not desde or not ate:
        desde, ate = janela_padrao()

    for rotulo, valor in (("--desde", desde), ("--ate", ate)):
        try:
            date.fromisoformat(valor)
        except ValueError:
            erro(f"{rotulo} invalido: {valor}. Use AAAA-MM-DD.")
    if date.fromisoformat(ate) < date.fromisoformat(desde):
        erro("--ate e anterior a --desde.")
    if date.fromisoformat(ate) >= date.today():
        erro("A janela precisa terminar em D-1 ou antes. Dia em curso entra pela "
             "metade e contamina o relatorio.", {"ate": ate, "hoje": date.today().isoformat()})

    env, caminho_env = carregar_env()
    token = env.get("META_ADS_TOKEN") or os.environ.get("META_ADS_TOKEN")
    app_id = env.get("META_APP_ID") or os.environ.get("META_APP_ID")
    if not token:
        erro("Token da Meta nao encontrado.", {
            "procurado_em": [
                os.path.abspath(os.path.join(SKILL_DIR, "..", "meta-ads-ratos", ".env")),
                os.path.expanduser("~/.claude/skills/meta-ads-ratos/.env"),
                "variavel de ambiente META_ADS_TOKEN",
            ],
            "dica": "Prefira o MCP oficial da Meta. Este script e fallback.",
        })

    conta = args.conta or cfg["meta"]["conta_anuncio"]
    if not conta.startswith("act_"):
        conta = "act_" + conta

    campos = CAMPOS_BASE + campos_extras(cfg)
    linhas = puxar_insights(conta, desde, ate, token, app_id, campos, nivel="ad")

    if args.descobrir:
        resultado = {
            "modo": "descoberta", "conta": conta,
            "periodo": {"inicio": desde, "fim": ate},
            "env": caminho_env,
            **descobrir(linhas),
        }
    else:
        padroes = compilar_padroes(cfg)
        ids = mapa_ids(cfg)
        etapas, nao_classificados = agregar(linhas, cfg, padroes, ids)

        diarias = puxar_insights(
            conta, desde, ate, token, app_id,
            ["campaign_id", "campaign_name", "spend", "impressions"],
            nivel="campaign", time_increment=1,
        )
        por_dia, sem_entrega = agregar_diario(diarias, cfg, padroes, ids, desde, ate)

        resultado = montar_saida(cfg, desde, ate, etapas, nao_classificados,
                                 por_dia, sem_entrega, len(linhas))

        avisos = []
        faltando = [e for e in ETAPAS_ORDEM if etapas[e]["resultado"] is None]
        if faltando:
            avisos.append(
                f"Sem Resultado apurado para: {', '.join(faltando)}. Confira o bloco "
                "`resultado` dessas etapas no conta.yaml (rode --descobrir)."
            )
        for e, dias in sem_entrega.items():
            if dias:
                avisos.append(f"{e} sem entrega em {len(dias)} dia(s): {', '.join(dias)}.")
        if nao_classificados:
            avisos.append(f"{len(nao_classificados)} linha(s) com gasto nao classificadas.")
        if avisos:
            resultado["avisos"] = avisos

    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
        with open(args.saida, "w", encoding="utf-8") as fh:
            fh.write(texto)
        print(f"Salvo em {args.saida}")
        print(texto[:1800])
    else:
        print(texto)


if __name__ == "__main__":
    main()
