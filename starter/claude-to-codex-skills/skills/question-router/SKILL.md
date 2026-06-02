---
name: question-router
description: Compatibility entrypoint for analytics question routing. Use when an old workflow expects the `question-router` skill name.
---

# question-router

This compatibility skill exists because the original Claude tree exposed `question-router` as a
separate entrypoint. In the Codex pack, that behavior is folded into `ask-question`.

## Use

- Route the task to `ask-question` instead of running a parallel workflow.
- Preserve the original user intent when you hand off.
- Mention that `question classification is now built into the main analytics entrypoint` when that context matters.

## Handoff

When `question-router` is invoked, continue with `ask-question` and carry over:
- the business question
- active dataset or source context
- any requested output such as metrics, charts, or a deck
