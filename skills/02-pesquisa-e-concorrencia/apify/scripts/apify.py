#!/usr/bin/env python3
"""
Apify Ratos - CLI

Roda actors da Apify pra coletar dados de 4 fontes e salva o JSON na pasta do cliente.

Uso:
  python apify.py google-maps  --query "dentista em Natal RN" --max 50 [--cliente "Nome"]
  python apify.py instagram     --profile usuario --type posts --limit 30 [--cliente "Nome"]
  python apify.py instagram     --hashtag marketing --limit 30
  python apify.py tiktok        --profile usuario --limit 30 [--cliente "Nome"]
  python apify.py tiktok        --search "palavra-chave" --limit 30
  python apify.py tiktok        --hashtag marketing --limit 30
  python apify.py facebook-ads  --term "marca concorrente" --country BR --max 50 [--cliente "Nome"]
  python apify.py facebook-ads  --page-url "https://www.facebook.com/ads/library/?...page..." --max 50

Saida: clientes/<cliente>/apify/<fonte>-<label>-<data>.json (ou dados/apify/ se sem cliente)
Imprime no final um resumo legivel + o caminho do arquivo salvo.
"""

import argparse
import sys
import urllib.parse

import lib


# ---------------------------------------------------------------------------
# Google Maps  (leads: empresas, telefone, site, avaliacoes)
# ---------------------------------------------------------------------------

def cmd_google_maps(args):
    run_input = {
        "searchStringsArray": [args.query],
        "maxCrawledPlacesPerSearch": args.max,
        "language": args.language,
    }
    if args.country:
        run_input["countryCode"] = args.country.lower()

    items = lib.run_actor(lib.get_actor("google_maps"), run_input, timeout_secs=args.timeout)
    path = lib.save_results(items, "google-maps", cliente=args.cliente, label=args.query)

    print(f"\n=== GOOGLE MAPS — {len(items)} resultado(s) para '{args.query}' ===")
    for it in items[:25]:
        nome = it.get("title", "?")
        tel = it.get("phone") or it.get("phoneUnformatted") or "-"
        site = it.get("website") or "-"
        nota = it.get("totalScore", "-")
        avals = it.get("reviewsCount", "-")
        cat = it.get("categoryName") or "-"
        print(f"- {nome} | {cat} | nota {nota} ({avals} avals) | tel {tel} | {site}")
    if len(items) > 25:
        print(f"... +{len(items) - 25} no arquivo.")
    print(f"\nArquivo: {path}")


# ---------------------------------------------------------------------------
# Google Maps — Auditoria de ficha (rankeamento no nicho)
# ---------------------------------------------------------------------------

def _norm(s):
    return "".join(c for c in (s or "").lower() if c.isalnum() or c == " ").strip()


def _peak_time(it):
    """Extrai o horario de pico do popularTimesHistogram (dia + hora com maior ocupacao)."""
    hist = it.get("popularTimesHistogram") or {}
    best = None
    for day, slots in hist.items():
        if not isinstance(slots, list):
            continue
        for slot in slots:
            occ = slot.get("occupancyPercent", 0) or 0
            if best is None or occ > best[2]:
                best = (day, slot.get("hour"), occ)
    if best and best[2] > 0:
        return f"{best[0]} {best[1]}h ({best[2]}%)"
    return "nao informado"


def _hours_summary(it):
    oh = it.get("openingHours") or []
    if not oh:
        return "nao informado"
    return f"{len(oh)} dia(s) com horario"


def _posts_count(it):
    # Alguns actors expoem um numero direto; outros, a lista de posts. So queremos a quantidade.
    for key in ("postsCount", "updatesCount", "ownerUpdatesCount"):
        v = it.get(key)
        if isinstance(v, int):
            return v
    for key in ("ownerUpdates", "updatesFromCustomers", "posts", "placePosts"):
        v = it.get(key)
        if isinstance(v, list):
            return len(v)
    return None


def _ficha_block(idx, it, marca=""):
    nome = it.get("title", "?")
    cat = it.get("categoryName") or "-"
    nota = it.get("totalScore", "-")
    avals = it.get("reviewsCount", "-")
    desc = (it.get("description") or "").strip()
    desc_txt = (desc[:120] + "...") if len(desc) > 120 else (desc or "SEM descricao")
    posts = _posts_count(it)
    posts_txt = f"{posts} post(s)" if posts is not None else "posts n/d"
    lines = [
        f"{idx:>2}. {nome}{marca}",
        f"    categoria: {cat}",
        f"    nota: {nota} | avaliacoes: {avals}",
        f"    descricao: {desc_txt}",
        f"    horario de funcionamento: {_hours_summary(it)}",
        f"    horario de pico: {_peak_time(it)}",
        f"    postagens: {posts_txt}",
    ]
    return "\n".join(lines)


def cmd_google_maps_audit(args):
    run_input = {
        "searchStringsArray": [args.query],
        "maxCrawledPlacesPerSearch": args.max,
        "language": args.language,
        "scrapePlaceDetailPage": True,
    }
    if args.country:
        run_input["countryCode"] = args.country.lower()

    items = lib.run_actor(lib.get_actor("google_maps"), run_input, timeout_secs=args.timeout)
    label = (args.target or args.query)
    path = lib.save_results(items, "google-maps-audit", cliente=args.cliente, label=label)

    # A ordem retornada pelo actor segue o rankeamento do Google Maps para a busca.
    alvo_norm = _norm(args.target) if args.target else None
    alvo_pos = None

    print(f"\n=== AUDITORIA GOOGLE MAPS — '{args.query}' ({len(items)} fichas) ===\n")
    for idx, it in enumerate(items, start=1):
        marca = ""
        if alvo_norm and alvo_norm in _norm(it.get("title", "")):
            marca = "   <<< FICHA DO CLIENTE"
            alvo_pos = alvo_pos or idx
        if idx <= 20 or marca:
            print(_ficha_block(idx, it, marca))
            print()
    if len(items) > 20:
        print(f"... +{len(items) - 20} fichas no arquivo (analise completa no JSON).\n")

    # Medias do topo (referencia pro plano de acao)
    topo = items[:5]
    notas = [it.get("totalScore") for it in topo if isinstance(it.get("totalScore"), (int, float))]
    avals = [it.get("reviewsCount") for it in topo if isinstance(it.get("reviewsCount"), (int, float))]
    if notas:
        print(f">>> Top 5 do nicho: nota media {sum(notas)/len(notas):.2f} | "
              f"media de avaliacoes {sum(avals)/len(avals):.0f}")

    if args.target:
        if alvo_pos:
            acima = alvo_pos - 1
            print(f">>> '{args.target}' esta na POSICAO {alvo_pos} de {len(items)} no nicho "
                  f"({acima} concorrente(s) acima).")
        else:
            print(f">>> '{args.target}' NAO apareceu nas {len(items)} fichas da busca "
                  "(baixa visibilidade local para esse termo).")
    print(f"\nArquivo: {path}")


# ---------------------------------------------------------------------------
# Instagram  (perfil/posts ou hashtag)
# ---------------------------------------------------------------------------

def cmd_instagram(args):
    if not args.profile and not args.hashtag:
        lib.fail("Informe --profile USUARIO ou --hashtag TAG.")

    if args.profile:
        url = f"https://www.instagram.com/{args.profile.lstrip('@')}/"
        run_input = {
            "directUrls": [url],
            "resultsType": args.type,
            "resultsLimit": args.limit,
        }
        label = args.profile.lstrip("@")
    else:
        tag = args.hashtag.lstrip("#")
        run_input = {
            "directUrls": [f"https://www.instagram.com/explore/tags/{tag}/"],
            "resultsType": "posts",
            "resultsLimit": args.limit,
        }
        label = "tag-" + tag

    items = lib.run_actor(lib.get_actor("instagram"), run_input, timeout_secs=args.timeout)
    path = lib.save_results(items, "instagram", cliente=args.cliente, label=label)

    print(f"\n=== INSTAGRAM — {len(items)} item(ns) ({label}) ===")
    for it in items[:25]:
        tipo = it.get("type", "?")
        likes = it.get("likesCount", "-")
        coments = it.get("commentsCount", "-")
        cap = (it.get("caption") or "").replace("\n", " ")[:80]
        link = it.get("url", "-")
        print(f"- [{tipo}] {likes} likes / {coments} coments | {cap} | {link}")
    if len(items) > 25:
        print(f"... +{len(items) - 25} no arquivo.")
    print(f"\nArquivo: {path}")


# ---------------------------------------------------------------------------
# TikTok  (perfil, hashtag ou busca)
# ---------------------------------------------------------------------------

def cmd_tiktok(args):
    run_input = {"resultsPerPage": args.limit}
    if args.profile:
        run_input["profiles"] = [args.profile.lstrip("@")]
        label = args.profile.lstrip("@")
    elif args.hashtag:
        run_input["hashtags"] = [args.hashtag.lstrip("#")]
        label = "tag-" + args.hashtag.lstrip("#")
    elif args.search:
        run_input["searchQueries"] = [args.search]
        label = "busca-" + args.search
    else:
        lib.fail("Informe --profile, --hashtag ou --search.")

    items = lib.run_actor(lib.get_actor("tiktok"), run_input, timeout_secs=args.timeout)
    path = lib.save_results(items, "tiktok", cliente=args.cliente, label=label)

    print(f"\n=== TIKTOK — {len(items)} video(s) ({label}) ===")
    for it in items[:25]:
        views = it.get("playCount", "-")
        likes = it.get("diggCount", "-")
        shares = it.get("shareCount", "-")
        autor = (it.get("authorMeta") or {}).get("name", "-")
        desc = (it.get("text") or "").replace("\n", " ")[:70]
        link = it.get("webVideoUrl", "-")
        print(f"- @{autor} | {views} views / {likes} likes / {shares} shares | {desc} | {link}")
    if len(items) > 25:
        print(f"... +{len(items) - 25} no arquivo.")
    print(f"\nArquivo: {path}")


# ---------------------------------------------------------------------------
# Facebook Ad Library  (anuncios ativos de concorrentes)
# ---------------------------------------------------------------------------

def _ad_library_url(term, country):
    q = urllib.parse.urlencode({
        "active_status": "all",
        "ad_type": "all",
        "country": country.upper(),
        "q": term,
        "search_type": "keyword_unordered",
        "media_type": "all",
    })
    return f"https://www.facebook.com/ads/library/?{q}"


def cmd_facebook_ads(args):
    if args.page_url:
        url = args.page_url
        label = "page"
    elif args.term:
        url = _ad_library_url(args.term, args.country)
        label = args.term
    else:
        lib.fail("Informe --term TERMO (com --country) ou --page-url URL.")

    run_input = {
        "startUrls": [{"url": url, "method": "GET"}],
        "count": args.max,
    }

    items = lib.run_actor(lib.get_actor("facebook_ads"), run_input, timeout_secs=args.timeout)
    path = lib.save_results(items, "facebook-ads", cliente=args.cliente, label=label)

    print(f"\n=== FACEBOOK AD LIBRARY — {len(items)} anuncio(s) ({label}) ===")
    for it in items[:25]:
        pagina = it.get("pageName") or "-"
        snap = it.get("snapshot") or {}
        corpo = ""
        if isinstance(snap, dict):
            body = snap.get("body")
            if isinstance(body, dict):
                corpo = (body.get("text") or "")
        corpo = corpo.replace("\n", " ")[:90]
        ativo = it.get("isActive", "-")
        link = it.get("url") or it.get("adLibraryUrl") or "-"
        print(f"- {pagina} | ativo={ativo} | {corpo} | {link}")
    if len(items) > 25:
        print(f"... +{len(items) - 25} no arquivo.")
    print(f"\nArquivo: {path}")


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(description="Apify Ratos - coleta de dados via Apify")
    sub = p.add_subparsers(dest="cmd", required=True)

    common = lambda sp: (
        sp.add_argument("--cliente", help="Nome do cliente (define a pasta de saida)"),
        sp.add_argument("--timeout", type=int, default=300, help="Timeout do actor em segundos"),
    )

    gm = sub.add_parser("google-maps", help="Leads do Google Maps")
    gm.add_argument("--query", required=True, help="Ex: 'dentista em Natal RN'")
    gm.add_argument("--max", type=int, default=50, help="Maximo de lugares")
    gm.add_argument("--language", default="pt-BR", help="Idioma (pt-BR, es, en...)")
    gm.add_argument("--country", default="br", help="Codigo do pais (br, ar, cl, mx)")
    common(gm)
    gm.set_defaults(func=cmd_google_maps)

    ga = sub.add_parser("google-maps-audit", help="Auditoria de ficha: rankeamento no nicho")
    ga.add_argument("--query", required=True, help="Nicho + regiao. Ex: 'dentista em Natal RN'")
    ga.add_argument("--target", help="Nome da ficha auditada (pra achar a posicao no ranking)")
    ga.add_argument("--max", type=int, default=50, help="Quantas fichas do nicho coletar")
    ga.add_argument("--language", default="pt-BR", help="Idioma (pt-BR, es, en...)")
    ga.add_argument("--country", default="br", help="Codigo do pais (br, ar, cl, mx)")
    common(ga)
    ga.set_defaults(func=cmd_google_maps_audit)

    ig = sub.add_parser("instagram", help="Perfil/posts ou hashtag do Instagram")
    ig.add_argument("--profile", help="Usuario (sem @)")
    ig.add_argument("--hashtag", help="Hashtag (sem #)")
    ig.add_argument("--type", default="posts", choices=["posts", "details", "reels", "stories"])
    ig.add_argument("--limit", type=int, default=30)
    common(ig)
    ig.set_defaults(func=cmd_instagram)

    tk = sub.add_parser("tiktok", help="Perfil, hashtag ou busca no TikTok")
    tk.add_argument("--profile", help="Usuario (sem @)")
    tk.add_argument("--hashtag", help="Hashtag (sem #)")
    tk.add_argument("--search", help="Palavra-chave de busca")
    tk.add_argument("--limit", type=int, default=30)
    common(tk)
    tk.set_defaults(func=cmd_tiktok)

    fb = sub.add_parser("facebook-ads", help="Anuncios ativos no Meta Ad Library")
    fb.add_argument("--term", help="Termo/marca pra buscar no Ad Library")
    fb.add_argument("--country", default="BR", help="Pais do Ad Library (BR, AR, CL, MX)")
    fb.add_argument("--page-url", help="URL pronta do Ad Library (alternativa ao --term)")
    fb.add_argument("--max", type=int, default=50, help="Maximo de anuncios")
    common(fb)
    fb.set_defaults(func=cmd_facebook_ads)

    return p


def main():
    # Console do Windows costuma ser cp1252 e quebra acentos no resumo. Forca UTF-8.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
