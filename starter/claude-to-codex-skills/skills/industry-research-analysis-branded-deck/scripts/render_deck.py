#!/usr/bin/env python3
"""Validate the chain and render a branded deck for any industry slug."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def pick_python() -> str:
    preferred = Path("/home/shekerk/.venv/o2c/bin/python")
    if preferred.exists():
        return str(preferred)
    return sys.executable


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_registry() -> dict[str, str]:
    registry_path = skill_root() / "references" / "builder-registry.json"
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    return payload.get("custom_builders", {})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--copy-downloads", action="store_true")
    parser.add_argument("--windows-target", default="")
    args = parser.parse_args()

    root = repo_root()
    py = pick_python()
    env = os.environ.copy()
    env.setdefault("MPLCONFIGDIR", "/tmp/mpl")

    source_notes = root / "research-notes" / args.slug / "source-notes.json"
    analysis_pack = root / "analytics-comms" / args.slug / "analysis-pack.json"
    deck_plan = root / "analytics-comms" / args.slug / "deck-plan.json"
    validate = root / "starter" / "claude-to-codex-skills" / "skills" / "research-analysis-deck" / "scripts" / "validate_chain.py"
    preview = root / "scripts" / "preview_pptx.py"
    skill_ref_dir = skill_root() / "references"

    optional_artifacts = [
        ("customer-brief", skill_ref_dir / "customer-brief.schema.json", root / "analytics-comms" / args.slug / "customer-brief.json"),
        ("strategy-brief", skill_ref_dir / "strategy-brief.schema.json", root / "analytics-comms" / args.slug / "strategy-brief.json"),
        ("use-case-priorities", skill_ref_dir / "use-case-priorities.schema.json", root / "analytics-comms" / args.slug / "use-case-priorities.json"),
        ("executive-angle", skill_ref_dir / "executive-angle.schema.json", root / "analytics-comms" / args.slug / "executive-angle.json"),
    ]

    validate_cmd = [
        py,
        str(validate),
        "--source-notes",
        str(source_notes),
        "--analysis-pack",
        str(analysis_pack),
        "--deck-plan",
        str(deck_plan),
    ]
    for label, schema_path, payload_path in optional_artifacts:
        if payload_path.exists():
            validate_cmd.extend(["--optional-json", label, str(schema_path), str(payload_path)])

    subprocess.run(
        validate_cmd,
        cwd=root,
        env=env,
        check=True,
    )

    custom = load_registry().get(args.slug)
    if custom:
        subprocess.run([py, str(root / custom)], cwd=root, env=env, check=True)
        output = root / "docs" / "reports" / f"{args.slug}-branded.pptx"
    else:
        generic = root / "scripts" / "build_industry_branded_pptx.py"
        subprocess.run([py, str(generic), "--slug", args.slug], cwd=root, env=env, check=True)
        output = root / "docs" / "reports" / f"{args.slug}-branded.pptx"

    preview_dir = root / "docs" / "reports" / "_preview" / args.slug
    subprocess.run(
        [py, str(preview), str(output), "--out-dir", str(preview_dir)],
        cwd=root,
        env=env,
        check=True,
    )
    print(preview_dir)

    if args.copy_downloads:
        target = Path(args.windows_target) if args.windows_target else Path(f"/mnt/c/Users/sheke/Downloads/{args.slug}-branded.pptx")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output, target)
        print(target)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
