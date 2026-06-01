---
name: content-topic-queue
description: Generate a ranked queue of concrete content topics by combining fresh outlier patterns with the user's active workstreams and point of view. Use when the user asks what to write next, wants a topic backlog, or needs ideas separated by channel such as LinkedIn, Substack, or deck format.
---

# Content Topic Queue

This is a Codex-native chain skill for turning research and expertise into a writeable backlog.

## Inputs

Best inputs:

- a recent outlier research pack
- the user's active workstreams
- preferred channels such as LinkedIn, Substack, or deck

## Workflow

1. Read the latest outlier patterns first. If none exist, suggest running `content-outlier-research`.
2. Read the user's active themes, current projects, and strong opinions.
3. Cross the two:
   - what is working externally
   - what the user can credibly say from lived work
4. Generate candidate topics with:
   - title
   - angle
   - suggested channel
   - why now
   - source inspiration
5. Rank the queue by usefulness, specificity, and freshness.
6. If the user wants drafts immediately, pass the top topics into `content-repurpose` or a direct drafting step and run `anti-slop` on the result.

## Output structure

```markdown
# Content Topic Queue — <date>

## Top Topics

### 1. <title>
- Channel: ...
- Angle: ...
- Why now: ...
- Inspired by: ...

## Reserve Topics
- ...
```

## Rules

- Every topic should tie back to a real workstream, operator insight, or concrete case.
- Do not produce interchangeable "AI trends" topics.
- Make the channel recommendation explicit.
- Kill weak ideas instead of padding the queue.
