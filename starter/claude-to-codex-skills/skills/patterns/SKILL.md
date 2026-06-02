---
name: patterns
description: Compatibility entrypoint for recurring-pattern analysis across segments, cohorts, or time. Use when an old workflow expects the `patterns` skill name.
---

# patterns

This compatibility skill exists because the original Claude tree exposed `patterns` as a
separate entrypoint. In the Codex pack, that behavior is folded into `run-analysis`.

## Use

- Route the task to `run-analysis` instead of running a parallel workflow.
- Preserve the original user intent when you hand off.
- Mention that `pattern discovery is now part of the validated analysis workflow` when that context matters.

## Handoff

When `patterns` is invoked, continue with `run-analysis` and carry over:
- the business question
- active dataset or source context
- any requested output such as metrics, charts, or a deck
