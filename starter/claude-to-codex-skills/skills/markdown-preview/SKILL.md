---
name: markdown-preview
description: Render a markdown file to a quick local HTML preview, with Marp-aware handling for `.marp.md` decks when possible. Use when the user wants to preview markdown, inspect a README or note in the browser, or quickly render markdown without a full publishing flow.
---

# Markdown Preview

Use this skill for quick local previews of markdown files.

## Workflow

1. Identify the target markdown file.
2. If the file is a `.marp.md` deck and Marp is available, prefer a Marp HTML render.
3. Otherwise render a lightweight HTML preview with the bundled script:

```bash
python3 "$CODEX_HOME/skills/markdown-preview/scripts/render_markdown_preview.py" <input.md>
```

4. The script prints the output HTML path. If the user wants a live local server, rerun with:

```bash
python3 "$CODEX_HOME/skills/markdown-preview/scripts/render_markdown_preview.py" <input.md> --serve
```

## Rules

- Prefer preview generation over editing the original markdown.
- If markdown parser libraries are missing, the script falls back to a plain-text HTML wrapper instead of failing.
- For Marp decks, keep `.marp.md` as the source and treat preview HTML as disposable output.
