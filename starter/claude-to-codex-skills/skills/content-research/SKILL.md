---
name: content-research
description: Ingest URLs, videos, documents, or repositories into structured research notes, then optionally persist them into a second brain or Obsidian vault backed by GitHub. Use when the user wants content research, source notes, durable knowledge capture, or multi-source synthesis.
---

# Content Research

This is the Codex-native research ingestion chain.

## Companion skills

- `watch` for video URLs or local video files
- `url-dossier` for one-off link analysis
- `second-brain-capture` when the notes should become durable knowledge assets
- `obsidian-vault-manager` when the user wants the research stored in an Obsidian vault
- `obsidian-github-sync` when the vault or notes should live in GitHub
- `graphify` for relationship mapping

## Workflow

1. Parse the sources and classify them:
   - video
   - GitHub repo or file
   - web page or article
   - local document
2. Ingest each source with the most reliable available method:
   - `watch` for video
   - `gh` plus file inspection for GitHub
   - web access or `curl` for web pages
   - direct file reads for local documents
3. Write one structured markdown note per source.
4. Produce a cross-source synthesis.
5. If the user wants durable storage:
   - use `second-brain-capture` to convert source notes into long-lived notes
   - use `obsidian-vault-manager` if an Obsidian vault is needed or missing
   - use `obsidian-github-sync` if the vault or note set should sync through GitHub
6. If the user wants relationships or graph output, run `graphify` on the note directory.

## Outputs

- `research-notes/<slug>.md` per source
- `research-notes/INDEX.md`
- `research-synthesis.md`
- optional second-brain or vault note paths when the chain continues

## Rules

- Keep raw excerpts separate from synthesis.
- Preserve source URLs and source types in frontmatter.
- If the user asks for a second brain, prefer durable markdown notes over chat-only summaries.
- If the user asks for Obsidian storage, use wikilinks and note-friendly frontmatter.
- If the user asks for GitHub-backed storage, keep the note set plain-text and repo-friendly.
