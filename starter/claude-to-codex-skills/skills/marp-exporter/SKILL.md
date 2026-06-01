---
name: marp-exporter
description: Lint and export a `.marp.md` deck to HTML or PDF using the vendored Marp helper scripts and bundled themes. Use when the user wants to preview, share, print, or validate a Marp deck after authoring it.
---

# Marp Exporter

Use this skill after a `.marp.md` deck already exists.

## Bundled tools

- `scripts/marp_linter.py`
- `scripts/marp_export.py`
- bundled theme CSS under `assets/themes/`

## Workflow

1. Lint the deck first:

```bash
python3 "$CODEX_HOME/skills/marp-exporter/scripts/marp_linter.py" <deck.marp.md>
```

2. If Marp CLI is unavailable, stop and use `install-marp`.
3. Export to HTML and/or PDF:

```bash
python3 "$CODEX_HOME/skills/marp-exporter/scripts/marp_export.py" <deck.marp.md> analytics both
```

4. If the user needs PPTX and Marp CLI is installed, use direct Marp CLI:

```bash
marp <deck.marp.md> -o <deck.pptx>
```

## Rules

- Lint before export whenever the deck changed materially.
- Treat the `.marp.md` file as the source of truth; exports are generated artifacts.
- If export fails, surface the exact Marp or theme error instead of guessing.
- Use the bundled themes unless the deck already ships with its own `themes/` directory.
