# Note Types

Use this reference when `second-brain-capture` is active.

## Folder mapping

- `sources/` — direct captures from URLs, videos, repos, or articles
- `evergreen/` — distilled ideas that should stay useful over time
- `projects/` — notes tied to one product, client, repo, or initiative
- `meetings/` — meeting summaries and decisions
- `daily/` — daily logs and inbox-style captures

## Frontmatter baseline

```yaml
---
title: <human title>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [tag-one, tag-two]
source: <url-or-path-when-relevant>
source_type: <video|github|web|meeting|internal>
status: active
---
```

## Source note structure

```markdown
# <Title>

## TL;DR

## Key claims or facts

## Evidence or excerpts

## Why it matters

## Related notes

## Open questions
```

## Evergreen note structure

```markdown
# <Idea>

## Claim

## Why it matters

## Supporting evidence

## Counterpoints or limits

## Related notes
```

## Meeting note structure

```markdown
# <Meeting title>

## Context

## Decisions

## Action items

## Risks or blockers
```
