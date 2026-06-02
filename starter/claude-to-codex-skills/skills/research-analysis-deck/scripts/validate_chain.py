#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REF_DIR = SCRIPT_DIR.parent / "references"


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_datetime(value: str, path: str) -> None:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{path}: invalid date-time '{value}'") from exc


def validate(schema: dict[str, Any], value: Any, path: str) -> None:
    schema_type = schema.get("type")
    if schema_type == "object":
        if not isinstance(value, dict):
            raise ValidationError(f"{path}: expected object")
        for key in schema.get("required", []):
            if key not in value:
                raise ValidationError(f"{path}: missing required key '{key}'")
        properties = schema.get("properties", {})
        for key, sub_value in value.items():
            sub_schema = properties.get(key)
            if sub_schema is not None:
                validate(sub_schema, sub_value, f"{path}.{key}")
    elif schema_type == "array":
        if not isinstance(value, list):
            raise ValidationError(f"{path}: expected array")
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            raise ValidationError(f"{path}: expected at least {min_items} items")
        item_schema = schema.get("items")
        if item_schema is not None:
            for idx, item in enumerate(value):
                validate(item_schema, item, f"{path}[{idx}]")
    elif schema_type == "string":
        if not isinstance(value, str):
            raise ValidationError(f"{path}: expected string")
        if "enum" in schema and value not in schema["enum"]:
            raise ValidationError(f"{path}: expected one of {schema['enum']}, got '{value}'")
        if schema.get("format") == "date-time":
            check_datetime(value, path)
    elif schema_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValidationError(f"{path}: expected integer")
    elif schema_type == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValidationError(f"{path}: expected number")
    elif schema_type == "boolean":
        if not isinstance(value, bool):
            raise ValidationError(f"{path}: expected boolean")
    elif schema_type is None:
        return
    else:
        raise ValidationError(f"{path}: unsupported schema type '{schema_type}'")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate chain artifacts against the bundled schemas.")
    parser.add_argument("--source-notes", type=Path, required=True)
    parser.add_argument("--analysis-pack", type=Path, required=True)
    parser.add_argument("--deck-plan", type=Path, required=True)
    args = parser.parse_args()

    targets = [
        ("source-notes", REF_DIR / "source-note.schema.json", args.source_notes),
        ("analysis-pack", REF_DIR / "analysis-pack.schema.json", args.analysis_pack),
        ("deck-plan", REF_DIR / "deck-plan.schema.json", args.deck_plan)
    ]

    for label, schema_path, payload_path in targets:
        schema = load_json(schema_path)
        payload = load_json(payload_path)
        validate(schema, payload, label)
        print(f"valid: {payload_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
