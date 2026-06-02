#!/usr/bin/env python3
"""Validate the chain and render a branded deck for any industry slug."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


CUSTOM_BUILDERS = {
    "healthcare-provider-ops-ai-usecases": "scripts/build_healthcare_provider_ops_branded_pptx.py",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def pick_python() -> str:
    preferred = Path("/home/shekerk/.venv/o2c/bin/python")
    if preferred.exists():
        return str(preferred)
    return sys.executable


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

    subprocess.run(
        [
            py,
            str(validate),
            "--source-notes",
            str(source_notes),
            "--analysis-pack",
            str(analysis_pack),
            "--deck-plan",
            str(deck_plan),
        ],
        cwd=root,
        env=env,
        check=True,
    )

    custom = CUSTOM_BUILDERS.get(args.slug)
    if custom:
        subprocess.run([py, str(root / custom)], cwd=root, env=env, check=True)
        output = root / "docs" / "reports" / f"{args.slug}-branded.pptx"
    else:
        generic = root / "scripts" / "build_industry_branded_pptx.py"
        subprocess.run([py, str(generic), "--slug", args.slug], cwd=root, env=env, check=True)
        output = root / "docs" / "reports" / f"{args.slug}-branded.pptx"

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
