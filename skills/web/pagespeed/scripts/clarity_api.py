#!/usr/bin/env python3
"""
Microsoft Clarity API — wrapper para pagespeed

A Clarity API usa autenticação Bearer com API Key gerada no painel:
Clarity > Settings > API Keys

Endpoints disponíveis:
  metrics   → métricas gerais do projeto por período
  pages     → top páginas com métricas de comportamento

Uso:
  python3 clarity_api.py metrics --project-id ABC123 --api-key KEY --start-date 2026-05-01 --end-date 2026-05-31
  python3 clarity_api.py pages   --project-id ABC123 --api-key KEY --start-date 2026-05-01 --end-date 2026-05-31
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

API_BASE = "https://www.clarity.ms/api/v0"


def make_request(endpoint, api_key):
    url = f"{API_BASE}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(json.dumps({
            "error": f"HTTP {e.code}: {e.reason}",
            "body": body,
            "dica": "Verifique se a API Key está correta e tem permissão de leitura."
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


def get_metrics(project_id, api_key, start_date, end_date):
    """Retorna métricas gerais do projeto."""
    params = urllib.parse.urlencode({
        "startDate": start_date,
        "endDate": end_date,
        "numOfDays": 1,
    })
    endpoint = f"/projects/{project_id}/metrics?{params}"
    data = make_request(endpoint, api_key)

    metrics = data.get("metrics", {}) if isinstance(data, dict) else {}

    result = {
        "project_id": project_id,
        "period": {"start": start_date, "end": end_date},
        "sessions": metrics.get("totalSessionCount", "N/A"),
        "pageViews": metrics.get("totalPageviewCount", "N/A"),
        "avgSessionDuration": metrics.get("avgSessionDuration", "N/A"),
        "pagesPerSession": metrics.get("pagesPerSession", "N/A"),
        "botTrafficPercent": metrics.get("botTrafficPercent", "N/A"),
        "deadClickPercent": metrics.get("deadClickPercent", "N/A"),
        "rageClickPercent": metrics.get("rageClickPercent", "N/A"),
        "quickBackPercent": metrics.get("quickBackPercent", "N/A"),
        "excessiveScrollPercent": metrics.get("excessiveScrollPercent", "N/A"),
        "raw": data,
    }
    return result


def get_pages(project_id, api_key, start_date, end_date):
    """Retorna top páginas com métricas de comportamento."""
    params = urllib.parse.urlencode({
        "startDate": start_date,
        "endDate": end_date,
        "pageSize": 10,
    })
    endpoint = f"/projects/{project_id}/pages?{params}"
    data = make_request(endpoint, api_key)

    pages_raw = data.get("pages", []) if isinstance(data, dict) else []

    pages = []
    for page in pages_raw:
        pages.append({
            "url": page.get("url", ""),
            "sessions": page.get("sessionCount", 0),
            "pageViews": page.get("pageviewCount", 0),
            "avgScrollDepth": page.get("avgScrollDepth", "N/A"),
            "deadClickPercent": page.get("deadClickPercent", "N/A"),
            "rageClickPercent": page.get("rageClickPercent", "N/A"),
        })

    return {
        "project_id": project_id,
        "period": {"start": start_date, "end": end_date},
        "pages": pages,
    }


def default_dates():
    end = datetime.today()
    start = end - timedelta(days=30)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description="Microsoft Clarity API wrapper")
    subparsers = parser.add_subparsers(dest="command")

    default_start, default_end = default_dates()

    for cmd in ["metrics", "pages"]:
        sub = subparsers.add_parser(cmd)
        sub.add_argument("--project-id", required=True)
        sub.add_argument("--api-key", required=True)
        sub.add_argument("--start-date", default=default_start)
        sub.add_argument("--end-date", default=default_end)

    args = parser.parse_args()

    if args.command == "metrics":
        result = get_metrics(args.project_id, args.api_key, args.start_date, args.end_date)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "pages":
        result = get_pages(args.project_id, args.api_key, args.start_date, args.end_date)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
