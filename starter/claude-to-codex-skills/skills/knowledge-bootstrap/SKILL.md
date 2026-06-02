---
name: knowledge-bootstrap
description: Compatibility entrypoint for loading workspace context and prior analytical knowledge. Use when an old workflow expects the `knowledge-bootstrap` skill name.
---

# knowledge-bootstrap

This compatibility skill exists because the original Claude tree exposed `knowledge-bootstrap` as a
separate entrypoint. In the Codex pack, that behavior is folded into `ask-question`.

## Use

- Route the task to `ask-question` instead of running a parallel workflow.
- Preserve the original user intent when you hand off.
- Mention that `context loading is now part of the default analytics entrypoint` when that context matters.

## Handoff

When `knowledge-bootstrap` is invoked, continue with `ask-question` and carry over:
- the business question
- active dataset or source context
- any requested output such as metrics, charts, or a deck
