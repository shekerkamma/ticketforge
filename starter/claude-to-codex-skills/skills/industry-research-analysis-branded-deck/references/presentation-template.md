# Presentation Template System

This skill has a specific visual system. Do not treat deck styling as open-ended.

## Primary reference assets

- PowerPoint reference deck:
  - `assets/Prasad_Agentic_AI_Use_Cases_Across_Industries.pptx`
- Visual reference PDF:
  - `assets/slide deck-reference.pdf`

Use these as the first reference for:

- color system
- type scale
- cover and divider tone
- density level
- spacing and card treatment

These binaries are checked into the repo as part of the skill so the template system travels with the workflow.

## Repo implementation references

- Canva-adapted use-case layout:
  - `scripts/build_yc_usecase_deck.py`
- Generic branded renderer:
  - `scripts/build_industry_branded_pptx.py`
- Healthcare custom builder:
  - `scripts/build_healthcare_provider_ops_branded_pptx.py`
- Template manifest:
  - `references/template-manifest.json`
- Builder registry:
  - `references/builder-registry.json`

## Brand system

Match the established palette already used in the repo:

- navy: `#0A1628`
- teal: `#00C9A7`
- accent: `#009B82`
- gold: `#FFB800`
- font: `Calibri`

## Use-case layout rule

For workflow-heavy or prioritization-heavy use-case sections, prefer the Canva-adapted pattern already proven in `build_yc_usecase_deck.py`:

- teal left panel
- navy right strip
- gold accent rule
- white cards for:
  - current state / challenge
  - how it is realized / what to sell
  - executive logic
  - implication / action checks

Use this layout when the goal is to show:

- why the use case matters
- how it works in the workflow
- what an executive should fund or do

Do not use a plain table if the slide is really a prioritization or realization slide.

## Slide-family guidance

- `hero`
  - strong cover, minimal clutter, one thesis
- `agenda`
  - clean numbered progression
- `section-divider`
  - reset the story, do not overload
- `summary-cards`
  - 3-4 conclusions only
- `kpi-grid`
  - keep metrics big and sparse
- `bar-chart` / `comparison`
  - use when ranking or contrasting matters
- `use-case cards`
  - use for landscape or prioritization
- `case-study`
  - use for named customer, named use case, or executive-action deep dives
- `roadmap`
  - sequence actions clearly

## Minimum expectation

The template is part of the skill.

That means:

- the deck should visibly resemble the reference system
- use-case slides should use the Canva-style layout language
- layout choice should vary with content, not repeat one generic structure
- render should produce a QA preview bundle so overflow and density issues are visible before handoff
