---
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
