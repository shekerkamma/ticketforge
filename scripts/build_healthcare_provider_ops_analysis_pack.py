#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from industry_contract_example_utils import (
    ROOT,
    action_items_from_recommendations,
    load_json,
    normalize_deck_plan,
    tiered_cluster_names,
    unique_strings,
    write_json,
)


REPORT_SLUG = "healthcare-provider-ops-ai-usecases"
CREATED_AT = "2026-06-02T22:00:00Z"
DECISION_QUESTION = (
    "Which AI use cases in healthcare provider operations are strongest right now, "
    "and how should a health system prioritize them?"
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
        "Produce a research-backed executive deck on healthcare provider operations AI use cases "
        "with clear prioritization and operating implications."
    )
    payload["theme_reference"] = "Use the branded executive slide system already established in this repo."
    payload["story_arc"] = [
        "Why provider-ops AI is moving now",
        "Which workflow families have the clearest proof",
        "How to prioritize the top use cases",
        "What healthcare executives should fund next",
    ]
    payload["export_targets"] = ["pptx", "html", "memo"]
    return normalize_deck_plan(payload, SLIDE_TYPE_MAP)


def build_strategy_brief(analysis_pack: dict) -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "decision": (
            "Prioritize ambient documentation and visit support, patient access and prior authorization, "
            "revenue-cycle status and denial prevention, capacity and perioperative orchestration, and coding automation "
            "as the first healthcare provider-operations AI programs."
        ),
        "why_this_matters": (
            "Healthcare provider-operations AI now matters because the clearest value is emerging in workflow-embedded "
            "administrative domains where systems can reduce manual coordination, improve cash flow, or reclaim clinician time."
        ),
        "executive_view": (
            "Health system leaders should read AI as an operating-model prioritization problem inside the EHR, revenue cycle, "
            "and access workflows, not as a generic enterprise-assistant rollout."
        ),
        "strategic_implications": [
            "Administrative workflows with clear owners and clear economics should lead over broad assistant deployments.",
            "EHR-adjacent execution matters more than standalone AI experiences because downstream workflow ownership determines whether value compounds.",
            "Assistive and autonomous workflows should be sequenced differently so governance and operating readiness stay explicit.",
            "Operational proof from access, RCM, and perioperative workflows gives executives a stronger funding story than abstract innovation narratives.",
        ],
        "recommended_actions": action_items_from_recommendations(analysis_pack["recommendations"]),
        "kpis": [
            "prior-authorization turnaround time",
            "denial rate and avoidable rework",
            "visit documentation time returned",
            "cash-collection or reimbursement cycle time",
            "OR block utilization and schedule throughput",
        ],
        "bottom_line": (
            "The right provider-operations AI story is workflow relief with hard operating metrics, "
            "not broad enterprise assistant deployment."
        ),
    }


def build_customer_brief(analysis_pack: dict) -> dict:
    clusters = analysis_pack["use_case_clusters"]
    buyers = unique_strings([cluster["buyer"] for cluster in clusters])
    owners = unique_strings([cluster["workflow_owner"] for cluster in clusters])
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "customer_scope": "industry-only",
        "customer_label": "Health system and provider-operations executive teams",
        "why_this_customer_matters": (
            "Provider organizations already have visible administrative pain, growing AI adoption, and concrete public proof points "
            "across documentation, access, prior authorization, perioperative orchestration, and coding."
        ),
        "public_signals": [
            "McKinsey's 2026 healthcare survey shows implementation has moved beyond experimentation.",
            "The AMA reported two in three physicians were already using health AI in 2025.",
            "UCHealth scaled ambient documentation with Abridge systemwide.",
            "Qventus published perioperative throughput proof at Saint Luke's.",
            "Notable published automation proof for prior authorizations at Fort HealthCare.",
            "AKASA and CodaMetrix show durable revenue-cycle and coding workflow demand.",
        ],
        "executive_priorities": [
            "reduce administrative burden without breaking clinical flow",
            "improve cash acceleration and denial prevention",
            "reclaim clinician time inside the EHR",
            "increase capacity utilization in constrained workflows",
            "sequence assistive and executional AI with clear accountability",
        ],
        "workflow_owners": owners,
        "best_entry_points": buyers,
        "best_use_case_angles": [cluster["name"] for cluster in clusters],
    }


def build_executive_angle() -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "primary_audience": "healthcare provider executives",
        "lead_with": [
            "operating friction and time recovery",
            "cash-flow and denial economics",
            "workflow ownership inside the EHR and RCM stack",
            "what to sequence first versus later",
        ],
        "avoid_leading_with": [
            "generic clinical AI hype",
            "broad assistant narratives without workflow owners",
            "tool demos detached from downstream process change",
            "shrinking text-dense tables instead of surfacing operating choices",
        ],
        "decision_frame": (
            "Frame the deck as a provider-operations investment and sequencing decision rather than as a general AI-awareness presentation."
        ),
    }


def build_use_case_priorities(analysis_pack: dict) -> dict:
    names = [cluster["name"] for cluster in analysis_pack["use_case_clusters"]]
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "prioritization_basis": "workflow ownership, measurable economics, and EHR-adjacent operating readiness",
        "tiers": tiered_cluster_names(names),
        "rationale": (
            "The order follows which healthcare workflows already show public proof, have a named operational owner, "
            "and can be measured in time, capacity, or revenue-cycle impact."
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
