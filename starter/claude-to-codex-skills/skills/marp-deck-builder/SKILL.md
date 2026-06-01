---
name: marp-deck-builder
description: Create or update a `.marp.md` presentation deck from a memo, research pack, topic outline, or existing deck notes. Use when the user asks for a Marp deck, markdown slide deck, or wants slides in Marp format instead of HTML-only presentation output.
---

# Marp Deck Builder

This is the Marp-specific deck-authoring skill.

Read these references before writing the deck:

- `references/deck_skeleton.marp.md`
- `references/marp_components.md`

## Workflow

1. Confirm the source material:
   - topic only
   - memo
   - research pack
   - proposal or architecture brief
2. Build the deck as `.marp.md`, not plain markdown.
3. Use the skeleton and component guidance to ensure:
   - valid Marp frontmatter
   - explicit slide boundaries
   - one job per slide
   - HTML component usage where it improves the deck
4. If the content needs narrative shaping first, use `presentation` or `presentation-content-writer`, then convert the result into Marp.
5. If the user wants rendered outputs, hand the finished deck to `marp-exporter`.

## Rules

- Keep the output in `.marp.md` form.
- Do not mix generic markdown notes with a deck source file.
- If the deck is data-heavy, prefer componentized slides and explicit takeaway slides.
- If the environment cannot render Marp yet, still produce a valid `.marp.md` source.
