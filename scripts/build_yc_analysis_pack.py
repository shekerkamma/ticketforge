#!/usr/bin/env python3
"""Build a structured YC agent-company analysis pack for downstream decks."""

from __future__ import annotations

import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import scripts.yc_companies_cli as yc


BATCH = "Spring 2025"
QUERY = "agent"
MAX_TEAM_SIZE = 10
OUTPUT_DIR = Path("analytics-comms/yc-agent-companies-spring-2025")
JSON_PATH = OUTPUT_DIR / "analysis.json"
MD_PATH = OUTPUT_DIR / "analysis.md"
CHART_PATH = OUTPUT_DIR / "chart-brief.md"
SOURCE_SUMMARY_PATH = Path("research-notes/yc-agent-companies-spring-2025/source-summary.json")


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


def build_deck_plan(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    top_clusters = analysis["use_case_clusters"][:4]
    vertical_clusters = [
        cluster
        for cluster in analysis["use_case_clusters"]
        if cluster["name"] in {"healthcare operations", "security and governance", "legal and compliance workflows", "finance and trading"}
    ]
    company_rows = []
    for cluster in top_clusters[:3]:
        for company in cluster["companies"][:2]:
            company_rows.append(
                {
                    "name": company["name"],
                    "cluster": cluster["name"],
                    "what_they_do": company.get("proof_line") or company["what_they_do"],
                }
            )
    return [
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
                {"number": "02", "title": "Business use cases", "detail": "Structured jobs, buyers, and evidence clusters"},
                {"number": "03", "title": "Strategic implications", "detail": "Sync2, ReprisesAI, and what to do next"},
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
            "type": "structured_table",
            "title": "Top Use Cases, Structured As Business Jobs",
            "subtitle": "These are the highest-signal business shapes in the cohort",
            "clusters": top_clusters,
        },
        {
            "type": "vertical_table",
            "title": "Vertical And Specialist Lanes Matter Too",
            "subtitle": "Smaller clusters can still be strategically attractive when pain and willingness to pay are high",
            "clusters": vertical_clusters,
            "companies": company_rows[:6],
        },
        {
            "type": "section_divider",
            "section": "SECTION 02",
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
            "type": "recommendation_grid",
            "title": "What I Would Do Next",
            "subtitle": "The recommendations follow directly from the cohort structure",
            "recommendations": analysis["recommendations"],
        },
        {
            "type": "methodology",
            "title": "Method And Reproducibility",
            "bullets": [
                "Website tested: https://www.ycombinator.com/companies",
                "yc-companies discovers the live YC backend from the public page each run",
                "Primary filter: Spring 2025, agent / agentic pattern, team size <= 10",
                f"Structured cluster counts derived from {analysis['cohort_summary']['company_count']} filtered companies",
                "Use-case labels are inferred from company text, not official YC categories",
            ],
        },
    ]


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


def build_analysis() -> dict[str, Any]:
    config = yc.discover_backend()
    companies = filtered_hits(config)
    team_sizes = [hit.get("team_size") for hit in companies if hit.get("team_size") is not None]
    source_summary = load_source_summary()
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
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
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
    return analysis


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    analysis = build_analysis()
    JSON_PATH.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    MD_PATH.write_text(markdown_for_analysis(analysis), encoding="utf-8")
    CHART_PATH.write_text(markdown_for_charts(analysis), encoding="utf-8")


if __name__ == "__main__":
    main()
