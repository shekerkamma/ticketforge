---
name: research-analysis-deck
description: Orchestrate a source-backed workflow from research to structured analysis to a slide-ready deck plan using explicit JSON handoffs. Use when the user wants a serious market, company, use-case, or strategy report that must survive chaining into charts, stakeholder framing, and deck production.
---

# Research Analysis Deck

This is the chain skill for `research -> analysis -> deck`.

Use it when the job is too important to trust to loose markdown handoffs.

## Companion skills

- `content-research`
- `analytics-to-comms`
- `chart-storyteller`
- `stakeholder-comms`
- `presentation-content-writer`
- `presentation`

## Contract

Read these only as needed:

- `references/chain-contract.md`
- `references/source-note.schema.json`
- `references/analysis-pack.schema.json`
- `references/slide-spec.schema.json`
- `references/deck-plan.schema.json`

Use the bundled scripts when helpful:

- `scripts/scaffold_chain.py`
- `scripts/validate_chain.py`

## Workflow

1. Confirm the decision question, audience, and final artifact:
   - report only
   - deck plan
   - branded presentation
2. Create or refresh the chain scaffold:
   - `research-notes/<slug>/source-notes.json`
   - `analytics-comms/<slug>/analysis-pack.json`
   - `analytics-comms/<slug>/deck-plan.json`
3. Run `content-research` and convert the gathered notes into `source-notes.json`.
4. Run `analytics-to-comms` on top of the research and write `analysis-pack.json`.
5. Run `chart-storyteller` for each chart-worthy finding and fold the output into the analysis pack or deck plan.
6. Run `stakeholder-comms` to adapt the framing for the target audience.
7. Run `presentation-content-writer` to produce a slide-by-slide plan.
8. Run `presentation` only after the deck plan is structurally sound.
9. Validate the JSON handoffs before exporting a deck or report.

## Required file layout

- `research-notes/<slug>/source-notes.json`
- `analytics-comms/<slug>/analysis-pack.json`
- `analytics-comms/<slug>/deck-plan.json`

Optional downstream artifacts:

- `analytics-comms/<slug>/analysis.md`
- `analytics-comms/<slug>/chart-brief.md`
- `docs/reports/<slug>.pptx`
- `docs/reports/<slug>.html`

## Rules

- Do not jump straight from raw research into slides.
- Keep evidence and interpretation separate.
- Every major finding in the analysis pack must point back to at least one source note.
- Every slide in the deck plan must map back to one or more findings, recommendations, or source-backed examples.
- Split dense content into additional slides instead of shrinking the font to fit.
- If the deck is PowerPoint-native, treat HTML presentation helpers as optional, not as the backbone.
