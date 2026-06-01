---
name: ai-strategy-researcher
description: Research a market, vertical, or AI strategy topic deeply and produce a structured strategy report. Use when the user wants market intelligence, a strategy document, or a researched view of how an AI opportunity should be evaluated.
---

# AI Strategy Researcher

This is the Codex-native strategy research workflow.

## Research passes

1. Market signals
2. Competitive proof points
3. Failure analysis
4. Unit economics and GTM patterns
5. Framework application

## Frameworks to apply

- Copilot vs Autopilot
- Intelligence vs Judgment
- Mirage PMF risk
- North Star Metric

## Default outputs

- `strategy-research/<slug>-strategy.md`
- `strategy-research/<slug>-sources.md`

Optional:

- `.docx` export if requested and the environment supports it

## Report structure

```markdown
# Strategy Research: <topic>

## Executive Summary

## Market Signal Analysis

## Macro Thesis

## Market Sizing and Vertical Analysis

## Proof Points

## Operational Playbook

## Unit Economics

## Competitive Moats

## Risk Analysis

## Strategic Framework

## Competitive Landscape

## References
```

## Rules

- Prefer primary and operator-grade sources.
- Separate evidence from your interpretation.
- Convert relative dates into absolute dates.
- If you cannot support a section with evidence, say so instead of padding it.
