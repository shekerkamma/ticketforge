#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def normalize_deck_plan(deck_plan: dict, slide_type_map: dict[str, str]) -> dict:
    updated = copy.deepcopy(deck_plan)
    for slide in updated.get("slides", []):
        slide_type = slide.get("slide_type")
        if slide_type in slide_type_map:
            slide["slide_type"] = slide_type_map[slide_type]
    return updated


def tiered_cluster_names(names: list[str]) -> dict[str, list[str]]:
    tier_1 = names[:2]
    tier_2 = names[2:4]
    tier_3 = names[4:]
    return {
        "tier_1": tier_1,
        "tier_2": tier_2,
        "tier_3": tier_3,
    }


def action_items_from_recommendations(recommendations: list[dict]) -> list[dict]:
    actions: list[dict] = []
    for item in recommendations:
        actions.append(
            {
                "title": item["title"],
                "why": item["why"],
                "priority": item.get("priority", "medium"),
            }
        )
    return actions
