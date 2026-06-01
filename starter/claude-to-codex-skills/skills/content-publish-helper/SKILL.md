---
name: content-publish-helper
description: Prepare an approved content draft for manual publishing, including final checklist, formatting cleanup, and status handoff. Use when the user wants to ship the next approved post, prep a draft for publishing, or bridge the last step between review and manual post.
---

# Content Publish Helper

This is a Codex-native chain skill for the human-gated publishing step.

## Workflow

1. Confirm the asset is approved and channel-ready.
2. Run a final preflight:
   - title or opening line
   - body formatting
   - link placement
   - CTA
   - obvious copy errors
3. Produce a publish packet:
   - final copy
   - channel-specific checklist
   - any manual actions still required
4. Stop at the handoff. Do not pretend to auto-publish unless the environment actually includes a real posting path and the user explicitly wants it.

## Output structure

```markdown
# Publish Packet — <title>

## Final Copy
...

## Channel Checklist
- ...

## Manual Handoff
- ...
```

## Rules

- Treat publishing as a human-controlled step by default.
- If the workflow depends on browser or platform login state, say so directly.
- Never mark something as published unless the user confirms it actually shipped.
