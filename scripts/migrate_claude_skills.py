#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pwd
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
STAGING_ROOT = REPO_ROOT / "starter" / "claude-to-codex-skills"
STAGING_SKILLS_DIR = STAGING_ROOT / "skills"

CHAIN_TEMPLATE_SKILLS = {
    "agent-browser",
    "ai-strategy-council",
    "ai-strategy-researcher",
    "analytics-to-comms",
    "architect",
    "architecture-to-everything",
    "carousel-to-deck",
    "content-repurpose",
    "competitive-intel-sprint",
    "morning-briefing",
    "obsidian-github-sync",
    "obsidian-vault-manager",
    "printing-press",
    "presentation",
    "presales-deal-prep",
    "content-research",
    "research-to-strategy",
    "second-brain-capture",
    "ss",
    "llm-council",
    "url-dossier",
}

SUPPORTED_SKILLS = {
    "anti-slop",
    "agent-browser",
    "architect",
    "architecture-to-everything",
    "ai-strategy-brief",
    "ai-strategy-council",
    "ai-strategy-researcher",
    "analytics-to-comms",
    "session-handoff",
    "ss",
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
    "competitive-intel-sprint",
    "content-repurpose",
    "llm-council",
    "morning-briefing",
    "obsidian-github-sync",
    "obsidian-vault-manager",
    "printing-press",
    "presentation",
    "presentation-content-writer",
    "presentation-theme",
    "presentation-exporter",
    "presentation-speaker-notes",
    "presentation-accessibility",
    "content-research",
    "research-to-strategy",
    "second-brain-capture",
    "watch",
    "url-dossier",
    "vertical-scorer",
    "presales-deal-prep",
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
WATCH_SOURCE_ROOT = CLAUDE_SKILLS_DIR / "watch"
SOURCE_BUNDLES: dict[str, dict[str, str]] = {
    "watch": {
        "scripts/download.py": "scripts/download.py",
        "scripts/frames.py": "scripts/frames.py",
        "scripts/setup.py": "scripts/setup.py",
        "scripts/transcribe.py": "scripts/transcribe.py",
        "scripts/watch.py": "scripts/watch.py",
        "scripts/whisper.py": "scripts/whisper.py",
    }
}


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
        source_path = WATCH_SOURCE_ROOT / source_rel
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
