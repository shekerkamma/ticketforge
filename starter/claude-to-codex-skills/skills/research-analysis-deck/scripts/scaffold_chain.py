#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold the research -> analysis -> deck chain files.")
    parser.add_argument("--slug", required=True, help="Stable slug for the report or analysis.")
    parser.add_argument("--question", required=True, help="Decision or research question.")
    parser.add_argument("--audience", required=True, help="Primary target audience.")
    parser.add_argument("--goal", default="Produce a deck-ready market or company analysis.", help="Deck goal.")
    parser.add_argument(
        "--theme-reference",
        default="Use the current branded reference deck or client template.",
        help="Reference template or theme note."
    )
    parser.add_argument(
        "--include-industry-pack",
        action="store_true",
        help="Also scaffold customer/strategy/use-case/executive JSON artifacts for the industry deck wrapper.",
    )
    args = parser.parse_args()

    stamp = now_iso()
    source_path = Path("research-notes") / args.slug / "source-notes.json"
    analysis_path = Path("analytics-comms") / args.slug / "analysis-pack.json"
    deck_path = Path("analytics-comms") / args.slug / "deck-plan.json"
    customer_path = Path("analytics-comms") / args.slug / "customer-brief.json"
    strategy_path = Path("analytics-comms") / args.slug / "strategy-brief.json"
    priorities_path = Path("analytics-comms") / args.slug / "use-case-priorities.json"
    executive_angle_path = Path("analytics-comms") / args.slug / "executive-angle.json"

    source_payload = {
        "report_slug": args.slug,
        "created_at": stamp,
        "decision_question": args.question,
        "sources": []
    }
    analysis_payload = {
        "report_slug": args.slug,
        "created_at": stamp,
        "decision_question": args.question,
        "audience": args.audience,
        "headline": "",
        "source_ids": [],
        "findings": [],
        "use_case_clusters": [],
        "risks": [],
        "recommendations": [],
        "chart_briefs": [],
        "methodology": {
            "approach": "",
            "limitations": []
        }
    }
    deck_payload = {
        "report_slug": args.slug,
        "created_at": stamp,
        "audience": args.audience,
        "deck_goal": args.goal,
        "theme_reference": args.theme_reference,
        "story_arc": [],
        "slides": [],
        "export_targets": [
            "pptx"
        ]
    }

    write_json(source_path, source_payload)
    write_json(analysis_path, analysis_payload)
    write_json(deck_path, deck_payload)

    if args.include_industry_pack:
        customer_payload = {
            "report_slug": args.slug,
            "created_at": stamp,
            "customer_scope": "industry-only",
            "customer_label": "",
            "why_this_customer_matters": "",
            "public_signals": [],
            "executive_priorities": [],
            "workflow_owners": [],
            "best_entry_points": [],
            "best_use_case_angles": [],
        }
        strategy_payload = {
            "report_slug": args.slug,
            "created_at": stamp,
            "decision": "",
            "why_this_matters": "",
            "executive_view": "",
            "strategic_implications": [],
            "recommended_actions": [],
            "kpis": [],
            "bottom_line": "",
        }
        priorities_payload = {
            "report_slug": args.slug,
            "created_at": stamp,
            "prioritization_basis": "",
            "tiers": {
                "tier_1": [],
                "tier_2": [],
                "tier_3": []
            },
            "rationale": "",
        }
        executive_angle_payload = {
            "report_slug": args.slug,
            "created_at": stamp,
            "primary_audience": args.audience,
            "lead_with": [],
            "avoid_leading_with": [],
            "decision_frame": "",
        }
        write_json(customer_path, customer_payload)
        write_json(strategy_path, strategy_payload)
        write_json(priorities_path, priorities_payload)
        write_json(executive_angle_path, executive_angle_payload)

    print(source_path)
    print(analysis_path)
    print(deck_path)
    if args.include_industry_pack:
        print(customer_path)
        print(strategy_path)
        print(priorities_path)
        print(executive_angle_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
