#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "starter" / "claude-to-codex-skills" / "skills"
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
ACTIVE_CODEX_HOME = Path("/home/shekerk/snap/codex/34/skills")


CATEGORY_ORDER = [
    "Research, Analysis, and Strategy",
    "Presentations and Visuals",
    "Content and Communication",
    "Sales and Presales",
    "Engineering and Automation",
    "Utilities and Personal Workflow",
]


def parse_frontmatter(skill_path: Path) -> tuple[str, str]:
    text = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return skill_path.name, ""
    name = skill_path.name
    description = ""
    for line in match.group(1).splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip()
    return name, description


def categorize(name: str) -> str:
    if (
        name.startswith("ai-strategy")
        or name in {
            "analytics-to-comms",
            "architect",
            "architecture-to-everything",
            "chart-storyteller",
            "competitive-intel-sprint",
            "content-research",
            "export-results",
            "explainer-graphic",
            "graphify",
            "llm-council",
            "obsidian-github-sync",
            "obsidian-vault-manager",
            "research-analysis-deck",
            "research-to-strategy",
            "second-brain-capture",
            "stakeholder-comms",
            "url-dossier",
            "vertical-scorer",
            "video-to-deck",
            "watch",
            "workflow-visualizer",
        }
    ):
        return "Research, Analysis, and Strategy"
    if (
        name.startswith("presentation")
        or name.startswith("marp")
        or name in {
            "carousel-to-deck",
            "install-marp",
            "markdown-preview",
            "slide-deck-builder",
        }
    ):
        return "Presentations and Visuals"
    if (
        name.startswith("content-")
        or name in {
            "anti-slop",
            "log-performance",
            "morning-briefing",
            "review-draft",
            "tune-voice",
        }
    ):
        return "Content and Communication"
    if (
        name.endswith("-architect")
        or name.endswith("-briefer")
        or name in {
            "account-intelligence-analyst",
            "crm-hygiene-enforcer",
            "presales-deal-prep",
            "proposal-generator",
        }
    ):
        return "Sales and Presales"
    if name in {
        "agent-browser",
        "code-review-specialist",
        "contract-reviewer",
        "printing-press",
    }:
        return "Engineering and Automation"
    return "Utilities and Personal Workflow"


def render() -> str:
    skills = []
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        name, description = parse_frontmatter(skill_dir)
        skills.append(
            {
                "name": name,
                "description": description,
                "path": skill_dir,
                "category": categorize(name),
            }
        )

    lines: list[str] = []
    lines.append("# AGENTS.md")
    lines.append("")
    lines.append("This repo stages a large Codex skill pack. Keep this file in sync with `starter/claude-to-codex-skills/skills/`.")
    lines.append("")
    lines.append("## Skills")
    lines.append("")
    lines.append(f"- Staged pack: `{SKILLS_DIR}`")
    lines.append(f"- Typical active install target: `{ACTIVE_CODEX_HOME}`")
    lines.append(f"- Current staged skill count: `{len(skills)}`")
    lines.append("")
    lines.append("### How to use")
    lines.append("")
    lines.append("- If the user explicitly names a skill or the task clearly matches one, use it.")
    lines.append("- Read only the minimum needed from the skill file, then follow its workflow.")
    lines.append("- Prefer the vendored scripts, references, and assets inside the skill directory over re-creating the workflow manually.")
    lines.append("- Treat `research-analysis-deck` as the default orchestrator when a request needs `research -> analysis -> deck` chaining.")
    lines.append("")
    lines.append("### Available skills")
    lines.append("")
    for category in CATEGORY_ORDER:
        category_skills = [skill for skill in skills if skill["category"] == category]
        if not category_skills:
            continue
        lines.append(f"#### {category}")
        lines.append("")
        for skill in category_skills:
            lines.append(
                f"- `{skill['name']}`: {skill['description']} "
                f"Skill file: `{skill['path'] / 'SKILL.md'}`"
            )
        lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- This file is generated by `scripts/sync_agents_skill_index.py`.")
    lines.append("- Re-run that script after adding, renaming, or removing staged skills.")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    AGENTS_PATH.write_text(render(), encoding="utf-8")
    print(AGENTS_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
