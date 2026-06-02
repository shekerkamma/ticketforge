#!/usr/bin/env python3
"""Fetch source notes for representative YC agent companies."""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import scripts.yc_companies_cli as yc


ANALYSIS_PATH = Path("analytics-comms/yc-agent-companies-spring-2025/analysis.json")
NOTES_DIR = Path("research-notes/yc-agent-companies-spring-2025")
SUMMARY_PATH = NOTES_DIR / "source-summary.json"
INDEX_PATH = NOTES_DIR / "INDEX.md"
SYNTHESIS_PATH = NOTES_DIR / "research-synthesis.md"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8", "ignore")


def clean(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = " ".join(text.split())
    return text.strip()


def extract_field(pattern: str, blob: str) -> str:
    match = re.search(pattern, blob, re.I | re.S)
    return clean(match.group(1)) if match else ""


def extract_website_signals(blob: str) -> dict[str, str]:
    title = extract_field(r"<title[^>]*>(.*?)</title>", blob)
    meta_desc = extract_field(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', blob)
    if not meta_desc:
        meta_desc = extract_field(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']', blob)
    h1 = extract_field(r"<h1[^>]*>(.*?)</h1>", blob)
    h2 = extract_field(r"<h2[^>]*>(.*?)</h2>", blob)
    first_p = extract_field(r"<p[^>]*>(.*?)</p>", blob)
    proof_line = meta_desc or h1 or h2 or first_p or title
    return {
        "title": title,
        "meta_description": meta_desc,
        "h1": h1,
        "h2": h2,
        "first_paragraph": first_p,
        "proof_line": proof_line,
    }


def load_analysis() -> dict[str, Any]:
    return json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))


def select_company_names(analysis: dict[str, Any]) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for cluster in analysis["use_case_clusters"][:5]:
        for company in cluster["companies"][:2]:
            name = company["name"]
            if name not in seen:
                names.append(name)
                seen.add(name)
    for key in ["sync2_matches", "reprisesai_matches"]:
        for match in analysis["adjacency"][key][:4]:
            name = match["name"]
            if name not in seen:
                names.append(name)
                seen.add(name)
    return names


def resolve_company(config: dict[str, str], name: str) -> dict[str, Any] | None:
    hits = yc.algolia_query(config, name, hits=12)
    target = name.lower()
    for hit in hits:
        if str(hit.get("name", "")).lower() == target:
            return hit
    return hits[0] if hits else None


def write_note(company: dict[str, Any], signals: dict[str, str], error: str | None = None) -> None:
    slug = slugify(str(company["name"]))
    note_path = NOTES_DIR / f"{slug}.md"
    lines = [
        "---",
        "source_type: company-website",
        f"company: {company['name']}",
        f"website: {company.get('website','')}",
        f"yc_batch: {company.get('batch','')}",
        "---",
        "",
        f"# {company['name']}",
        "",
        "## Raw Source Signals",
        "",
        f"- Title: {signals.get('title','')}",
        f"- Meta description: {signals.get('meta_description','')}",
        f"- H1: {signals.get('h1','')}",
        f"- H2: {signals.get('h2','')}",
        f"- First paragraph: {signals.get('first_paragraph','')}",
        "",
        "## Working Summary",
        "",
        f"- YC one-liner: {company.get('one_liner','')}",
        f"- Proof line: {signals.get('proof_line','')}",
    ]
    if error:
        lines.extend(["", "## Fetch Note", "", f"- Error: {error}"])
    note_path.write_text("\n".join(lines), encoding="utf-8")


def build_synthesis(summary: dict[str, Any]) -> str:
    lines = ["# YC Source Research Synthesis", "", "## What the websites reinforce", ""]
    patterns = [
        "Many company sites lead with a workflow outcome, not with a generic agent claim.",
        "Healthcare companies consistently foreground operations, scheduling, billing, claims, or patient flow.",
        "Tooling and infrastructure companies emphasize context, QA, testing, or control rather than broad automation.",
        "The stronger sites sound like system-of-action software, not chat wrappers.",
    ]
    for item in patterns:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Companies covered")
    lines.append("")
    for name, payload in sorted(summary.items()):
        lines.append(f"- **{name}**: {payload.get('proof_line','')}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    if not ANALYSIS_PATH.exists():
        raise SystemExit(f"Missing analysis file: {ANALYSIS_PATH}")

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    analysis = load_analysis()
    config = yc.discover_backend()
    selected = select_company_names(analysis)
    summary: dict[str, Any] = {}

    for name in selected:
        company = resolve_company(config, name)
        if not company:
            continue
        website = str(company.get("website") or "").strip()
        signals = {
            "title": "",
            "meta_description": "",
            "h1": "",
            "h2": "",
            "first_paragraph": "",
            "proof_line": str(company.get("one_liner") or ""),
        }
        error = None
        if website:
            try:
                blob = fetch_html(website)
                parsed = extract_website_signals(blob)
                if parsed["proof_line"]:
                    signals = parsed
            except urllib.error.URLError as exc:
                error = str(exc)
            except Exception as exc:  # noqa: BLE001
                error = str(exc)

        payload = {
            "name": company.get("name"),
            "website": website,
            "batch": company.get("batch"),
            "one_liner": company.get("one_liner"),
            "proof_line": signals["proof_line"] or str(company.get("one_liner") or ""),
            "title": signals["title"],
            "meta_description": signals["meta_description"],
            "h1": signals["h1"],
            "h2": signals["h2"],
            "error": error,
        }
        summary[str(company.get("name"))] = payload
        write_note(company, signals, error)

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    INDEX_PATH.write_text(
        "\n".join(
            ["# YC Agent Companies Source Notes", ""]
            + [f"- [{name}]({slugify(name)}.md)" for name in sorted(summary.keys())]
        ),
        encoding="utf-8",
    )
    SYNTHESIS_PATH.write_text(build_synthesis(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
