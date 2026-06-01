#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pwd
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STAGING_ROOT = REPO_ROOT / "starter" / "claude-to-codex-skills"
STAGING_SKILLS_DIR = STAGING_ROOT / "skills"

CHAIN_TEMPLATE_SKILLS = {
    "architect",
    "architecture-to-everything",
    "presentation",
    "content-research",
    "research-to-strategy",
}

SUPPORTED_SKILLS = {
    "architect",
    "architecture-to-everything",
    "session-handoff",
    "time-skill",
    "time-tokyo",
    "weather-fetcher",
    "weather-fetcher-tokyo",
    "code-review-specialist",
    "contract-reviewer",
    "difficult-conversation-prep",
    "workflow-visualizer",
    "graphify",
    "explainer-graphic",
    "presentation",
    "presentation-content-writer",
    "presentation-theme",
    "presentation-exporter",
    "presentation-speaker-notes",
    "presentation-accessibility",
    "content-research",
    "research-to-strategy",
}

REWRITE_MARKERS = {
    "AskUserQuestion": "depends on Claude-only AskUserQuestion flow",
    "~/.claude/skills/gstack": "depends on gstack helper scripts",
    ".claude/skills/gstack": "depends on vendored gstack helper scripts",
    "preamble-tier:": "uses Claude-specific preamble metadata",
    "run_in_background": "depends on Claude background shell tracking",
    "TodoWrite": "depends on Claude todo state",
}

LIGHT_EDIT_MARKERS = {
    "~/.claude/": "hard-codes Claude home paths",
    "/clear": "references Claude slash commands",
    "WebFetch tool": "names a Claude-specific web tool",
    "Read tool": "names a Claude-specific read tool",
    "Write tool": "names a Claude-specific write tool",
    "Edit tool": "names a Claude-specific edit tool",
    "user-invocable:": "uses non-essential Claude frontmatter",
    "allowed-tools:": "uses Claude-specific tool metadata",
    "benefits-from:": "uses Claude-specific skill metadata",
}

PORT_TEMPLATES = {
    "session-handoff": """---
name: session-handoff
description: Use when the user asks for a session handoff, wrap-up summary, or a structured context transfer for the next Codex session. Produces a terse handoff covering decisions, shipped changes, key files, running state, verification, and open questions.
---

# Session Handoff

Produce a repeatable handoff artifact for the next Codex session. The audience is a fresh agent, not a stakeholder.

## Workflow

1. Review the current conversation before summarizing.
2. Pull state from:
   - files created or edited this session
   - plan files or prompts that drove the work
   - running processes, open branches, and local services
   - unresolved questions or deferred tasks
3. Do not audit unrelated repo history. Summarize this session only.
4. Write the handoff to `~/.codex/session-handoff.md`.
5. Also print the same handoff in chat.

## Output structure

Use exactly this structure:

```markdown
# Session Handoff — <one-line title>

## Where it started
<2-3 sentences>

## Decisions locked + what shipped
- <decision or change> — <why, and where it lives>

## Key files for next session
- `<absolute path>` — <why it matters>

## Running state
- Background processes: <ids + purpose + kill command> or `none`
- Dev servers / ports: <url + port> or `none`
- Open branches / worktrees: <paths> or `none`

## Verification — how to confirm things still work
- `<command>` — <expected outcome>

## Deferred + open questions
- Deferred: <item> — <why later>
- Open: <question> — <context>

## Pick up here
<1-2 sentences with the most likely next action>
```

## Hard rules

- Always use absolute paths.
- Never invent state. If a section is empty, write `none`.
- If a plan file drove the session, list it first under `Key files for next session`.
- Keep the tone terse and operational.

## After writing the handoff

Tell the user:

> Handoff saved. Start the next Codex session and ask it to read `~/.codex/session-handoff.md` first.
""",
    "time-skill": """---
name: time-skill
description: Display the current time in Pakistan Standard Time (PKT, UTC+5). Use when the user asks for the current time, Pakistan time, or PKT.
---

# Time Skill

Run:

```bash
TZ='Asia/Karachi' date '+%Y-%m-%d %H:%M:%S %Z'
```

Return the result as:

```text
Current Time in Pakistan (PKT): YYYY-MM-DD HH:MM:SS PKT
```

Requirements:

- Always use the `Asia/Karachi` timezone.
- Use 24-hour format.
- Keep the response concise.
""",
    "weather-fetcher": """---
name: weather-fetcher
description: Fetch the current temperature for Dubai, UAE from Open-Meteo. Use when the user asks for Dubai weather or the current Dubai temperature in Celsius or Fahrenheit.
---

# Weather Fetcher

Fetch the current Dubai temperature from Open-Meteo. Use the available web tool or `curl`.

## URLs

- Celsius: `https://api.open-meteo.com/v1/forecast?latitude=25.2048&longitude=55.2708&current=temperature_2m&temperature_unit=celsius`
- Fahrenheit: `https://api.open-meteo.com/v1/forecast?latitude=25.2048&longitude=55.2708&current=temperature_2m&temperature_unit=fahrenheit`

## What to extract

- Value: `current.temperature_2m`
- Unit: `current_units.temperature_2m`

## Output

```text
Current Dubai Temperature: [X]°[C/F]
Unit: [Celsius/Fahrenheit]
```

If network access is unavailable, say so directly instead of guessing.
""",
    "code-review-specialist": """---
name: code-review-specialist
description: Review code changes for bugs, regressions, security issues, performance problems, and missing tests. Use when the user asks for a review, PR review, code quality audit, or risk assessment.
---

# Code Review Specialist

Review the change with a bug-finding mindset first. Prioritize correctness and risk over style.

## Review order

1. Correctness and behavioral regressions
2. Security and data exposure
3. Performance or scaling risks
4. Operability and developer workflow impacts
5. Missing tests or weak verification

## Output format

- Findings first, ordered by severity.
- Each finding should include the file path, line reference when available, why it matters, and the likely fix direction.
- Keep summaries brief and place them after the findings.
- If there are no findings, say so explicitly and note any residual risks or testing gaps.

## Constraints

- Focus on concrete issues, not speculative refactors.
- Prefer changed files and directly affected call paths first.
- Call out high-confidence issues only.
""",
}

PORT_TEMPLATES.update(
    {
        "architect": {
            "SKILL.md": """---
name: architect
description: Produce a structured build plan for a project, feature, or system design using multiple expert perspectives, debate, and synthesis. Use when the user asks to architect something, plan a build, design a system, or turn a brief into an execution plan.
---

# Architect

Turn a project brief into a master plan that can actually be executed.

Read `references/planning-methodology.md` before producing the plan.

## Workflow

1. Parse the brief.
2. Choose 3-5 expert personas that cover the problem from distinct angles.
3. Generate an independent round-1 plan from each persona.
4. Produce a debate summary covering agreements, conflicts, and gaps.
5. Revise the persona plans against the debate summary.
6. Synthesize a master plan.
7. If the user wants execution tracking, create `BUILD_STATUS.yaml`.

## Output files

- `working/plans/round1/<persona>.md`
- `working/plans/debate-summary.md`
- `working/plans/round2/<persona>.md`
- `<project>_MASTER_PLAN.md`
- `BUILD_STATUS.yaml` when requested

## Rules

- Ask at most one clarifying question if the brief is too vague.
- Use absolute or repo-root-relative paths in the master plan.
- Prefer concrete waves, task IDs, dependencies, and changed-file summaries over prose.
- If parallel subagents are unavailable, simulate the same methodology sequentially in one session.
""",
            "references/planning-methodology.md": """# Planning Methodology

Use this when the `architect` skill is active.

## Phase 0: Scope and personas

- Define the brief, constraints, examples, and success criteria.
- Pick 3-5 personas with distinct concerns.
- Good persona mix:
  - End-user advocate
  - Technical architect
  - Domain specialist
  - Growth or business strategist
  - Ops or delivery engineer

## Phase 1: Independent plans

Each persona should cover:

1. What needs to be built
2. How it should be structured
3. Proposed waves or phases
4. Dependencies
5. Risks and unknowns
6. What they would push back on

## Phase 2: Debate summary

The moderator should extract:

- Agreements
- Conflicts
- Gaps
- Resolutions with reasoning
- Open questions

## Phase 3: Revised plans

Each persona revises their plan using the debate summary.

## Phase 4: Synthesis

The master plan should include:

1. Executive summary
2. Wave structure table
3. Detailed waves and task specs
4. Dependency graph
5. Files changed summary
6. Open questions

## BUILD_STATUS.yaml

Recommended fields:

```yaml
project: example-project
master_plan: ./EXAMPLE_MASTER_PLAN.md
current_wave: 0
total_waves: 4
tasks:
  - id: W0.1
    wave: 0
    description: Example task
    status: not_started
    depends_on: []
    output_files: []
```

## Practical rules

- Never run parallel builders against the same output file.
- Prefer explicit task IDs and dependencies over vague checklists.
- Keep the tracker current if work continues across sessions.
""",
        },
        "presentation": {
            "SKILL.md": """---
name: presentation
description: Create, update, or repair presentation decks and slide content. Use when the user asks to edit slides, build a deck, change presentation structure, adjust styling, add notes, export a deck, or improve presentation accessibility.
---

# Presentation

This is the Codex-native presentation curator. It replaces the old Claude agent wrapper with a direct workflow.

## Companion skills

Use these when they are installed and relevant:

- `presentation-content-writer`
- `presentation-theme`
- `presentation-speaker-notes`
- `presentation-exporter`
- `presentation-accessibility`

## References

Read these on demand:

- `references/structure.md` for numbering, section transitions, and navigation
- `references/styling.md` for HTML/CSS component patterns
- `references/framework.md` for narrative arc and slide sequencing

## Workflow

1. Locate the target deck. Default to `presentation/index.html` if the user did not specify a file.
2. Classify the request:
   - content creation
   - structure or numbering
   - styling or theming
   - speaker notes
   - export
   - accessibility
3. Load only the references needed for that task.
4. Edit the deck directly instead of delegating to a separate agent.
5. After any structural edit:
   - renumber slides sequentially
   - update any navigation links such as `goToSlide(...)`
   - keep section transitions coherent
6. When notes, export, or accessibility are requested, either use the companion skills or follow their workflow directly.

## Rules

- Preserve content unless the user asked for rewrites.
- Never leave duplicate or skipped slide numbers.
- Keep deck changes reviewable; prefer scoped edits over whole-deck rewrites.
- Report which slides changed and any follow-on work still needed.
""",
            "references/structure.md": """# Presentation Structure

Use this when changing slide order or section flow.

## Core rules

- Each slide should have a sequential `data-slide` number.
- Section divider slides may carry a `data-level` or similar journey marker.
- After adding, removing, or moving slides:
  - renumber all slide indices
  - update table-of-contents links
  - verify no gaps or duplicates

## Typical slide types

- Title slide
- Section divider
- Content slide
- Comparison slide
- Code example slide
- Closing or call-to-action slide

## Good editing behavior

- Keep the narrative progression intact.
- Use section dividers for large topic changes.
- If the deck already has a progress or journey bar, preserve its underlying logic.
""",
            "references/styling.md": """# Presentation Styling

Use this when changing HTML/CSS presentation decks.

## Common component patterns

- Two-column comparisons for before/after
- Card grids for grouped information
- Highlight boxes for key concepts or warnings
- Code blocks with clear syntax contrast
- Icon lists for capabilities or options

## Theme rules

- Maintain readable contrast.
- Keep code blocks legible.
- Avoid changing content when the task is only visual.
- Prefer CSS variables or a single theme block when possible.

## Practical reminders

- Match the established layout system before inventing a new one.
- Preserve responsive behavior.
- Use semantic HTML where possible.
""",
            "references/framework.md": """# Presentation Framework

Use this when creating or rewriting the deck narrative.

## Narrative arc

1. Establish the problem
2. Show why the audience should care
3. Explain the mechanism or approach
4. Present evidence, examples, or comparisons
5. End with a concrete recommendation or next step

## Content rules

- One strong idea per slide
- Prefer concrete claims over vague topics
- Use contrast to create clarity
- Make transitions explicit
- End with action, not summary-only filler
""",
        },
        "content-research": """---
name: content-research
description: Ingest URLs, documents, repositories, or mixed source material into structured research notes and synthesis. Use when the user wants to research content, collect source notes, build a second brain, or analyze multiple sources before strategy work.
---

# Content Research

This is the Codex-native version of the content research pipeline.

## Workflow

1. Parse the input sources.
2. Classify each source:
   - video
   - LinkedIn or social post
   - GitHub repo or file
   - web page
   - local document
3. Ingest each source with the most reliable available tool:
   - web access or `curl` for URLs
   - `gh` for GitHub metadata when useful
   - direct file reads for local documents
4. Create one structured markdown note per source.
5. Produce a cross-source synthesis.
6. If the user wants relationships or graph output, run `graphify` on the note directory when available.

## Suggested note structure

```markdown
---
title: <source title>
source: <url or path>
source_type: <type>
date_captured: <YYYY-MM-DD>
tags: [research]
---

# <title>

## TL;DR

## Key claims

## Evidence and quotes

## Risks or uncertainties

## Why it matters
```

## Outputs

- `research-notes/<slug>.md` per source
- `research-notes/INDEX.md` source register
- `research-synthesis.md`

## Rules

- Keep raw excerpts separate from your synthesis.
- Do not invent engagement metrics, pricing, or author claims.
- Flag uncertainty explicitly when data is partial or scraped indirectly.
- Prefer a reusable notes directory over one-off chat summaries.
""",
        "research-to-strategy": """---
name: research-to-strategy
description: Turn research notes and source material into a strategic recommendation, brief, or deck. Use when the user wants research transformed into a recommendation, strategy memo, decision brief, or presentation.
---

# Research To Strategy

This is a Codex-native chain skill that turns gathered research into a decision-ready output.

## Expected chain

1. Gather or refresh source notes with `content-research`
2. Optional: connect themes with `graphify`
3. Synthesize options and tensions
4. Recommend a strategy
5. Optional: package the result with `presentation`

## Workflow

1. Confirm the decision question, audience, and output format.
2. Reuse existing research notes if they are current; otherwise create or refresh them.
3. Extract:
   - strongest claims
   - strongest evidence
   - contradictions
   - missing information
4. Turn the evidence into 2-4 strategic options.
5. Evaluate each option for upside, downside, cost, risk, and reversibility.
6. Make a recommendation with explicit assumptions.
7. If a deck or talk track is requested, draft it through the `presentation` workflow.

## Outputs

- `strategy-brief.md`
- `strategy-options.md`
- optional deck outline or slide content

## Rules

- Do not confuse research volume with conviction.
- Separate evidence, interpretation, and recommendation.
- If confidence is low, say why and what would raise it.
- End with one concrete next action.
""",
        "architecture-to-everything": """---
name: architecture-to-everything
description: Turn a system description or architecture artifact into a full package: plan, architecture brief, diagram, interactive walkthrough, and presentation. Use when the user wants one architecture represented in multiple formats.
---

# Architecture To Everything

This is a Codex-native chain skill for creating a full architecture package.

## Companion skills

- `architect`
- `workflow-visualizer`
- `explainer-graphic`
- `presentation`

## Workflow

1. Capture the system brief, constraints, and target audience.
2. If the system is still fuzzy, run the `architect` methodology first to produce a master plan.
3. Produce the architecture brief:
   - system purpose
   - component inventory
   - data flows
   - dependencies
   - risks and open questions
4. Create the workflow or system diagram. Use `workflow-visualizer` when appropriate.
5. Create one analogy-driven explainer artifact for non-technical audiences. Use `explainer-graphic` when appropriate.
6. Build the deck or slide outline through the `presentation` workflow.

## Suggested outputs

- `architecture-brief.md`
- `architecture-components.md`
- `architecture-workflow.html`
- `architecture-explainer.md` or infographic brief
- `architecture-deck.md` or deck files

## Rules

- Keep technical and executive outputs aligned on the same source truth.
- Prefer one canonical component list that every artifact reuses.
- If assumptions differ across artifacts, call that out explicitly.
- Report which parts are complete and which still need design polish or export.
""",
    }
)

TemplateValue = str | dict[str, str]


@dataclass
class Skill:
    rel_path: str
    path: Path
    name: str
    description: str
    raw_text: str


def resolve_user_home() -> Path:
    try:
        return Path(pwd.getpwuid(os.getuid()).pw_dir)
    except KeyError:
        return Path.home()


USER_HOME = resolve_user_home()
CLAUDE_SKILLS_DIR = USER_HOME / ".claude" / "skills"


def parse_frontmatter(raw_text: str) -> tuple[dict[str, str], str]:
    if not raw_text.startswith("---\n"):
        return {}, raw_text

    parts = raw_text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, raw_text

    metadata: dict[str, str] = {}
    for line in parts[0].splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, parts[1]


def discover_skills() -> list[Skill]:
    if not CLAUDE_SKILLS_DIR.exists():
        return []

    skills: list[Skill] = []
    for skill_path in sorted(CLAUDE_SKILLS_DIR.rglob("SKILL.md")):
        if not skill_path.exists() or not skill_path.is_file():
            continue
        rel_path = skill_path.parent.relative_to(CLAUDE_SKILLS_DIR).as_posix()
        try:
            raw_text = skill_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            continue
        metadata, _ = parse_frontmatter(raw_text)
        name = metadata.get("name", skill_path.parent.name)
        description = metadata.get("description", "")
        skills.append(
            Skill(
                rel_path=rel_path,
                path=skill_path,
                name=name,
                description=description,
                raw_text=raw_text,
            )
        )
    return skills


def classify_skill(skill: Skill) -> tuple[str, list[str]]:
    if skill.name in SUPPORTED_SKILLS:
        reasons = ["has a repo-managed Codex adaptation template"]
        if skill.name in CHAIN_TEMPLATE_SKILLS:
            reasons.append("uses a Codex-native chain workflow instead of the Claude wrapper")
            return "light_edit", reasons
        if skill.name == "session-handoff":
            reasons.append("needs path and session-flow rewrites")
            return "light_edit", reasons
        if skill.name in {
            "weather-fetcher",
            "weather-fetcher-tokyo",
            "code-review-specialist",
            "presentation-content-writer",
            "presentation-theme",
            "presentation-exporter",
            "presentation-speaker-notes",
            "presentation-accessibility",
        }:
            reasons.append("needs small wording changes for Codex tools")
            return "light_edit", reasons
        return "direct_port", reasons

    if skill.rel_path.startswith("gstack/"):
        return "rewrite", ["nested gstack skill tree is Claude-specific"]

    rewrite_reasons = [
        reason for marker, reason in REWRITE_MARKERS.items() if marker in skill.raw_text
    ]
    if rewrite_reasons:
        return "rewrite", rewrite_reasons

    light_reasons = [
        reason for marker, reason in LIGHT_EDIT_MARKERS.items() if marker in skill.raw_text
    ]
    if light_reasons:
        return "light_edit", light_reasons

    return "direct_port", ["plain instruction skill with no obvious Claude coupling"]


def inventory() -> int:
    skills = discover_skills()
    if not skills:
        print(f"No Claude skills found under {CLAUDE_SKILLS_DIR}", file=sys.stderr)
        return 1

    print("classification\tskill\tpath\treasons")
    for skill in skills:
        classification, reasons = classify_skill(skill)
        joined = "; ".join(reasons)
        print(f"{classification}\t{skill.name}\t{skill.rel_path}\t{joined}")
    return 0


def clean_staging_dir() -> None:
    STAGING_SKILLS_DIR.mkdir(parents=True, exist_ok=True)


def build_skill_index(skills: list[Skill]) -> dict[str, Skill]:
    skill_index: dict[str, Skill] = {}
    names_seen: dict[str, Skill] = {}
    duplicate_names: set[str] = set()

    for skill in skills:
        skill_index[skill.rel_path] = skill
        if skill.name in names_seen:
            duplicate_names.add(skill.name)
        else:
            names_seen[skill.name] = skill
            skill_index[skill.name] = skill

    for name in duplicate_names:
        skill_index.pop(name, None)

    return skill_index


def generic_adaptation(skill: Skill) -> str:
    _, body = parse_frontmatter(skill.raw_text)
    description = skill.description or f"Migrated from Claude skill: {skill.rel_path}"
    content = body.strip()

    replacements = (
        ("~/.claude/", "~/.codex/"),
        ("WebFetch tool", "available web tool or curl"),
        ("Read tool", "file-reading tools"),
        ("Write tool", "file-editing tools"),
        ("Edit tool", "file-editing tools"),
        ("/clear", "start a fresh Codex session"),
    )
    for old, new in replacements:
        content = content.replace(old, new)

    return "\n".join(
        (
            "---",
            f"name: {skill.name}",
            f"description: {description}",
            "---",
            "",
            content,
            "",
        )
    )


def write_template_bundle(skill_dir: Path, rendered: TemplateValue) -> None:
    if isinstance(rendered, str):
        (skill_dir / "SKILL.md").write_text(rendered, encoding="utf-8")
        return

    for relative_path, content in rendered.items():
        target = skill_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def stage_skills(selected_names: list[str]) -> int:
    clean_staging_dir()
    skills = discover_skills()
    skill_index = build_skill_index(skills)

    status = 0

    for name in selected_names:
        rendered = PORT_TEMPLATES.get(name)
        if rendered is None:
            skill = skill_index.get(name)
            if skill is None:
                print(f"Missing Claude skill or staged template: {name}", file=sys.stderr)
                status = 1
                continue

            classification, reasons = classify_skill(skill)
            if classification == "rewrite":
                joined = "; ".join(reasons)
                print(f"rewrite-only\t{name}\t{joined}", file=sys.stderr)
                status = 1
                continue
            rendered = generic_adaptation(skill)

        skill_dir = STAGING_SKILLS_DIR / name
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        skill_dir.mkdir(parents=True, exist_ok=True)
        write_template_bundle(skill_dir, rendered)
        print(f"staged\t{name}\t{skill_dir}")
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory Claude skills and stage Codex-ready adaptations."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("inventory", help="List Claude skills and migration classes.")

    stage_parser = subparsers.add_parser(
        "stage", help="Write staged Codex skill adaptations into the repo."
    )
    stage_parser.add_argument(
        "--skills",
        default=",".join(sorted(SUPPORTED_SKILLS)),
        help="Comma-separated skill names to stage. Default: the supported starter set.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "inventory":
        return inventory()

    if args.command == "stage":
        selected_names = [name.strip() for name in args.skills.split(",") if name.strip()]
        return stage_skills(selected_names)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
