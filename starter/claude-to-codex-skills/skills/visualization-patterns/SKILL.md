---
name: visualization-patterns
description: Compatibility entrypoint for chart-pattern guidance and SWD-style analytical visuals. Use when an old workflow expects the `visualization-patterns` skill name.
---

# visualization-patterns

This compatibility skill exists because the original Claude tree exposed `visualization-patterns` as a
separate entrypoint. In the Codex pack, that behavior is folded into `chart-storyteller`.

## Use

- Route the task to `chart-storyteller` instead of running a parallel workflow.
- Preserve the original user intent when you hand off.
- Mention that `chart-pattern selection now lives in the chart storytelling workflow` when that context matters.

## Handoff

When `visualization-patterns` is invoked, continue with `chart-storyteller` and carry over:
- the business question
- active dataset or source context
- any requested output such as metrics, charts, or a deck
