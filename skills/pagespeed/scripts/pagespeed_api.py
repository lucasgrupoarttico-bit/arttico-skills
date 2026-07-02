#!/usr/bin/env python3
"""
Google PageSpeed Insights API — wrapper para pagespeed
Uso: python3 pagespeed_api.py analyze --url https://exemplo.com --strategy mobile
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse

API_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

CATEGORIES = ["performance", "accessibility", "best-practices", "seo"]

CWV_THRESHOLDS = {
    "largest-contentful-paint": {"bom": 2500, "medio": 4000, "unit": "ms"},
    "first-contentful-paint":   {"bom": 1800, "medio": 3000, "unit": "ms"},
    "total-blocking-time":      {"bom": 200,  "medio": 600,  "unit": "ms"},
    "cumulative-layout-shift":  {"bom": 0.1,  "medio": 0.25, "unit": ""},
    "interactive":              {"bom": 3800, "medio": 7300, "unit": "ms"},
    "speed-index":              {"bom": 3400, "medio": 5800, "unit": "ms"},
}


def classify_cwv(audit_id, numeric_value):
    if audit_id not in CWV_THRESHOLDS:
        return "N/A"
    t = CWV_THRESHOLDS[audit_id]
    if numeric_value <= t["bom"]:
        return "BOM"
    elif numeric_value <= t["medio"]:
        return "MELHORIA"
    return "RUIM"


def classify_score(score):
    if score >= 90:
        return "BOM"
    elif score >= 50:
        return "MELHORIA"
    return "RUIM"


def analyze(url, strategy="mobile", api_key=None):
    params = {
        "url": url,
        "strategy": strategy,
        "category": CATEGORIES,
    }
    if api_key:
        params["key"] = api_key

    query = urllib.parse.urlencode(params, doseq=True)
    full_url = f"{API_ENDPOINT}?{query}"

    try:
        with urllib.request.urlopen(full_url, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    lhr = data.get("lighthouseResult", {})
    categories = lhr.get("categories", {})
    audits = lhr.get("audits", {})

    scores = {}
    for cat in CATEGORIES:
        raw = categories.get(cat, {}).get("score")
        score = round(raw * 100) if raw is not None else None
        scores[cat] = {
            "score": score,
            "status": classify_score(score) if score is not None else "N/A",
        }

    cwv_keys = [
        "largest-contentful-paint",
        "first-contentful-paint",
        "total-blocking-time",
        "cumulative-layout-shift",
        "interactive",
        "speed-index",
    ]
    core_web_vitals = {}
    for key in cwv_keys:
        a = audits.get(key, {})
        numeric = a.get("numericValue", 0)
        core_web_vitals[key] = {
            "displayValue": a.get("displayValue", "N/A"),
            "numericValue": round(numeric, 3),
            "status": classify_cwv(key, numeric),
        }

    opportunities = []
    diagnostics = []

    for audit_id, audit in audits.items():
        details = audit.get("details", {})
        score = audit.get("score")
        mode = audit.get("scoreDisplayMode", "")

        if details.get("type") == "opportunity" and score is not None and score < 0.9:
            savings_ms = details.get("overallSavingsMs", 0)
            opportunities.append({
                "id": audit_id,
                "title": audit.get("title", ""),
                "description": audit.get("description", ""),
                "displayValue": audit.get("displayValue", ""),
                "savingsMs": round(savings_ms),
                "score": round(score * 100) if score is not None else None,
            })

        elif mode == "binary" and score == 0:
            diagnostics.append({
                "id": audit_id,
                "title": audit.get("title", ""),
                "description": audit.get("description", ""),
            })

    opportunities.sort(key=lambda x: x["savingsMs"], reverse=True)

    result = {
        "url": url,
        "strategy": strategy,
        "scores": scores,
        "coreWebVitals": core_web_vitals,
        "opportunities": opportunities[:10],
        "diagnostics": diagnostics[:10],
        "fetchTime": lhr.get("fetchTime", ""),
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="PageSpeed Insights API wrapper")
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analisa uma URL")
    analyze_parser.add_argument("--url", required=True, help="URL para analisar")
    analyze_parser.add_argument(
        "--strategy",
        default="mobile",
        choices=["mobile", "desktop"],
        help="Estratégia (padrão: mobile)",
    )
    analyze_parser.add_argument("--api-key", default=None, help="Google API Key (opcional)")

    args = parser.parse_args()

    if args.command == "analyze":
        result = analyze(args.url, args.strategy, args.api_key)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
