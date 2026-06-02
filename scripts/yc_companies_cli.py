#!/usr/bin/env python3
"""Small local CLI for Y Combinator's public company directory backend.

This CLI discovers the public Algolia config from https://www.ycombinator.com/companies
at runtime, then queries the same backend the site uses.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import urllib.parse
import urllib.request
from typing import Any


COMPANIES_URL = "https://www.ycombinator.com/companies"


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as response:
        return response.read().decode("utf-8", "ignore")


def discover_backend() -> dict[str, str]:
    html = fetch_text(COMPANIES_URL)

    algolia_match = re.search(r"window\.AlgoliaOpts = (\{.*?\});", html, re.S)
    if not algolia_match:
        raise SystemExit("Could not discover Algolia config from YC companies page")
    opts = json.loads(algolia_match.group(1))

    batch_match = re.search(r'&quot;currentBatch&quot;:&quot;([^&]+)&quot;', html)
    current_batch = batch_match.group(1) if batch_match else ""

    return {
        "app": opts["app"],
        "key": opts["key"],
        "current_batch": current_batch,
        "companies_url": COMPANIES_URL,
    }


def algolia_query(config: dict[str, str], query: str, *, filters: str | None = None, hits: int = 20) -> list[dict[str, Any]]:
    endpoint = f"https://{config['app']}-dsn.algolia.net/1/indexes/YCCompany_By_Launch_Date_production/query"
    params = [f"query={urllib.parse.quote(query)}", f"hitsPerPage={hits}"]
    if filters:
        params.append("filters=" + urllib.parse.quote(filters))

    body = json.dumps({"params": "&".join(params)}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "X-Algolia-API-Key": config["key"],
            "X-Algolia-Application-Id": config["app"],
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["hits"]


def company_text(hit: dict[str, Any]) -> str:
    fields = [
        hit.get("name", ""),
        hit.get("one_liner", ""),
        hit.get("long_description", ""),
        hit.get("subindustry", ""),
        " ".join(hit.get("tags") or []),
    ]
    return " ".join(str(field) for field in fields)


def first_sentence(text: str) -> str:
    cleaned = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    if not cleaned:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", cleaned, maxsplit=1)
    return parts[0]


USE_CASE_RULES: list[tuple[str, list[str]]] = [
    ("healthcare operations", [r"\bhealthcare\b", r"\bclinic(s)?\b", r"\bpatient(s)?\b", r"\bhospital(s)?\b", r"\behr\b", r"\bmedical\b", r"\bpharmacy\b", r"\bcare management\b"]),
    ("security and governance", [r"\bsecurity\b", r"\bgovernance\b", r"\bsoc\b", r"\bcompliance\b", r"\bpermission(ing|s)?\b", r"\bauth\b"]),
    ("analytics and reporting", [r"\banalytics\b", r"\bdashboard(s)?\b", r"\breporting\b", r"\bknowledge base(s)?\b", r"\bresearch\b"]),
    ("developer tools and testing", [r"\bdeveloper\b", r"\btesting\b", r"\bqa\b", r"\bdesign docs?\b", r"\bcodebase\b", r"\bbrowser agents?\b", r"\bweb testing\b"]),
    ("workflow automation", [r"\bworkflow(s)?\b", r"\bautomate\b", r"\bautomation\b", r"\boperating system\b", r"\bprocess(es)?\b", r"\bcopilot(s)?\b"]),
    ("sales and customer ops", [r"\bsales\b", r"\bcrm\b", r"\bcustomer(s)?\b", r"\bfunnel\b", r"\boutreach\b", r"\bsupport\b", r"\bguest complaints\b"]),
    ("data and agent infrastructure", [r"\bcontext layer\b", r"\bdata gateway\b", r"\binfrastructure\b", r"\bretrieval\b", r"\bagent platform\b", r"\binbox api\b", r"\bemail inbox(api|es)?\b"]),
    ("finance and trading", [r"\btrading\b", r"\bfinance\b", r"\bbank(ing)?\b", r"\bclaims?\b", r"\binsurance\b", r"\brevenue cycle\b"]),
    ("legal and compliance workflows", [r"\blawyer(s)?\b", r"\blegal\b", r"\bcontract(s)?\b", r"\bip enforcement\b"]),
]


def infer_use_case_focus(hit: dict[str, Any]) -> list[str]:
    text = company_text(hit).lower()
    labels: list[str] = []
    for label, patterns in USE_CASE_RULES:
        if any(re.search(pattern, text) for pattern in patterns):
            labels.append(label)
    if not labels:
        labels.append("general AI applications")
    return labels[:3]


def summarize_company(hit: dict[str, Any]) -> dict[str, Any]:
    long_description = str(hit.get("long_description") or "")
    one_liner = str(hit.get("one_liner") or "")
    summary = one_liner or first_sentence(long_description)
    return {
        "name": hit.get("name"),
        "batch": hit.get("batch"),
        "team_size": hit.get("team_size"),
        "website": hit.get("website"),
        "subindustry": hit.get("subindustry"),
        "what_they_do": summary,
        "use_case_focus": infer_use_case_focus(hit),
    }


def filter_agent_startups(hits: list[dict[str, Any]], max_team_size: int) -> list[dict[str, Any]]:
    agent_pattern = re.compile(r"\bagent(ic|s)?\b", re.I)
    rows = []
    for hit in hits:
        team_size = hit.get("team_size")
        if team_size is None or team_size > max_team_size:
            continue
        if not agent_pattern.search(company_text(hit)):
            continue
        rows.append(
            {
                "name": hit.get("name"),
                "team_size": team_size,
                "batch": hit.get("batch"),
                "one_liner": hit.get("one_liner"),
            }
        )
    rows.sort(key=lambda row: (row["team_size"], str(row["name"]).lower()))
    return rows


def merged_query_scan(config: dict[str, str], queries: list[str], *, limit: int = 8) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for query in queries:
        for hit in algolia_query(config, query, hits=10):
            object_id = hit["objectID"]
            row = seen.setdefault(
                object_id,
                {
                    "name": hit.get("name"),
                    "batch": hit.get("batch"),
                    "team_size": hit.get("team_size"),
                    "one_liner": hit.get("one_liner"),
                    "subindustry": hit.get("subindustry"),
                    "matched": set(),
                },
            )
            row["matched"].add(query)

    rows = list(seen.values())
    rows.sort(key=lambda row: (-len(row["matched"]), row["team_size"] or 999, str(row["name"]).lower()))
    out = []
    for row in rows[:limit]:
        rendered = dict(row)
        rendered["matched"] = sorted(rendered["matched"])
        out.append(rendered)
    return out


def handle_discover(_: argparse.Namespace) -> int:
    print(json.dumps(discover_backend(), indent=2))
    return 0


def handle_search(args: argparse.Namespace) -> int:
    config = discover_backend()
    filters = f'batch:"{args.batch}"' if args.batch else None
    hits = algolia_query(config, args.query, filters=filters, hits=max(args.limit * 4, 20))
    if args.agentish:
        rows = filter_agent_startups(hits, args.max_team_size)
    else:
        rows = [
            {
                "name": hit.get("name"),
                "team_size": hit.get("team_size"),
                "batch": hit.get("batch"),
                "one_liner": hit.get("one_liner"),
            }
            for hit in hits[: args.limit]
        ]
    print(json.dumps(rows[: args.limit], indent=2))
    return 0


def handle_analyze(args: argparse.Namespace) -> int:
    config = discover_backend()
    filters = f'batch:"{args.batch}"' if args.batch else None
    hits = algolia_query(config, args.query, filters=filters, hits=max(args.limit * 4, 40))
    rows = hits
    if args.agentish:
        rows = [hit for hit in hits if re.search(r"\bagent(ic|s)?\b", company_text(hit), re.I)]
    summaries = [summarize_company(hit) for hit in rows[: args.limit]]
    result = {
        "source": config["companies_url"],
        "current_batch": config["current_batch"],
        "query": args.query,
        "batch": args.batch,
        "results": summaries,
    }
    print(json.dumps(result, indent=2))
    return 0


def handle_use_cases(args: argparse.Namespace) -> int:
    config = discover_backend()
    filters = f'batch:"{args.batch}"' if args.batch else None
    hits = algolia_query(config, args.query, filters=filters, hits=max(args.limit * 4, 40))
    if args.agentish:
        hits = [hit for hit in hits if re.search(r"\bagent(ic|s)?\b", company_text(hit), re.I)]

    grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for hit in hits[: args.limit]:
        summary = summarize_company(hit)
        for label in summary["use_case_focus"]:
            grouped[label].append(
                {
                    "name": summary["name"],
                    "batch": summary["batch"],
                    "team_size": summary["team_size"],
                    "what_they_do": summary["what_they_do"],
                }
            )

    ordered = dict(sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])))
    result = {
        "source": config["companies_url"],
        "current_batch": config["current_batch"],
        "query": args.query,
        "batch": args.batch,
        "groups": ordered,
    }
    print(json.dumps(result, indent=2))
    return 0


def handle_prompt(args: argparse.Namespace) -> int:
    prompt = args.text.lower()
    config = discover_backend()

    if "read every company in y combinator" in prompt and "ai agent startups under 10 people" in prompt:
        batch = args.batch or "Spring 2025"
        hits = algolia_query(config, "agent", filters=f'batch:"{batch}"', hits=100)
        rows = filter_agent_startups(hits, args.max_team_size)
        result = {
            "source": config["companies_url"],
            "current_batch": config["current_batch"],
            "executed_batch": batch,
            "results": rows[: args.limit],
        }
        print(json.dumps(result, indent=2))
        return 0

    if "sync2.ai" in prompt and "reprisesai.com" in prompt:
        sync2_queries = [
            "clinic operations AI",
            "patient scheduling AI",
            "medical receptionist AI",
            "healthcare operations agents",
        ]
        reprise_queries = [
            "AI consulting automation",
            "software implementation AI agents",
            "workflow automation enterprise AI",
            "mid-market agent platform",
        ]
        result = {
            "source": config["companies_url"],
            "current_batch": config["current_batch"],
            "sync2_matches": merged_query_scan(config, sync2_queries, limit=args.limit),
            "reprisesai_matches": merged_query_scan(config, reprise_queries, limit=args.limit),
        }
        print(json.dumps(result, indent=2))
        return 0

    if "what these companies are doing" in prompt or "what these companies do" in prompt:
        batch_match = re.search(r"(spring|summer|winter|fall)\s+20\d{2}", args.text, re.I)
        batch = batch_match.group(0).title() if batch_match else None
        query = "agent" if "agent" in prompt else "ai"
        filters = f'batch:"{batch}"' if batch else None
        hits = algolia_query(config, query, filters=filters, hits=max(args.limit * 4, 40))
        result = {
            "source": config["companies_url"],
            "current_batch": config["current_batch"],
            "executed_batch": batch,
            "query": query,
            "results": [summarize_company(hit) for hit in hits[: args.limit]],
        }
        print(json.dumps(result, indent=2))
        return 0

    if "use case" in prompt or "use cases" in prompt:
        batch_match = re.search(r"(spring|summer|winter|fall)\s+20\d{2}", args.text, re.I)
        batch = batch_match.group(0).title() if batch_match else None
        query = "agent" if "agent" in prompt else "ai"
        filters = f'batch:"{batch}"' if batch else None
        hits = algolia_query(config, query, filters=filters, hits=max(args.limit * 4, 40))
        grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for hit in hits[: args.limit]:
            summary = summarize_company(hit)
            for label in summary["use_case_focus"]:
                grouped[label].append(
                    {
                        "name": summary["name"],
                        "what_they_do": summary["what_they_do"],
                        "team_size": summary["team_size"],
                    }
                )
        result = {
            "source": config["companies_url"],
            "current_batch": config["current_batch"],
            "executed_batch": batch,
            "query": query,
            "groups": dict(sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0]))),
        }
        print(json.dumps(result, indent=2))
        return 0

    raise SystemExit("Prompt pattern not supported by this demo CLI")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="yc-companies", description="Query YC's public companies backend")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover", help="Discover YC public backend config")
    discover_parser.set_defaults(func=handle_discover)

    search_parser = subparsers.add_parser("search", help="Run a direct company search")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--batch")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--max-team-size", type=int, default=10)
    search_parser.add_argument("--agentish", action="store_true", help="Filter for agent/agentic companies")
    search_parser.set_defaults(func=handle_search)

    analyze_parser = subparsers.add_parser("analyze", help="Summarize what matched companies do")
    analyze_parser.add_argument("--query", required=True)
    analyze_parser.add_argument("--batch")
    analyze_parser.add_argument("--limit", type=int, default=10)
    analyze_parser.add_argument("--agentish", action="store_true", help="Filter for agent/agentic companies")
    analyze_parser.set_defaults(func=handle_analyze)

    use_cases_parser = subparsers.add_parser("use-cases", help="Group matched companies by inferred use-case focus")
    use_cases_parser.add_argument("--query", required=True)
    use_cases_parser.add_argument("--batch")
    use_cases_parser.add_argument("--limit", type=int, default=20)
    use_cases_parser.add_argument("--agentish", action="store_true", help="Filter for agent/agentic companies")
    use_cases_parser.set_defaults(func=handle_use_cases)

    prompt_parser = subparsers.add_parser("prompt", help="Execute a known natural-language demo prompt")
    prompt_parser.add_argument("text")
    prompt_parser.add_argument("--batch", help="Override batch for the first demo prompt")
    prompt_parser.add_argument("--limit", type=int, default=10)
    prompt_parser.add_argument("--max-team-size", type=int, default=10)
    prompt_parser.set_defaults(func=handle_prompt)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
