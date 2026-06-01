---
name: url-dossier
description: Turn any URL into a structured dossier. Use when the user wants a link analyzed, summarized, turned into notes, or classified by source type. Supports web pages, GitHub URLs, and video URLs by chaining to the right workflow.
---

# URL Dossier

This is a Codex-native chain skill for "analyze this link" requests.

## Companion skills

- `watch` for video URLs or local video files
- `content-research` for multi-source research
- `graphify` when the user wants relationship mapping

## Workflow

1. Parse the URL or list of URLs.
2. Classify each source:
   - video URL or local video file
   - GitHub repo or file URL
   - generic web page
   - document URL
3. Route by type:
   - video: use `watch`
   - GitHub: use `gh` plus direct file reads when useful
   - web/document: use web access or `curl`
4. Produce a structured dossier for each source.
5. If there are multiple sources, add a cross-source synthesis.

## Suggested dossier format

```markdown
# URL Dossier — <title>

## Source
- URL:
- Type:
- Captured:

## TL;DR

## Key claims or contents

## Evidence

## Risks, gaps, or uncertainty

## Why it matters
```

## Output paths

- `url-dossiers/<slug>.md`
- optional `url-dossiers/INDEX.md`

## Rules

- Prefer the narrowest tool that fits the source.
- Keep raw evidence separate from your interpretation.
- If the source is a video, rely on frame and transcript evidence instead of title-only summaries.
- If the source is GitHub, capture repo metadata and key files, not just the README headline.
