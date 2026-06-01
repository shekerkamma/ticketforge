---
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
