# Chain Contract

This skill exists because the current research, analysis, and presentation skills are individually strong but too loose at the handoff boundaries.

## Goal

Standardize three machine-readable checkpoints:

1. `source-notes.json`
2. `analysis-pack.json`
3. `deck-plan.json`

If these files are valid, the chain is healthy.

## File meanings

### `source-notes.json`

One structured record per source. This is the durable evidence layer.

Use it to capture:

- source identity
- source type
- source URL or file path
- raw excerpts
- extracted claims
- use-case hints

### `analysis-pack.json`

The interpreted findings layer. This is where the evidence becomes a point of view.

Use it to capture:

- decision question
- audience
- headline
- findings
- use-case clusters
- risks
- recommendations
- chart briefs

### `deck-plan.json`

The communication layer. This is where the story becomes slides.

Use it to capture:

- narrative arc
- slide sequence
- slide types
- content blocks
- evidence mapping
- speaker-note intent

## Rules of evidence

- A recommendation without a supporting finding is weak.
- A finding without linked source IDs is invalid.
- A slide without a clear objective or source mapping is not ready.

## Practical guidance

- Keep source notes broad and factual.
- Keep the analysis pack selective and opinionated.
- Keep the deck plan concise and audience-specific.
- When content grows, add slides. Do not cram.
