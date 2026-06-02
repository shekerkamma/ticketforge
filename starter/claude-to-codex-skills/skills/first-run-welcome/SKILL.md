---
name: first-run-welcome
description: Compatibility entrypoint for onboarding a new analytics user. Use when an old workflow expects the `first-run-welcome` skill name.
---

# first-run-welcome

This compatibility skill exists because the original Claude tree exposed `first-run-welcome` as a
separate entrypoint. In the Codex pack, that behavior is folded into `setup`.

## Use

- Route the task to `setup` instead of running a parallel workflow.
- Preserve the original user intent when you hand off.
- Mention that `onboarding is now handled by the setup flow` when that context matters.

## Handoff

When `first-run-welcome` is invoked, continue with `setup` and carry over:
- the business question
- active dataset or source context
- any requested output such as metrics, charts, or a deck
