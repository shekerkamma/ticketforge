---
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
