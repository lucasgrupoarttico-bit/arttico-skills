#!/usr/bin/env python3
"""
Verifica o status do GitHub Actions (deploy) do repositorio atual.

Descobre owner/repo pelo `git remote get-url origin`, pega o token do GitHub
via Git Credential Manager (`git credential fill`) e consulta a API de Actions.

Uso:
    python check_deploy.py            # status do run mais recente
    python check_deploy.py --watch    # acompanha ate concluir
    python check_deploy.py --repo owner/nome   # forca um repo especifico
"""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request

# Garante UTF-8 no stdout (Windows usa cp1252 por padrao e quebra com acentos/emoji).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API = "https://api.github.com"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def get_owner_repo(explicit=None):
    if explicit:
        return explicit
    r = run(["git", "remote", "get-url", "origin"])
    if r.returncode != 0:
        sys.exit("Nao consegui ler o remote 'origin'. Rode dentro do repo ou use --repo owner/nome.")
    url = r.stdout.strip()
    # https://github.com/owner/repo(.git)  ou  git@github.com:owner/repo(.git)
    m = re.search(r"github\.com[:/]+([^/]+)/([^/.]+)", url)
    if not m:
        sys.exit(f"Nao reconheci o remote como GitHub: {url}")
    return f"{m.group(1)}/{m.group(2)}"


def get_token():
    """Pega o token via Git Credential Manager. Nunca imprime o token."""
    inp = "protocol=https\nhost=github.com\n\n"
    r = run(["git", "credential", "fill"], input=inp)
    for line in r.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    return None


def api_get(path, token):
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github+json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def latest_run(repo, token):
    data = api_get(f"/repos/{repo}/actions/runs?per_page=1", token)
    runs = data.get("workflow_runs") or []
    return runs[0] if runs else None


def fmt(run):
    msg = (run.get("head_commit") or {}).get("message", "")
    first_line = msg.splitlines()[0] if msg else ""
    return (
        f"  workflow : {run.get('name')}\n"
        f"  status   : {run.get('status')}\n"
        f"  conclusao: {run.get('conclusion')}\n"
        f"  commit   : {first_line}\n"
        f"  url      : {run.get('html_url')}"
    )


def main():
    ap = argparse.ArgumentParser(description="Status do deploy (GitHub Actions)")
    ap.add_argument("--watch", action="store_true", help="acompanha ate concluir")
    ap.add_argument("--repo", help="owner/nome (forca o repo)")
    ap.add_argument("--interval", type=int, default=15, help="segundos entre checagens no --watch")
    args = ap.parse_args()

    repo = get_owner_repo(args.repo)
    token = get_token()
    if not token:
        print("Aviso: sem token do GitHub (repos privados vao falhar).", file=sys.stderr)

    print(f"Repo: {repo}")
    run_obj = latest_run(repo, token)
    if not run_obj:
        sys.exit("Nenhum run encontrado ainda.")
    print(fmt(run_obj))

    if not args.watch:
        return

    while run_obj.get("status") != "completed":
        time.sleep(args.interval)
        run_obj = latest_run(repo, token)
        print(f"... {run_obj.get('status')}")

    ok = run_obj.get("conclusion") == "success"
    print("\n" + ("DEPLOY OK [success]" if ok else f"DEPLOY FALHOU [{run_obj.get('conclusion')}] -> {run_obj.get('html_url')}"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
