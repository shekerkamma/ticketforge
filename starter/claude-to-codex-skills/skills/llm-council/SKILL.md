---
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
