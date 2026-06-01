---
name: carousel-to-deck
description: Turn carousel copy into a usable slide deck or presentation file plan. Use when the user has carousel text and wants it converted into slides, a deck outline, or a presentation artifact they can present or hand off.
---

# Carousel To Deck

Convert social-carousel content into a real presentation structure.

## Companion skills

- `presentation`
- `presentation-content-writer`
- `presentation-speaker-notes`
- `presentation-exporter`

## Workflow

1. Read the carousel source:
   - pasted copy
   - markdown file
   - repurposed content file
2. Parse each slide's:
   - number
   - headline
   - body copy
   - design direction, if present
3. Map the slides into presentation roles:
   - cover
   - content slides
   - close / CTA
4. Build a slide outline or HTML deck through the `presentation` workflow.
5. Put design-direction notes into speaker notes or production notes instead of audience-facing body text.
6. If the environment supports deck export, use `presentation-exporter`; otherwise leave a clean deck source plus notes.

## Rules

- Keep slide headlines sharp; do not bury them in paragraph text.
- Vary the slide rhythm; do not make every slide structurally identical.
- Treat design-direction text as production guidance, not visible copy.
- If the user wants an actual `.pptx`, say whether the environment has a real export path instead of pretending.
