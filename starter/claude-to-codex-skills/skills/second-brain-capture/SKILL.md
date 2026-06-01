---
name: second-brain-capture
description: Capture research, meeting notes, findings, or source material into durable markdown notes for a second brain or Obsidian vault. Use when the user asks to save knowledge, create evergreen notes, turn sources into reusable notes, or persist findings beyond the chat.
---

# Second Brain Capture

Turn raw material into durable notes that can survive across sessions, repos, and tools.

Read `references/note-types.md` before choosing the note structure.

## Workflow

1. Choose the storage root.
   - Prefer an explicit path from the user.
   - Otherwise prefer, in order: `second-brain/`, `vault/`, `notes/`, `knowledge/`.
   - If none exists and the user wants a full vault, use `obsidian-vault-manager`.
2. Pick the note type:
   - source note
   - evergreen note
   - project note
   - meeting note
   - daily note
3. Create a slugged markdown file in the appropriate subdirectory.
4. Add frontmatter with at least:
   - `title`
   - `created`
   - `updated`
   - `tags`
   - `source` when applicable
   - `source_type` when applicable
5. Write the note with clear separation between:
   - facts or excerpts
   - synthesis
   - open questions
   - next actions
6. Add wikilinks to related notes when an Obsidian-style vault is in use.
7. Update one lightweight index or MOC so the note is discoverable.
8. If the user wants graph-style retrieval, run `graphify` on the note root.

## Default outputs

- `second-brain/sources/<slug>.md`
- `second-brain/evergreen/<slug>.md`
- `second-brain/projects/<slug>.md`
- `second-brain/meetings/<slug>.md`
- `second-brain/daily/YYYY-MM-DD.md`

Adjust the root when the repo already uses `vault/`, `notes/`, or another explicit notes directory.

## Rules

- Do not hide the original source; keep links and attribution.
- Prefer small, reusable notes over giant transcript dumps.
- Use markdown and frontmatter rather than app-specific formats.
- If the notes are meant for Obsidian, prefer wikilinks over standard relative markdown links.
- If the note should become presentation, strategy, or research input later, make the takeaway section explicit.
