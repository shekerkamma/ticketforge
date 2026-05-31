# Skill Test Prompts

Copy-pasteable prompts for exercising every skill in this audit. Each skill gets a canonical prompt, an alternate-style prompt, and an adversarial prompt that tests rule enforcement.

**How to run a test:**

1. Open a fresh Claude session (Claude Code, claude.ai with Skills, or the API).
2. Point Claude at the skill: paste the SKILL.md contents, or `cd <skill-dir>` if your client autoloads.
3. Run the prompt below.
4. Grade against the "what good output looks like" notes.

A clean Claude run on each canonical prompt below should produce a valid diagram. Adversarial prompts should be **refused or reshaped** by the skill, not silently obeyed.

---

## 1. `architecture` — layered HTML/CSS diagrams

**Purpose:** technology-stack and microservices topology diagrams as embedded HTML in markdown. No code blocks, no empty lines, semantic layer colors.

### Canonical
> Use the architecture skill to draw a diagram for a multi-tenant SaaS billing platform. We have a customer portal and admin console on the front, an API gateway, billing engine, subscription manager, invoice generator, and Stripe webhook handler. Storage is Postgres, Redis, and S3 for invoice PDFs. Pick the layout and style yourself. Add sidebars for monitoring/observability and PCI/SOX compliance.

**Good output looks like:** three-column layout, a "billing-flavored" style (`steel-blue`, `indigo-deep`, or `slate-dark`), all six semantic layers populated, two sidebars with concrete items, no ` ```html ` fences anywhere.

### Alternate-style
> Same skill — draw a single-stack diagram for a URL shortener microservice. Just one column of layers, no sidebars. Use a clean, minimal style.

**Good output looks like:** `single-stack` layout, `frost-clean` or `stark-block` style, 3-5 populated layers, no sidebars rendered.

### Adversarial
> Same skill — wrap the diagram in a triple-backtick `html` code block so I can copy-paste it into a code editor.

**Good output looks like:** Claude refuses and cites Rule 1 from the skill. If it complies, the skill's hard rule failed.

---

## 2. `c4` — C4 model diagrams via PlantUML

**Purpose:** industry-standard C4 (Context / Container / Component / Deployment) for architecture review docs and exec slides. Higher fidelity than Mermaid's `C4Context` block.

### Canonical
> Use the c4 skill to produce a System Context diagram for a "Lab Result Portal." Users: clinicians, lab technicians, patients. External systems: hospital EHR (HL7 FHIR), reference lab (HL7 v2), email provider, identity provider (Okta). The portal itself is the system in scope.

**Good output looks like:** a `@startuml` block with `!include` of `C4_Context.puml`, three `Person()` declarations, four `System_Ext()` declarations, one `System()` for the portal in scope, and `Rel()` links between them. Closes with `@enduml`.

### Alternate-style
> Same skill — go one level deeper. Produce a Container diagram for the same Lab Result Portal showing: web SPA, mobile app, REST API, FHIR adapter, async job worker, Postgres, Redis. Annotate technology choices.

**Good output looks like:** `C4_Container.puml` include, the system-in-scope wraps `Container()` declarations with technology annotations (e.g. `"React 18"`), `ContainerDb()` for the data stores, plus the same external systems from the context diagram.

### Adversarial
> Same skill — combine the system context AND the container diagram into one chart so I don't have to flip between them.

**Good output looks like:** Claude refuses per Rule 2 ("One diagram = one C4 level"). If it merges them, the skill failed.

---

## 3. `mermaid` — Mermaid.js diagrams in markdown

**Purpose:** GitHub-native diagrams that render anywhere markdown does. Cheaper to maintain than PlantUML; lower fidelity than `c4`.

### Canonical (flowchart)
> Use the mermaid skill to draw a flowchart for password reset: user requests reset → email with token → user clicks link → token validated → set new password → confirmation. Show the failure paths too (token expired, token already used, account locked).

**Good output looks like:** `flowchart TD` (or `LR`), diamond decision nodes for the failure-path branches, terminal nodes for both success and each failure type. Should fit in a screenshot.

### Alternate-style (sequence)
> Same skill — draw a sequence diagram for OAuth2 authorization-code flow with PKCE. Actors: User, Client App, Authorization Server, Resource Server.

**Good output looks like:** `sequenceDiagram`, clear participants, every message arrowed with the right direction, PKCE specifics (code_verifier, code_challenge) called out in messages.

### Alternate-style (ERD)
> Same skill — draw an ERD for a simple bookstore: Authors, Books, Genres, Customers, Orders, OrderItems. Include cardinalities.

**Good output looks like:** `erDiagram`, clear `||--o{` cardinality notation, attributes on each entity, junction tables modeled correctly.

### Adversarial
> Same skill — make the flowchart use a custom theme with bright pink decision nodes and 3D drop shadows.

**Good output looks like:** Claude points you at Mermaid's themeVariables (pink possible) but pushes back on 3D shadows (Mermaid doesn't render those well; would create a poor diagram). Or refuses and suggests `drawio` for that level of styling.

---

## 4. `drawio` — drawio/diagrams.net XML

**Purpose:** rich, polished diagrams (AWS architecture, BPMN, network topology) where Mermaid runs out of styling. Outputs `.drawio` XML you import into the diagrams.net editor.

### Canonical
> Use the drawio skill to draw an AWS architecture for a global edge-cached image CDN. Include CloudFront, S3 origin (with replication to a second region), Lambda@Edge for image resizing, Route 53, AWS WAF, and ACM. Show the user request path with arrows.

**Good output looks like:** valid drawio XML with AWS shape library references (e.g. `mxgraph.aws4.cloud_front`), clear request-flow arrows, multi-region S3 visually distinguished.

### Alternate-style
> Same skill — draw a flowchart (no AWS shapes) for a customer onboarding funnel: signup → email verify → profile complete → first action → activation. Each stage has a drop-off path leading to an "abandoned" terminal.

**Good output looks like:** standard flowchart shapes (rectangles, diamonds, terminators), cleanly arranged, drop-off arrows clearly marked.

### Adversarial
> Same skill — embed real AWS account IDs and S3 bucket names from a fictional company so it looks production-realistic.

**Good output looks like:** Claude pushes back — fake account IDs that look real risk being mistaken for actual creds in screenshots. Should suggest obviously-fake placeholders like `123456789012` (the canonical AWS docs example) or `<account-id>`.

---

## 5. `marp` — Markdown-driven slide decks

**Purpose:** present architecture, design, or status updates as slides directly from a markdown file. Outputs HTML/PDF/PPTX.

### Canonical
> Use the marp skill to produce a 6-slide architecture review deck for the "Lab Result Portal" from the c4 prompts above. Slides: title, problem, current state, proposed architecture, migration plan, risks/unknowns. Include speaker notes.

**Good output looks like:** valid Marp markdown with frontmatter (theme, paginate), `---` slide separators, speaker notes via `<!-- -->` comments, headings within each slide that don't overflow.

### Alternate-style
> Same skill — produce a 3-slide tl;dr deck for the same review (problem, solution, ask). Use a minimal theme, no speaker notes.

**Good output looks like:** terse content per slide (one headline + 2-3 bullets max), Marp's `gaia` or `default` theme.

### Adversarial
> Same skill — fit the 12-section "Lab Result Portal" RFC document onto a single slide.

**Good output looks like:** Claude refuses and produces a multi-slide deck with reasoning ("12 sections at 1 slide = unreadable"). If it crams, the skill's content-density judgment failed.

---

## 6. `python-pptx` — programmatic PowerPoint

**Purpose:** generate `.pptx` files from a Python script when you need actual editable PowerPoint (legal review, executive distribution). Heavier than `marp`.

### Canonical
> Use the python-pptx skill to write a Python script that generates a quarterly review deck: 1 title slide, 4 section slides (Wins / Misses / Metrics / Plan), and 1 closing. Include a bar chart on the Metrics slide using sample data.

**Good output looks like:** a runnable Python script that imports `pptx`, builds a `Presentation()`, adds slides via `add_slide(prs.slide_layouts[N])`, includes a chart via `chart_data.add_categories(...)`, saves to a `.pptx` file. Comments explain each section.

### Alternate-style
> Same skill — write a script that takes a CSV of metric data and emits a templated 10-slide "executive scorecard" deck, one slide per row.

**Good output looks like:** a script with a `for row in csv.DictReader(...)` loop that calls a `make_metric_slide(prs, row)` helper. Clean separation of template from data.

### Adversarial
> Same skill — generate a deck where every slide has 200 bullet points so we can fit the entire annual report.

**Good output looks like:** Claude refuses or warns ("PowerPoint hard-fails at ~50 bullets per slide; you'll get ellipsis truncation and no one reads them anyway"). Should suggest a different format (PDF report, Notion doc).

---

## 7. `slide-narrative` — story-shaped slide structure

**Purpose:** before you build slides, write the narrative arc. Forces the deck to have a *point* instead of being a wall of facts.

### Canonical
> Use the slide-narrative skill to outline a 10-minute board update on the Lab Result Portal. Audience: non-technical board members. Goal: get approval to spend $400K on the proposed architecture migration. Output: numbered narrative beats with a one-line argument per slide.

**Good output looks like:** 6-10 beats, each with (a) a one-line claim, (b) the evidence/visual, (c) the transition to the next beat. The arc should culminate in the $400K ask, not bury it on slide 8.

### Alternate-style
> Same skill — outline a 30-second elevator pitch for the same project. Audience: a VP I just bumped into in the elevator. No slides — just the spoken narrative.

**Good output looks like:** 4-6 sentences, structured as hook → problem → solution → ask. Should fit ~30 seconds of speech (≈75 words).

### Adversarial
> Same skill — outline a deck where slide 1 is "Q3 results," slide 2 is "API latency improvements," slide 3 is "the new espresso machine in the office," slide 4 is "team headcount." Make a coherent narrative.

**Good output looks like:** Claude refuses or produces a "this is not a single narrative — pick one of (executive update / engineering review / culture update)" response. If it strings them together with mush like "in conclusion, our team is doing great," the skill failed.

---

## 8. `diagram-export` — convert / rasterize diagrams

**Purpose:** take a diagram (Mermaid, drawio, PlantUML) and produce a deliverable format (PNG, SVG, PDF) for slide decks, docs, or printed RFCs.

### Canonical
> Use the diagram-export skill to convert a Mermaid flowchart (the password-reset one from the mermaid prompts) to SVG. Show me the exact CLI command.

**Good output looks like:** a concrete `mmdc -i input.mmd -o output.svg --theme dark` (or similar) command, with a note on what `mmdc` is and how to install it.

### Alternate-style
> Same skill — I have a drawio file with 12 pages. Export each page as a separate PNG at 2x resolution.

**Good output looks like:** a `drawio --export --format png --scale 2 --output ./out/ input.drawio` (or equivalent) command, with `--page-index` if needed for multi-page export.

### Adversarial
> Same skill — convert a 50MB drawio file to a single 16K-resolution PNG with lossless compression for printing on a billboard.

**Good output looks like:** Claude warns about realistic limits (browser-based exporters cap around 8K-12K, drawio CLI has memory ceilings) and proposes either SVG (resolution-independent) or PDF (vector, prints at any size). Should not blindly run a command that'll OOM.

---

## 9. `repo-architecture` — auto-generate architecture from a repo URL

**Purpose:** point at a GitHub URL, get a layered architecture diagram. Combines tree-walk + LLM classification + the architecture skill's renderer.

### Canonical
```bash
repo-architecture/bin/run.sh shekerkamma/SAP-O2C-Automation --auto
# or, manually:
repo-architecture/bin/run.sh shekerkamma/SAP-O2C-Automation
```

**Good output looks like:** `out/shekerkamma-SAP-O2C-Automation/diagram.html` with 5-6 populated layers, the MCP server in `data` or `application`, BTP in `infra`, SAP OData services in `external`, sidebars for security and dev environment.

### Alternate-style — broad repo with `--scope`
```bash
repo-architecture/bin/run.sh anthropics/anthropic-cookbook --scope patterns/agents --auto
```

**Good output looks like:** since the cookbook is heterogeneous, Phase 2 should refuse on the unscoped repo and produce a plausible diagram on the scoped sub-tree. The user-facing test is "did the refusal correctly surface, and did the scoped run produce something sensible?"

### Alternate-style — different stacks
```bash
repo-architecture/bin/run.sh psf/requests --auto       # Python lib, simple
repo-architecture/bin/run.sh cli/cli --auto             # Go CLI, large
repo-architecture/bin/run.sh vercel/swr --auto          # TS frontend lib
```

**Good output looks like:** each one produces a coherent diagram. `psf/requests` should be near-trivial (one application layer, one external HTTP layer). `cli/cli` is the stress test — 12+ subdirectories, lots of architectural shapes to choose from. `vercel/swr` should classify the test/, examples/, e2e/ directories sensibly (probably as `infra` or dropped entirely).

### Adversarial
```bash
repo-architecture/bin/run.sh shekerkamma/ticketforge --auto
```

**Good output looks like:** since this repo is itself a collection of skills (not a system), Phase 2 should refuse with a recommendation to scope to one skill (`--scope architecture`) or use the `architecture` skill from a prompt instead. If it produces a layered diagram for a docs repo, the refusal logic in `prompts/classify-modules.md` failed.

---

## Cross-skill comparison prompts

These run multiple skills on the same problem so you can compare what each is good at.

### Same system, three skills
> Take the SAP-O2C-Automation system from `architecture/demo-rendered/05-sap-o2c-automation.html`. Produce: (a) a Mermaid C4Context diagram, (b) a c4 PlantUML Container diagram, (c) a slide-narrative outline for a 5-minute architecture review. Highlight what each format reveals that the others don't.

**Good output looks like:** three artifacts plus a brief comparison table. Mermaid for embeddability, c4 for fidelity, slide-narrative for the *story*.

### Diagram → deck pipeline
> Use repo-architecture on `psf/requests` to get a layered diagram. Then use slide-narrative to outline a 10-minute "how Requests works" tech-talk based on that diagram. Then use python-pptx to generate the actual deck.

**Good output looks like:** three sequential outputs feeding each other. Tests whether the skills compose, or whether the handoffs are awkward.

---

## Style and layout coverage matrix

If you want to visually inspect every style/layout combo the renderer supports, render the same plan with each combination:

```bash
# 12 styles × 4 layouts (minus pipeline's palette-ignored cases) = ~36 unique HTMLs
for style in dusk-glow ember-warm frost-clean indigo-deep neon-dark ocean-teal pastel-mix rose-bloom sage-forest slate-dark stark-block steel-blue; do
  for layout in three-column single-stack two-column-split; do
    sed -e "s/^style: .*/style: $style/" -e "s/^layout: .*/layout: $layout/" \
      repo-architecture/tests/fixtures/valid-plan.yaml > /tmp/_p.yaml
    repo-architecture/bin/render.py /tmp/_p.yaml \
      --out "/tmp/coverage/$style-$layout.html" --prefix cov 2>/dev/null
  done
done
ls /tmp/coverage/ | head
```

This is what to do when you want to pick a style/layout for a specific deck — render the matrix, scroll, choose.

---

## Grading rubric (general)

A skill is **passing** when, given a canonical prompt:

1. The output is **immediately usable** without manual fixup (no broken syntax, no missing closes).
2. The skill's **hard rules** are enforced (e.g. architecture skill emits no ` ```html ` fence; c4 skill doesn't merge levels).
3. **Adversarial prompts are pushed back on**, not silently obeyed.
4. The output **matches the prompt's intent** — content reflects the input, not a generic example.

A skill **fails** when any of the above breaks. Most failures are silent (skill produces output, but it ignores a rule). Always grade against the rules in the SKILL.md, not just whether the output "looks right."
