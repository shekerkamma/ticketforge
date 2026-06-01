---
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
