---
name: presentation-speaker-notes
description: Manage speaker notes for presentation slides. Generate, edit, export, or import notes per slide. Use when the user wants to prepare talking points, rehearsal notes, or presenter scripts for their slides.
---

# Presentation Speaker Notes Skill

Manages speaker notes for HTML presentations — generate, edit, export, and sync.

## Storage Format

Speaker notes are stored in a companion file alongside the presentation:

```
presentation/
├── index.html              # The slides
└── speaker-notes.json      # The notes
```

### speaker-notes.json Structure

```json
{
  "meta": {
    "presentation": "presentation/index.html",
    "totalSlides": 46,
    "lastUpdated": "2026-05-10T12:00:00Z"
  },
  "notes": {
    "1": {
      "title": "Vibe Coding to Agentic Engineering",
      "duration": "30s",
      "notes": "Welcome everyone. Today we'll walk through the journey from unstructured AI coding to a fully configured agentic engineering system.",
      "keyPoints": ["Set the narrative arc", "Establish the destination"],
      "transition": "Let's start by looking at what we're building toward."
    },
    "2": {
      "title": "Example Project: TodoApp",
      "duration": "1m",
      "notes": "This is our running example throughout the presentation...",
      "keyPoints": ["Before/after comparison", "Why TodoApp works as an example"],
      "transition": "Now that you've seen the destination, let's define where most people start."
    }
  }
}
```

## Workflows

### Generate Notes for All Slides

1. Read the presentation HTML
2. For each slide, extract:
   - Slide number and title (`<h1>` text)
   - Slide type (section-divider, content, comparison, code)
   - Key content (bullet points, code examples, comparisons)
3. Generate appropriate notes based on slide type:

| Slide Type | Notes Style |
|---|---|
| Title slide | Opening hook, set expectations |
| Section divider | Transition statement, preview what's coming |
| Content slide | Explain the key concept, give an anecdote or example |
| Comparison slide | Walk through the before, then the after, highlight the contrast |
| Code example | Explain what the code does, why each line matters |
| List slide | Hit each point briefly, expand on the most important one |

4. Estimate duration per slide (default: 1 minute for content, 30s for transitions)
5. Write to `speaker-notes.json`

### Generate Notes for Specific Slides

Same as above but only for the requested slide numbers. Preserve existing notes for other slides.

### Edit Notes

Update the notes for a specific slide in `speaker-notes.json`. Preserve all other fields.

### Export Notes

Export notes to readable formats:

#### Markdown Export (for printing)

```markdown
# Speaker Notes: [Presentation Title]
Total duration: ~45 minutes

---

## Slide 1: Vibe Coding to Agentic Engineering
**Duration:** 30s

Welcome everyone. Today we'll walk through...

**Key Points:**
- Set the narrative arc
- Establish the destination

**Transition:** Let's start by looking at what we're building toward.

---

## Slide 2: Example Project: TodoApp
...
```

Write to `exports/speaker-notes.md`.

#### Teleprompter Export (minimal, large text)

```markdown
# SLIDE 1

Welcome everyone.

Today we walk through the journey from vibe coding to agentic engineering.

> NEXT: Example Project

---

# SLIDE 2
...
```

Write to `exports/teleprompter.md`.

#### Timeline Export (duration overview)

```markdown
| Slide | Title | Duration | Cumulative |
|-------|-------|----------|------------|
| 1 | Vibe Coding to Agentic Engineering | 0:30 | 0:30 |
| 2 | Example Project: TodoApp | 1:00 | 1:30 |
| 3 | What is Vibe Coding? | 1:30 | 3:00 |
```

Write to `exports/timeline.md`.

### Import Notes

Import notes from a markdown file or paste. Parse the structure and update `speaker-notes.json`.

### Sync Notes

After slides are added, removed, or reordered:
1. Read current `speaker-notes.json`
2. Read current presentation HTML
3. Match existing notes to slides by title (handles renumbering)
4. Flag orphaned notes (slide was removed)
5. Flag new slides without notes
6. Update slide numbers and titles
7. Write updated `speaker-notes.json`

## Rehearsal Mode

Generate a rehearsal script that combines slides and notes:

```markdown
# Rehearsal Script
Target time: 45 minutes

## [0:00] Slide 1 — Vibe Coding to Agentic Engineering

[SHOW SLIDE]

"Welcome everyone. Today we'll walk through the journey..."

Key points to hit:
- Set the narrative arc
- Establish the destination

[TRANSITION] "Let's start by looking at what we're building toward."

[ADVANCE TO SLIDE 2]

## [0:30] Slide 2 — Example Project: TodoApp
...
```

Write to `exports/rehearsal-script.md`.

## Rules

- Never modify the presentation HTML — notes live in the companion JSON file
- Preserve existing notes when generating for new slides
- Keep notes conversational — written as spoken word, not bullet points
- Estimate 1 minute per content slide, 30 seconds per transition/divider slide
- Total presentation time should be reported after any notes operation
