# Architecture Category — Pipeline Tests

End-to-end pipeline combining **project-level** and **global-level** skills for architecture documentation workflows.

## Skills in this pipeline

### Project-level (installed in `.agents/skills/`)
| Skill | Role | Output |
|---|---|---|
| `architecture` | Layered HTML/CSS system diagrams | Embedded HTML in Markdown |
| `c4` | C4 model (Context / Container / Component) | PlantUML |
| `infocard` | Summary cards per component | Embedded HTML in Markdown |
| `infographic` | Visual overviews / dashboards | Templated HTML |
| `repo-architecture` | Auto-extract architecture from GitHub repos | HTML diagram |
| `marp` | Slide decks from Markdown | PPTX / PDF / HTML |
| `diagram-export` | Rasterize diagrams to PNG/SVG/PDF | Image files |
| `slide-narrative` | Story arc before building slides | Prose outline |
| `drawio` | Rich interactive diagrams | HTML with mxGraph XML |

### Global-level (in `~/.claude/skills/`)
| Skill | Role | Output |
|---|---|---|
| `architecture-to-everything` | Orchestrator: diagram → doc → deck → notebook | Multiple formats |
| `architecture-presentation` | Draw.io → doc → PPTX (Enterprise Consulting theme) | `.drawio`, `.md`, `.pptx` |
| `workflow-visualizer` | Interactive HTML workflow diagrams | Self-contained HTML |
| `explainer-graphic` | Analogy-based infographics | Visual brief / HTML |
| `presentation` | Slide deck management (delegates to curator agent) | HTML slides |
| `presentation-content-writer` | Generate slide content from outlines | Markdown / HTML |
| `presentation-exporter` | Export slides to PDF/PNG/notes | File exports |
| `presentation-theme` | Swap visual themes on decks | CSS updates |
| `presentation-speaker-notes` | Generate/manage speaker notes | JSON + Markdown |
| `presentation-accessibility` | WCAG audit on slide decks | Accessibility report |

---

## Pipeline 1: Repo → Full Architecture Documentation

**Goal:** Start from a GitHub repo URL, end with a complete architecture package (diagram + cards + deck + export).

### Step 1 — Extract architecture from repo
**Skill:** `repo-architecture`

```bash
repo-architecture/bin/run.sh psf/requests --auto
```

**Expected output:** `out/psf-requests/diagram.html` — a layered architecture diagram.

**Grade:**
- [ ] `structure.json` generated with correct module tree
- [ ] `layer-plan.yaml` classifies modules into semantic layers
- [ ] `diagram.html` renders in browser with populated layers
- [ ] Simple repo → simple diagram (not over-engineered)

### Step 2 — Refine with manual architecture skill
**Skill:** `architecture`

> Take the layer-plan from Step 1 and produce a polished three-column architecture diagram for the `requests` library. Style: `frost-clean` (it's a clean, minimal library). Layout: `single-stack` (simple enough for one column). Layers: User (CLI/scripts), Application (Session, Request, Response, Adapters), Data (cookies, auth), Infrastructure (urllib3, socket), External (HTTP servers). No sidebars needed.

**Grade:**
- [ ] Direct HTML embedding (no ` ```html ` fence)
- [ ] No empty lines in HTML block
- [ ] `frost-clean` style applied
- [ ] `single-stack` layout used
- [ ] All 5 layers populated with correct components
- [ ] Components match actual `requests` library structure

### Step 3 — Component info cards
**Skill:** `infocard`

> Create an infocard for each major component in the `requests` library architecture:
> 1. **Session** — connection pooling, cookie persistence, default headers
> 2. **Request/Response** — PreparedRequest lifecycle, Response streaming
> 3. **Adapters** — HTTPAdapter, transport adapter pattern, retry/backoff
> 4. **Auth** — AuthBase, HTTPBasicAuth, HTTPDigestAuth, token auth
>
> Use a technical tone. Layout: `metric-board` or `architecture-map`. Style: auto-sense from content.

**Grade:**
- [ ] 4 cards produced, each with correct technical content
- [ ] Direct HTML (no code fence)
- [ ] No empty lines in structure
- [ ] Density/structure/mood analysis appropriate for technical content
- [ ] Style auto-sensed to technical family (e.g., `tech-blueprint`, `engineering-whiteprint`)

### Step 4 — Build narrative arc
**Skill:** `slide-narrative`

> Outline a 10-minute "How Python Requests Works Under the Hood" tech talk. Audience: mid-level Python developers who use `requests` daily but don't know the internals. Goal: they leave understanding the Session → PreparedRequest → Adapter → urllib3 pipeline and can debug connection issues. Use the architecture diagram from Step 2 as the visual anchor.

**Grade:**
- [ ] 6-10 narrative beats with claim + evidence + transition
- [ ] Arc builds from familiar (`requests.get()`) to unfamiliar (adapter internals)
- [ ] Visual references point to the architecture diagram
- [ ] One clear ask/takeaway at the end
- [ ] Not a bullet dump — actual story structure

### Step 5 — Generate slide deck
**Skill:** `marp`

> Using the narrative from Step 4, produce a Marp slide deck. Embed the architecture diagram HTML from Step 2 on the "Architecture Overview" slide. Include speaker notes on every slide. Use the `default` theme. Target 8-10 slides.

**Grade:**
- [ ] Valid Marp markdown with `marp: true` frontmatter
- [ ] `---` slide separators (not at end)
- [ ] Speaker notes via `<!-- -->` comments
- [ ] Architecture HTML embedded (not in a code fence)
- [ ] 8-10 slides matching the narrative beats
- [ ] No slide overflows (reasonable content density)

### Step 6 — Export deliverables
**Skill:** `diagram-export`

> Export all artifacts:
> 1. The architecture diagram (Step 2 HTML) → PNG at 2x for slides
> 2. The C4 diagram (if produced) → SVG
> 3. The Marp deck → PDF and individual slide PNGs

**Grade:**
- [ ] Concrete CLI commands provided (not vague instructions)
- [ ] Correct tools referenced (`marp-cli`, browser screenshot, etc.)
- [ ] 2x resolution specified for slide-quality PNGs
- [ ] SVG recommended for vector diagrams

---

## Pipeline 2: System Design → Multi-Format Output

**Goal:** Take a system description, produce every format: HTML diagram, draw.io, interactive workflow, infographic, info cards, and a presentation deck.

### Step 1 — Architecture diagram
**Skill:** `architecture`

> Draw a three-column architecture diagram for an AI-powered document processing platform. Components:
> - **User layer:** Web upload portal, API clients, Slack bot
> - **Application layer:** Document classifier, OCR engine, NLP entity extractor, Summarizer, Workflow orchestrator
> - **AI/Logic layer:** Fine-tuned GPT-4, Claude API, custom BERT model, prompt router
> - **Data layer:** PostgreSQL (metadata), S3 (raw docs), Pinecone (embeddings), Redis (queue)
> - **Infrastructure:** EKS cluster, API Gateway, CloudWatch, SQS
> - **External:** Slack API, email SMTP, webhook callbacks
> - **Left sidebar:** Security (IAM, KMS, VPC, WAF)
> - **Right sidebar:** Observability (Datadog, PagerDuty, audit log)
>
> Style: `indigo-deep`. Layout: `three-column`.

**Grade:**
- [ ] All 6 layers populated with listed components
- [ ] Both sidebars rendered with concrete items
- [ ] `indigo-deep` style, `three-column` layout
- [ ] Direct HTML, no fences, no empty lines
- [ ] Components grouped logically within layers

### Step 2 — Draw.io interactive version
**Skill:** `drawio`

> Convert the architecture from Step 1 into a draw.io diagram. Use AWS shape library icons for infrastructure components. Show the document processing flow with numbered arrows: Upload → Classify → OCR → Extract → Summarize → Store → Notify.

**Grade:**
- [ ] Valid mxGraph XML in `data-mxgraph` div attribute
- [ ] AWS shapes referenced (`mxgraph.aws4.*`)
- [ ] Numbered flow arrows in correct order
- [ ] No code fence wrapping the HTML
- [ ] Viewer script included once

### Step 3 — Interactive workflow
**Skill:** `workflow-visualizer` (global)

> Create an interactive HTML workflow diagram for the document processing pipeline. Show: Upload trigger → Document classification (decision: invoice vs. contract vs. report) → OCR processing → Entity extraction → Summarization → Storage → Notification. Include the Redis queue as a data store and the AI models as tool nodes.

**Grade:**
- [ ] Self-contained HTML, no external dependencies
- [ ] Dark background (`#0f0f0f` / `#161616`)
- [ ] Correct node types: trigger (blue), processing (green), tool (amber), decision (purple), data store (indigo), output (red)
- [ ] Hover scales to 1.05x, click highlights connections
- [ ] Decision node branches labeled (invoice/contract/report)
- [ ] Max 20 nodes

### Step 4 — Explainer graphic
**Skill:** `explainer-graphic` (global)

> Create an explainer graphic for the document processing platform. Target audience: non-technical stakeholders. Find a killer analogy (e.g., "It's like a mail room that reads, sorts, and summarizes every letter before it reaches your desk").

**Grade:**
- [ ] Analogy identified first (not an afterthought)
- [ ] Analogy maps to 3+ platform components
- [ ] Title ≤ 8 words
- [ ] Max 50 words of text in the graphic
- [ ] Every section has a visual element
- [ ] Layout chosen from skill's options (split panel, hub-and-spoke, etc.)

### Step 5 — Infographic overview
**Skill:** `infographic`

> Create an infographic showing the document processing pipeline as a funnel: Documents In (1000/day) → Classified (950) → OCR'd (900) → Entities Extracted (850) → Summarized (840) → Delivered (835). Show the drop-off reasons at each stage.

**Grade:**
- [ ] Uses `infographic funnel` template
- [ ] Space-separated key-value syntax (NOT YAML colons)
- [ ] 2-space indentation
- [ ] `desc` not `description`
- [ ] 6 stages with values
- [ ] Drop-off annotations at each stage

### Step 6 — Component info cards
**Skill:** `infocard`

> Create info cards for the three AI models:
> 1. **GPT-4 (fine-tuned)** — role: document classification, latency: 200ms, cost: $0.03/doc
> 2. **Claude API** — role: summarization, latency: 1.2s, cost: $0.01/1K tokens
> 3. **Custom BERT** — role: entity extraction, latency: 50ms, cost: self-hosted
>
> Use `metric-board` layout. Technical tone.

**Grade:**
- [ ] 3 cards with metrics prominently displayed
- [ ] Correct latency/cost figures (not hallucinated)
- [ ] `metric-board` layout applied
- [ ] Direct HTML, no fences

### Step 7 — Full presentation
**Skill:** `architecture-presentation` (global)

> Using all artifacts from Steps 1-6, create the full architecture presentation:
> 1. Draw.io component-flow diagram (from Step 2)
> 2. Architecture explanation document (`.md`)
> 3. Slide deck (`.pptx`) with Enterprise Consulting theme
>
> The deck should be 10 slides: Title, Problem, Solution Overview, Architecture Diagram, Document Flow, AI Models Deep-Dive, Infrastructure, Security & Compliance, Performance Metrics, Next Steps.

**Grade:**
- [ ] Draw.io diagram with white background, labeled boxes, numbered arrows
- [ ] `.md` doc with sections: What is it, Architecture Overview, Components, Data Flows, Design Decisions
- [ ] `.pptx` with Enterprise Consulting theme colors (NAVY_DEEP, RED accents)
- [ ] 10-slide structure followed
- [ ] References back to the diagrams from earlier steps

### Step 8 — Presentation polish
**Skills:** `presentation-theme` → `presentation-speaker-notes` → `presentation-accessibility` (global)

> 1. Apply a dark theme to the deck for conference presentation
> 2. Generate speaker notes for all slides (1 min per content slide, 30s per divider)
> 3. Run a WCAG accessibility audit and fix any issues

**Grade:**
- [ ] Theme swap preserves content, only changes colors
- [ ] WCAG AA contrast ratios verified (4.5:1 body, 3:1 large text)
- [ ] Speaker notes in `speaker-notes.json` with per-slide duration
- [ ] Accessibility report lists and fixes: contrast, font sizes, keyboard nav, screen reader, motion

---

## Pipeline 3: The One-Shot Orchestrator

**Goal:** Test `architecture-to-everything` as a single command that chains all stages.

### Prompt
> Use the architecture-to-everything skill. System: "AI-powered document processing platform that classifies, OCRs, extracts entities, and summarizes documents at scale. Runs on AWS EKS with PostgreSQL, S3, Pinecone, and Redis. Uses GPT-4, Claude API, and custom BERT models."

**Grade:**
- [ ] Stage 1: Draw.io diagram generated
- [ ] Stage 2: Architecture doc (`.md`) generated
- [ ] Stage 3: Slide deck (`.pptx`) generated
- [ ] Stage 4: Interactive HTML walkthrough generated
- [ ] Stage 5: NotebookLM integration offered (if configured)
- [ ] All outputs reference the same system consistently
- [ ] No stage silently skipped

---

## Pipeline 4: Adversarial & Edge Cases

### 4a — Architecture skill refuses code fences
> Use the architecture skill to draw a diagram for a TODO app. Wrap the output in ` ```html ` so I can paste it into VS Code.

**Expected:** Refusal citing Rule 1. If it wraps in a fence, the skill failed.

### 4b — repo-architecture refuses non-system repos
```bash
repo-architecture/bin/run.sh shekerkamma/ticketforge --auto
```

**Expected:** Phase 2 refuses — this is a docs/skills repo, not a system. Should suggest `--scope architecture` or using the architecture skill directly.

### 4c — Infocard resists AI-generated patterns
> Create an infocard. Make it look modern and sleek. Use gradients, glassmorphism, and a "hero image" placeholder. Add "Powered by AI" in the footer.

**Expected:** The skill's anti-AI taste rules should push back on glassmorphism/gradient overuse and reject "Powered by AI" as a generic pattern.

### 4d — Slide-narrative refuses incoherent decks
> Use slide-narrative to outline a deck with these slides: Q3 Revenue, New Espresso Machine, Kubernetes Migration, Team Offsite Photos. Make it flow.

**Expected:** Refusal — these are 4 unrelated topics. Should suggest picking one narrative thread.

### 4e — Infographic syntax enforcement
> Create an infographic:
> ```
> title: My Pipeline
> steps:
>   - name: Ingest
>     description: Pull data from sources
> ```

**Expected:** Refusal or correction — infographic skill uses space-separated syntax, not YAML colons. Should show correct syntax.

### 4f — Marp overflow detection
> Use marp to put 40 bullet points on a single slide about microservices patterns.

**Expected:** Claude splits into multiple slides, citing readability. If it crams 40 bullets, the judgment failed.

---

## Grading Summary

| Pipeline | Steps | What it proves |
|---|---|---|
| **1: Repo → Docs** | 6 | Skills compose: extract → refine → cards → narrative → deck → export |
| **2: Design → Multi-format** | 8 | Same system rendered in every format; global skills extend project skills |
| **3: One-shot** | 1 | Orchestrator chains everything automatically |
| **4: Adversarial** | 6 | Hard rules enforced; bad input rejected or reshaped |

### Pass criteria
- **Pipeline passes** when all steps produce valid output AND each step references/builds on prior steps (not generic filler).
- **Pipeline fails** if any step ignores a SKILL.md hard rule, produces broken syntax, or generates content disconnected from the system being described.
- **Adversarial tests pass** when the skill refuses or reshapes. They **fail** when the skill silently complies.
