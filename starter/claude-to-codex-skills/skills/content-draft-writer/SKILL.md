---
name: content-draft-writer
description: Draft a single LinkedIn post, essay, or channel-specific content piece from a selected topic while applying voice and anti-slop checks before handoff. Use when the user asks to draft the next post, write from a queued topic, or turn a ranked content idea into a review-ready draft.
---

# Content Draft Writer

This is a Codex-native chain skill for taking one topic from queue to review-ready draft.

## Inputs

Best inputs:

- a specific topic
- channel target such as LinkedIn or Substack
- source outlier patterns or notes
- any voice or style constraints already in use

## Workflow

1. Select one topic only.
2. Pull the minimum useful context:
   - topic title and angle
   - source inspiration or research notes
   - channel constraints
3. Draft for the selected channel.
4. Run the result through:
   - `anti-slop` for generic-AI cleanup
   - `review-draft` for voice alignment and rewrite if needed
5. Return a clean draft plus any unresolved review flags.

## Output structure

```markdown
# Draft Package — <topic>

## Channel
...

## Draft
...

## Review Notes
- ...
```

## Rules

- Draft one asset per invocation.
- Keep the draft specific to the topic's real angle, not to a generic niche.
- If channel constraints are missing, call that out instead of guessing silently.
- If the piece still fails voice review after one rewrite pass, surface the remaining issues explicitly.
