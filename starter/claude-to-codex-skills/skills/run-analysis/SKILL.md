---
name: run-analysis
description: Run a full analytical pipeline from question brief to validated findings, charts, and stakeholder-ready outputs. Use when the user wants a deep investigation, comprehensive analysis, or a polished readout or deck.
---

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
