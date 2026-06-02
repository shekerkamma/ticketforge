#!/usr/bin/env python3
"""Build a structured YC agent-company analysis pack for downstream decks."""

from __future__ import annotations

import json
import math
import re
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import scripts.yc_companies_cli as yc


BATCH = "Spring 2025"
QUERY = "agent"
MAX_TEAM_SIZE = 10
REPORT_SLUG = "yc-agent-companies-spring-2025"
DECISION_QUESTION = "Which YC small-team agent companies show the clearest commercially viable use cases?"
PRIMARY_AUDIENCE = "executive"
THEME_REFERENCE = "c:/Users/sheke/OneDrive/Desktop/slide deck-reference.pdf"
OUTPUT_DIR = Path(f"analytics-comms/{REPORT_SLUG}")
JSON_PATH = OUTPUT_DIR / "analysis.json"
ANALYSIS_PACK_PATH = OUTPUT_DIR / "analysis-pack.json"
DECK_PLAN_PATH = OUTPUT_DIR / "deck-plan.json"
MD_PATH = OUTPUT_DIR / "analysis.md"
CHART_PATH = OUTPUT_DIR / "chart-brief.md"
SOURCE_SUMMARY_PATH = Path(f"research-notes/{REPORT_SLUG}/source-summary.json")
SOURCE_NOTES_PATH = Path(f"research-notes/{REPORT_SLUG}/source-notes.json")


CLUSTER_PLAYBOOK: dict[str, dict[str, str]] = {
    "workflow automation": {
        "buyer": "COO, operations leader, or workflow owner",
        "workflow_owner": "ops managers running repetitive multi-step work",
        "business_job": "Turn high-volume, rules-heavy operational queues into agent-run systems of action.",
        "value_prop": "Throughput, faster cycle times, and lower labor cost without requiring users to learn a new interface.",
        "why_now": "LLMs plus tool use make it possible to automate the whole queue, not just summarize it.",
        "recommendation": "Best starting point when a team already exists and the handoffs are obvious.",
    },
    "sales and customer ops": {
        "buyer": "sales leaders, revenue ops, customer success, or service managers",
        "workflow_owner": "frontline teams handling customer-facing repetitive work",
        "business_job": "Use agents to qualify, route, support, and operationalize customer interaction workflows.",
        "value_prop": "Improves responsiveness and rep leverage while keeping the workflow anchored in revenue teams.",
        "why_now": "Customer conversations already create structured data and clear SLAs, which agents can exploit.",
        "recommendation": "Strong wedge when the product can own a narrow workflow like intake, triage, or follow-up.",
    },
    "analytics and reporting": {
        "buyer": "heads of analytics, operations leaders, and knowledge-work teams",
        "workflow_owner": "analysts and operators who summarize, monitor, and report",
        "business_job": "Turn raw data or context into dashboards, summaries, and decision-ready reporting.",
        "value_prop": "Makes information work faster and cheaper while reducing manual synthesis.",
        "why_now": "Reporting is repetitive, high-frequency, and already evaluated on output quality and speed.",
        "recommendation": "Works best when paired with trusted data access and a narrow reporting loop.",
    },
    "developer tools and testing": {
        "buyer": "engineering leaders, product teams, QA, and platform teams",
        "workflow_owner": "teams responsible for software quality and release safety",
        "business_job": "Use agents to test, monitor, and validate software and model-driven systems.",
        "value_prop": "Catches regressions and scales QA capacity without linearly scaling headcount.",
        "why_now": "Agentic products create new failure modes, so testing and observability have become first-order needs.",
        "recommendation": "Durable if the product becomes part of the default release process.",
    },
    "data and agent infrastructure": {
        "buyer": "platform engineering, CTO staff, and teams building agent products",
        "workflow_owner": "teams responsible for context, retrieval, and safe system access",
        "business_job": "Provide the data, context, and permissioning layer that agent products depend on.",
        "value_prop": "Becomes infrastructure rather than a single workflow app, increasing platform stickiness.",
        "why_now": "Agents fail without trustworthy context and controlled system access.",
        "recommendation": "Attractive when the team wants a horizontal wedge instead of a workflow application.",
    },
    "security and governance": {
        "buyer": "CISO orgs, security engineering, and compliance leaders",
        "workflow_owner": "security teams managing alerts, access, and policy enforcement",
        "business_job": "Automate security workflows and govern how agents interact with systems and data.",
        "value_prop": "Security pain is urgent, measurable, and hard to outsource to generic tools.",
        "why_now": "Every new agent deployment introduces additional governance and control needs.",
        "recommendation": "Strong if the product can sit in a real enforcement or response loop.",
    },
    "healthcare operations": {
        "buyer": "clinic operators, provider groups, revenue cycle leaders, and healthcare IT buyers",
        "workflow_owner": "front desk, billing, claims, scheduling, and patient-ops teams",
        "business_job": "Reduce repetitive administrative work in patient and provider operations.",
        "value_prop": "High-friction workflows, high willingness to pay, and measurable ROI in staffing and collections.",
        "why_now": "Healthcare workflows are still overloaded with manual coordination and structured repetitive work.",
        "recommendation": "One of the clearest vertical lanes if the product owns a painful workflow end to end.",
    },
    "finance and trading": {
        "buyer": "finance operators, claims leaders, and risk teams",
        "workflow_owner": "teams handling claims, trading, and financially sensitive repetitive workflows",
        "business_job": "Apply agents to high-value workflows with direct financial consequences.",
        "value_prop": "Easier to justify because cycle time and error rates map to money quickly.",
        "why_now": "Structured rules and measurable impact make finance-adjacent workflows attractive for automation.",
        "recommendation": "Works best when the team has domain expertise and clear data/control boundaries.",
    },
    "legal and compliance workflows": {
        "buyer": "legal ops, compliance teams, and specialized knowledge teams",
        "workflow_owner": "professionals doing high-cost document and rule-based review work",
        "business_job": "Embed agents inside document-heavy or policy-heavy professional workflows.",
        "value_prop": "Saves expert time where labor is expensive and throughput matters.",
        "why_now": "Language-heavy professional work is now tractable enough for narrow workflow products.",
        "recommendation": "Promising if the product can specialize around a precise workflow, not generic legal AI.",
    },
}


def filtered_hits(config: dict[str, str]) -> list[dict[str, Any]]:
    hits = yc.algolia_query(config, QUERY, filters=f'batch:"{BATCH}"', hits=100)
    rows = yc.filter_agent_startups(hits, MAX_TEAM_SIZE)
    names = {row["name"] for row in rows}
    agent_hits = [hit for hit in hits if hit.get("name") in names]
    agent_hits.sort(key=lambda hit: (hit.get("team_size") or 999, str(hit.get("name", "")).lower()))
    return agent_hits


def summarize_clusters(companies: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], Counter[str]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    counts: Counter[str] = Counter()
    for hit in companies:
        summary = yc.summarize_company(hit)
        for label in summary["use_case_focus"]:
            counts[label] += 1
            grouped.setdefault(label, []).append(summary)

    clusters: list[dict[str, Any]] = []
    for label, members in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        play = CLUSTER_PLAYBOOK.get(label, {})
        clusters.append(
            {
                "name": label,
                "count": len(members),
                "buyer": play.get("buyer", "Cross-functional operator"),
                "workflow_owner": play.get("workflow_owner", "Team running the underlying workflow"),
                "business_job": play.get("business_job", "Own a narrow operational workflow with agents."),
                "value_prop": play.get("value_prop", "Reduce cycle time and manual coordination."),
                "why_now": play.get("why_now", "Agents can now execute more of the workflow directly."),
                "recommendation": play.get("recommendation", "Viable when the workflow is clear and expensive."),
                "companies": members,
                "examples": [member["name"] for member in members[:5]],
            }
        )
    return clusters, counts


def load_source_summary() -> dict[str, Any]:
    if SOURCE_SUMMARY_PATH.exists():
        return json.loads(SOURCE_SUMMARY_PATH.read_text(encoding="utf-8"))
    return {}


def build_chart_recommendations(clusters: list[dict[str, Any]], team_sizes: list[int]) -> list[dict[str, str]]:
    return [
        {
            "title": "Use-case density by cluster",
            "best_chart_type": "Horizontal bar chart",
            "why_this_fits": "The question is ranking and comparison across use-case clusters.",
            "narrative_takeaway": "Workflow automation and customer-facing ops dominate the cohort.",
            "encoding_guidance": "Sort clusters descending by company count and label each bar directly.",
            "annotation_plan": "Call out the top two clusters and note that healthcare is smaller but strategically important.",
        },
        {
            "title": "Team-size distribution",
            "best_chart_type": "Histogram or binned bar chart",
            "why_this_fits": "The question is distribution, not ranking.",
            "narrative_takeaway": "The cohort is extremely early, with a strong concentration at 1-2 person teams.",
            "encoding_guidance": f"Use bins for 1-2, 3-4, 5-6, 7-8, 9-10 based on sizes {team_sizes}.",
            "annotation_plan": "Highlight the median team size and the share of teams with 1-2 people.",
        },
        {
            "title": "Use-case map by business shape",
            "best_chart_type": "2x2 matrix",
            "why_this_fits": "The question is strategic positioning, not exact counts.",
            "narrative_takeaway": "The strongest names cluster where workflow ownership and willingness to pay are both high.",
            "encoding_guidance": "Axes: horizontal = horizontal tooling to vertical workflow ownership; vertical = weak to strong willingness to pay.",
            "annotation_plan": "Place healthcare ops high/right, tooling/infra left/high, generic agent apps lower/left.",
        },
    ]


def build_recommendations(clusters: list[dict[str, Any]]) -> list[dict[str, str]]:
    top = {cluster["name"]: cluster for cluster in clusters}
    return [
        {
            "title": "Choose workflow-heavy use cases first",
            "why": f"{top['workflow automation']['count']} companies cluster around operational systems of action, making this the clearest YC pattern.",
        },
        {
            "title": "Own context, governance, or workflow position",
            "why": "The more durable clusters pair agents with data access, infrastructure, or embedded workflow ownership.",
        },
        {
            "title": "Treat healthcare operations as a real wedge",
            "why": "The count is smaller than horizontal ops, but the workflow pain and willingness to pay are strong.",
        },
        {
            "title": "Avoid generic agent-platform messaging",
            "why": "The cohort repeatedly rewards products with explicit jobs and operators, not broad agent claims.",
        },
    ]


def build_team_size_bins(team_sizes: list[int]) -> list[dict[str, Any]]:
    bins = [("1-2", 1, 2), ("3-4", 3, 4), ("5-6", 5, 6), ("7-8", 7, 8), ("9-10", 9, 10)]
    rows = []
    for label, low, high in bins:
        count = sum(1 for size in team_sizes if low <= size <= high)
        rows.append({"label": label, "count": count})
    return rows


def build_snapshot_groups(analysis: dict[str, Any], per_slide: int = 4) -> list[list[dict[str, Any]]]:
    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    for cluster in analysis["use_case_clusters"][:5]:
        for company in cluster["companies"][:2]:
            if company["name"] in seen:
                continue
            ordered.append(
                {
                    "name": company["name"],
                    "cluster": cluster["name"],
                    "proof_line": company.get("proof_line") or company["what_they_do"],
                }
            )
            seen.add(company["name"])
    for key in ["sync2_matches", "reprisesai_matches"]:
        for match in analysis["adjacency"][key][:4]:
            if match["name"] in seen:
                continue
            ordered.append(
                {
                    "name": match["name"],
                    "cluster": "adjacency",
                    "proof_line": match.get("proof_line") or match["one_liner"],
                }
            )
            seen.add(match["name"])
    return [ordered[idx : idx + per_slide] for idx in range(0, len(ordered), per_slide)]


def truncate(text: str, limit: int = 160) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def build_deck_plan(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    top_clusters = analysis["use_case_clusters"][:5]
    vertical_clusters = [
        cluster
        for cluster in analysis["use_case_clusters"]
        if cluster["name"] in {"healthcare operations", "security and governance", "legal and compliance workflows", "finance and trading"}
    ]
    company_rows = []
    for cluster in top_clusters[:4]:
        for company in cluster["companies"][:2]:
            company_rows.append(
                {
                    "name": company["name"],
                    "cluster": cluster["name"],
                    "what_they_do": truncate(company.get("proof_line") or company["what_they_do"]),
                }
            )
    snapshot_groups = build_snapshot_groups(analysis)
    deck = [
        {
            "type": "title",
            "title": "Y Combinator Agent Companies",
            "subtitle": "What Spring 2025 YC's small-team agent startups are actually building",
            "strapline": "Structured business use cases, density map, and implications for Sync2 and ReprisesAI",
        },
        {
            "type": "agenda",
            "title": "What You'll See",
            "sections": [
                {"number": "01", "title": "What the cohort actually says", "detail": "Headline findings, size, and density map"},
                {"number": "02", "title": "Business use cases", "detail": "Structured jobs, buyers, and source-backed company proof"},
                {"number": "03", "title": "Strategic implications", "detail": "Sync2, ReprisesAI, and what to do next"},
                {"number": "04", "title": "Execution priorities", "detail": "Recommendations, opportunity ladder, and methodology"},
            ],
        },
        {
            "type": "section_divider",
            "section": "SECTION 01",
            "title": "What The Cohort Actually Says",
            "subtitle": "The data is more operational and workflow-shaped than the generic agent narrative suggests.",
        },
        {
            "type": "summary_cards",
            "title": "Three Conclusions Matter Most",
            "cards": [
                {
                    "number": "01",
                    "title": "Workflow automation leads",
                    "body": "The strongest YC signal is not generic assistants. It is agents wrapped around concrete operational jobs.",
                },
                {
                    "number": "02",
                    "title": "Ops and tooling dominate",
                    "body": "Customer ops, analytics, QA, testing, context, and infra appear more often than broad platform narratives.",
                },
                {
                    "number": "03",
                    "title": "Healthcare is a real vertical wedge",
                    "body": "Administrative healthcare workflows show enough density and pain to warrant focused product bets.",
                },
            ],
        },
        {
            "type": "kpi_grid",
            "title": "This Cohort Is Tiny But Focused",
            "subtitle": "The cohort is young, but the use-case pattern is already visible",
            "kpis": [
                {"value": str(analysis["cohort_summary"]["company_count"]), "label": "companies", "note": "filtered Spring 2025 cohort"},
                {"value": str(analysis["cohort_summary"]["median_team_size"]), "label": "median team size", "note": "very early-stage cohort"},
                {"value": str(analysis["cohort_summary"]["teams_1_2"]), "label": "teams with 1-2 people", "note": "nearly half the cohort"},
                {"value": str(top_clusters[0]["count"]), "label": top_clusters[0]["name"], "note": "largest cluster"},
            ],
            "takeaway": "Likely winners will be defined by workflow choice and ownership, not by model novelty.",
        },
        {
            "type": "team_distribution",
            "title": "The Cohort Is Front-Loaded With Tiny Teams",
            "subtitle": "Team size distribution reinforces how early and still-forming these bets are",
            "series": build_team_size_bins(analysis["cohort_summary"]["team_sizes"]),
            "takeaway": "The market signal is meaningful, but the products are still converging on the right wedge.",
        },
        {
            "type": "bar_chart",
            "title": "Use-Case Density Favors Real Jobs",
            "subtitle": "The highest-density clusters are operational software categories",
            "series": [{"label": cluster["name"], "value": cluster["count"]} for cluster in analysis["use_case_clusters"][:7]],
            "takeaway": "The center of gravity is workflow automation, customer ops, analytics, testing, and infrastructure.",
        },
        {
            "type": "comparison",
            "title": "What People Expect vs. What The Cohort Shows",
            "left_title": "Expected narrative",
            "right_title": "Observed YC pattern",
            "left_points": [
                "General-purpose agent assistants",
                "Broad agent platform positioning",
                "Abstract AI capability claims",
                "Model novelty as the main story",
            ],
            "right_points": [
                "Workflow-bound systems of action",
                "Buyer-owned operational categories",
                "Testing, context, claims, reporting, and ops ownership",
                "Clear job boundaries and measurable business outcomes",
            ],
        },
        {
            "type": "section_divider",
            "section": "SECTION 02",
            "title": "Business Use Cases",
            "subtitle": "The strongest signal comes from the jobs these companies are trying to own, not from the word agent itself.",
        },
        {
            "type": "structured_table",
            "title": "Top Use Cases, Structured As Business Jobs",
            "subtitle": "These are the highest-signal business shapes in the cohort",
            "clusters": top_clusters,
        },
    ]

    for cluster in top_clusters:
        deck.append(
            {
                "type": "cluster_spotlight",
                "title": cluster["name"].title(),
                "buyer": cluster["buyer"],
                "workflow_owner": cluster["workflow_owner"],
                "business_job": cluster["business_job"],
                "value_prop": cluster["value_prop"],
                "why_now": cluster["why_now"],
                "recommendation": cluster["recommendation"],
                "examples": [
                    {
                        "name": company["name"],
                        "proof_line": truncate(company.get("proof_line") or company["what_they_do"], 150),
                    }
                    for company in cluster["companies"][:4]
                ],
            }
        )

    deck.extend(
        [
            {
                "type": "vertical_table",
                "title": "Vertical And Specialist Lanes Matter Too",
                "subtitle": "Smaller clusters can still be strategically attractive when pain and willingness to pay are high",
                "clusters": vertical_clusters,
                "companies": company_rows[:8],
            },
        ]
    )

    for idx, group in enumerate(snapshot_groups, start=1):
        deck.append(
            {
                "type": "company_grid",
                "title": f"Source-Backed Company Snapshots {idx}",
                "subtitle": "Website language reinforces the workflow-first pattern",
                "companies": [
                    {
                        "name": item["name"],
                        "cluster": item["cluster"],
                        "proof_line": truncate(item["proof_line"], 170),
                    }
                    for item in group
                ],
            }
        )

    deck.extend(
        [
            {
                "type": "section_divider",
                "section": "SECTION 03",
                "title": "Strategic Implications",
                "subtitle": "Where the YC pattern supports Sync2, where it pressures ReprisesAI, and what the next build direction should be.",
            },
            {
                "type": "case_study",
                "title": "Sync2 Has Real YC Adjacency",
                "match_title": "Closest YC matches",
                "matches": analysis["adjacency"]["sync2_matches"],
                "implication_title": "What this means",
                "implications": [
                    "The lane is real, but the stronger names own deeper workflow than a thin front-desk wrapper.",
                    "Scheduling, claims, billing, intake, and patient communication are stronger system-of-action wedges.",
                    "The winning product is likely the one that captures more of the actual clinic workflow.",
                ],
                "kpis": [
                    {"value": str(len(analysis["adjacency"]["sync2_matches"])), "label": "strong adjacency matches"},
                    {"value": "Ops", "label": "workflow depth wins"},
                    {"value": "$", "label": "high-friction buyer pain"},
                ],
            },
            {
                "type": "implication_bullets",
                "title": "What A Stronger Sync2 Wedge Looks Like",
                "subtitle": "The opportunity is not a generic receptionist. It is a deeper clinic workflow product.",
                "bullets": [
                    "Own a workflow chain like intake -> scheduling -> billing -> claims instead of a single chat entry point.",
                    "Use operational integration as the moat: EHR, claims, pharmacy, lab, and payer connectivity.",
                    "Sell around measurable staffing relief, collection lift, and cycle-time compression.",
                    "Position as system-of-action software for clinic operations, not as another AI front desk.",
                ],
            },
            {
                "type": "case_study",
                "title": "ReprisesAI Faces Productization Risk",
                "match_title": "Closest YC matches",
                "matches": analysis["adjacency"]["reprisesai_matches"],
                "implication_title": "What this means",
                "implications": [
                    "There are fewer direct AI-agency clones than expected.",
                    "The bigger risk is productized implementation software absorbing repeatable service work.",
                    "The safer posture is a specialized wedge, not generic AI delivery.",
                ],
                "kpis": [
                    {"value": str(len(analysis["adjacency"]["reprisesai_matches"])), "label": "clear comparables"},
                    {"value": "Risk", "label": "services get productized"},
                    {"value": "Focus", "label": "specialize the wedge"},
                ],
            },
            {
                "type": "implication_bullets",
                "title": "What ReprisesAI Should Learn From This",
                "subtitle": "The threat is not another generic agency. It is software eating the repeatable implementation layer.",
                "bullets": [
                    "Find the repeatable implementation workflow that can become a product wedge.",
                    "Move toward embedded execution inside customer systems, not just advisory delivery.",
                    "Package methodology into software artifacts, templates, or agents that shorten time-to-value.",
                    "Compete on owned workflow and operational leverage, not just on custom project quality.",
                ],
            },
            {
                "type": "section_divider",
                "section": "SECTION 04",
                "title": "Execution Priorities",
                "subtitle": "The final question is not what YC companies exist. It is where to place the next build bets.",
            },
            {
                "type": "recommendation_grid",
                "title": "What I Would Do Next",
                "subtitle": "The recommendations follow directly from the cohort structure",
                "recommendations": analysis["recommendations"],
            },
            {
                "type": "opportunity_ladder",
                "title": "Priority Order For New Agentic Bets",
                "subtitle": "Rank opportunities by workflow ownership, data access, and willingness to pay",
                "items": [
                    {"label": "Best first bet", "value": "Workflow automation for existing ops teams", "detail": "Highest density in the cohort and clearest buyer pain."},
                    {"label": "Best vertical bet", "value": "Healthcare operations", "detail": "Smaller cluster, but stronger ROI logic and deeper workflow pain."},
                    {"label": "Best horizontal bet", "value": "Context, testing, and control infrastructure", "detail": "Durable wedge if the goal is platform leverage."},
                    {"label": "Avoid first", "value": "Generic agent platform positioning", "detail": "Too abstract unless there is a very specific infrastructure wedge."},
                ],
            },
            {
                "type": "methodology",
                "title": "Method And Reproducibility",
                "bullets": [
                    "Website tested: https://www.ycombinator.com/companies",
                    "yc-companies discovers the live YC backend from the public page each run",
                    "Primary filter: Spring 2025, agent / agentic pattern, team size <= 10",
                    f"Structured cluster counts derived from {analysis['cohort_summary']['company_count']} filtered companies",
                    "Company website notes were collected for representative names and adjacency matches",
                    "Use-case labels are inferred from company text, not official YC categories",
                ],
            },
            {
                "type": "appendix_sources",
                "title": "Source Coverage",
                "subtitle": "Representative source-note coverage used in this deck",
                "companies": [
                    {"name": name, "proof_line": truncate(payload.get("proof_line") or payload.get("one_liner") or "", 170)}
                    for name, payload in sorted(analysis["source_summary"].items())[:8]
                ],
            },
        ]
    )

    return deck


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build_source_notes_contract(
    config: dict[str, str],
    summaries: list[dict[str, Any]],
    source_summary: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    summary_by_name = {summary["name"]: summary for summary in summaries}
    directory_evidence = (
        f"Queried {config['companies_url']} for batch {BATCH} with query '{QUERY}' "
        f"and team size <= {MAX_TEAM_SIZE}; current YC website batch is {config['current_batch']}."
    )
    sources: list[dict[str, Any]] = [
        {
            "source_id": "src-yc-companies-directory",
            "entity_name": "YC Directory",
            "title": "Y Combinator Companies Directory",
            "source_type": "web",
            "locator": config["companies_url"],
            "captured_at": generated_at,
            "summary": "Public YC directory used as the baseline source for the filtered company cohort.",
            "raw_evidence": [
                {
                    "evidence_id": "dir-1",
                    "kind": "quote",
                    "text": directory_evidence,
                    "locator": config["companies_url"],
                }
            ],
            "claims": [
                {
                    "claim_id": "dir-claim-1",
                    "statement": "The filtered cohort is derived from the live public YC companies directory.",
                    "confidence": "high",
                    "evidence_ids": ["dir-1"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "workflow automation",
                    "rationale": "The directory is the shared baseline for use-case clustering across the cohort.",
                }
            ],
            "tags": ["yc", "directory", BATCH, QUERY],
        }
    ]

    for name, payload in sorted(source_summary.items()):
        summary = summary_by_name.get(name, {})
        evidence_inputs = [
            ("title", payload.get("title")),
            ("quote", payload.get("proof_line")),
            ("quote", payload.get("meta_description")),
            ("quote", payload.get("h1")),
            ("quote", payload.get("h2")),
            ("quote", payload.get("one_liner") or summary.get("what_they_do")),
        ]
        raw_evidence = []
        for idx, (kind, text) in enumerate(evidence_inputs, start=1):
            if not text:
                continue
            raw_evidence.append(
                {
                    "evidence_id": f"{slugify(name)}-ev-{idx}",
                    "kind": "quote" if kind != "title" else "other",
                    "text": text,
                    "locator": payload.get("website") or payload.get("title") or name,
                }
            )
        claim_text = payload.get("proof_line") or payload.get("meta_description") or summary.get("what_they_do") or ""
        claim_ids = [item["evidence_id"] for item in raw_evidence] or [f"{slugify(name)}-ev-1"]
        use_case_hints = [
            {
                "label": label,
                "rationale": claim_text or summary.get("what_they_do") or f"{name} appears in the filtered YC cohort.",
            }
            for label in summary.get("use_case_focus", [])[:3]
        ]
        if not use_case_hints:
            use_case_hints = [
                {
                    "label": "general AI applications",
                    "rationale": claim_text or f"{name} appears relevant to the YC agent cohort.",
                }
            ]
        sources.append(
            {
                "source_id": f"src-company-{slugify(name)}",
                "entity_name": name,
                "title": payload.get("title") or f"{name} website note",
                "source_type": "web",
                "locator": payload.get("website") or config["companies_url"],
                "captured_at": generated_at,
                "author": name,
                "published_at": "",
                "summary": payload.get("meta_description") or payload.get("one_liner") or summary.get("what_they_do") or "",
                "raw_evidence": raw_evidence,
                "claims": [
                    {
                        "claim_id": f"{slugify(name)}-claim-1",
                        "statement": claim_text or f"{name} is part of the filtered YC cohort.",
                        "confidence": "high" if payload.get("proof_line") else "medium",
                        "evidence_ids": claim_ids,
                    }
                ],
                "use_case_hints": use_case_hints,
                "tags": [tag for tag in [summary.get("batch"), summary.get("subindustry"), QUERY] if tag],
            }
        )

    return {
        "report_slug": REPORT_SLUG,
        "created_at": generated_at,
        "decision_question": DECISION_QUESTION,
        "sources": sources,
    }


def build_source_id_lookup(source_notes: dict[str, Any]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for source in source_notes["sources"]:
        entity_name = source.get("entity_name")
        if entity_name:
            lookup[entity_name] = source["source_id"]
    return lookup


def source_ids_for_names(names: list[str], source_id_by_name: dict[str, str], default_id: str) -> list[str]:
    source_ids = [source_id_by_name.get(name, default_id) for name in names]
    ordered = []
    seen: set[str] = set()
    for source_id in source_ids or [default_id]:
        if source_id in seen:
            continue
        ordered.append(source_id)
        seen.add(source_id)
    return ordered or [default_id]


def build_findings(analysis: dict[str, Any], source_id_by_name: dict[str, str], default_id: str) -> list[dict[str, Any]]:
    top_clusters = analysis["use_case_clusters"][:4]
    workflow = next((cluster for cluster in analysis["use_case_clusters"] if cluster["name"] == "workflow automation"), top_clusters[0])
    healthcare = next((cluster for cluster in analysis["use_case_clusters"] if cluster["name"] == "healthcare operations"), None)
    return [
        {
            "finding_id": "finding-workflow-density",
            "title": "Workflow automation leads the cohort",
            "statement": "The highest-signal YC agent companies are wrapped around concrete operational jobs, not generic assistant positioning.",
            "implication": "The strongest wedge is workflow ownership with a clear operator and measurable queue.",
            "confidence": "high",
            "metric": f"{workflow['count']} companies in the workflow automation cluster",
            "source_ids": source_ids_for_names(workflow["examples"][:4], source_id_by_name, default_id),
        },
        {
            "finding_id": "finding-ops-and-tooling",
            "title": "Operational categories dominate broad agent narratives",
            "statement": "Customer ops, analytics, QA, testing, and infrastructure appear more frequently than generic platform claims.",
            "implication": "Buyers respond better to operational jobs and embedded tooling than to abstract agent platform language.",
            "confidence": "high",
            "metric": f"Top clusters: {', '.join(cluster['name'] for cluster in top_clusters[:4])}",
            "source_ids": source_ids_for_names(
                [name for cluster in top_clusters for name in cluster["examples"][:2]],
                source_id_by_name,
                default_id,
            ),
        },
        {
            "finding_id": "finding-cohort-maturity",
            "title": "The cohort is very early but already shaped",
            "statement": "Most of the filtered Spring 2025 companies are tiny teams, yet the use-case pattern is already visible.",
            "implication": "The category signal is useful, but product and positioning are still converging.",
            "confidence": "medium",
            "metric": f"Median team size {analysis['cohort_summary']['median_team_size']}; {analysis['cohort_summary']['teams_1_2']} teams have 1-2 people",
            "source_ids": [default_id],
        },
        {
            "finding_id": "finding-healthcare-wedge",
            "title": "Healthcare operations is a credible vertical wedge",
            "statement": "Healthcare admin workflows show enough density and pain to support focused product bets despite a smaller company count.",
            "implication": "Vertical agents with painful, repetitive workflows can outrun broader horizontal positioning.",
            "confidence": "medium",
            "metric": f"{healthcare['count']} healthcare-operations companies" if healthcare else "Healthcare appears as a smaller but high-value lane",
            "source_ids": source_ids_for_names(healthcare["examples"][:4], source_id_by_name, default_id) if healthcare else [default_id],
        },
    ]


def build_analysis_pack_contract(analysis: dict[str, Any], source_notes: dict[str, Any]) -> dict[str, Any]:
    source_id_by_name = build_source_id_lookup(source_notes)
    default_id = "src-yc-companies-directory"
    priorities = ["high", "high", "medium", "medium"]
    return {
        "report_slug": REPORT_SLUG,
        "created_at": analysis["generated_at_utc"],
        "decision_question": DECISION_QUESTION,
        "audience": PRIMARY_AUDIENCE,
        "headline": "Workflow-heavy, operator-owned agent products are the clearest commercial pattern in the Spring 2025 YC cohort.",
        "source_ids": [source["source_id"] for source in source_notes["sources"]],
        "findings": build_findings(analysis, source_id_by_name, default_id),
        "use_case_clusters": [
            {
                "cluster_id": f"cluster-{slugify(cluster['name'])}",
                "name": cluster["name"],
                "buyer": cluster["buyer"],
                "workflow_owner": cluster["workflow_owner"],
                "business_job": cluster["business_job"],
                "value_prop": cluster["value_prop"],
                "why_now": cluster["why_now"],
                "recommendation": cluster["recommendation"],
                "evidence_companies": [
                    {
                        "name": company["name"],
                        "proof_line": company.get("proof_line") or company["what_they_do"],
                        "source_id": source_id_by_name.get(company["name"], default_id),
                    }
                    for company in cluster["companies"][:5]
                ],
            }
            for cluster in analysis["use_case_clusters"]
        ],
        "risks": [
            "YC directory and company website language can overstate product maturity.",
            "Use-case labels are inferred from company text, not official taxonomy.",
            "Only a subset of companies has deeper website-backed source notes; the rest fall back to directory evidence.",
        ],
        "recommendations": [
            {
                "title": recommendation["title"],
                "why": recommendation["why"],
                "priority": priorities[idx] if idx < len(priorities) else "medium",
            }
            for idx, recommendation in enumerate(analysis["recommendations"])
        ],
        "chart_briefs": analysis["chart_recommendations"],
        "methodology": {
            "approach": (
                "Discover the live YC companies backend, filter Spring 2025 agent-pattern companies with team size <= 10, "
                "summarize use-case clusters, and enrich representative names with website-backed proof lines."
            ),
            "limitations": [
                "This is a public-web analysis, not a financial or customer-validated market study.",
                "Representative source coverage is deeper for highlighted names than for the full cohort.",
                "The cohort snapshot can change as YC company pages or descriptions change over time.",
            ],
        },
    }


def slide_type_for(spec_type: str) -> str:
    mapping = {
        "title": "hero",
        "agenda": "agenda",
        "section_divider": "section-divider",
        "summary_cards": "summary-cards",
        "kpi_grid": "kpi-grid",
        "team_distribution": "distribution-chart",
        "bar_chart": "bar-chart",
        "comparison": "comparison",
        "structured_table": "use-case-table",
        "cluster_spotlight": "cluster-spotlight",
        "vertical_table": "use-case-table",
        "company_grid": "snapshot-grid",
        "case_study": "case-study",
        "implication_bullets": "recommendation",
        "recommendation_grid": "recommendation",
        "opportunity_ladder": "roadmap",
        "methodology": "methodology",
        "appendix_sources": "source-coverage",
    }
    return mapping.get(spec_type, "custom")


def slide_objective_for(spec: dict[str, Any]) -> str:
    objectives = {
        "title": "Frame the report and set expectations quickly.",
        "agenda": "Show the narrative arc before the detailed evidence begins.",
        "section_divider": "Reset the audience and signal the next chapter of the story.",
        "summary_cards": "Land the top conclusions before the audience gets lost in the detail.",
        "kpi_grid": "Quantify the size and shape of the cohort at a glance.",
        "team_distribution": "Show how early the cohort is and why maturity assumptions should stay conservative.",
        "bar_chart": "Rank the strongest use-case clusters clearly.",
        "comparison": "Contrast expected narratives with the actual cohort pattern.",
        "structured_table": "Translate clusters into business jobs, buyers, and value propositions.",
        "cluster_spotlight": "Go deeper on one high-signal use-case cluster with evidence.",
        "vertical_table": "Show smaller but strategically important vertical or specialist lanes.",
        "company_grid": "Ground the story in source-backed company examples.",
        "case_study": "Show adjacency and implications for a specific company or strategy.",
        "implication_bullets": "Translate the case-study insight into explicit action.",
        "recommendation_grid": "Summarize the recommended moves in decision-ready form.",
        "opportunity_ladder": "Rank opportunity types by strategic attractiveness.",
        "methodology": "Explain how the analysis was built and what its limits are.",
        "appendix_sources": "Show source coverage for auditability.",
    }
    return objectives.get(spec["type"], f"Explain why {spec['title']} matters.")


def content_blocks_for_slide(spec: dict[str, Any]) -> list[dict[str, str]]:
    spec_type = spec["type"]
    if spec_type == "title":
        return [
            {"kind": "headline", "label": "Title", "body": spec["title"]},
            {"kind": "callout", "label": "Subtitle", "body": spec["subtitle"]},
            {"kind": "callout", "label": "Strapline", "body": spec["strapline"]},
        ]
    if spec_type == "agenda":
        return [
            {"kind": "roadmap-step", "label": section["number"], "body": f"{section['title']} — {section['detail']}"}
            for section in spec["sections"]
        ]
    if spec_type == "section_divider":
        return [
            {"kind": "headline", "label": spec["section"], "body": spec["title"]},
            {"kind": "callout", "label": "Transition", "body": spec["subtitle"]},
        ]
    if spec_type == "summary_cards":
        return [{"kind": "callout", "label": card["title"], "body": card["body"]} for card in spec["cards"]]
    if spec_type == "kpi_grid":
        blocks = [{"kind": "metric", "label": item["label"], "body": f"{item['value']} | {item['note']}"} for item in spec["kpis"]]
        blocks.append({"kind": "callout", "label": "Takeaway", "body": spec["takeaway"]})
        return blocks
    if spec_type in {"team_distribution", "bar_chart"}:
        return [
            {"kind": "chart-brief", "label": item["label"], "body": str(item.get("value", item.get("count")))}
            for item in spec["series"]
        ] + [{"kind": "callout", "label": "Takeaway", "body": spec["takeaway"]}]
    if spec_type == "comparison":
        return [
            {"kind": "comparison-column", "label": spec["left_title"], "body": " | ".join(spec["left_points"])},
            {"kind": "comparison-column", "label": spec["right_title"], "body": " | ".join(spec["right_points"])},
        ]
    if spec_type == "structured_table":
        return [
            {
                "kind": "table",
                "label": cluster["name"],
                "body": (
                    f"Buyer: {cluster['buyer']} | Job: {cluster['business_job']} | "
                    f"Value: {cluster['value_prop']} | Why now: {cluster['why_now']}"
                ),
            }
            for cluster in spec["clusters"][:5]
        ]
    if spec_type == "cluster_spotlight":
        blocks = [
            {"kind": "callout", "label": "Buyer", "body": spec["buyer"]},
            {"kind": "callout", "label": "Workflow owner", "body": spec["workflow_owner"]},
            {"kind": "callout", "label": "Business job", "body": spec["business_job"]},
            {"kind": "callout", "label": "Recommendation", "body": spec["recommendation"]},
        ]
        blocks.extend({"kind": "company-card", "label": example["name"], "body": example["proof_line"]} for example in spec["examples"])
        return blocks
    if spec_type == "vertical_table":
        blocks = [
            {"kind": "table", "label": cluster["name"], "body": f"{cluster['count']} | {cluster['business_job']}"}
            for cluster in spec["clusters"][:4]
        ]
        blocks.extend({"kind": "company-card", "label": company["name"], "body": company["what_they_do"]} for company in spec["companies"][:6])
        return blocks
    if spec_type == "company_grid":
        return [{"kind": "company-card", "label": company["name"], "body": company["proof_line"]} for company in spec["companies"]]
    if spec_type == "case_study":
        blocks = [{"kind": "company-card", "label": match["name"], "body": match.get("proof_line") or match.get("one_liner", "")} for match in spec["matches"][:4]]
        blocks.extend({"kind": "bullet-list", "label": "Implication", "body": item} for item in spec["implications"])
        return blocks
    if spec_type == "implication_bullets":
        return [{"kind": "bullet-list", "label": f"Action {idx}", "body": bullet} for idx, bullet in enumerate(spec["bullets"], start=1)]
    if spec_type == "recommendation_grid":
        return [{"kind": "callout", "label": item["title"], "body": item["why"]} for item in spec["recommendations"]]
    if spec_type == "opportunity_ladder":
        return [{"kind": "roadmap-step", "label": item["label"], "body": f"{item['value']} | {item['detail']}"} for item in spec["items"]]
    if spec_type == "methodology":
        return [{"kind": "bullet-list", "label": "Method", "body": bullet} for bullet in spec["bullets"]]
    if spec_type == "appendix_sources":
        return [{"kind": "company-card", "label": company["name"], "body": company["proof_line"]} for company in spec["companies"]]
    return [{"kind": "note", "label": "Content", "body": spec.get("title", "")}]


def source_names_for_slide(spec: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for key in ("companies", "matches", "examples"):
        for item in spec.get(key, []):
            name = item.get("name")
            if name:
                names.append(name)
    for cluster in spec.get("clusters", []):
        names.extend(cluster.get("examples", []))
        for company in cluster.get("companies", []):
            if company.get("name"):
                names.append(company["name"])
    return names


def build_deck_plan_contract(analysis: dict[str, Any], source_notes: dict[str, Any]) -> dict[str, Any]:
    source_id_by_name = build_source_id_lookup(source_notes)
    default_id = "src-yc-companies-directory"
    story_arc = [
        "What the cohort actually says",
        "Business use cases",
        "Strategic implications",
        "Execution priorities",
    ]
    slides = []
    current_section = "Overview"
    for idx, spec in enumerate(analysis["deck_plan"], start=1):
        if spec["type"] == "section_divider":
            current_section = spec["title"]
        elif idx <= 2:
            current_section = "Overview"
        slide = {
            "slide_id": f"slide-{idx:02d}",
            "section": current_section,
            "slide_type": slide_type_for(spec["type"]),
            "title": spec["title"],
            "objective": slide_objective_for(spec),
            "audience": PRIMARY_AUDIENCE,
            "layout": spec["type"].replace("_", "-"),
            "content_blocks": content_blocks_for_slide(spec),
            "speaker_notes": [slide_objective_for(spec)],
            "source_ids": source_ids_for_names(source_names_for_slide(spec), source_id_by_name, default_id),
            "render_spec": spec,
        }
        slides.append(slide)

    return {
        "report_slug": REPORT_SLUG,
        "created_at": analysis["generated_at_utc"],
        "audience": PRIMARY_AUDIENCE,
        "deck_goal": "Explain what Spring 2025 YC small-team agent startups are building and which use cases look strongest.",
        "theme_reference": THEME_REFERENCE,
        "story_arc": story_arc,
        "slides": slides,
        "export_targets": ["pptx", "html"],
    }


def markdown_for_analysis(analysis: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# YC Agent Companies Analysis Pack")
    lines.append("")
    lines.append(f"Generated: {analysis['generated_at_utc']}")
    lines.append("")
    lines.append("## Cohort Summary")
    lines.append("")
    lines.append(f"- Source: {analysis['source']}")
    lines.append(f"- Current YC website batch: {analysis['current_batch']}")
    lines.append(f"- Analyzed cohort: {analysis['cohort_summary']['batch']}")
    lines.append(f"- Companies: {analysis['cohort_summary']['company_count']}")
    lines.append(f"- Median team size: {analysis['cohort_summary']['median_team_size']}")
    lines.append(f"- Teams with 1-2 people: {analysis['cohort_summary']['teams_1_2']}")
    lines.append("")
    lines.append("## Structured Business Use Cases")
    lines.append("")
    for cluster in analysis["use_case_clusters"]:
        lines.append(f"### {cluster['name'].title()} ({cluster['count']})")
        lines.append("")
        lines.append(f"- Buyer: {cluster['buyer']}")
        lines.append(f"- Workflow owner: {cluster['workflow_owner']}")
        lines.append(f"- Business job: {cluster['business_job']}")
        lines.append(f"- Value prop: {cluster['value_prop']}")
        lines.append(f"- Why now: {cluster['why_now']}")
        lines.append(f"- Recommendation: {cluster['recommendation']}")
        lines.append(f"- Example companies: {', '.join(cluster['examples'])}")
        lines.append("")
    lines.append("## Sync2 Adjacency")
    lines.append("")
    for match in analysis["adjacency"]["sync2_matches"]:
        lines.append(f"- {match['name']}: {match['one_liner']}")
    lines.append("")
    lines.append("## ReprisesAI Adjacency")
    lines.append("")
    for match in analysis["adjacency"]["reprisesai_matches"]:
        lines.append(f"- {match['name']}: {match['one_liner']}")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    for rec in analysis["recommendations"]:
        lines.append(f"- **{rec['title']}**: {rec['why']}")
    lines.append("")
    return "\n".join(lines)


def markdown_for_charts(analysis: dict[str, Any]) -> str:
    lines = ["# Chart Brief", ""]
    for chart in analysis["chart_recommendations"]:
        lines.append(f"## {chart['title']}")
        lines.append("")
        lines.append(f"- Best chart type: {chart['best_chart_type']}")
        lines.append(f"- Why this fits: {chart['why_this_fits']}")
        lines.append(f"- Narrative takeaway: {chart['narrative_takeaway']}")
        lines.append(f"- Encoding guidance: {chart['encoding_guidance']}")
        lines.append(f"- Annotation plan: {chart['annotation_plan']}")
        lines.append("")
    return "\n".join(lines)


def build_analysis() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    config = yc.discover_backend()
    companies = filtered_hits(config)
    team_sizes = [hit.get("team_size") for hit in companies if hit.get("team_size") is not None]
    source_summary = load_source_summary()
    generated_at = datetime.now(timezone.utc).isoformat()
    summaries = [yc.summarize_company(hit) for hit in companies]
    for summary in summaries:
        source = source_summary.get(summary["name"])
        if source:
            summary["proof_line"] = source.get("proof_line") or summary["what_they_do"]
        else:
            summary["proof_line"] = summary["what_they_do"]
    clusters, cluster_counts = summarize_clusters(companies)
    for cluster in clusters:
        for company in cluster["companies"]:
            source = source_summary.get(company["name"])
            company["proof_line"] = (source or {}).get("proof_line") or company["what_they_do"]
    adjacency = {
        "sync2_matches": yc.merged_query_scan(
            config,
            ["clinic operations AI", "patient scheduling AI", "medical receptionist AI", "healthcare operations agents"],
            limit=8,
        ),
        "reprisesai_matches": yc.merged_query_scan(
            config,
            ["AI consulting automation", "software implementation AI agents", "workflow automation enterprise AI", "mid-market agent platform"],
            limit=8,
        ),
    }
    for key in ["sync2_matches", "reprisesai_matches"]:
        for item in adjacency[key]:
            source = source_summary.get(item["name"])
            item["proof_line"] = (source or {}).get("proof_line") or item["one_liner"]
    analysis: dict[str, Any] = {
        "generated_at_utc": generated_at,
        "report_slug": REPORT_SLUG,
        "decision_question": DECISION_QUESTION,
        "audience": PRIMARY_AUDIENCE,
        "source": config["companies_url"],
        "current_batch": config["current_batch"],
        "cohort_summary": {
            "batch": BATCH,
            "company_count": len(companies),
            "median_team_size": int(statistics.median(team_sizes)),
            "teams_1_2": sum(1 for size in team_sizes if size <= 2),
            "team_sizes": team_sizes,
            "max_team_size": MAX_TEAM_SIZE,
        },
        "companies": summaries,
        "use_case_clusters": clusters,
        "cluster_counts": dict(cluster_counts),
        "adjacency": adjacency,
        "source_summary": source_summary,
    }
    analysis["recommendations"] = build_recommendations(clusters)
    analysis["chart_recommendations"] = build_chart_recommendations(clusters, team_sizes)
    analysis["deck_plan"] = build_deck_plan(analysis)
    source_notes = build_source_notes_contract(config, summaries, source_summary, generated_at)
    analysis_pack = build_analysis_pack_contract(analysis, source_notes)
    deck_plan = build_deck_plan_contract(analysis, source_notes)
    analysis["contract_outputs"] = {
        "source_notes_path": str(SOURCE_NOTES_PATH),
        "analysis_pack_path": str(ANALYSIS_PACK_PATH),
        "deck_plan_path": str(DECK_PLAN_PATH),
    }
    return analysis, source_notes, analysis_pack, deck_plan


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_NOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    analysis, source_notes, analysis_pack, deck_plan = build_analysis()
    JSON_PATH.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    SOURCE_NOTES_PATH.write_text(json.dumps(source_notes, indent=2), encoding="utf-8")
    ANALYSIS_PACK_PATH.write_text(json.dumps(analysis_pack, indent=2), encoding="utf-8")
    DECK_PLAN_PATH.write_text(json.dumps(deck_plan, indent=2), encoding="utf-8")
    MD_PATH.write_text(markdown_for_analysis(analysis), encoding="utf-8")
    CHART_PATH.write_text(markdown_for_charts(analysis), encoding="utf-8")


if __name__ == "__main__":
    main()
