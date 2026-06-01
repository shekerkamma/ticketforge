---
name: slide-deck-builder
description: Build a presentation or self-contained HTML slide deck using Sheker's enterprise style: dark navy, teal accents, widescreen layout, and visual-first slides. Use when the user asks for a slide deck, presentation, HTML deck, or visual narrative from a topic, memo, or research pack.
---

# Slide Deck Builder

This is a Codex-native chain skill for turning a topic or document into a deck source.

## Brand defaults

- widescreen layout
- dark navy base
- teal accent system
- enterprise tone
- visual-first slides, not bullet dumps

## Workflow

1. Identify the input shape:
   - topic only
   - memo or proposal
   - research pack
   - existing carousel or notes
2. Choose the supporting path:
   - `presentation` for core deck structure
   - `presentation-theme` for consistent visual direction
   - `chart-storyteller` for metric slides
   - `architecture-to-everything` for system or workflow slides
   - `carousel-to-deck` if the source is already in carousel form
3. Build the deck with:
   - title / setup
   - core content
   - evidence
   - takeaway / next steps
4. If the environment supports export, use the appropriate exporter. Otherwise produce the clean HTML or markdown-backed deck source.

## Rules

- One idea per slide.
- Every slide needs a visual treatment or strong structural reason not to have one.
- Prefer 5 to 12 slides unless the user explicitly wants a larger deck.
- Keep speaker-support copy tight; do not write essays on slides.
- If you cannot generate a real `.pptx`, say so and provide the best deck source available.
