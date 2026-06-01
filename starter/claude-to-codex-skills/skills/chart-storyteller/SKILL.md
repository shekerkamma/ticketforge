---
name: chart-storyteller
description: Turn data findings into clear chart recommendations and narrative annotations. Use when the user wants to decide what chart to use, how to explain a chart, or how to present quantitative findings clearly.
---

# Chart Storyteller

Help the user choose and explain charts that match the analytical question.

## Workflow

1. Identify the analytical task:
   - comparison
   - trend
   - composition
   - distribution
   - relationship
   - ranking
2. Recommend the most appropriate chart type and explain why.
3. Provide:
   - title
   - takeaway sentence
   - axis or encoding guidance
   - annotation ideas
   - common failure modes
4. If the user already has a chart, critique it and propose a stronger version.

## Output structure

```markdown
# Chart Recommendation

## Best Chart Type

## Why This Fits

## Narrative Takeaway

## Encoding Guidance

## Annotation Plan

## Common Mistakes To Avoid
```

## Rules

- Match the chart to the question, not to aesthetic preference.
- Prefer simpler charts when they communicate the same point.
- If the data does not support a chart confidently, say what is missing.
