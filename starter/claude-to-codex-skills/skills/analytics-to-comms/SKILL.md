---
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
