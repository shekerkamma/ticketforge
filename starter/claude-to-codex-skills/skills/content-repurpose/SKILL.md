---
name: content-repurpose
description: Turn one source asset into multiple platform-specific content outputs. Use when the user wants a video, article, transcript, notes, or source document repurposed into hooks, posts, captions, outlines, or a content calendar.
---

# Content Repurpose

This is a Codex-native content repurposing chain skill.

## Companion skills

- `watch` for video sources
- `content-research` for URL or document ingestion
- `presentation` when the source should become a talk or deck

## Workflow

1. Capture the source asset and target platforms.
2. Ingest the source:
   - video -> `watch`
   - article, URL, doc -> `content-research`
3. Extract:
   - core thesis
   - 3-7 atomic ideas
   - strongest quotes or hooks
   - reusable proof points
4. Generate platform-specific outputs such as:
   - short hooks
   - LinkedIn posts
   - X threads
   - email outline
   - captions
   - content calendar
5. Keep one source-of-truth note that shows which outputs came from which idea.

## Outputs

- `content-repurpose/<slug>-source.md`
- `content-repurpose/<slug>-idea-map.md`
- `content-repurpose/<slug>-outputs.md`

## Rules

- Do not invent claims that are not in the source.
- Keep platform variations faithful to the same core idea set.
- Separate extraction from rewriting so the lineage is visible.
