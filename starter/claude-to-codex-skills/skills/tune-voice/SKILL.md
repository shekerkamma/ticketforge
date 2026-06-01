---
name: tune-voice
description: Analyze accumulated content performance and propose concrete updates to the content strategy or voice profile based on what is actually working. Use when the user asks what is performing, how to improve the voice, or what patterns to post more of after enough performance data has been logged.
---

# Tune Voice

This is a Codex-native chain skill for turning performance history into strategy changes.

## Workflow

1. Read the performance log first.
2. If available, also read the current voice profile or recent review patterns.
3. Analyze by:
   - platform
   - format
   - hook style
   - topic
   - expectation hits vs misses
4. Produce:
   - what is working
   - what is not
   - the highest-leverage next bet
   - suggested voice-profile updates
5. Offer concrete updates before rewriting any standing voice profile.

## Output structure

```markdown
# Performance Insights

## What's Working
...

## What's Not
...

## Highest-Leverage Bet
...

## Suggested Voice Updates
...
```

## Rules

- Prefer non-obvious, actionable patterns over shallow summaries.
- If the data set is small, say so explicitly and lower confidence.
- Do not force a confident recommendation if the evidence is mixed.
- Separate analysis from profile edits; show proposed changes before applying them.
