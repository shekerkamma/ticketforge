#!/usr/bin/env python3
from __future__ import annotations

from industry_contract_example_utils import (
    ROOT,
    action_items_from_recommendations,
    load_json,
    normalize_deck_plan,
    tiered_cluster_names,
    unique_strings,
    write_json,
)


REPORT_SLUG = "toyota-automotive-ai-usecases"
CREATED_AT = "2026-06-02T22:15:00Z"
DECISION_QUESTION = (
    "Which AI use cases in the automotive industry look strongest right now, "
    "and how does Toyota show what an OEM-grade AI operating model should look like?"
)

RESEARCH_DIR = ROOT / "research-notes" / REPORT_SLUG
ANALYTICS_DIR = ROOT / "analytics-comms" / REPORT_SLUG

SLIDE_TYPE_MAP = {
    "use-case-table": "use-case-card-grid",
    "case-study": "use-case-deep-dive",
    "roadmap": "executive-action",
}


def build_source_notes() -> dict:
    payload = load_json(RESEARCH_DIR / "source-notes.json")
    payload["report_slug"] = REPORT_SLUG
    payload["created_at"] = CREATED_AT
    payload["decision_question"] = DECISION_QUESTION
    return payload


def build_analysis_pack() -> dict:
    payload = load_json(ANALYTICS_DIR / "analysis-pack.json")
    payload["report_slug"] = REPORT_SLUG
    payload["created_at"] = CREATED_AT
    payload["decision_question"] = DECISION_QUESTION
    payload["audience"] = "executive"
    return payload


def build_deck_plan() -> dict:
    payload = load_json(ANALYTICS_DIR / "deck-plan.json")
    payload["report_slug"] = REPORT_SLUG
    payload["created_at"] = CREATED_AT
    payload["audience"] = "executive"
    payload["deck_goal"] = (
        "Produce a research-backed executive deck on automotive AI priorities using Toyota as the named customer lens."
    )
    payload["theme_reference"] = "Use the branded executive slide system already established in this repo."
    payload["story_arc"] = [
        "Why automotive AI is shifting toward platform and workflow value",
        "Why Toyota is the strongest named-customer lens",
        "Which AI workflow families matter most",
        "What automotive executives should sequence next",
    ]
    payload["export_targets"] = ["pptx", "html", "memo"]
    payload = normalize_deck_plan(payload, SLIDE_TYPE_MAP)
    title_map = {
        "s1": "Toyota Automotive AI Operating Model",
        "s3": "Automotive AI Is The Operating System",
        "s7": "Toyota's AI Story Is Bigger Than In-Car Assistants",
        "s15": "GAIA As Toyota's Group AI Operating System",
        "s19": "What This Means For OEM Strategy",
        "s20": "Four Strategic Implications",
        "s21": "Where Toyota Should Bet Next",
        "s25": "The Decision Is Workflow Ownership",
    }
    for slide in payload.get("slides", []):
        if slide.get("slide_id") in title_map:
            slide["title"] = title_map[slide["slide_id"]]
    return payload


def build_strategy_brief(analysis_pack: dict) -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "decision": (
            "Toyota should keep prioritizing software-defined vehicle platform reuse, manufacturing and engineering productivity, "
            "connected vehicle data services, safety and validation workflows, and live mobility ecosystem experimentation over generic in-cabin AI feature narratives."
        ),
        "why_this_matters": (
            "Automotive AI value is concentrating around platforms, reusable validation systems, data loops, and operating workflows that compound across vehicle programs."
        ),
        "executive_view": (
            "Toyota is strongest where a workflow owner exists, software or data gets reused across programs, and real-world validation closes the loop."
        ),
        "strategic_implications": [
            "Toyota's emerging moat is operational and platform-based, not only manufacturing-based.",
            "The best AI bets are workflow-led because they directly improve release speed, engineering throughput, service quality, safety, and new service revenue.",
            "Executives should keep separating reusable platform work from feature theater in the vehicle cabin.",
            "Toyota's public materials suggest compounding value sits where software reuse, validation, and connected-data services reinforce one another.",
        ],
        "recommended_actions": action_items_from_recommendations(analysis_pack["recommendations"]),
        "kpis": [
            "software reuse rate across vehicle programs",
            "validation cycle time and release confidence",
            "engineering throughput",
            "connected-service or claims cycle time",
            "pilot-to-scale learning velocity",
        ],
        "bottom_line": (
            "Toyota's strongest automotive AI strategy is AI in the platform, workflow, validation loop, and mobility system, not just AI in the car."
        ),
    }


def build_customer_brief(analysis_pack: dict) -> dict:
    clusters = analysis_pack["use_case_clusters"]
    buyers = unique_strings([cluster["buyer"] for cluster in clusters])
    owners = unique_strings([cluster["workflow_owner"] for cluster in clusters])
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "customer_scope": "named-customer",
        "customer_label": "Toyota Motor Corporation",
        "why_this_customer_matters": (
            "Toyota provides one of the clearest public examples of an OEM treating AI as operating-system infrastructure across software-defined vehicles, "
            "engineering productivity, connected services, and real-world mobility experimentation."
        ),
        "public_signals": [
            "Arene is debuting in the new RAV4 as Toyota's software-defined vehicle platform backbone.",
            "GAIA and the Toyota Software Academy show AI capability building as a group-level operating system.",
            "Connected-car and telematics workflows already link vehicle data to service and claims outcomes.",
            "Woven City remains a live experimentation environment for cross-system mobility services.",
            "Toyota's production and vehicle scale make workflow improvements strategically meaningful across programs.",
        ],
        "executive_priorities": [
            "software-defined vehicle platform reuse",
            "engineering and manufacturing productivity",
            "connected-services monetization and workflow quality",
            "safety and validation coverage",
            "disciplined mobility-system experimentation",
        ],
        "workflow_owners": owners,
        "best_entry_points": buyers,
        "best_use_case_angles": [cluster["name"] for cluster in clusters],
    }


def build_executive_angle() -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "primary_audience": "automotive business and operating executives",
        "lead_with": [
            "platform reuse and compounding economics",
            "workflow ownership across engineering, manufacturing, and service",
            "validation and safety confidence",
            "which AI lanes create monetizable or operational leverage first",
        ],
        "avoid_leading_with": [
            "generic in-cabin assistant hype",
            "feature demos without workflow ownership",
            "AI taxonomies detached from OEM operating systems",
            "weak tables where platform-vs-feature choices should be explicit",
        ],
        "decision_frame": (
            "Frame the deck as an automotive operating-model and sequencing decision, using Toyota as the proof that platform and workflow AI create the durable moat."
        ),
    }


def build_use_case_priorities(analysis_pack: dict) -> dict:
    names = [cluster["name"] for cluster in analysis_pack["use_case_clusters"]]
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "prioritization_basis": "workflow ownership, software reuse, validation loop strength, and monetizable operating impact",
        "tiers": tiered_cluster_names(names),
        "rationale": (
            "The order follows where Toyota already demonstrates a reusable platform layer, a real workflow owner, and closed-loop validation or customer operations value."
        ),
    }


def main() -> int:
    source_notes = build_source_notes()
    analysis_pack = build_analysis_pack()
    deck_plan = build_deck_plan()

    write_json(RESEARCH_DIR / "source-notes.json", source_notes)
    write_json(ANALYTICS_DIR / "analysis-pack.json", analysis_pack)
    write_json(ANALYTICS_DIR / "deck-plan.json", deck_plan)
    write_json(ANALYTICS_DIR / "strategy-brief.json", build_strategy_brief(analysis_pack))
    write_json(ANALYTICS_DIR / "customer-brief.json", build_customer_brief(analysis_pack))
    write_json(ANALYTICS_DIR / "executive-angle.json", build_executive_angle())
    write_json(ANALYTICS_DIR / "use-case-priorities.json", build_use_case_priorities(analysis_pack))
    print(REPORT_SLUG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
