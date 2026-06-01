---
name: presentation-content-writer
description: Generate slide content from a topic or outline. Transforms ideas, bullet points, or rough notes into structured slide content with titles, key points, and examples. Use when the user wants to create new slides from scratch or flesh out an outline.
---

# Presentation Content Writer Skill

Generates slide content from topics, outlines, or rough notes. Focuses on **what to say**, not how to format it.

## Workflow

### Step 1: Understand the Request

Determine what the user needs:
- **Topic only** — "create slides about X" → research and generate full content
- **Outline** — bullet points or structure → flesh out into slide content
- **Rough notes** — raw ideas → organize into a narrative arc
- **Single slide** — "add a slide about Y after slide N" → generate one slide's content

### Step 2: Research (if needed)

If the topic requires current data or specific facts:
- Use WebSearch to gather key statistics, quotes, and examples
- Use WebFetch to pull specific sources
- Cite sources in speaker notes, not on slides

### Step 3: Generate Content Structure

For each slide, produce:

```markdown
## Slide N: [Title]
**Type**: content | section-divider | comparison | code-example | list | quote

### Key Message
[One sentence — the single takeaway for this slide]

### Content
[Bullet points, comparison columns, code snippets, or narrative text]

### Speaker Notes
[What to say when presenting this slide — 2-4 sentences]

### Transition
[How this slide connects to the next one]
```

### Step 4: Apply Content Principles

Follow these presentation content rules:

1. **One idea per slide** — if you need "and" in the title, split into two slides
2. **6-word titles** — titles should be statements, not topics ("Data Governance Drives AI Success" not "Data Governance")
3. **Rule of three** — group content into 3 points, 3 examples, 3 steps
4. **Concrete over abstract** — use specific numbers, names, and examples
5. **Progressive disclosure** — each slide should build on the previous one
6. **Contrast drives clarity** — use before/after, good/bad, old/new comparisons
7. **End with action** — final slide should tell the audience what to do next

### Step 5: Determine Slide Types

Match content to the best slide pattern:

| Content Type | Slide Pattern | When to Use |
|---|---|---|
| New section intro | Section divider | Starting a new topic area |
| Before/after comparison | Two-column (good/bad) | Showing transformation or contrast |
| Technical concept | Code block + explanation | Teaching syntax or configuration |
| Feature list | Icon list | Showing capabilities or options |
| Key concept | Trigger box | Highlighting important ideas |
| Warning or caveat | Warning box | Calling out risks or gotchas |
| Statistic or quote | Large centered text | Making a single point memorable |

### Step 6: Output

Deliver content in one of two formats based on the user's needs:

**Content-only** (default): Markdown document with slide content, ready for the user or `presentation-curator` to convert to HTML.

**HTML-ready**: If the user wants slides added directly, provide the HTML using the presentation's CSS classes. Delegate to the `presentation-curator` agent for actual insertion.

## Content Templates

### Opening Slide (Hook)
- Start with a surprising statistic or provocative question
- Make the audience feel the problem before offering the solution
- Example: "54% of C-suite executives say AI adoption is tearing their company apart"

### Teaching Slide (Concept)
- Title states the takeaway
- 3 bullet points max
- One concrete example or code snippet
- Speaker note explains the "why"

### Comparison Slide (Before/After)
- Left column: the problem state (red/bad styling)
- Right column: the solution state (green/good styling)
- Title frames the transformation

### Closing Slide (Call to Action)
- Summarize in 3 points
- Give one specific next step
- End with a memorable statement or callback to the opening hook
