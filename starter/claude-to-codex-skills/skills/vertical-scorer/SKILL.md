---
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
