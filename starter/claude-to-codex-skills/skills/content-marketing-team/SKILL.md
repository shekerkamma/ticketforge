---
name: content-marketing-team
description: Coordinate a text-first content workflow across research, topic generation, drafting, review, and weekly reporting. Use when the user asks to run a content cycle, decide what to publish next, or orchestrate a repeatable content pipeline instead of a one-off post.
---

# Content Marketing Team

This is the Codex-native parent chain for the content workflow.

## Modes

- `full`
- `research-only`
- `topic-only`
- `draft-only`
- `report-only`

Default to `full`.

## Workflow

1. Read the current state:
   - recent outlier research
   - current topic queue
   - drafts in progress
   - published work this week
2. Route work by need:
   - low research coverage -> `content-outlier-research`
   - weak backlog -> `content-topic-queue`
   - strong topic ready to write -> direct drafting plus `anti-slop`
   - existing source asset that needs channel variants -> `content-repurpose`
   - end-of-week review -> `content-weekly-report`
3. Return a concise operating summary:
   - what ran
   - what is queued
   - what is blocked on human review
   - what the next best content action is

## Output structure

```markdown
# Content Team Cycle — <date>

## Ran
- ...

## Queue Health
- ...

## Blockers
- ...

## Next Best Action
- ...
```

## Rules

- Do not pile up more drafts if the review queue is already backed up.
- Prefer steady throughput over idea-hoarding.
- Be explicit about the mode and what was skipped because of it.
- If the user lacks any system of record, work from provided notes and say so directly.
