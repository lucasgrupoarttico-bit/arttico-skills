#!/usr/bin/env python3
"""
Apify Ratos - Biblioteca compartilhada
.env loader (sem dependencias externas) + cliente HTTP da API da Apify + helpers de output.

Usa apenas a stdlib (urllib). Nao precisa instalar nada.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# .../scripts/lib/__init__.py -> sobe 3 niveis -> pasta da skill
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Raiz do workspace: .claude/skills/apify -> sobe 3 -> raiz
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SKILL_DIR)))

_ENV_SEARCH_PATHS = [
    os.path.join(SKILL_DIR, ".env"),
    os.path.expanduser("~/.claude/skills/apify/.env"),
]

# ---------------------------------------------------------------------------
# Actor IDs padrao (slug owner~nome). Podem ser sobrescritos no .env.
# ---------------------------------------------------------------------------

DEFAULT_ACTORS = {
    "google_maps": "compass~crawler-google-places",
    "instagram": "apify~instagram-scraper",
    "tiktok": "clockworks~tiktok-scraper",
    "facebook_ads": "apify~facebook-ads-scraper",
}


# ---------------------------------------------------------------------------
# .env loader
# ---------------------------------------------------------------------------

def _parse_env(path):
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def load_env():
    """Carrega o primeiro .env encontrado nos caminhos de busca."""
    for env_path in _ENV_SEARCH_PATHS:
        if os.path.isfile(env_path):
            _parse_env(env_path)
            return env_path
    return None


def get_token():
    load_env()
    token = os.environ.get("APIFY_TOKEN", "").strip()
    if not token:
        fail(
            "APIFY_TOKEN nao configurado.\n"
            "  Crie o arquivo .claude/skills/apify/.env com a linha:\n"
            "    APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxx\n"
            "  Pegue o token em: https://console.apify.com/account/integrations"
        )
    return token


def get_actor(kind):
    """Resolve o actor id, permitindo override via .env (ex: APIFY_ACTOR_INSTAGRAM)."""
    load_env()
    override = os.environ.get(f"APIFY_ACTOR_{kind.upper()}", "").strip()
    return override or DEFAULT_ACTORS[kind]


# ---------------------------------------------------------------------------
# Cliente HTTP da Apify
# ---------------------------------------------------------------------------

API_BASE = "https://api.apify.com/v2"


def run_actor(actor_id, run_input, *, timeout_secs=300, memory_mbytes=2048):
    """
    Roda um actor de forma sincrona e retorna os itens do dataset (lista de dicts).

    Usa o endpoint run-sync-get-dataset-items, que bloqueia ate o run terminar
    (ou ate o timeout) e devolve os resultados direto.
    """
    token = get_token()
    params = urllib.parse.urlencode({
        "token": token,
        "timeout": int(timeout_secs),
        "memory": int(memory_mbytes),
    })
    url = f"{API_BASE}/acts/{actor_id}/run-sync-get-dataset-items?{params}"

    body = json.dumps(run_input).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    log(f"Rodando actor '{actor_id}'... (pode levar de 30s a alguns minutos)")
    t0 = time.time()
    try:
        # +30s de folga sobre o timeout do actor pra rede nao cortar antes
        with urllib.request.urlopen(req, timeout=timeout_secs + 30) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        if exc.code == 401:
            fail("Token invalido (401). Confira APIFY_TOKEN no .env.")
        if exc.code == 403:
            fail(
                "Acesso negado (403). Causa mais comum: limite mensal de uso da conta Apify\n"
                "  atingido ('Monthly usage hard limit exceeded'). Verifique em\n"
                "  https://console.apify.com/billing e aumente o limite ou aguarde o ciclo renovar."
            )
        if exc.code == 404:
            fail(
                f"Actor '{actor_id}' nao encontrado (404).\n"
                "  Verifique o slug ou ajuste no .env (ex: APIFY_ACTOR_INSTAGRAM=...)."
            )
        fail(f"Erro HTTP {exc.code} da Apify:\n{detail[:1500]}")
    except urllib.error.URLError as exc:
        fail(f"Falha de rede ao chamar a Apify: {exc.reason}")

    elapsed = time.time() - t0
    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        fail(f"Resposta inesperada da Apify:\n{raw[:1000]}")

    if not isinstance(items, list):
        items = [items]

    # Alguns actors devolvem um item de erro em vez de falhar o run (ex: perfil privado).
    err_items = [it for it in items if isinstance(it, dict) and "error" in it]
    if err_items and len(err_items) == len(items):
        first = err_items[0]
        log(
            "Actor retornou erro (nenhum dado): "
            f"{first.get('error')} - {first.get('errorDescription', '')}"
        )
    log(f"Concluido em {elapsed:.0f}s. {len(items)} item(ns) retornado(s).")
    return items


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def log(msg):
    print(f"[apify] {msg}", file=sys.stderr)


def fail(msg, code=1):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(code)


def slugify(text):
    keep = "abcdefghijklmnopqrstuvwxyz0123456789-"
    s = "".join(c if c in keep else "-" for c in (text or "").lower())
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-") or "sem-nome"


def resolve_output_dir(cliente=None):
    """
    Decide onde salvar: clientes/<cliente>/apify/ se cliente informado,
    senao dados/apify/.
    """
    if cliente:
        base = os.path.join(WORKSPACE_ROOT, "clientes", slugify(cliente), "apify")
    else:
        base = os.path.join(WORKSPACE_ROOT, "dados", "apify")
    os.makedirs(base, exist_ok=True)
    return base


def save_results(items, fonte, *, cliente=None, label=""):
    """Salva o JSON e devolve o caminho."""
    out_dir = resolve_output_dir(cliente)
    date = time.strftime("%Y-%m-%d")
    parts = [fonte, slugify(label)] if label else [fonte]
    fname = f"{'-'.join(parts)}-{date}.json"
    path = os.path.join(out_dir, fname)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(items, fh, ensure_ascii=False, indent=2)
    log(f"Salvo em: {path}")
    return path
