#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pwd
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
STAGING_ROOT = REPO_ROOT / "starter" / "claude-to-codex-skills"
STAGING_SKILLS_DIR = STAGING_ROOT / "skills"

CHAIN_TEMPLATE_SKILLS = {
    "agent-browser",
    "account-intelligence-analyst",
    "ai-analyst",
    "ai-strategy-council",
    "ai-strategy-researcher",
    "ask-question",
    "analytics-to-comms",
    "compare-datasets",
    "architect",
    "architecture-to-everything",
    "carousel-to-deck",
    "connect-data",
    "content-draft-writer",
    "content-marketing-team",
    "content-outlier-research",
    "content-performance-tracker",
    "content-publish-helper",
    "content-repurpose",
    "content-topic-queue",
    "content-weekly-report",
    "competitive-intel-sprint",
    "crm-hygiene-enforcer",
    "define-metric",
    "design-experiment",
    "explore-data",
    "export-results",
    "forecast",
    "install-marp",
    "manage-runs",
    "markdown-preview",
    "marp-deck-builder",
    "marp-exporter",
    "morning-briefing",
    "obsidian-github-sync",
    "obsidian-vault-manager",
    "outreach-architect",
    "printing-press",
    "precall-briefer",
    "presentation",
    "proposal-generator",
    "presales-deal-prep",
    "run-analysis",
    "research-analysis-deck",
    "review-draft",
    "setup",
    "size-opportunity",
    "content-research",
    "research-to-strategy",
    "second-brain-capture",
    "slide-deck-builder",
    "ss",
    "stakeholder-comms",
    "tune-voice",
    "video-to-deck",
    "llm-council",
    "url-dossier",
}

SUPPORTED_SKILLS = {
    "ai-analyst",
    "ask-question",
    "analysis-design-spec",
    "account-intelligence-analyst",
    "anti-slop",
    "agent-browser",
    "architect",
    "archaeology",
    "archive-analysis",
    "architecture-to-everything",
    "ai-strategy-brief",
    "ai-strategy-council",
    "ai-strategy-researcher",
    "analytics-to-comms",
    "business-context",
    "close-the-loop",
    "compare-datasets",
    "connect-data",
    "crm-hygiene-enforcer",
    "session-handoff",
    "ss",
    "time-skill",
    "time-tokyo",
    "weather-fetcher",
    "weather-fetcher-tokyo",
    "code-review-specialist",
    "contract-reviewer",
    "content-draft-writer",
    "content-marketing-team",
    "content-outlier-research",
    "content-performance-tracker",
    "content-publish-helper",
    "content-topic-queue",
    "content-weekly-report",
    "data-quality-check",
    "deep-profile",
    "define-metric",
    "design-experiment",
    "difficult-conversation-prep",
    "explore-data",
    "workflow-visualizer",
    "feedback-capture",
    "first-run-welcome",
    "forecast",
    "guardrails",
    "graphify",
    "explainer-graphic",
    "competitive-intel-sprint",
    "content-repurpose",
    "export-results",
    "install-marp",
    "knowledge-bootstrap",
    "llm-council",
    "log-correction",
    "log-performance",
    "manage-runs",
    "markdown-preview",
    "marp-deck-builder",
    "marp-exporter",
    "morning-briefing",
    "obsidian-github-sync",
    "obsidian-vault-manager",
    "outreach-architect",
    "printing-press",
    "precall-briefer",
    "presentation",
    "presentation-content-writer",
    "presentation-theme",
    "presentation-exporter",
    "presentation-speaker-notes",
    "presentation-accessibility",
    "proposal-generator",
    "question-framing",
    "question-router",
    "research-analysis-deck",
    "review-draft",
    "resume-analysis",
    "run-analysis",
    "content-research",
    "research-to-strategy",
    "semantic-validation",
    "second-brain-capture",
    "setup",
    "size-opportunity",
    "switch-dataset",
    "tracking-gaps",
    "triangulation",
    "view-history",
    "view-metrics",
    "visualization-patterns",
    "watch",
    "url-dossier",
    "vertical-scorer",
    "presales-deal-prep",
    "presentation-themes",
    "slide-deck-builder",
    "stakeholder-comms",
    "tune-voice",
    "video-to-deck",
    "chart-storyteller",
    "carousel-to-deck",
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
        "watch": """---
name: watch
description: Watch a video from YouTube, Vimeo, TikTok, X, or a local file by extracting frames and transcript evidence. Use when the user asks to analyze a video, summarize a YouTube link, inspect a screen recording, or answer questions about what happens in a video.
---

# Watch

This is a Codex-adapted version of the open-source `watch` skill. It vendors the working Python scripts from the original project and removes the Claude-only setup flow.

## Skill directory

Use:

```bash
WATCH_SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/watch"
```

In this environment, `CODEX_HOME` should already point to the active Codex skill home.

## Workflow

1. Run silent preflight:

```bash
python3 "$WATCH_SKILL_DIR/scripts/setup.py" --check
```

2. If preflight fails, run:

```bash
python3 "$WATCH_SKILL_DIR/scripts/setup.py"
```

3. If Whisper API keys are still missing after setup, continue with `--no-whisper` unless the user explicitly wants full fallback transcription.
4. Run the watcher:

```bash
python3 "$WATCH_SKILL_DIR/scripts/watch.py" "<video-url-or-path>"
```

5. Read every frame path the report prints.
6. Use the transcript and frames together to answer the user.

## Good use cases

- summarize a YouTube video
- inspect a screen recording or bug repro video
- analyze the opening hook of a creator video
- answer timestamp-specific questions about a video

## Focus mode

When the user asks about a specific moment or range, pass `--start` and `--end` to get denser frame coverage:

```bash
python3 "$WATCH_SKILL_DIR/scripts/watch.py" "<video-url-or-path>" --start 2:15 --end 2:45
```

## Constraints

- Best results are on videos under about 10 minutes unless you focus on a specific section.
- Token cost is dominated by frames; use focus ranges for long videos.
- Native captions are preferred. Whisper fallback requires a key in the watch config.
- `agent-browser` is not required for this skill.

## Provenance

Based on the MIT-licensed `bradautomates/claude-video` project, adapted for Codex use.
""",
        "url-dossier": """---
name: url-dossier
description: Turn any URL into a structured dossier. Use when the user wants a link analyzed, summarized, turned into notes, or classified by source type. Supports web pages, GitHub URLs, and video URLs by chaining to the right workflow.
---

# URL Dossier

This is a Codex-native chain skill for "analyze this link" requests.

## Companion skills

- `watch` for video URLs or local video files
- `content-research` for multi-source research
- `graphify` when the user wants relationship mapping

## Workflow

1. Parse the URL or list of URLs.
2. Classify each source:
   - video URL or local video file
   - GitHub repo or file URL
   - generic web page
   - document URL
3. Route by type:
   - video: use `watch`
   - GitHub: use `gh` plus direct file reads when useful
   - web/document: use web access or `curl`
4. Produce a structured dossier for each source.
5. If there are multiple sources, add a cross-source synthesis.

## Suggested dossier format

```markdown
# URL Dossier — <title>

## Source
- URL:
- Type:
- Captured:

## TL;DR

## Key claims or contents

## Evidence

## Risks, gaps, or uncertainty

## Why it matters
```

## Output paths

- `url-dossiers/<slug>.md`
- optional `url-dossiers/INDEX.md`

## Rules

- Prefer the narrowest tool that fits the source.
- Keep raw evidence separate from your interpretation.
- If the source is a video, rely on frame and transcript evidence instead of title-only summaries.
- If the source is GitHub, capture repo metadata and key files, not just the README headline.
""",
    }
)

PORT_TEMPLATES.update(
    {
        "llm-council": """---
name: llm-council
description: Pressure-test a real decision or tradeoff through multiple advisor perspectives, peer review, and synthesis. Use when the user wants multiple viewpoints on a consequential choice, asks to run a council, or needs a decision stress-tested instead of answered once.
---

# LLM Council

This is the Codex-native version of the council pattern.

## When to use it

Use this for decisions with stakes, competing options, or unclear tradeoffs.

Do not use it for:

- simple factual lookups
- straightforward writing tasks
- trivial yes/no questions with no meaningful downside

## Workflow

1. Frame the decision clearly.
2. Pull in the minimum relevant context from the workspace or linked material.
3. Run five viewpoints:
   - The Killer
   - The Rebuilder
   - The Maximizer
   - The Stranger
   - The Operator
4. Anonymize the five responses as A-E.
5. Run a peer review pass over those responses.
6. Synthesize a chairman verdict.
7. Save the results if the user wants a durable artifact.

## Required output structure

```markdown
## Where the Council Agrees

## Where the Council Clashes

## Blind Spots the Council Caught

## The Recommendation

## The One Thing to Do First
```

## Optional output files

- `council-output/<slug>-report.md`
- `council-output/<slug>-report.html`

## Rules

- If the question is too vague, ask at most one clarifying question.
- The final recommendation must pick a side.
- If subagent fan-out is available, use it. If not, simulate the same five-advisor structure sequentially in one session without collapsing the viewpoints into one voice.
- Keep advisor responses distinct. Do not smooth out disagreement too early.
""",
        "vertical-scorer": """---
name: vertical-scorer
description: Score one or more AI verticals or business opportunities against a structured investment-style framework. Use when the user wants to compare opportunities, prioritize a market, or evaluate whether a vertical is structurally attractive for AI.
---

# Vertical Scorer

Score a vertical using a structured matrix rather than gut feel.

## The seven dimensions

1. Intelligence Ratio
2. Outsourcing Readiness
3. TAM Accessibility
4. Data Moat Potential
5. Regulatory Friction
6. Incumbent Vulnerability
7. Mirage PMF Risk

Score each from `1` to `5` with evidence.

## Research protocol

For each vertical, gather signals on:

- market size and accessibility
- outsourcing or labor structure
- regulation and compliance
- incumbents and fragmentation
- proof points and failures

## Output format

Produce a scannable scorecard:

```markdown
VERTICAL SCORECARD: <name>

Dimension | Score | Signal
--- | --- | ---
...

COMPOSITE SCORE: XX/35
VERDICT: GO / CONDITIONAL / WAIT / PASS
KEY RISK:
COPILOT TO AUTOPILOT PATH:
SOURCES:
```

For multiple verticals, also produce a comparison matrix and a recommendation.

## Rules

- Scores must be backed by evidence, not vibes.
- Include at least one failure or cautionary signal.
- If evidence is thin, lower confidence and say so explicitly.
""",
        "ai-strategy-brief": """---
name: ai-strategy-brief
description: Produce a concise executive decision memo for an AI strategy topic, market, or vertical. Use when the user wants a quick strategic brief, not a full long-form report.
---

# AI Strategy Brief

Generate a short decision memo a stakeholder can read quickly.

## Workflow

1. Gather focused market, competition, thesis, and risk signals.
2. Distill them into:
   - The Signal
   - The Opportunity
   - Who Is Winning
   - The Risk
   - Framework Fit
3. End with a verdict and rationale.

## Default output

Write markdown first:

- `strategy-briefs/<slug>-brief.md`

Optional:

- export to `.docx` if the environment has `python-docx` and the user asked for it

## Structure

```markdown
# Executive Brief: <topic>

## The Signal

## The Opportunity

## Who Is Winning

## The Risk

## Framework Fit

## Verdict

## References
```

## Rules

- Keep the core memo under roughly 500 words.
- Lead with the most concrete number or event.
- Prefer signal over completeness.
""",
        "ai-strategy-researcher": """---
name: ai-strategy-researcher
description: Research a market, vertical, or AI strategy topic deeply and produce a structured strategy report. Use when the user wants market intelligence, a strategy document, or a researched view of how an AI opportunity should be evaluated.
---

# AI Strategy Researcher

This is the Codex-native strategy research workflow.

## Research passes

1. Market signals
2. Competitive proof points
3. Failure analysis
4. Unit economics and GTM patterns
5. Framework application

## Frameworks to apply

- Copilot vs Autopilot
- Intelligence vs Judgment
- Mirage PMF risk
- North Star Metric

## Default outputs

- `strategy-research/<slug>-strategy.md`
- `strategy-research/<slug>-sources.md`

Optional:

- `.docx` export if requested and the environment supports it

## Report structure

```markdown
# Strategy Research: <topic>

## Executive Summary

## Market Signal Analysis

## Macro Thesis

## Market Sizing and Vertical Analysis

## Proof Points

## Operational Playbook

## Unit Economics

## Competitive Moats

## Risk Analysis

## Strategic Framework

## Competitive Landscape

## References
```

## Rules

- Prefer primary and operator-grade sources.
- Separate evidence from your interpretation.
- Convert relative dates into absolute dates.
- If you cannot support a section with evidence, say so instead of padding it.
""",
        "competitive-intel-sprint": """---
name: competitive-intel-sprint
description: Build a structured competitive intelligence package from a competitor name, video, site, or source bundle. Use when the user wants competitive analysis, a threat assessment, or an executive brief on what a competitor is doing.
---

# Competitive Intel Sprint

This is a Codex-native chain skill for competitive analysis.

## Companion skills

- `watch`
- `content-research`
- `ai-strategy-researcher`
- `vertical-scorer`
- `ai-strategy-brief`
- `presentation`

## Workflow

1. Capture the competitor name, source material, and the comparison lens.
2. If there is a demo or presentation video, run `watch`.
3. Build structured source notes with `content-research`.
4. Add broader market context with `ai-strategy-researcher`.
5. Score the opportunity or threat with `vertical-scorer`.
6. Turn the result into an executive brief with `ai-strategy-brief`.
7. If requested, package the findings into slides through `presentation`.

## Outputs

- `competitive-intel/<slug>-research.md`
- `competitive-intel/<slug>-market-context.md`
- `competitive-intel/<slug>-scorecard.md`
- `competitive-intel/<slug>-brief.md`
- optional deck outline or slide files

## Deliverable requirements

Always include:

- threat level
- 3 actionable takeaways
- win/loss matrix
- recommended next move

## Rules

- Distinguish between observed product facts, inferred GTM strategy, and speculation.
- Quote exact claims when they come from videos or marketing material.
- Treat absence of evidence as uncertainty, not a negative signal.
""",
        "analytics-to-comms": """---
name: analytics-to-comms
description: Turn a data question and its analysis into a stakeholder-ready communication package. Use when the user wants data analyzed and then translated into an infographic, slide outline, memo, or shareable summary.
---

# Analytics To Comms

This is a Codex-native chain skill for going from analysis to communication.

## Companion skills

- `explainer-graphic`
- `presentation`

## Workflow

1. Clarify the data question, audience, and data source.
2. Run the analysis using the normal repo or environment tools available for the dataset.
3. Distill:
   - the headline finding
   - the key metric
   - the most important supporting evidence
4. Build one visual explanation with `explainer-graphic`.
5. Package the result with `presentation` when a deck is needed.
6. If no downstream publishing tool exists, write a shareable draft instead of pretending to post anywhere.

## Outputs

- `analytics-comms/<slug>-analysis.md`
- `analytics-comms/<slug>-key-visual.md` or infographic brief
- `analytics-comms/<slug>-deck.md` or slide files
- `analytics-comms/<slug>-share-draft.md`

## Rules

- Never hide the methodology behind the recommendation.
- Keep the communication layer faithful to the underlying numbers.
- If confidence is weak, say so in the share draft as well as the analysis.
- Prefer draft artifacts over fake integrations to Slack or Notion.
""",
    }
)

PORT_TEMPLATES.update(
    {
        "ai-strategy-council": """---
name: ai-strategy-council
description: Combine real market research with a structured council verdict. Use when the user wants evidence-backed strategic judgment rather than generic brainstorming or research alone.
---

# AI Strategy Council

This is the Codex-native synthesis of `ai-strategy-researcher` and `llm-council`.

## Companion skills

- `ai-strategy-researcher`
- `llm-council`

## Workflow

1. Clarify the decision question.
2. Run a rapid market evidence pass using the `ai-strategy-researcher` workflow.
3. Extract the few evidence points that should constrain the decision.
4. Run `llm-council` on the evidence-backed question, not the raw vague prompt.
5. If the council surfaces major blind spots, do a short follow-up research pass.
6. Produce a final decision package.

## Outputs

- `strategy-council/<slug>-evidence.md`
- `strategy-council/<slug>-verdict.md`
- optional `strategy-council/<slug>-report.html`

## Required sections

```markdown
## The Evidence Says

## Where the Council Agrees

## Where the Council Clashes

## Blind Spots Filled

## The Verdict

## Decision Framework

## The Next Three Moves
```

## Rules

- Research narrows the decision space first; the council should not operate on generic framing.
- The verdict must cite specific evidence, not only advisor opinion.
- If confidence remains low after follow-up research, say exactly why.
""",
        "presales-deal-prep": """---
name: presales-deal-prep
description: Prepare for a prospect or client meeting with research, positioning, contract risk review, and objection handling. Use when the user wants presales prep, meeting prep, pitch prep, or deal prep for a prospect.
---

# Presales Deal Prep

This is a Codex-native chain skill for enterprise deal preparation.

## Companion skills

- `content-research`
- `ai-strategy-brief`
- `contract-reviewer`
- `difficult-conversation-prep`
- `presentation`

## Workflow

1. Capture the prospect, meeting context, and your offering.
2. Build an account brief with `content-research`.
3. Turn that into a vertical-aware positioning memo with `ai-strategy-brief`.
4. If a contract or terms document exists, run `contract-reviewer`.
5. Build objection handling and conversation scripts with `difficult-conversation-prep`.
6. If needed, package the pitch angle into slides through `presentation`.

## Outputs

- `presales/<slug>-account-brief.md`
- `presales/<slug>-positioning-brief.md`
- `presales/<slug>-contract-review.md` when relevant
- `presales/<slug>-meeting-prep.md`
- optional slide outline or deck draft

## Required cheat sheet

Always produce a compact one-page summary with:

- 3 key facts about the prospect
- your positioning angle
- top 3 objections and responses
- recommended opening line

## Rules

- Prefer concrete company signals over generic vertical boilerplate.
- Keep legal review separate from sales positioning.
- If no contract exists, say that explicitly instead of implying it was checked.
""",
        "content-repurpose": """---
name: content-repurpose
description: Turn one source asset into multiple platform-specific content outputs. Use when the user wants a video, article, transcript, notes, or source document repurposed into hooks, posts, captions, outlines, or a content calendar.
---

# Content Repurpose

This is a Codex-native content repurposing chain skill.

## Companion skills

- `watch` for video sources
- `content-research` for URL or document ingestion
- `presentation` when the source should become a talk or deck

## Workflow

1. Capture the source asset and target platforms.
2. Ingest the source:
   - video -> `watch`
   - article, URL, doc -> `content-research`
3. Extract:
   - core thesis
   - 3-7 atomic ideas
   - strongest quotes or hooks
   - reusable proof points
4. Generate platform-specific outputs such as:
   - short hooks
   - LinkedIn posts
   - X threads
   - email outline
   - captions
   - content calendar
5. Keep one source-of-truth note that shows which outputs came from which idea.

## Outputs

- `content-repurpose/<slug>-source.md`
- `content-repurpose/<slug>-idea-map.md`
- `content-repurpose/<slug>-outputs.md`

## Rules

- Do not invent claims that are not in the source.
- Keep platform variations faithful to the same core idea set.
- Separate extraction from rewriting so the lineage is visible.
""",
        "chart-storyteller": """---
name: chart-storyteller
description: Turn data findings into clear chart recommendations and narrative annotations. Use when the user wants to decide what chart to use, how to explain a chart, or how to present quantitative findings clearly.
---

# Chart Storyteller

Help the user choose and explain charts that match the analytical question.

## Workflow

1. Identify the analytical task:
   - comparison
   - trend
   - composition
   - distribution
   - relationship
   - ranking
2. Recommend the most appropriate chart type and explain why.
3. Provide:
   - title
   - takeaway sentence
   - axis or encoding guidance
   - annotation ideas
   - common failure modes
4. If the user already has a chart, critique it and propose a stronger version.

## Output structure

```markdown
# Chart Recommendation

## Best Chart Type

## Why This Fits

## Narrative Takeaway

## Encoding Guidance

## Annotation Plan

## Common Mistakes To Avoid
```

## Rules

- Match the chart to the question, not to aesthetic preference.
- Prefer simpler charts when they communicate the same point.
- If the data does not support a chart confidently, say what is missing.
""",
    }
)

PORT_TEMPLATES.update(
    {
        "anti-slop": """---
name: anti-slop
description: Remove AI-sounding prose patterns from writing. Use when the user wants LinkedIn posts, emails, briefs, reports, blog posts, summaries, or any human-facing prose to sound direct and non-generic.
---

# Anti-Slop

This skill is a writing filter, not a content generator.

## Core rule

Write like a competent human talking to another competent human. Cut inflated, corporate, influencer, and AI-default phrasing.

## Enforce these rules

- Prefer plain verbs over abstract ones.
- Start with the point; remove throat-clearing.
- Avoid hype, cheerleading, and fake-casual honesty markers.
- Do not pad with synonym stacks or rhetorical question/answer patterns.
- End when the point is finished.

## Replace patterns like these

- `utilize` -> `use`
- `leverage` -> `use`
- `facilitate` -> `help` or `enable`
- `robust` -> `strong`, `reliable`, or be specific
- `seamless` -> `smooth`, `simple`, or explain what is easy
- `cutting-edge`, `innovative`, `transformative` -> describe what is actually new
- `stakeholders` -> name the actual group
- `it's important to note` -> delete
- `in today's landscape` -> delete
- `honestly`, `frankly`, `real talk` -> delete
- `excited to share`, `thrilled to announce` -> delete unless the user explicitly wants that tone

## Structural rules

- Avoid "not just X, but Y" framing unless contrast is genuinely necessary.
- Avoid rule-of-three padding if two points are enough.
- Avoid dramatic fragments unless the content truly calls for them.
- Prefer one sharp sentence over three vague ones.

## How to use it

Apply this skill as a final pass on drafts:

1. remove banned words and phrases
2. compress obvious filler
3. replace abstractions with specifics
4. keep the user's actual point and voice

If the draft already sounds clean, make only minimal edits.
""",
        "agent-browser": """---
name: agent-browser
description: Browser automation CLI for websites, forms, login flows, screenshots, scraping, and interactive web testing. Use when the user wants to open a site, click through a flow, fill a form, take browser screenshots, or automate browser actions with the `agent-browser` CLI.
---

# Agent Browser

Use the `agent-browser` CLI as the browser automation runtime.

## Preflight

First verify the CLI exists:

```bash
command -v agent-browser
```

If it is missing, say so directly and stop instead of inventing browser steps.

## Core workflow

1. Open a page:

```bash
agent-browser open <url>
```

2. Snapshot interactive elements:

```bash
agent-browser snapshot -i
```

3. Interact using refs like `@e1`, `@e2`:

```bash
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser select @e3 "option"
```

4. Re-snapshot after any navigation or DOM-changing action.

## Common commands

```bash
agent-browser open <url>
agent-browser close
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser type @e2 "text"
agent-browser select @e3 "option"
agent-browser check @e4
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser wait --url "**/dashboard"
agent-browser get text @e1
agent-browser get url
agent-browser get title
agent-browser screenshot
agent-browser screenshot --full
agent-browser pdf output.pdf
```

## Stateful flows

For authenticated or repeated sessions:

```bash
agent-browser state save auth.json
agent-browser state load auth.json
```

For parallel sessions:

```bash
agent-browser --session site1 open <url>
agent-browser --session site2 open <url>
agent-browser session list
```

## Rules

- Re-snapshot after navigation, submissions, or dynamic DOM changes.
- Use the CLI's own state mechanism instead of inventing cookie storage.
- If the task depends on the user's real desktop Chrome profile, say that this skill alone is not enough.
- If the user wants visible debugging, prefer `--headed`.
""",
        "carousel-to-deck": """---
name: carousel-to-deck
description: Turn carousel copy into a usable slide deck or presentation file plan. Use when the user has carousel text and wants it converted into slides, a deck outline, or a presentation artifact they can present or hand off.
---

# Carousel To Deck

Convert social-carousel content into a real presentation structure.

## Companion skills

- `presentation`
- `presentation-content-writer`
- `presentation-speaker-notes`
- `presentation-exporter`

## Workflow

1. Read the carousel source:
   - pasted copy
   - markdown file
   - repurposed content file
2. Parse each slide's:
   - number
   - headline
   - body copy
   - design direction, if present
3. Map the slides into presentation roles:
   - cover
   - content slides
   - close / CTA
4. Build a slide outline or HTML deck through the `presentation` workflow.
5. Put design-direction notes into speaker notes or production notes instead of audience-facing body text.
6. If the environment supports deck export, use `presentation-exporter`; otherwise leave a clean deck source plus notes.

## Rules

- Keep slide headlines sharp; do not bury them in paragraph text.
- Vary the slide rhythm; do not make every slide structurally identical.
- Treat design-direction text as production guidance, not visible copy.
- If the user wants an actual `.pptx`, say whether the environment has a real export path instead of pretending.
""",
        "morning-briefing": """---
name: morning-briefing
description: Produce a daily enterprise-AI briefing focused on Sheker's priorities: automotive AI, Azure, AWS Bedrock, Google Vertex AI, Anthropic, and agentic frameworks. Use when the user asks for a morning briefing, daily scan, or what matters today.
---

# Morning Briefing

Generate a focused daily signal brief, not a generic news dump.

## Priorities

Bias the scan toward:

- Anthropic and Claude updates
- Azure OpenAI, Power Platform, Copilot Studio
- AWS Bedrock and Bedrock Agents
- Google Vertex AI and ADK
- automotive AI and SAP + AI work
- agentic framework releases with real enterprise relevance

Ignore low-signal items like consumer AI apps, generic funding news, or hype with no enterprise angle.

## Workflow

1. Gather at least 6 targeted searches and collect at least 8 raw findings.
2. Score each finding for:
   - relevance to active work
   - buzz
   - timeliness
   - POC applicability
   - client impact
   - accessibility today
3. Discard weak items.
4. Build the briefing:
   - top signals
   - quick hits
   - one concrete recommendation for today

## Output structure

```markdown
# Morning Briefing — <date>

## Top 3 Signals

### 1. <title>
**Score:** <n>/22 | **Urgency:** <red/yellow/green>
**What happened:** ...
**POC / client angle:** ...
**Action:** ...

## Quick Hits
- ...

## Recommendation
...
```

## Rules

- Be opinionated.
- Frame every item through enterprise POC delivery, not abstract interest.
- If a Claude / Anthropic developer product update is materially relevant, it belongs near the top.
- If only 2 items matter, return 2. Do not pad to 3.
""",
        "account-intelligence-analyst": """---
name: account-intelligence-analyst
description: Build a concise B2B account and prospect intelligence brief from public sources, CRM notes, and company materials. Use when the user asks to research a prospect, build an account profile, prep for first outreach, or identify buying signals and risk flags before engaging.
---

# Account Intelligence Analyst

This is a Codex-native chain skill for turning scattered account context into a usable sales brief.

## When to use it

Use this skill when the user needs:

- a prospect intelligence profile
- account research before outreach
- buying signals and risk flags
- conversation hooks grounded in real company context

## Workflow

1. Gather the minimum useful inputs:
   - prospect name or profile URL
   - company name or domain
   - any CRM notes, prior emails, or deal context if available
2. Use `content-research` or `url-dossier` if the inputs include public URLs or source documents.
3. Extract only decision-relevant facts:
   - title, tenure, influence, likely mandate
   - company priorities, recent launches, funding, hiring, leadership changes
   - existing relationship history or stale-record signals
4. Synthesize into a single brief with:
   - company overview
   - prospect profile
   - buying signals
   - risk flags
   - conversation starters
   - open questions
5. If the user maintains durable research notes, hand the result to `second-brain-capture`.

## Output structure

```markdown
# <Prospect Name> — <Company> Intelligence Brief

## Company Overview
- ...

## Prospect Profile
- ...

## Buying Signals
- ...

## Risk Flags
- ...

## Conversation Starters
- ...

## Open Questions
- ...
```

## Rules

- Timestamp and source any non-obvious factual claims.
- Prioritize signal over completeness; a short accurate brief beats a noisy dossier.
- Separate observed facts from inferences.
- If CRM access is unavailable, say so and proceed with public-source research only.
""",
        "outreach-architect": """---
name: outreach-architect
description: Design a personalized multi-step B2B outreach sequence using account context, relationship stage, and a clear call to action. Use when the user asks for cold outreach, warm outreach, follow-up sequencing, or tailored email and LinkedIn copy for a specific prospect.
---

# Outreach Architect

This is a Codex-native chain skill for turning account intelligence into a usable outreach plan.

## Inputs

Best inputs:

- an account intelligence brief
- prospect name, role, and company
- relationship type: cold, warm, previous contact, or active deal
- any deal stage, timing, or close-date pressure

## Workflow

1. Read the account context first. If it does not exist yet, ask for the minimum facts or suggest running `account-intelligence-analyst`.
2. Classify the motion:
   - cold outreach
   - warm referral or inbound
   - re-engagement
   - active opportunity follow-up
3. Build a sequence with:
   - one primary email
   - one alternate channel touch if useful
   - follow-up steps with timing
   - no-reply handling
4. Personalize every message to one or two real signals from the account brief.
5. Run the copy through `anti-slop` before finalizing.

## Output structure

```markdown
# Outreach Plan — <Prospect> @ <Company>

## Sequence Strategy
...

## Touch 1
**Channel:** Email
**Timing:** ...
**Goal:** ...
**Copy:** ...

## Touch 2
...

## Touch 3
...

## No-Reply Handling
- ...
```

## Rules

- Keep each message short and single-purpose.
- One CTA per touch.
- Do not use generic openers that could fit any company.
- If the account context is weak, say so and lower the personalization claims.
""",
        "precall-briefer": """---
name: precall-briefer
description: Produce a one-page pre-call brief for a sales, success, or deal call using CRM history, recent account activity, and company changes. Use when the user asks for call prep, meeting prep, or a last-minute summary before talking to a prospect or customer.
---

# Precall Briefer

This is a Codex-native chain skill for compressing deal context into a 60-second read.

## Workflow

1. Gather:
   - meeting date and objective
   - prospect or customer participants
   - prior notes, emails, CRM history, or account brief
2. If the account context is thin, use `account-intelligence-analyst` first.
3. Extract:
   - last meaningful interaction
   - what changed since then
   - likely stakeholders and roles
   - active risks, blockers, or competing pressures
4. Produce a brief that optimizes for action during the call, not for archival completeness.

## Output structure

```markdown
# Pre-Call Brief — <Date> — <Company>

## Call Context
- ...

## Last Conversation
- ...

## What Changed Since Last Contact
- ...

## Decision-Maker Map
- ...

## Talk Track Priorities
- ...

## Risks And Blockers
- ...
```

## Rules

- Keep it to roughly one page.
- Every section should help the caller decide what to say, ask, or avoid.
- Flag missing context explicitly instead of smoothing over it.
- Separate confirmed facts from likely inferences.
""",
        "crm-hygiene-enforcer": """---
name: crm-hygiene-enforcer
description: Audit CRM exports or pipeline snapshots for stale deals, missing fields, duplicates, stage mismatches, and reporting risk. Use when the user asks to clean CRM data, audit pipeline quality, review imports, or produce a prioritized data hygiene queue.
---

# CRM Hygiene Enforcer

This is a Codex-native chain skill for turning messy CRM exports into an action queue.

## When to use it

Use this skill for:

- weekly CRM hygiene reviews
- post-import audits
- forecast cleanup
- duplicate and stale-deal detection

## Inputs

Typical inputs:

- CSV exports from CRM
- spreadsheets
- snapshots of account, contact, and opportunity tables
- funnel rules or stage definitions

## Workflow

1. Confirm the scope:
   - contacts
   - accounts
   - opportunities
   - activities
2. Identify the rules that matter:
   - stale thresholds
   - required fields
   - valid stage transitions
   - duplicate tolerance
3. Audit the data for:
   - stale records
   - missing owners or critical fields
   - impossible close dates or amounts
   - stage mismatches
   - likely duplicates
4. Separate:
   - safe auto-fix suggestions
   - items requiring human review
5. Produce a ranked hygiene report with explicit owners and recommended actions.

## Output structure

```markdown
# CRM Hygiene Audit — <date>

## Summary
- ...

## Critical Issues
- ...

## Stale Deals
- ...

## Missing Data
- ...

## Duplicate Candidates
- ...

## Manual Action Queue
- ...
```

## Rules

- Be conservative about auto-corrections; prefer recommendations over silent edits.
- Explain the rule behind each flagged issue.
- Treat the output as an operations queue, not a generic report.
- If the user only provides narrative descriptions instead of data exports, offer the audit logic and required columns.
""",
        "proposal-generator": """---
name: proposal-generator
description: Generate a tailored B2B proposal, quote, or statement of work from deal context, discovery notes, and pricing inputs. Use when the user asks for a proposal, quote, SOW, commercial document, or deal-ready summary for a qualified opportunity.
---

# Proposal Generator

This is a Codex-native chain skill for going from deal context to a sendable proposal draft.

## Inputs

Gather as many of these as exist:

- prospect and company name
- deal stage and target timeline
- discovery notes or call transcripts
- pricing or rate-card inputs
- requested scope, deliverables, or commercial constraints

## Workflow

1. Read the deal context and extract:
   - desired outcomes
   - pain points in the prospect's own language
   - scope and assumptions
   - pricing constraints or discount approvals
2. Structure the draft in this order:
   - executive summary
   - current situation and challenge
   - proposed solution
   - scope of work
   - investment
   - commercial terms
   - next steps
3. Keep the narrative specific to the deal; do not produce brochure copy.
4. If terms need extra scrutiny, route the draft through `contract-reviewer`.
5. If the user needs a slide version, route the core proposal story into `presentation`.

## Output structure

```markdown
# Proposal — <Company>

## Executive Summary
...

## Situation And Challenge
...

## Proposed Solution
...

## Scope Of Work
...

## Investment
...

## Terms
...

## Next Steps
...
```

## Rules

- Document assumptions clearly.
- Keep scope boundaries explicit to prevent scope creep.
- Separate base scope from optional add-ons.
- If the environment cannot export PDF or branded documents, say so and produce the clean source draft.
""",
        "content-outlier-research": """---
name: content-outlier-research
description: Research high-performing posts, essays, videos, and discussions in a target niche, then extract the hook, structure, angle, and likely reason each one worked. Use when the user asks what is working now, wants outlier content research, or needs pattern mining before creating new content.
---

# Content Outlier Research

This is a Codex-native chain skill for turning raw content examples into reusable pattern notes.

## Workflow

1. Confirm the niche, window, and source mix.
   Default to recent enterprise-AI, automotive-AI, and agentic-systems content if the user does not specify.
2. Gather candidates with `content-research`, `watch`, and `url-dossier` as needed.
3. Rank candidates by practical outlier value:
   - visible engagement or reach
   - freshness
   - relevance to the user's actual work
   - clarity of the pattern
4. For the top items, extract:
   - hook
   - structure
   - angle
   - likely reason it worked
   - what is reusable vs. what is unique to that creator
5. If the user keeps durable research notes, save the result through `second-brain-capture`.

## Output structure

```markdown
# Content Outlier Research — <topic> — <date>

## Top Outliers

### 1. <title>
- Source: ...
- URL: ...
- Why it matters: ...
- Hook: ...
- Structure: ...
- Angle: ...
- Reusable pattern: ...

## Pattern Summary
- ...

## Best Next Moves
- ...
```

## Rules

- Favor actionable patterns over vanity metrics.
- Separate observed facts from your hypothesis about why something worked.
- Avoid generic advice like "be authentic" or "tell stories."
- If engagement data is partial or inferred, say so.
""",
        "content-topic-queue": """---
name: content-topic-queue
description: Generate a ranked queue of concrete content topics by combining fresh outlier patterns with the user's active workstreams and point of view. Use when the user asks what to write next, wants a topic backlog, or needs ideas separated by channel such as LinkedIn, Substack, or deck format.
---

# Content Topic Queue

This is a Codex-native chain skill for turning research and expertise into a writeable backlog.

## Inputs

Best inputs:

- a recent outlier research pack
- the user's active workstreams
- preferred channels such as LinkedIn, Substack, or deck

## Workflow

1. Read the latest outlier patterns first. If none exist, suggest running `content-outlier-research`.
2. Read the user's active themes, current projects, and strong opinions.
3. Cross the two:
   - what is working externally
   - what the user can credibly say from lived work
4. Generate candidate topics with:
   - title
   - angle
   - suggested channel
   - why now
   - source inspiration
5. Rank the queue by usefulness, specificity, and freshness.
6. If the user wants drafts immediately, pass the top topics into `content-repurpose` or a direct drafting step and run `anti-slop` on the result.

## Output structure

```markdown
# Content Topic Queue — <date>

## Top Topics

### 1. <title>
- Channel: ...
- Angle: ...
- Why now: ...
- Inspired by: ...

## Reserve Topics
- ...
```

## Rules

- Every topic should tie back to a real workstream, operator insight, or concrete case.
- Do not produce interchangeable "AI trends" topics.
- Make the channel recommendation explicit.
- Kill weak ideas instead of padding the queue.
""",
        "content-draft-writer": """---
name: content-draft-writer
description: Draft a single LinkedIn post, essay, or channel-specific content piece from a selected topic while applying voice and anti-slop checks before handoff. Use when the user asks to draft the next post, write from a queued topic, or turn a ranked content idea into a review-ready draft.
---

# Content Draft Writer

This is a Codex-native chain skill for taking one topic from queue to review-ready draft.

## Inputs

Best inputs:

- a specific topic
- channel target such as LinkedIn or Substack
- source outlier patterns or notes
- any voice or style constraints already in use

## Workflow

1. Select one topic only.
2. Pull the minimum useful context:
   - topic title and angle
   - source inspiration or research notes
   - channel constraints
3. Draft for the selected channel.
4. Run the result through:
   - `anti-slop` for generic-AI cleanup
   - `review-draft` for voice alignment and rewrite if needed
5. Return a clean draft plus any unresolved review flags.

## Output structure

```markdown
# Draft Package — <topic>

## Channel
...

## Draft
...

## Review Notes
- ...
```

## Rules

- Draft one asset per invocation.
- Keep the draft specific to the topic's real angle, not to a generic niche.
- If channel constraints are missing, call that out instead of guessing silently.
- If the piece still fails voice review after one rewrite pass, surface the remaining issues explicitly.
""",
        "content-publish-helper": """---
name: content-publish-helper
description: Prepare an approved content draft for manual publishing, including final checklist, formatting cleanup, and status handoff. Use when the user wants to ship the next approved post, prep a draft for publishing, or bridge the last step between review and manual post.
---

# Content Publish Helper

This is a Codex-native chain skill for the human-gated publishing step.

## Workflow

1. Confirm the asset is approved and channel-ready.
2. Run a final preflight:
   - title or opening line
   - body formatting
   - link placement
   - CTA
   - obvious copy errors
3. Produce a publish packet:
   - final copy
   - channel-specific checklist
   - any manual actions still required
4. Stop at the handoff. Do not pretend to auto-publish unless the environment actually includes a real posting path and the user explicitly wants it.

## Output structure

```markdown
# Publish Packet — <title>

## Final Copy
...

## Channel Checklist
- ...

## Manual Handoff
- ...
```

## Rules

- Treat publishing as a human-controlled step by default.
- If the workflow depends on browser or platform login state, say so directly.
- Never mark something as published unless the user confirms it actually shipped.
""",
        "content-performance-tracker": """---
name: content-performance-tracker
description: Refresh and summarize performance metrics for published content, then route the result into the performance log so future voice tuning has real data. Use when the user asks to update content metrics, check how posts are doing, or run a recurring performance refresh.
---

# Content Performance Tracker

This is a Codex-native chain skill for closing the loop between publishing and learning.

## Workflow

1. Gather the content items to refresh:
   - one URL
   - a recent published batch
   - a spreadsheet or note export
2. Normalize the available metrics by channel.
3. Summarize:
   - current top performer
   - biggest recent change
   - obvious missing data
4. Append clean entries through `log-performance`.
5. If enough data exists, suggest `tune-voice`.

## Output structure

```markdown
# Performance Refresh — <date>

## Updated Items
- ...

## Top Performer
- ...

## Biggest Delta
- ...

## Missing Or Failed Reads
- ...
```

## Rules

- Trends matter more than false precision.
- If metrics are partial, say exactly what is missing.
- Do not fabricate engagement numbers from weak signals.
- Keep the result structured so it can feed `log-performance`.
""",
        "content-weekly-report": """---
name: content-weekly-report
description: Produce a weekly content digest that summarizes what shipped, what is blocked, what performed best, and what should be turned into content next week. Use when the user asks for a weekly content report, Friday digest, or content retrospective.
---

# Content Weekly Report

This is a Codex-native chain skill for converting raw content activity into a decision-oriented weekly digest.

## Workflow

1. Gather the week's source data:
   - published posts, essays, decks, or videos
   - drafts in progress or stuck in review
   - recent outlier research
   - queue candidates for next week
2. If the data lives in spreadsheets, markdown notes, or screenshots, normalize it first.
3. Build the report around four questions:
   - what shipped
   - what worked
   - what is stuck
   - what should happen next week
4. If the environment supports delivery into notes, email, or a vault, save it there after generating the markdown.

## Output structure

```markdown
# Content Week — <date range>

## What Shipped
...

## What Worked
...

## What Is Stuck
...

## Cadence Check
...

## Next Week
...
```

## Rules

- Do not invent wins if nothing shipped.
- Treat this as an operator report, not a morale memo.
- Keep the lead metric simple and defensible.
- If the underlying data is thin, say what is missing.
""",
        "content-marketing-team": """---
name: content-marketing-team
description: Coordinate a text-first content workflow across research, topic generation, drafting, review, and weekly reporting. Use when the user asks to run a content cycle, decide what to publish next, or orchestrate a repeatable content pipeline instead of a one-off post.
---

# Content Marketing Team

This is the Codex-native parent chain for the content workflow.

## Modes

- `full`
- `research-only`
- `topic-only`
- `draft-only`
- `report-only`

Default to `full`.

## Workflow

1. Read the current state:
   - recent outlier research
   - current topic queue
   - drafts in progress
   - approved drafts awaiting publish
   - published work this week
2. Route work by need:
   - low research coverage -> `content-outlier-research`
   - weak backlog -> `content-topic-queue`
   - strong topic ready to write -> `content-draft-writer`
   - approved asset ready to ship -> `content-publish-helper`
   - recent published work needs metrics -> `content-performance-tracker`
   - existing source asset that needs channel variants -> `content-repurpose`
   - end-of-week review -> `content-weekly-report`
3. Return a concise operating summary:
   - what ran
   - what is queued
   - what is blocked on human review
   - what the next best content action is

## Output structure

```markdown
# Content Team Cycle — <date>

## Ran
- ...

## Queue Health
- ...

## Blockers
- ...

## Next Best Action
- ...
```

## Rules

- Do not pile up more drafts if the review queue is already backed up.
- Prefer steady throughput over idea-hoarding.
- Be explicit about the mode and what was skipped because of it.
- If the user lacks any system of record, work from provided notes and say so directly.
""",
        "log-performance": """---
name: log-performance
description: Record structured performance data for published content so future review and voice-tuning decisions are based on actual outcomes. Use when the user shares engagement metrics, wants to log a post's performance, or needs a consistent performance history for later analysis.
---

# Log Performance

This skill is the structured data-entry layer for content performance.

## Workflow

1. Capture the minimum useful fields:
   - content title or identifier
   - platform
   - publish date
   - primary metric and value
2. Capture optional but useful context:
   - format
   - hook style
   - topic
   - secondary metrics
   - notes
3. Append the entry in a consistent markdown structure.
4. If the user has enough entries for pattern analysis, recommend `tune-voice`.

## Output structure

Use a stable append-only format:

```markdown
---
**<DATE> | <PLATFORM> | <FORMAT>**

**Content:** ...
**Hook style:** ...
**Topic:** ...

**Metrics:**
- ...

**Hit expectations:** ...
**Notes:** ...
---
```

## Rules

- Consistency matters more than verbosity.
- If a field is unknown, use `—` instead of inventing it.
- Treat failed content as equally important data.
""",
        "review-draft": """---
name: review-draft
description: Review a draft against an established brand voice or recent writing patterns, score the fit, identify what is off, and provide a corrected version when needed. Use when the user asks whether a draft sounds like them, wants a voice review, or needs cleanup before publishing.
---

# Review Draft

This is the voice-editor layer for generated content.

## Workflow

1. Load the best available voice reference:
   - existing voice profile
   - recent strong examples
   - user-supplied sample posts
2. Review the draft for:
   - banned or overused words
   - generic AI structures
   - weak hooks
   - tone mismatch
   - format mismatch for the channel
3. Return:
   - a blunt score
   - what is off
   - a clean rewrite if the draft needs one
4. If recurring voice patterns show up across multiple reviews, suggest `tune-voice`.

## Output structure

- `Voice Score: X/5`
- short honest assessment
- grouped issues with fixes
- full clean version when needed

## Rules

- Prioritize voice fidelity over superficial polish.
- Do not soften clear problems.
- Preserve the core argument while fixing the delivery.
- Skip the rewrite only if the draft is already strong enough to publish.
""",
        "tune-voice": """---
name: tune-voice
description: Analyze accumulated content performance and propose concrete updates to the content strategy or voice profile based on what is actually working. Use when the user asks what is performing, how to improve the voice, or what patterns to post more of after enough performance data has been logged.
---

# Tune Voice

This is a Codex-native chain skill for turning performance history into strategy changes.

## Workflow

1. Read the performance log first.
2. If available, also read the current voice profile or recent review patterns.
3. Analyze by:
   - platform
   - format
   - hook style
   - topic
   - expectation hits vs misses
4. Produce:
   - what is working
   - what is not
   - the highest-leverage next bet
   - suggested voice-profile updates
5. Offer concrete updates before rewriting any standing voice profile.

## Output structure

```markdown
# Performance Insights

## What's Working
...

## What's Not
...

## Highest-Leverage Bet
...

## Suggested Voice Updates
...
```

## Rules

- Prefer non-obvious, actionable patterns over shallow summaries.
- If the data set is small, say so explicitly and lower confidence.
- Do not force a confident recommendation if the evidence is mixed.
- Separate analysis from profile edits; show proposed changes before applying them.
""",
        "slide-deck-builder": """---
name: slide-deck-builder
description: Build a presentation or self-contained HTML slide deck using Sheker's enterprise style: dark navy, teal accents, widescreen layout, and visual-first slides. Use when the user asks for a slide deck, presentation, HTML deck, or visual narrative from a topic, memo, or research pack.
---

# Slide Deck Builder

This is a Codex-native chain skill for turning a topic or document into a deck source.

## Brand defaults

- widescreen layout
- dark navy base
- teal accent system
- enterprise tone
- visual-first slides, not bullet dumps

## Workflow

1. Identify the input shape:
   - topic only
   - memo or proposal
   - research pack
   - existing carousel or notes
2. Choose the supporting path:
   - `presentation` for core deck structure
   - `presentation-theme` for consistent visual direction
   - `chart-storyteller` for metric slides
   - `architecture-to-everything` for system or workflow slides
   - `carousel-to-deck` if the source is already in carousel form
3. Build the deck with:
   - title / setup
   - core content
   - evidence
   - takeaway / next steps
4. If the environment supports export, use the appropriate exporter. Otherwise produce the clean HTML or markdown-backed deck source.

## Rules

- One idea per slide.
- Every slide needs a visual treatment or strong structural reason not to have one.
- Prefer 5 to 12 slides unless the user explicitly wants a larger deck.
- Keep speaker-support copy tight; do not write essays on slides.
- If you cannot generate a real `.pptx`, say so and provide the best deck source available.
""",
        "install-marp": """---
name: install-marp
description: Check for Node/npm and install or verify Marp CLI so markdown slide decks can be rendered to HTML, PDF, or PPTX. Use when the user asks to install Marp, set up markdown slide generation, or enable Marp exports.
---

# Install Marp

Use this skill when the user explicitly wants Marp available in the environment.

## Workflow

1. Check prerequisites:

```bash
which npm
npm --version
```

2. Check whether Marp is already available:

```bash
npx @marp-team/marp-cli --version
```

3. If missing, install it:

```bash
npm install -g @marp-team/marp-cli
```

4. Verify:

```bash
marp --version
```

## Rules

- Do not install Marp unless the user wants it or the workflow genuinely depends on it.
- Prefer user-scoped installs over root installs.
- If npm is missing, say that Node.js/npm must be installed first.
- Always verify the installed version after setup.
""",
        "marp-deck-builder": """---
name: marp-deck-builder
description: Create or update a `.marp.md` presentation deck from a memo, research pack, topic outline, or existing deck notes. Use when the user asks for a Marp deck, markdown slide deck, or wants slides in Marp format instead of HTML-only presentation output.
---

# Marp Deck Builder

This is the Marp-specific deck-authoring skill.

Read these references before writing the deck:

- `references/deck_skeleton.marp.md`
- `references/marp_components.md`

## Workflow

1. Confirm the source material:
   - topic only
   - memo
   - research pack
   - proposal or architecture brief
2. Build the deck as `.marp.md`, not plain markdown.
3. Use the skeleton and component guidance to ensure:
   - valid Marp frontmatter
   - explicit slide boundaries
   - one job per slide
   - HTML component usage where it improves the deck
4. If the content needs narrative shaping first, use `presentation` or `presentation-content-writer`, then convert the result into Marp.
5. If the user wants rendered outputs, hand the finished deck to `marp-exporter`.

## Rules

- Keep the output in `.marp.md` form.
- Do not mix generic markdown notes with a deck source file.
- If the deck is data-heavy, prefer componentized slides and explicit takeaway slides.
- If the environment cannot render Marp yet, still produce a valid `.marp.md` source.
""",
        "marp-exporter": """---
name: marp-exporter
description: Lint and export a `.marp.md` deck to HTML or PDF using the vendored Marp helper scripts and bundled themes. Use when the user wants to preview, share, print, or validate a Marp deck after authoring it.
---

# Marp Exporter

Use this skill after a `.marp.md` deck already exists.

## Bundled tools

- `scripts/marp_linter.py`
- `scripts/marp_export.py`
- bundled theme CSS under `assets/themes/`

## Workflow

1. Lint the deck first:

```bash
python3 "$CODEX_HOME/skills/marp-exporter/scripts/marp_linter.py" <deck.marp.md>
```

2. If Marp CLI is unavailable, stop and use `install-marp`.
3. Export to HTML and/or PDF:

```bash
python3 "$CODEX_HOME/skills/marp-exporter/scripts/marp_export.py" <deck.marp.md> analytics both
```

4. If the user needs PPTX and Marp CLI is installed, use direct Marp CLI:

```bash
marp <deck.marp.md> -o <deck.pptx>
```

## Rules

- Lint before export whenever the deck changed materially.
- Treat the `.marp.md` file as the source of truth; exports are generated artifacts.
- If export fails, surface the exact Marp or theme error instead of guessing.
- Use the bundled themes unless the deck already ships with its own `themes/` directory.
""",
        "markdown-preview": {
            "SKILL.md": """---
name: markdown-preview
description: Render a markdown file to a quick local HTML preview, with Marp-aware handling for `.marp.md` decks when possible. Use when the user wants to preview markdown, inspect a README or note in the browser, or quickly render markdown without a full publishing flow.
---

# Markdown Preview

Use this skill for quick local previews of markdown files.

## Workflow

1. Identify the target markdown file.
2. If the file is a `.marp.md` deck and Marp is available, prefer a Marp HTML render.
3. Otherwise render a lightweight HTML preview with the bundled script:

```bash
python3 "$CODEX_HOME/skills/markdown-preview/scripts/render_markdown_preview.py" <input.md>
```

4. The script prints the output HTML path. If the user wants a live local server, rerun with:

```bash
python3 "$CODEX_HOME/skills/markdown-preview/scripts/render_markdown_preview.py" <input.md> --serve
```

## Rules

- Prefer preview generation over editing the original markdown.
- If markdown parser libraries are missing, the script falls back to a plain-text HTML wrapper instead of failing.
- For Marp decks, keep `.marp.md` as the source and treat preview HTML as disposable output.
""",
            "scripts/render_markdown_preview.py": """#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import http.server
import os
import socketserver
import subprocess
import sys
import threading
from pathlib import Path


def render_markdown(text: str) -> str:
    try:
        import markdown  # type: ignore

        return markdown.markdown(
            text,
            extensions=["fenced_code", "tables", "toc"],
        )
    except Exception:
        pass

    try:
        from cmarkgfm import github_flavored_markdown_to_html  # type: ignore

        return github_flavored_markdown_to_html(text)
    except Exception:
        pass

    try:
        import commonmark  # type: ignore

        return commonmark.commonmark(text)
    except Exception:
        pass

    return "<pre>{}</pre>".format(html.escape(text))


def maybe_render_marp(input_path: Path, output_path: Path) -> bool:
    if input_path.suffixes[-2:] != [".marp", ".md"]:
        return False

    marp = None
    for candidate in (["marp"], ["npx", "@marp-team/marp-cli"]):
        try:
            result = subprocess.run(
                [*candidate, "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                marp = candidate
                break
        except Exception:
            continue

    if marp is None:
        return False

    cmd = [
        *marp,
        "--html",
        "--allow-local-files",
        "--output",
        str(output_path),
        str(input_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.returncode == 0 and output_path.exists()


def build_html(title: str, body: str) -> str:
    return f\"\"\"<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      margin: 40px auto;
      max-width: 860px;
      padding: 0 24px 64px;
      font: 18px/1.6 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #1f2937;
      background: #f8fafc;
    }}
    main {{
      background: white;
      padding: 40px;
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    }}
    pre {{
      overflow-x: auto;
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 12px;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    td, th {{
      border: 1px solid #cbd5e1;
      padding: 8px 10px;
      text-align: left;
    }}
    blockquote {{
      border-left: 4px solid #94a3b8;
      margin-left: 0;
      padding-left: 16px;
      color: #475569;
    }}
    img {{
      max-width: 100%;
      height: auto;
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
\"\"\"


def serve_directory(directory: Path, port: int) -> None:
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"serving http://127.0.0.1:{port}/")
        httpd.serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a markdown file to HTML preview.")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("--output", help="Output HTML path")
    parser.add_argument("--serve", action="store_true", help="Serve the output directory locally")
    parser.add_argument("--port", type=int, default=8765, help="Port for --serve")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"missing input: {input_path}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        suffix = ".html"
        output_path = input_path.with_suffix(suffix)
        if input_path.name.endswith(".marp.md"):
            output_path = input_path.with_name(input_path.name[:-3] + ".html")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not maybe_render_marp(input_path, output_path):
        text = input_path.read_text(encoding="utf-8")
        body = render_markdown(text)
        output_path.write_text(build_html(input_path.name, body), encoding="utf-8")

    print(output_path)

    if args.serve:
        server_dir = output_path.parent
        thread = threading.Thread(
            target=serve_directory,
            args=(server_dir, args.port),
            daemon=False,
        )
        thread.start()
        thread.join()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
        },
        "video-to-deck": """---
name: video-to-deck
description: Turn a video URL or local video file into a research-backed presentation package. Use when the user wants to convert a video into slides, a deck outline, a Marp deck, or a richer explainer package instead of just a transcript.
---

# Video To Deck

This is a Codex-native chain skill for going from video to presentation artifacts.

## Workflow

1. Run `watch` on the video to extract transcript, frames, and structure.
2. Use `content-research` or `url-dossier` to enrich the topic with supporting sources.
3. If the concept benefits from a visual analogy, use `explainer-graphic`.
4. Build the slide artifact:
   - `slide-deck-builder` for HTML or presentation-source output
   - `marp-deck-builder` if the user wants markdown slides
5. If the user needs rendered Marp outputs, finish with `marp-exporter`.

## Output options

- transcript summary
- research note
- explainer graphic
- slide outline
- `.marp.md` deck
- rendered HTML or PDF deck

## Rules

- Stop if the video extraction failed; do not fake the downstream deck.
- Keep the deck anchored to what the video actually argues or demonstrates.
- Separate source-backed facts from your own synthesis.
- If the user wants a narrow section only, scope the deck to that segment instead of summarizing the full video.
""",
        "stakeholder-comms": """---
name: stakeholder-comms
description: Adapt the same finding, memo, or analysis to different audiences such as executives, product teams, engineering, or data stakeholders. Use when the user asks to reframe a message for a specific audience, tailor a deck or write-up, or change the level of detail without changing the underlying insight.
---

# Stakeholder Comms

This skill is the audience-adaptation layer for analytical, strategic, or product communication.

## Workflow

1. Identify the target audience:
   - executive
   - product team
   - engineering
   - data / analytics
   - mixed audience
2. Start from the existing source material:
   - analysis summary
   - memo
   - deck
   - recommendation note
3. Adapt:
   - lead sentence
   - detail level
   - recommendation framing
   - metrics language
   - caveat placement
4. Preserve the underlying finding; only change the framing and depth.

## Output structure

At the top, label:

```markdown
**Audience:** <...>
**Detail level:** <...>
```

Then deliver the adapted output.

## Rules

- Executives get impact and decision first.
- Product gets implications and next actions.
- Engineering gets root cause and scope.
- Data gets methodology and caveats.
- For mixed audiences, use layered sections instead of flattening everything to one level.
""",
        "export-results": """---
name: export-results
description: Turn completed analysis, strategy notes, or deck-ready material into audience-specific outputs such as slides, email summaries, Slack updates, briefs, or data exports. Use when the user asks to export, share, package, or send results in a specific format.
---

# Export Results

This is the packaging and delivery skill for completed work.

## Inputs

Best inputs:

- an existing analysis summary
- a recommendation memo
- a deck source
- data tables or charts
- target format and audience

## Supported output modes

- slides
- email summary
- Slack update
- decision brief
- data export
- all

## Workflow

1. Find the best available source artifact.
2. Identify the requested format.
3. If an audience is specified, adapt through `stakeholder-comms` first.
4. Generate the export:
   - slides -> `presentation`, `slide-deck-builder`, or `marp-deck-builder`
   - email / Slack / brief -> markdown output with the right tone and compression
   - data -> clean CSV or table exports when the data exists
5. List the generated artifacts clearly.

## Rules

- Do not fabricate findings or numbers.
- Match detail level to the delivery format.
- If the source analysis is partial, note that explicitly in the export.
- Treat the source analysis or deck as the system of record; exports are derived artifacts.
""",
        "printing-press": {
            "SKILL.md": """---
name: printing-press
description: Generate or improve a CLI for an API using the external `printing-press` binary. Use when the user wants a ship-ready CLI generated from an API name, spec file, HAR capture, or API docs URL.
---

# Printing Press

This is the Codex-native wrapper for the external `printing-press` binary.

Read `references/setup-checks.md` first.

## What this skill is for

Use it when the user wants to:

- generate a CLI from an API name
- generate from an OpenAPI or YAML spec
- generate from a HAR capture
- generate from a docs URL or product URL
- run the binary in its `codex` mode when supported

## Preflight

First verify the binary exists:

```bash
command -v printing-press
```

If it is missing, stop and show the install command from `references/setup-checks.md`.

## Main entry patterns

```bash
printing-press "<api>"
printing-press "<api>" codex
printing-press --spec ./openapi.yaml
printing-press --har ./capture.har --name MyAPI
printing-press https://postman.com/explore
```

## Workflow

1. Confirm the input shape:
   - API name
   - local spec file
   - HAR capture
   - URL
2. Read `references/spec-inputs.md` if the format or source is ambiguous.
3. Run the `printing-press` binary with the narrowest correct input form.
4. If the run needs temporary browser-based discovery, read `references/browser-sniff.md`.
5. Before any archive, publish, or share step, read `references/secret-protection.md`.
6. Before calling the result ship-ready, read `references/shipcheck.md`.

## Rules

- This skill wraps the binary; it does not replace it.
- Do not claim the CLI is shippable without both structural checks and behavioral testing.
- Browser sniffing is temporary discovery only, not permission to ship a resident browser runtime.
- If the user asks for second-pass cleanup and there is no dedicated polish skill installed yet, say that explicitly instead of pretending the old Claude-only polish workflow exists.
""",
            "references/setup-checks.md": """# Setup Checks

Use this before any `printing-press` run.

## Binary check

```bash
command -v printing-press
```

If missing, stop and tell the user to install it:

```bash
go install github.com/mvanhorn/cli-printing-press/v4/cmd/printing-press@latest
```

Then verify:

```bash
printing-press --version
```

## Upgrade check

If the binary exists, it is reasonable to inspect:

```bash
printing-press version --json
```

If the user wants to upgrade, use the same `go install ...@latest` command.

## Compatibility rule

If the installed binary is clearly older than the workflow expects, warn and continue only if the user accepts the risk.
""",
            "references/spec-inputs.md": """# Spec Inputs

Accepted `printing-press` input forms:

- API or product name:
  - `printing-press Notion`
- explicit Codex mode:
  - `printing-press Discord codex`
  - `printing-press --spec ./openapi.yaml codex`
- local spec file:
  - `printing-press --spec ./openapi.yaml`
- HAR capture:
  - `printing-press --har ./capture.har --name MyAPI`
- URL:
  - `printing-press https://postman.com/explore`

## Good defaults

- Prefer a local verified spec file when one exists.
- Use HAR when the API surface is discovered from real traffic rather than formal docs.
- Use a docs URL or product URL when discovery has to start from the public surface.

## Internal YAML spec

If there is no OpenAPI spec, `printing-press` can work from an internal YAML description of:

- API metadata
- auth scheme
- resources
- endpoints
- params
- response types

Preserve the wire-level field names from the upstream API instead of renaming them for cosmetics.
""",
            "references/browser-sniff.md": """# Browser Sniff

Load this only when generation requires temporary live-site discovery.

## Principle

Browser capture is a generation-time discovery aid. It is not a runtime transport model for the shipped CLI.

## What browser sniffing is for

- discovering hidden endpoints
- learning request shapes
- capturing persisted GraphQL queries
- understanding auth/header construction
- proving whether replayable HTTP or structured extraction is possible

## Rules

- Prefer replayable HTTP or structured extraction as the final CLI surface.
- If only live page-context execution works, hold or reduce scope instead of pretending the CLI is normal.
- Treat browser discovery as a temporary step and keep the artifacts out of published outputs unless sanitized.
""",
            "references/secret-protection.md": """# Secret Protection

Read this before archiving, publishing, or sharing any `printing-press` output.

## Hard rules

- Never store API key values, token values, passwords, or session cookies in repo artifacts.
- Env var names and placeholders are safe; secret values are not.
- Strip auth-bearing headers, cookies, query params, and response bodies from HAR captures before keeping them.

## Practical checks

- run fixed-string scans for exact known secret values before archiving
- redact any discovered exact-value leaks
- remove request/response cookies and auth headers from HAR files
- avoid publishing real workspace or customer PII in proofs or README examples
""",
            "references/shipcheck.md": """# Shipcheck

Structural success is not enough.

## Required checks

- build succeeds
- verification commands succeed
- behavior is tested against real or realistic targets
- headline commands and help output are plausible
- failure paths are exercised, not assumed

## Do not call it shipped if only these passed

- `go build`
- schema generation
- static verification

Those are necessary but not sufficient.

## Publish standard

A generated CLI is only ship-ready when it has passed both:

1. structural checks
2. behavioral testing / dogfooding
""",
        },
        "content-research": """---
name: content-research
description: Ingest URLs, videos, documents, or repositories into structured research notes, then optionally persist them into a second brain or Obsidian vault backed by GitHub. Use when the user wants content research, source notes, durable knowledge capture, or multi-source synthesis.
---

# Content Research

This is the Codex-native research ingestion chain.

## Companion skills

- `watch` for video URLs or local video files
- `url-dossier` for one-off link analysis
- `second-brain-capture` when the notes should become durable knowledge assets
- `obsidian-vault-manager` when the user wants the research stored in an Obsidian vault
- `obsidian-github-sync` when the vault or notes should live in GitHub
- `graphify` for relationship mapping

## Workflow

1. Parse the sources and classify them:
   - video
   - GitHub repo or file
   - web page or article
   - local document
2. Ingest each source with the most reliable available method:
   - `watch` for video
   - `gh` plus file inspection for GitHub
   - web access or `curl` for web pages
   - direct file reads for local documents
3. Write one structured markdown note per source.
4. Produce a cross-source synthesis.
5. If the user wants durable storage:
   - use `second-brain-capture` to convert source notes into long-lived notes
   - use `obsidian-vault-manager` if an Obsidian vault is needed or missing
   - use `obsidian-github-sync` if the vault or note set should sync through GitHub
6. If the user wants relationships or graph output, run `graphify` on the note directory.

## Outputs

- `research-notes/<slug>.md` per source
- `research-notes/INDEX.md`
- `research-synthesis.md`
- optional second-brain or vault note paths when the chain continues

## Rules

- Keep raw excerpts separate from synthesis.
- Preserve source URLs and source types in frontmatter.
- If the user asks for a second brain, prefer durable markdown notes over chat-only summaries.
- If the user asks for Obsidian storage, use wikilinks and note-friendly frontmatter.
- If the user asks for GitHub-backed storage, keep the note set plain-text and repo-friendly.
""",
        "second-brain-capture": {
            "SKILL.md": """---
name: second-brain-capture
description: Capture research, meeting notes, findings, or source material into durable markdown notes for a second brain or Obsidian vault. Use when the user asks to save knowledge, create evergreen notes, turn sources into reusable notes, or persist findings beyond the chat.
---

# Second Brain Capture

Turn raw material into durable notes that can survive across sessions, repos, and tools.

Read `references/note-types.md` before choosing the note structure.

## Workflow

1. Choose the storage root.
   - Prefer an explicit path from the user.
   - Otherwise prefer, in order: `second-brain/`, `vault/`, `notes/`, `knowledge/`.
   - If none exists and the user wants a full vault, use `obsidian-vault-manager`.
2. Pick the note type:
   - source note
   - evergreen note
   - project note
   - meeting note
   - daily note
3. Create a slugged markdown file in the appropriate subdirectory.
4. Add frontmatter with at least:
   - `title`
   - `created`
   - `updated`
   - `tags`
   - `source` when applicable
   - `source_type` when applicable
5. Write the note with clear separation between:
   - facts or excerpts
   - synthesis
   - open questions
   - next actions
6. Add wikilinks to related notes when an Obsidian-style vault is in use.
7. Update one lightweight index or MOC so the note is discoverable.
8. If the user wants graph-style retrieval, run `graphify` on the note root.

## Default outputs

- `second-brain/sources/<slug>.md`
- `second-brain/evergreen/<slug>.md`
- `second-brain/projects/<slug>.md`
- `second-brain/meetings/<slug>.md`
- `second-brain/daily/YYYY-MM-DD.md`

Adjust the root when the repo already uses `vault/`, `notes/`, or another explicit notes directory.

## Rules

- Do not hide the original source; keep links and attribution.
- Prefer small, reusable notes over giant transcript dumps.
- Use markdown and frontmatter rather than app-specific formats.
- If the notes are meant for Obsidian, prefer wikilinks over standard relative markdown links.
- If the note should become presentation, strategy, or research input later, make the takeaway section explicit.
""",
            "references/note-types.md": """# Note Types

Use this reference when `second-brain-capture` is active.

## Folder mapping

- `sources/` — direct captures from URLs, videos, repos, or articles
- `evergreen/` — distilled ideas that should stay useful over time
- `projects/` — notes tied to one product, client, repo, or initiative
- `meetings/` — meeting summaries and decisions
- `daily/` — daily logs and inbox-style captures

## Frontmatter baseline

```yaml
---
title: <human title>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [tag-one, tag-two]
source: <url-or-path-when-relevant>
source_type: <video|github|web|meeting|internal>
status: active
---
```

## Source note structure

```markdown
# <Title>

## TL;DR

## Key claims or facts

## Evidence or excerpts

## Why it matters

## Related notes

## Open questions
```

## Evergreen note structure

```markdown
# <Idea>

## Claim

## Why it matters

## Supporting evidence

## Counterpoints or limits

## Related notes
```

## Meeting note structure

```markdown
# <Meeting title>

## Context

## Decisions

## Action items

## Risks or blockers
```
""",
        },
        "ss": """---
name: ss
description: Load the most recent screenshots from a screenshot inbox and act on them quickly. Use when the user invokes `/ss`-style screenshot workflows, wants recent screenshots explained, compared, transcribed, remixed, or used as visual context for a task.
---

# Screenshot Inbox

Treat recent local screenshots as structured visual input.

## Configuration

Determine the screenshot folder in this order:

1. `SCREENSHOT_INBOX`
2. `~/Pictures/Screenshots`
3. `~/Pictures/Screen Shots`
4. `~/Desktop`

If none of these exist or no screenshots are found, say so directly.

## Parsing

Interpret the arguments this way:

- no args -> `N=1`, action=`explain`
- first token is a positive integer -> that is `N`
- first token is `diff` -> `N=2`, action=`compare`
- otherwise -> `N=1`, action=`<full arg string>`

## Load the images

List the most recent PNG, JPG, or JPEG files:

```bash
find "<folder>" -maxdepth 1 -type f \\( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \\) -printf '%T@ %p\n' | sort -nr | head -N
```

Then inspect each returned image path with the local image-viewing tool available in the environment.

## Actions

- `explain`: describe the screenshot concretely and transcribe key visible text
- `compare`: compare multiple screenshots and call out what changed
- `transcribe`: extract visible text faithfully
- `fix`: treat the screenshot as a bug report or UI defect and connect it to the repo when possible
- `remix` or freeform: extract the pattern and adapt it to the user's context
- `infographic`: synthesize multiple screenshots into one HTML artifact saved in the current working directory

## Rules

- Confirm which screenshots were loaded before acting on them.
- Keep outputs tight; this workflow is for speed.
- If the user wants non-inbox images, ask for explicit file paths instead of guessing.
""",
        "obsidian-vault-manager": {
            "SKILL.md": """---
name: obsidian-vault-manager
description: Set up or maintain an Obsidian vault for repo-backed notes, templates, MOCs, and second-brain workflows. Use when the user asks to create an Obsidian vault, organize vault folders, add templates, or make a note system Obsidian-friendly.
---

# Obsidian Vault Manager

Create or normalize a Git-friendly Obsidian vault.

Read `references/vault-layout.md` before changing the vault structure.

## Workflow

1. Detect the target vault path.
   - Prefer an explicit path.
   - Otherwise detect an existing `.obsidian/` directory.
   - If none exists, choose a repo-local folder such as `vault/`.
2. If the vault does not exist, bootstrap it with:

```bash
bash "$CODEX_HOME/skills/obsidian-vault-manager/scripts/bootstrap_vault.sh" "<vault-path>"
```

3. Ensure the core layout exists:
   - `_index/`
   - `_templates/`
   - `daily/`
   - `projects/`
   - `research/`
   - `sources/`
   - `evergreen/`
   - `attachments/`
   - `archive/`
4. Ensure starter files exist:
   - `README.md`
   - `_index/Second Brain MOC.md`
   - `_templates/source-note.md`
   - `_templates/evergreen-note.md`
   - `_templates/meeting-note.md`
5. Normalize `.gitignore` so local-only Obsidian state stays out of git.
6. If the user wants GitHub-backed storage, continue with `obsidian-github-sync`.

## Rules

- Keep the vault plain markdown first; Obsidian is a reader, not the storage format.
- Do not commit transient Obsidian workspace files unless the user explicitly wants them tracked.
- Prefer a small, predictable folder structure over plugin-heavy conventions.
- Preserve existing vault content; add structure without flattening the user's notes.
""",
            "references/vault-layout.md": """# Recommended Vault Layout

Use this reference when `obsidian-vault-manager` is active.

## Directory structure

```text
vault/
├── .obsidian/
├── _index/
├── _templates/
├── attachments/
├── archive/
├── daily/
├── evergreen/
├── projects/
├── research/
└── sources/
```

## What each directory is for

- `_index/` — maps of content, indexes, and entry points
- `_templates/` — note templates
- `attachments/` — images and binary assets
- `archive/` — old material that should stay searchable
- `daily/` — daily capture notes
- `evergreen/` — distilled reusable ideas
- `projects/` — project-specific work
- `research/` — synthesis docs and briefs
- `sources/` — raw source notes

## Git-safe defaults

Track:
- markdown notes
- templates
- index files
- minimal `.obsidian/` config only when useful

Ignore:
- `.obsidian/workspace.json`
- `.obsidian/workspaces.json`
- plugin-local state such as `data.json`
- trash or cache folders
""",
            "scripts/bootstrap_vault.sh": """#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${1:-vault}"
VAULT_PATH="${VAULT_PATH/#\\~/$HOME}"

mkdir -p "$VAULT_PATH/.obsidian/plugins"

for dir in _index _templates attachments archive daily evergreen projects research sources; do
  mkdir -p "$VAULT_PATH/$dir"
done

touch "$VAULT_PATH/.obsidian/app.json"
touch "$VAULT_PATH/.obsidian/appearance.json"
touch "$VAULT_PATH/.obsidian/community-plugins.json"

GITIGNORE="$VAULT_PATH/.gitignore"
touch "$GITIGNORE"
for line in \
  ".obsidian/cache/" \
  ".obsidian/workspace.json" \
  ".obsidian/workspaces.json" \
  ".obsidian/plugins/*/data.json" \
  ".trash/" \
  ".DS_Store"
do
  grep -qxF "$line" "$GITIGNORE" || echo "$line" >> "$GITIGNORE"
done

if [ ! -f "$VAULT_PATH/README.md" ]; then
  cat > "$VAULT_PATH/README.md" <<'EOF'
# Obsidian Vault

This vault is structured for Git-friendly, markdown-first knowledge work.

## Entry points

- `_index/Second Brain MOC.md`
- `projects/`
- `research/`
- `sources/`
EOF
fi

if [ ! -f "$VAULT_PATH/_index/Second Brain MOC.md" ]; then
  cat > "$VAULT_PATH/_index/Second Brain MOC.md" <<'EOF'
# Second Brain MOC

## Recent source notes

## Evergreen notes

## Active projects

## Research themes
EOF
fi

if [ ! -f "$VAULT_PATH/_templates/source-note.md" ]; then
  cat > "$VAULT_PATH/_templates/source-note.md" <<'EOF'
---
title:
created:
updated:
tags: []
source:
source_type:
---

# {{title}}

## TL;DR

## Key claims

## Evidence

## Why it matters

## Related notes
EOF
fi

if [ ! -f "$VAULT_PATH/_templates/evergreen-note.md" ]; then
  cat > "$VAULT_PATH/_templates/evergreen-note.md" <<'EOF'
---
title:
created:
updated:
tags: []
---

# {{title}}

## Claim

## Why it matters

## Supporting evidence

## Related notes
EOF
fi

if [ ! -f "$VAULT_PATH/_templates/meeting-note.md" ]; then
  cat > "$VAULT_PATH/_templates/meeting-note.md" <<'EOF'
---
title:
created:
updated:
tags: [meeting]
---

# {{title}}

## Context

## Decisions

## Action items

## Risks
EOF
fi

echo "bootstrapped vault at $VAULT_PATH"
""",
        },
        "obsidian-github-sync": {
            "SKILL.md": """---
name: obsidian-github-sync
description: Use GitHub as durable storage for an Obsidian vault or markdown-based second brain. Use when the user asks to sync Obsidian with GitHub, keep notes in a repo, or treat GitHub as the storage layer for their vault.
---

# Obsidian GitHub Sync

Use Git and GitHub as the storage and sync layer for a vault or second-brain directory.

Read `references/sync-rules.md` before configuring the repo.

## Workflow

1. Identify the vault or notes root.
2. If the target is not already a git repo, initialize it with:

```bash
bash "$CODEX_HOME/skills/obsidian-github-sync/scripts/setup_repo_sync.sh" "<vault-path>" "<optional-remote-url>"
```

3. Verify:
   - current branch
   - remote configuration
   - `.gitignore` safety rules
4. If the user wants a GitHub repo created and `gh` is available, create or connect the remote.
5. Use the sync helper when the user wants a snapshot commit:

```bash
bash "$CODEX_HOME/skills/obsidian-github-sync/scripts/sync_vault.sh" "<vault-path>" "vault snapshot"
```

## Recommended operating model

- one main branch unless the user needs more complex collaboration
- pull before editing on a different machine
- commit after meaningful note changes, not every keystroke
- push frequently enough that GitHub stays the source of truth

## Rules

- Never store secrets, tokens, or transient browser state in the vault repo.
- Keep note storage text-first; use Git LFS only if the user knowingly wants large binaries.
- Ignore Obsidian workspace and plugin-local state by default.
- If a user wants fully automatic sync, explain the tradeoff before wiring a scheduled commit/push flow.
""",
            "references/sync-rules.md": """# Sync Rules

Use this reference when `obsidian-github-sync` is active.

## Safe defaults to track

- `*.md`
- template files
- `_index/` MOCs and indexes
- selected `.obsidian/` config files when they help share the vault structure

## Defaults to ignore

- `.obsidian/workspace.json`
- `.obsidian/workspaces.json`
- `.obsidian/cache/`
- `.obsidian/plugins/*/data.json`
- OS trash or editor swap files

## GitHub storage guidance

- Prefer one repo per vault or one repo per major knowledge domain.
- Use SSH remotes when available.
- Keep commit messages descriptive enough to make note history useful.
- For private notes, prefer private GitHub repos.
- If the vault contains large attachments, separate them intentionally or use Git LFS.
""",
            "scripts/setup_repo_sync.sh": """#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${1:-.}"
REMOTE_URL="${2:-}"
VAULT_PATH="${VAULT_PATH/#\\~/$HOME}"

mkdir -p "$VAULT_PATH"
cd "$VAULT_PATH"

if [ ! -d .git ]; then
  git init -b main >/dev/null 2>&1 || git init >/dev/null 2>&1
fi

current_branch=$(git branch --show-current 2>/dev/null || true)
if [ "$current_branch" = "master" ]; then
  git branch -M main >/dev/null 2>&1 || true
elif [ -z "$current_branch" ]; then
  git checkout -b main >/dev/null 2>&1 || git switch -c main >/dev/null 2>&1 || true
fi

GITIGNORE=".gitignore"
touch "$GITIGNORE"
for line in \
  ".obsidian/cache/" \
  ".obsidian/workspace.json" \
  ".obsidian/workspaces.json" \
  ".obsidian/plugins/*/data.json" \
  ".trash/" \
  ".DS_Store"
do
  grep -qxF "$line" "$GITIGNORE" || echo "$line" >> "$GITIGNORE"
done

if [ -n "$REMOTE_URL" ]; then
  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REMOTE_URL"
  else
    git remote add origin "$REMOTE_URL"
  fi
fi

echo "repo ready at $VAULT_PATH"
git status --short
if git remote get-url origin >/dev/null 2>&1; then
  echo "origin=$(git remote get-url origin)"
else
  echo "origin=unset"
fi
""",
            "scripts/sync_vault.sh": """#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${1:-.}"
MESSAGE="${2:-vault snapshot}"
VAULT_PATH="${VAULT_PATH/#\\~/$HOME}"

cd "$VAULT_PATH"

git add -A
if git diff --cached --quiet; then
  echo "nothing to commit"
  exit 0
fi

git commit -m "$MESSAGE"

if git remote get-url origin >/dev/null 2>&1; then
  branch=$(git branch --show-current)
  git push -u origin "$branch"
else
  echo "committed locally; origin is not configured"
fi
""",
        },
    }
)

TemplateValue = str | dict[str, str]


@dataclass
class Skill:
    source_root: Path
    source_name: str
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
SOURCE_BUNDLES: dict[str, dict[str, str]] = {
    "ai-analyst": {
        "ai-analyst/helpers/analytics_chart_style.mplstyle": "assets/analytics_chart_style.mplstyle",
        "ai-analyst/themes/analytics-light.css": "assets/themes/analytics-light.css",
        "ai-analyst/themes/analytics-dark.css": "assets/themes/analytics-dark.css",
        "ai-analyst/templates/deck_skeleton.marp.md": "references/deck_skeleton.marp.md",
        "ai-analyst/templates/marp_components.md": "references/marp_components.md",
    },
    "connect-data": {
        "ai-analyst/connection_templates/bigquery.yaml.example": "references/connection-templates/bigquery.yaml.example",
        "ai-analyst/connection_templates/duckdb.yaml.example": "references/connection-templates/duckdb.yaml.example",
        "ai-analyst/connection_templates/postgres.yaml.example": "references/connection-templates/postgres.yaml.example",
        "ai-analyst/connection_templates/snowflake.yaml.example": "references/connection-templates/snowflake.yaml.example",
    },
    "watch": {
        "watch/scripts/download.py": "scripts/download.py",
        "watch/scripts/frames.py": "scripts/frames.py",
        "watch/scripts/setup.py": "scripts/setup.py",
        "watch/scripts/transcribe.py": "scripts/transcribe.py",
        "watch/scripts/watch.py": "scripts/watch.py",
        "watch/scripts/whisper.py": "scripts/whisper.py",
    },
    "marp-deck-builder": {
        "ai-analyst/templates/deck_skeleton.marp.md": "references/deck_skeleton.marp.md",
        "ai-analyst/templates/marp_components.md": "references/marp_components.md",
    },
    "marp-exporter": {
        "ai-analyst/helpers/marp_export.py": "scripts/marp_export.py",
        "ai-analyst/helpers/marp_linter.py": "scripts/marp_linter.py",
        "ai-analyst/themes/analytics-light.css": "assets/themes/analytics-light.css",
        "ai-analyst/themes/analytics-dark.css": "assets/themes/analytics-dark.css",
    },
}


def skill_template(name: str, description: str, body: str) -> str:
    return (
        f"---\nname: {name}\ndescription: {description}\n---\n\n"
        f"{dedent(body).strip()}\n"
    )


def embedded_alias_template(
    name: str,
    description: str,
    target: str,
    reason: str,
) -> str:
    return skill_template(
        name,
        description,
        f"""
        # {name}

        This compatibility skill exists because the original Claude tree exposed `{name}` as a
        separate entrypoint. In the Codex pack, that behavior is folded into `{target}`.

        ## Use

        - Route the task to `{target}` instead of running a parallel workflow.
        - Preserve the original user intent when you hand off.
        - Mention that `{reason}` when that context matters.

        ## Handoff

        When `{name}` is invoked, continue with `{target}` and carry over:
        - the business question
        - active dataset or source context
        - any requested output such as metrics, charts, or a deck
        """,
    )


def build_ai_analyst_templates() -> dict[str, TemplateValue]:
    templates: dict[str, TemplateValue] = {}

    templates["ai-analyst"] = {
        "SKILL.md": skill_template(
            "ai-analyst",
            "Codex-native analytics entrypoint for business questions, metrics, trends, forecasting, and stakeholder-ready analysis. Use when the user asks a quantitative question or wants data explored, validated, and turned into findings or a deck.",
            """
            # AI Analyst

            This is the Codex-native entrypoint for analytics work. Use it when a request is
            fundamentally about data, metrics, trends, comparisons, forecasting, or business
            opportunity sizing.

            Read these references first:
            - `references/workspace-layout.md`
            - `references/analysis-levels.md`

            Companion skills:
            - `ask-question` for first-pass routing
            - `setup` and `connect-data` for onboarding
            - `run-analysis` for a full pipeline
            - `analytics-to-comms`, `chart-storyteller`, and `research-analysis-deck` for
              packaging findings

            ## Workflow

            1. Treat the user question as a business decision question, not just a query request.
            2. Confirm or infer the active dataset, source files, or data connection.
            3. Route to the lightest sufficient path:
               - direct metric answer
               - exploratory analysis
               - validated investigation
               - full deck-producing pipeline
            4. Keep a durable run trail under the workspace when the analysis is non-trivial.
            5. End with findings, caveats, and specific next actions.

            ## Rules

            - Prefer `ask-question` as the first analytical step for ambiguous requests.
            - Use `run-analysis` when the user wants a multi-step investigation, charts, or a deck.
            - Use `research-analysis-deck` when the work needs explicit JSON handoffs into a
              presentation workflow.
            - Never present a number without its timeframe, grain, and caveats.
            """,
        ),
        "references/workspace-layout.md": dedent(
            """
            # AI Analyst Workspace Layout

            Use this layout when bootstrapping or repairing an analytics workspace.

            ```text
            <workspace>/
            ├── .knowledge/
            │   ├── user/
            │   ├── datasets/
            │   ├── analyses/
            │   ├── corrections/
            │   ├── setup-state.yaml
            │   └── active.yaml
            ├── data/
            ├── outputs/
            └── working/
                └── runs/
            ```

            Recommended durable artifacts:
            - `.knowledge/user/profile.md`
            - `.knowledge/user/business-context.md`
            - `.knowledge/datasets/<dataset-id>/manifest.yaml`
            - `.knowledge/datasets/<dataset-id>/schema.md`
            - `.knowledge/datasets/<dataset-id>/metrics/index.yaml`
            - `.knowledge/analyses/index.yaml`
            - `.knowledge/corrections/index.yaml`
            - `working/runs/<timestamp>_<slug>/`
            """,
        ).strip()
        + "\n",
        "references/analysis-levels.md": dedent(
            """
            # Analysis Levels

            Use these levels to scope the analytical path.

            - `L1` direct metric: one number or one simple time slice
            - `L2` descriptive comparison: one cut or chart with light commentary
            - `L3` analytical explanation: multiple cuts and validation
            - `L4` investigation: root cause, tradeoffs, or opportunity sizing
            - `L5` executive package: validated analysis plus charts, deck, or stakeholder memo

            Upgrade to `L5` when the user asks for:
            - a deck
            - a polished readout
            - a comprehensive analysis package
            - board, exec, or stakeholder-ready outputs
            """,
        ).strip()
        + "\n",
    }

    templates["ask-question"] = skill_template(
        "ask-question",
        "Mandatory analytics entrypoint for a data question, metric request, trend readout, breakdown, or chart request. Use to classify the question, load the active data context, and route to the right analytical path.",
        """
        # Ask Question

        Read `../ai-analyst/references/workspace-layout.md` and
        `../ai-analyst/references/analysis-levels.md` first.

        ## Workflow

        1. Load the active workspace and dataset context if it exists.
        2. Parse the user question into:
           - metric or outcome
           - entities or segments
           - time range
           - required output
        3. Classify the request as `L1` through `L5`.
        4. Route to the lightest sufficient next skill:
           - `define-metric`
           - `explore-data`
           - `compare-datasets`
           - `forecast`
           - `size-opportunity`
           - `run-analysis`
        5. Write a short question brief before doing expensive work.

        ## Question brief

        Save the brief under `working/runs/<timestamp>_<slug>/question-brief.md` with:
        - the user question
        - normalized analytical question
        - chosen level
        - metrics involved
        - candidate dimensions
        - known caveats
        - recommended next skill

        ## Rules

        - For `L1-L2`, proceed directly once the brief is clear.
        - For `L3+`, explain the plan briefly before continuing.
        - If the workspace does not exist yet, route to `setup` or `connect-data`.
        - If the question is presentation-oriented, route to `run-analysis`.
        """,
    )

    templates["setup"] = skill_template(
        "setup",
        "Set up or repair an AI Analyst workspace with user profile, business context, data pointers, and output preferences. Use when the user wants to onboard, configure, or reset the analytics environment.",
        """
        # Setup

        Read `../ai-analyst/references/workspace-layout.md` first.

        ## Workflow

        1. Create the workspace layout if it does not exist.
        2. Capture:
           - role and technical level
           - domain and team context
           - preferred output style
           - default metrics or KPIs
        3. Write:
           - `.knowledge/user/profile.md`
           - `.knowledge/user/business-context.md`
           - `.knowledge/setup-state.yaml`
        4. If no data is connected, route to `connect-data`.
        5. End with suggested first analytical questions.

        ## Rules

        - Ask only the minimum questions needed to make the environment usable.
        - Keep secrets out of repo-tracked files.
        - If the user already has a workspace, update it instead of recreating it.
        """,
    )

    templates["connect-data"] = {
        "SKILL.md": skill_template(
            "connect-data",
            "Connect CSV, DuckDB, Postgres, BigQuery, or Snowflake data into the AI Analyst workspace and create a durable dataset manifest plus schema notes. Use when the user wants to add, list, or switch data sources.",
            """
            # Connect Data

            Read `../ai-analyst/references/workspace-layout.md` first.

            Use the example manifests in `references/connection-templates/` as starting points.

            ## Workflow

            1. Identify the connection type:
               - local files
               - DuckDB
               - Postgres
               - BigQuery
               - Snowflake
            2. Gather only non-secret connection metadata.
            3. Write or update:
               - `.knowledge/datasets/<dataset-id>/manifest.yaml`
               - `.knowledge/datasets/<dataset-id>/schema.md`
               - `.knowledge/active.yaml` when switching or activating
            4. Record how credentials are supplied, but never inline secrets.
            5. Produce a short readiness summary: tables, files, time range, and obvious risks.

            ## Rules

            - Prefer environment variables for credentials.
            - If the user only has CSVs or Parquet files, still create a dataset manifest.
            - If the schema is large, summarize top-priority tables first.
            """,
        ),
        "references/connection-guide.md": dedent(
            """
            # Connection Guide

            ## Local files
            - Store file paths relative to the workspace when possible.
            - Capture file format, row estimate, and date coverage.

            ## DuckDB
            - Record the `.duckdb` file path.
            - Note the logical schema or key tables if known.

            ## Postgres / BigQuery / Snowflake
            - Record host, database, schema, and role metadata only.
            - Reference env vars for secrets.
            - Avoid writing passwords, tokens, or private keys into manifests.
            """,
        ).strip()
        + "\n",
    }

    templates["question-framing"] = skill_template(
        "question-framing",
        "Turn a vague business question into a measurable analytical problem with scope, metrics, segments, and timeframe. Use when the user asks an ambiguous or broad analytics question.",
        """
        # Question Framing

        ## Workflow

        1. Rewrite the user question in measurable terms.
        2. Identify:
           - primary metric
           - denominator if relevant
           - comparison or baseline
           - dimensions worth segmenting by
           - expected business decision
        3. Produce a framing note with:
           - analytical question
           - assumptions
           - exclusions
           - must-have data inputs
        4. Route to `define-metric`, `explore-data`, or `run-analysis`.

        ## Rule

        If the question cannot be measured as written, say what needs to be clarified instead of pretending it is precise.
        """,
    )

    templates["business-context"] = skill_template(
        "business-context",
        "Capture or refresh the business context behind an analysis: product, market, KPIs, goals, and decision stakes. Use when the analytics work needs domain framing before interpreting the numbers.",
        """
        # Business Context

        ## Workflow

        1. Summarize what the company or product does.
        2. List the business goals or operating constraints relevant to the question.
        3. Record which stakeholders care about the answer.
        4. Write or update `.knowledge/user/business-context.md`.
        5. Highlight how this context changes interpretation of the metrics.
        """,
    )

    templates["explore-data"] = skill_template(
        "explore-data",
        "Explore the active dataset to understand tables, fields, date coverage, grain, and obvious analytical starting points. Use before deeper analysis when the data shape is not yet clear.",
        """
        # Explore Data

        ## Workflow

        1. Inventory the available files or tables.
        2. Summarize:
           - likely fact tables
           - likely dimensions
           - event timestamps
           - join keys
           - grain and freshness
        3. Create a compact exploration note in the current run directory.
        4. Surface obvious blockers such as missing dates, no user keys, or sparse metrics.
        5. Recommend the next skill:
           - `deep-profile`
           - `define-metric`
           - `data-quality-check`
           - `run-analysis`
        """,
    )

    templates["deep-profile"] = skill_template(
        "deep-profile",
        "Run a deeper profile of selected tables or files: distributions, nulls, cardinality, date coverage, and suspicious columns. Use when the user wants a serious read on data quality or table readiness.",
        """
        # Deep Profile

        ## Workflow

        1. Select the priority tables or files for profiling.
        2. For each, record:
           - row estimate
           - primary or candidate key
           - null rates
           - distinct counts
           - min/max dates
           - suspicious free-text or JSON columns
        3. Save the result to `working/runs/<timestamp>_<slug>/deep-profile.md`.
        4. Highlight anything that blocks trustworthy analysis.
        """,
    )

    templates["data-quality-check"] = skill_template(
        "data-quality-check",
        "Audit data quality before analysis: nulls, duplicates, freshness, key integrity, date coverage, and implausible values. Use when the user wants validation or when analysis quality is at risk.",
        """
        # Data Quality Check

        ## Workflow

        1. Check for:
           - missing critical fields
           - duplicate primary keys
           - invalid dates or negative counts
           - stale data
           - mismatched join keys
        2. Classify findings as:
           - blocker
           - warning
           - note
        3. Save a concise report in the current run directory.
        4. If blockers exist, stop and explain what is unsafe to conclude.
        """,
    )

    templates["define-metric"] = skill_template(
        "define-metric",
        "Define a metric rigorously with formula, grain, filters, numerator, denominator, caveats, and validation checks. Use when the user asks what a metric means or before calculating a metric repeatedly.",
        """
        # Define Metric

        ## Workflow

        1. Write a metric spec with:
           - metric name
           - business meaning
           - formula
           - grain
           - inclusion and exclusion rules
           - required tables or fields
           - known caveats
        2. Save it to `.knowledge/datasets/<dataset-id>/metrics/<metric>.yaml` when appropriate.
        3. Update the metric index.
        4. Add one quick validation check the analyst should run before trusting the metric.
        """,
    )

    templates["compare-datasets"] = skill_template(
        "compare-datasets",
        "Compare metrics, schema assumptions, and findings across two or more connected datasets. Use when the user wants to know whether a pattern is shared, unique, or inconsistently defined across datasets.",
        """
        # Compare Datasets

        ## Workflow

        1. Identify the datasets to compare.
        2. Load shared metric definitions and schema notes.
        3. Compare:
           - metric definitions
           - baseline ranges
           - recurring findings
           - obvious divergences
        4. Save a cross-dataset note under `.knowledge/analyses/` or the active run.
        5. End with concrete recommendations:
           - align definitions
           - investigate divergence
           - segment by product or market
        """,
    )

    templates["switch-dataset"] = skill_template(
        "switch-dataset",
        "Change the active dataset in the analytics workspace and confirm what schema and metric context is now in scope. Use when the user wants to work on another dataset.",
        """
        # Switch Dataset

        ## Workflow

        1. Confirm the target dataset exists.
        2. Update `.knowledge/active.yaml`.
        3. Show the active dataset summary:
           - name
           - source type
           - top tables
           - key metrics if known
        4. Suggest the next likely analytical step.
        """,
    )

    templates["analysis-design-spec"] = skill_template(
        "analysis-design-spec",
        "Design the analytical plan before querying: hypotheses, cuts, validations, and deliverables. Use when the question is consequential enough to warrant an explicit analysis spec.",
        """
        # Analysis Design Spec

        ## Workflow

        1. Convert the question brief into a structured design spec.
        2. Include:
           - hypotheses
           - required data sources
           - proposed cuts and segments
           - validation checks
           - deliverables
        3. Save the spec in the run directory before heavy analysis starts.
        4. Use it as the contract for `run-analysis`.
        """,
    )

    templates["run-analysis"] = skill_template(
        "run-analysis",
        "Run a full analytical pipeline from question brief to validated findings, charts, and stakeholder-ready outputs. Use when the user wants a deep investigation, comprehensive analysis, or a polished readout or deck.",
        """
        # Run Analysis

        Read:
        - `../ai-analyst/references/workspace-layout.md`
        - `../ai-analyst/references/analysis-levels.md`

        ## Workflow

        1. Start from an `ask-question` brief or create one quickly.
        2. Create a run directory under `working/runs/`.
        3. Execute the minimum effective pipeline:
           - framing
           - metric definition
           - data exploration
           - quality checks
           - core analysis
           - validation
           - charts
           - stakeholder packaging
        4. Use:
           - `chart-storyteller` for chart decisions
           - `analytics-to-comms` and `stakeholder-comms` for output packaging
           - `research-analysis-deck` when you need explicit JSON handoffs into a deck
        5. Save final artifacts under `outputs/` and archive the run.

        ## Deliverables

        At minimum produce:
        - a findings summary
        - a caveats section
        - next actions

        When requested, also produce:
        - a deck plan
        - charts
        - a memo or stakeholder brief

        ## Rules

        - Halt if the data is too unreliable to answer the question honestly.
        - Keep a durable trail of decisions in the run directory.
        - Prefer a compact, validated storyline over an oversized chart dump.
        """,
    )

    templates["forecast"] = skill_template(
        "forecast",
        "Forecast a metric or business outcome with explicit assumptions, uncertainty, and backtesting expectations. Use when the user asks what will happen next or wants a forward-looking estimate.",
        """
        # Forecast

        ## Workflow

        1. Define the target metric and forecasting horizon.
        2. Check whether the history is long and clean enough for forecasting.
        3. Document:
           - baseline trend
           - seasonality assumptions
           - known interventions or shocks
           - uncertainty bounds
        4. Produce a forecast note and state the confidence honestly.
        5. If the history is weak, recommend scenario ranges instead of a fake precise forecast.
        """,
    )

    templates["patterns"] = embedded_alias_template(
        "patterns",
        "Compatibility entrypoint for recurring-pattern analysis across segments, cohorts, or time. Use when an old workflow expects the `patterns` skill name.",
        "run-analysis",
        "pattern discovery is now part of the validated analysis workflow",
    )

    templates["size-opportunity"] = skill_template(
        "size-opportunity",
        "Quantify the potential business upside or downside associated with a finding. Use when the user wants to know how much a problem or improvement is worth.",
        """
        # Size Opportunity

        ## Workflow

        1. State the baseline metric and the improvement scenario.
        2. Identify the population affected.
        3. Calculate rough upside, downside, or savings.
        4. Show the assumptions explicitly.
        5. Provide best case, base case, and conservative case when precision is weak.
        """,
    )

    templates["design-experiment"] = skill_template(
        "design-experiment",
        "Design a test or experiment from an analytical finding. Use when the user wants to validate a hypothesis, run an A/B test, or convert a finding into an intervention plan.",
        """
        # Design Experiment

        ## Workflow

        1. Define the hypothesis in business terms.
        2. Specify:
           - treatment and control
           - primary success metric
           - guardrail metrics
           - sample or exposure logic
           - decision threshold
        3. Note dependencies and rollout risks.
        4. End with a compact experiment brief the team can execute.
        """,
    )

    templates["guardrails"] = skill_template(
        "guardrails",
        "Apply publishing and interpretation guardrails before sharing analytical findings. Use when the output is high stakes and needs a final quality gate.",
        """
        # Guardrails

        ## Checklist

        Confirm:
        - the metric is clearly defined
        - the timeframe matches the claim
        - the denominator is appropriate
        - caveats are disclosed
        - segment math ties back to the whole
        - no visually misleading charts remain

        If any item fails, stop and say what must be fixed before publishing.
        """,
    )

    templates["semantic-validation"] = skill_template(
        "semantic-validation",
        "Validate that the business meaning of an analysis matches the metric definitions, event semantics, and stakeholder language. Use when a technically correct query may still be conceptually wrong.",
        """
        # Semantic Validation

        ## Workflow

        1. Compare the claimed finding to the actual metric and event semantics.
        2. Check for business-language mismatches such as:
           - signups vs activated users
           - revenue booked vs revenue recognized
           - churned accounts vs churned seats
        3. Rewrite the finding if the business meaning was overstated.
        """,
    )

    templates["triangulation"] = skill_template(
        "triangulation",
        "Cross-check a finding through multiple cuts, methods, or source types. Use when the user needs stronger confidence before acting on an analytical conclusion.",
        """
        # Triangulation

        ## Workflow

        1. Identify the main finding.
        2. Re-test it with at least one independent angle:
           - another segment
           - another calculation path
           - another dataset or source
        3. Report whether the story holds, weakens, or reverses.
        """,
    )

    templates["tracking-gaps"] = skill_template(
        "tracking-gaps",
        "Identify missing instrumentation, broken event coverage, or schema gaps that block confident analysis. Use when the data cannot support the business question cleanly.",
        """
        # Tracking Gaps

        ## Workflow

        1. List the questions the current data cannot answer reliably.
        2. Map each gap to:
           - missing field
           - missing event
           - inconsistent grain
           - no durable key
        3. Prioritize the gaps by business impact.
        4. End with a concrete instrumentation backlog.
        """,
    )

    templates["knowledge-bootstrap"] = embedded_alias_template(
        "knowledge-bootstrap",
        "Compatibility entrypoint for loading workspace context and prior analytical knowledge. Use when an old workflow expects the `knowledge-bootstrap` skill name.",
        "ask-question",
        "context loading is now part of the default analytics entrypoint",
    )

    templates["archaeology"] = skill_template(
        "archaeology",
        "Recover prior analytical work, query fragments, or reasoning from the workspace before repeating an analysis. Use when the user suspects the question was answered before.",
        """
        # Archaeology

        ## Workflow

        1. Search prior run folders, analysis notes, and metric definitions.
        2. Extract reusable pieces:
           - questions
           - SQL or query ideas
           - charts
           - caveats
        3. Summarize what can be reused and what needs fresh work.
        """,
    )

    templates["archive-analysis"] = skill_template(
        "archive-analysis",
        "Archive a completed analysis run with enough metadata to find and reuse it later. Use when a run is complete and should be preserved cleanly.",
        """
        # Archive Analysis

        ## Workflow

        1. Capture:
           - question
           - date
           - dataset
           - key findings
           - output artifacts
           - confidence
        2. Update `.knowledge/analyses/index.yaml`.
        3. Mark the run directory as archived or complete.
        """,
    )

    templates["log-correction"] = skill_template(
        "log-correction",
        "Record a known data caveat, metric correction, or interpretation fix so future analyses do not repeat the same mistake. Use when a data issue is discovered.",
        """
        # Log Correction

        ## Workflow

        1. Record the issue, affected metric or table, and corrected interpretation.
        2. Save it under `.knowledge/corrections/` and update the index.
        3. Reference the correction in future relevant analyses.
        """,
    )

    templates["feedback-capture"] = skill_template(
        "feedback-capture",
        "Capture user or stakeholder feedback on an analysis, chart set, or deck so the next iteration gets smarter. Use when someone reacts to a readout or asks for changes.",
        """
        # Feedback Capture

        ## Workflow

        1. Log the feedback with:
           - source
           - date
           - requested change
           - whether it affects metric logic, narrative, or presentation
        2. Save it in the current run directory and optionally in a durable feedback log.
        3. Convert feedback into follow-up actions when appropriate.
        """,
    )

    templates["first-run-welcome"] = embedded_alias_template(
        "first-run-welcome",
        "Compatibility entrypoint for onboarding a new analytics user. Use when an old workflow expects the `first-run-welcome` skill name.",
        "setup",
        "onboarding is now handled by the setup flow",
    )

    templates["manage-runs"] = skill_template(
        "manage-runs",
        "Inspect, summarize, and tidy analytical run folders. Use when the user wants to see what is running, what completed, or what artifacts were produced.",
        """
        # Manage Runs

        ## Workflow

        1. Enumerate runs under `working/runs/`.
        2. Show status:
           - active
           - blocked
           - complete
           - archived
        3. Summarize outputs and missing pieces.
        4. Suggest `resume-analysis`, `archive-analysis`, or `close-the-loop` when relevant.
        """,
    )

    templates["resume-analysis"] = skill_template(
        "resume-analysis",
        "Resume a partially completed analytical run from its saved context and remaining tasks. Use when a previous analysis was interrupted or left incomplete.",
        """
        # Resume Analysis

        ## Workflow

        1. Load the selected run directory.
        2. Inspect what exists:
           - question brief
           - spec
           - findings
           - charts
           - packaged outputs
        3. Identify the first incomplete stage.
        4. Continue from there instead of restarting the whole analysis.
        """,
    )

    templates["close-the-loop"] = skill_template(
        "close-the-loop",
        "Wrap an analysis with final recommendations, owners, open questions, and follow-up actions. Use when a run is complete and should end with an operational handoff.",
        """
        # Close The Loop

        ## Workflow

        1. Restate the question and answer.
        2. Summarize the evidence, confidence, and caveats.
        3. List:
           - decisions enabled
           - follow-up actions
           - owners or stakeholder audiences
           - unresolved questions
        4. Save a concise closing note in the run directory.
        """,
    )

    templates["view-history"] = skill_template(
        "view-history",
        "Browse prior analytical questions, findings, and archived runs. Use when the user wants to recall what has already been analyzed.",
        """
        # View History

        ## Workflow

        1. Read the analysis archive or run index.
        2. List recent analyses with:
           - date
           - title or question
           - dataset
           - confidence
           - output types
        3. Support search by term, dataset, or timeframe.
        4. Suggest `resume-analysis` if a relevant partial run exists.
        """,
    )

    templates["view-metrics"] = skill_template(
        "view-metrics",
        "Show the available metric definitions for the active dataset and highlight gaps or inconsistencies. Use when the user wants to browse or inspect defined metrics.",
        """
        # View Metrics

        ## Workflow

        1. Load the active dataset's metric index.
        2. Show metric name, business meaning, and grain.
        3. Flag metrics missing definitions or validation notes.
        4. Suggest `define-metric` where the catalog is weak.
        """,
    )

    templates["visualization-patterns"] = embedded_alias_template(
        "visualization-patterns",
        "Compatibility entrypoint for chart-pattern guidance and SWD-style analytical visuals. Use when an old workflow expects the `visualization-patterns` skill name.",
        "chart-storyteller",
        "chart-pattern selection now lives in the chart storytelling workflow",
    )

    templates["question-router"] = embedded_alias_template(
        "question-router",
        "Compatibility entrypoint for analytics question routing. Use when an old workflow expects the `question-router` skill name.",
        "ask-question",
        "question classification is now built into the main analytics entrypoint",
    )

    templates["presentation-themes"] = skill_template(
        "presentation-themes",
        "Apply or switch analysis presentation themes and chart/deck styling choices. Use when the user wants the analytical presentation restyled or wants a theme selected explicitly.",
        """
        # Presentation Themes

        This is the analytics-facing alias for `presentation-theme`.

        ## Workflow

        1. Inspect the existing deck or HTML presentation.
        2. Choose a theme that matches the audience and analysis tone.
        3. Apply the visual change without rewriting the analytical content.
        4. Keep chart styling and slide styling coherent.

        Prefer the existing `presentation-theme` skill when the work is centered on deck visuals.
        """,
    )

    return templates


PORT_TEMPLATES.update(build_ai_analyst_templates())


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


def normalize_source_name(path: Path) -> str:
    if path == CLAUDE_SKILLS_DIR:
        return "global"
    return path.name or path.as_posix()


def resolve_source_roots(extra_roots: Iterable[str] | None = None) -> list[Path]:
    roots: list[Path] = []
    seen: set[Path] = set()

    def add_root(raw: str | Path | None) -> None:
        if not raw:
            return
        path = Path(raw).expanduser().resolve()
        if path in seen:
            return
        seen.add(path)
        roots.append(path)

    add_root(CLAUDE_SKILLS_DIR)

    env_roots = os.environ.get("CLAUDE_SKILL_SOURCE_ROOTS", "")
    if env_roots:
        for entry in env_roots.split(os.pathsep):
            add_root(entry.strip())

    for entry in extra_roots or []:
        add_root(entry)

    return [root for root in roots if root.exists()]


def discover_skills(source_roots: Iterable[Path] | None = None) -> list[Skill]:
    roots = list(source_roots or [CLAUDE_SKILLS_DIR])
    skills: list[Skill] = []

    for source_root in roots:
        for skill_path in sorted(source_root.rglob("SKILL.md")):
            if not skill_path.exists() or not skill_path.is_file():
                continue
            rel_path = skill_path.parent.relative_to(source_root).as_posix()
            try:
                raw_text = skill_path.read_text(encoding="utf-8")
            except FileNotFoundError:
                continue
            metadata, _ = parse_frontmatter(raw_text)
            name = metadata.get("name", skill_path.parent.name)
            description = metadata.get("description", "")
            skills.append(
                Skill(
                    source_root=source_root,
                    source_name=normalize_source_name(source_root),
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
            "watch",
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


def display_path(skill: Skill) -> str:
    if skill.source_root == CLAUDE_SKILLS_DIR:
        return skill.rel_path
    return f"{skill.source_name}::{skill.rel_path}"


def inventory(extra_roots: Iterable[str] | None = None) -> int:
    roots = resolve_source_roots(extra_roots)
    skills = discover_skills(roots)
    if not skills:
        joined = ", ".join(str(root) for root in roots) or str(CLAUDE_SKILLS_DIR)
        print(f"No Claude skills found under {joined}", file=sys.stderr)
        return 1

    print("classification\tskill\tpath\treasons")
    for skill in skills:
        classification, reasons = classify_skill(skill)
        joined = "; ".join(reasons)
        print(f"{classification}\t{skill.name}\t{display_path(skill)}\t{joined}")
    return 0


def clean_staging_dir() -> None:
    STAGING_SKILLS_DIR.mkdir(parents=True, exist_ok=True)


def build_skill_index(skills: list[Skill]) -> dict[str, Skill]:
    skill_index: dict[str, Skill] = {}
    names_seen: dict[str, Skill] = {}
    duplicate_names: set[str] = set()

    for skill in skills:
        skill_index[skill.rel_path] = skill
        skill_index[display_path(skill)] = skill
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
    description = skill.description or f"Migrated from Claude skill: {display_path(skill)}"
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


def copy_source_bundle(skill_name: str, skill_dir: Path) -> None:
    bundle = SOURCE_BUNDLES.get(skill_name)
    if bundle is None:
        return

    for source_rel, dest_rel in bundle.items():
        source_path = CLAUDE_SKILLS_DIR / source_rel
        if not source_path.exists():
            raise FileNotFoundError(f"Missing source bundle file: {source_path}")
        target = skill_dir / dest_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target)


def patch_watch_bundle(skill_dir: Path) -> None:
    setup_path = skill_dir / "scripts" / "setup.py"
    whisper_path = skill_dir / "scripts" / "whisper.py"

    setup_text = setup_path.read_text(encoding="utf-8")
    setup_text = setup_text.replace(
        "import platform\n",
        "import platform\nimport pwd\n",
    )
    setup_text = setup_text.replace(
        'CONFIG_DIR = Path.home() / ".config" / "watch"\nCONFIG_FILE = CONFIG_DIR / ".env"\n',
        'def _real_home() -> Path:\n'
        '    try:\n'
        '        return Path(pwd.getpwuid(os.getuid()).pw_dir)\n'
        '    except KeyError:\n'
        '        return Path.home()\n\n'
        'CONFIG_DIR = _real_home() / ".config" / "watch"\n'
        'CONFIG_FILE = CONFIG_DIR / ".env"\n',
    )
    setup_path.write_text(setup_text, encoding="utf-8")

    whisper_text = whisper_path.read_text(encoding="utf-8")
    whisper_text = whisper_text.replace(
        "import uuid\nfrom pathlib import Path\n",
        "import uuid\nimport pwd\nfrom pathlib import Path\n",
    )
    whisper_text = whisper_text.replace(
        '    dotenv_paths = [\n'
        '        Path.home() / ".config" / "watch" / ".env",\n'
        '        Path.cwd() / ".env",\n'
        '    ]\n',
        "    try:\n"
        "        real_home = Path(pwd.getpwuid(os.getuid()).pw_dir)\n"
        "    except KeyError:\n"
        "        real_home = Path.home()\n\n"
        "    dotenv_paths = [\n"
        '        real_home / ".config" / "watch" / ".env",\n'
        '        Path.cwd() / ".env",\n'
        "    ]\n",
    )
    whisper_path.write_text(whisper_text, encoding="utf-8")


def patch_marp_bundle(skill_dir: Path) -> None:
    export_path = skill_dir / "scripts" / "marp_export.py"
    export_text = export_path.read_text(encoding="utf-8")
    export_text = export_text.replace(
        "    deck_dir = Path(deck_path).resolve().parent\n"
        "    # Search up to 3 levels up\n"
        "    for parent in [deck_dir] + list(deck_dir.parents)[:3]:\n"
        '        themes_dir = parent / "themes"\n'
        "        if themes_dir.is_dir():\n"
        "            return themes_dir\n"
        "    return None\n",
        "    deck_dir = Path(deck_path).resolve().parent\n"
        '    bundled_themes = Path(__file__).resolve().parents[1] / "assets" / "themes"\n'
        "    if bundled_themes.is_dir():\n"
        "        return bundled_themes\n\n"
        "    # Search up to 3 levels up\n"
        "    for parent in [deck_dir] + list(deck_dir.parents)[:3]:\n"
        '        themes_dir = parent / "themes"\n'
        "        if themes_dir.is_dir():\n"
        "            return themes_dir\n"
        "    return None\n",
    )
    export_path.write_text(export_text, encoding="utf-8")


def write_template_bundle(skill_name: str, skill_dir: Path, rendered: TemplateValue) -> None:
    if isinstance(rendered, str):
        (skill_dir / "SKILL.md").write_text(rendered, encoding="utf-8")
    else:
        for relative_path, content in rendered.items():
            target = skill_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    copy_source_bundle(skill_name, skill_dir)
    if skill_name == "watch":
        patch_watch_bundle(skill_dir)
    if skill_name == "marp-exporter":
        patch_marp_bundle(skill_dir)


def stage_skills(selected_names: list[str], extra_roots: Iterable[str] | None = None) -> int:
    clean_staging_dir()
    roots = resolve_source_roots(extra_roots)
    skills = discover_skills(roots)
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
        write_template_bundle(name, skill_dir, rendered)
        print(f"staged\t{name}\t{skill_dir}")
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory Claude skills and stage Codex-ready adaptations."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("inventory", help="List Claude skills and migration classes.")
    inventory_parser = subparsers.choices["inventory"]
    inventory_parser.add_argument(
        "--source-root",
        action="append",
        default=[],
        help="Additional skill source root to scan, e.g. a Claude Cowork workspace.",
    )

    stage_parser = subparsers.add_parser(
        "stage", help="Write staged Codex skill adaptations into the repo."
    )
    stage_parser.add_argument(
        "--skills",
        default=",".join(sorted(SUPPORTED_SKILLS)),
        help="Comma-separated skill names to stage. Default: the supported starter set.",
    )
    stage_parser.add_argument(
        "--source-root",
        action="append",
        default=[],
        help="Additional skill source root to scan when resolving Claude skills.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "inventory":
        return inventory(args.source_root)

    if args.command == "stage":
        selected_names = [name.strip() for name in args.skills.split(",") if name.strip()]
        return stage_skills(selected_names, args.source_root)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
