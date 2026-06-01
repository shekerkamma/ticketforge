---
name: content-outlier-research
description: Research high-performing posts, essays, videos, and discussions in a target niche, then extract the hook, structure, angle, and likely reason each one worked. Use when the user asks what is working now, wants outlier content research, or needs pattern mining before creating new content.
---

# Content Outlier Research

This is a Codex-native chain skill for turning raw content examples into reusable pattern notes.

## Workflow

1. Confirm the niche, window, and source mix.
   Default to recent enterprise-AI, automotive-AI, and agentic-systems content if the user does not specify.
2. Gather candidates with `content-research`, `watch`, and `url-dossier` as needed.
3. Rank candidates by practical outlier value:
   - visible engagement or reach
   - freshness
   - relevance to the user's actual work
   - clarity of the pattern
4. For the top items, extract:
   - hook
   - structure
   - angle
   - likely reason it worked
   - what is reusable vs. what is unique to that creator
5. If the user keeps durable research notes, save the result through `second-brain-capture`.

## Output structure

```markdown
# Content Outlier Research — <topic> — <date>

## Top Outliers

### 1. <title>
- Source: ...
- URL: ...
- Why it matters: ...
- Hook: ...
- Structure: ...
- Angle: ...
- Reusable pattern: ...

## Pattern Summary
- ...

## Best Next Moves
- ...
```

## Rules

- Favor actionable patterns over vanity metrics.
- Separate observed facts from your hypothesis about why something worked.
- Avoid generic advice like "be authentic" or "tell stories."
- If engagement data is partial or inferred, say so.
