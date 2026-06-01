# Recommended Vault Layout

Use this reference when `obsidian-vault-manager` is active.

## Directory structure

```text
vault/
├── .obsidian/
├── _index/
├── _templates/
├── attachments/
├── archive/
├── daily/
├── evergreen/
├── projects/
├── research/
└── sources/
```

## What each directory is for

- `_index/` — maps of content, indexes, and entry points
- `_templates/` — note templates
- `attachments/` — images and binary assets
- `archive/` — old material that should stay searchable
- `daily/` — daily capture notes
- `evergreen/` — distilled reusable ideas
- `projects/` — project-specific work
- `research/` — synthesis docs and briefs
- `sources/` — raw source notes

## Git-safe defaults

Track:
- markdown notes
- templates
- index files
- minimal `.obsidian/` config only when useful

Ignore:
- `.obsidian/workspace.json`
- `.obsidian/workspaces.json`
- plugin-local state such as `data.json`
- trash or cache folders
