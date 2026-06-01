---
name: content-research
description: Ingest URLs, documents, repositories, or mixed source material into structured research notes and synthesis. Use when the user wants to research content, collect source notes, build a second brain, or analyze multiple sources before strategy work.
---

# Content Research

This is the Codex-native version of the content research pipeline.

## Workflow

1. Parse the input sources.
2. Classify each source:
   - video
   - LinkedIn or social post
   - GitHub repo or file
   - web page
   - local document
3. Ingest each source with the most reliable available tool:
   - web access or `curl` for URLs
   - `gh` for GitHub metadata when useful
   - direct file reads for local documents
4. Create one structured markdown note per source.
5. Produce a cross-source synthesis.
6. If the user wants relationships or graph output, run `graphify` on the note directory when available.

## Suggested note structure

```markdown
---
title: <source title>
source: <url or path>
source_type: <type>
date_captured: <YYYY-MM-DD>
tags: [research]
---

# <title>

## TL;DR

## Key claims

## Evidence and quotes

## Risks or uncertainties

## Why it matters
```

## Outputs

- `research-notes/<slug>.md` per source
- `research-notes/INDEX.md` source register
- `research-synthesis.md`

## Rules

- Keep raw excerpts separate from your synthesis.
- Do not invent engagement metrics, pricing, or author claims.
- Flag uncertainty explicitly when data is partial or scraped indirectly.
- Prefer a reusable notes directory over one-off chat summaries.
