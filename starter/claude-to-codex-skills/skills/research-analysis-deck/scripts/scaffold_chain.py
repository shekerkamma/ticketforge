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
    args = parser.parse_args()

    stamp = now_iso()
    source_path = Path("research-notes") / args.slug / "source-notes.json"
    analysis_path = Path("analytics-comms") / args.slug / "analysis-pack.json"
    deck_path = Path("analytics-comms") / args.slug / "deck-plan.json"

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

    print(source_path)
    print(analysis_path)
    print(deck_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
