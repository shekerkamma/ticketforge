# Knowledge & Ideation Category — Pipeline Tests

End-to-end pipeline combining **project-level** knowledge mapping skills (`mindmap`, `canvas`, `graphviz`) with **global-level** research and strategy skills (`graphify`, `content-research`, `research-to-strategy`, `llm-council`) for brainstorming, research synthesis, decision-making, and knowledge graph workflows.

## Skills in this pipeline

### Project-level (installed in `.agents/skills/`)
| Skill | Role | Output | Notation |
|---|---|---|---|
| `mindmap` | Hierarchical brainstorming, topic decomposition, decision trees | PlantUML (` ```plantuml `) | `@startmindmap`/`@endmindmap`, `*`/`**`/`***` markers, `left side`, `[#hex]` colors |
| `canvas` | Spatial concept maps, knowledge boards, planning layouts | JSON (` ```canvas `) | `nodes` array (text/file/link/group) + `edges` array, 100px grid, Obsidian-compatible |
| `graphviz` | Dependency graphs, call graphs, module hierarchies | DOT (` ```dot `) | `digraph`/`graph`, `->` directed / `--` undirected, `cluster_*` subgraphs, layout engines |
| `infographic` | Visual summaries | Templated HTML | Space-separated key-value |
| `infocard` | Summary cards | Embedded HTML | Direct HTML |
| `marp` / `slide-narrative` | Presentation layer | Markdown slides / prose | Marp frontmatter |
| `vega` | Data charts | Vega-Lite/Vega JSON | Declarative spec |

### Global-level (in `~/.claude/skills/`)
| Skill | Role | Output |
|---|---|---|
| `graphify` | Any input → interactive knowledge graph with community detection | HTML graph + GraphRAG JSON + report |
| `content-research` | Ingest content (YouTube, LinkedIn, web) → Obsidian vault + analysis | Structured notes + MOC |
| `research-to-strategy` | Research → knowledge graph → AI strategy council → recommendation | Council judgment + slide deck |
| `llm-council` | 5 independent AI advisors pressure-test a decision | HTML report + markdown transcript |

### How They Connect

```
content-research ──→ graphify ──→ mindmap (decompose findings)
(ingest sources)     (knowledge      │
                      graph)         ├──→ canvas (spatial layout)
                         │           │
                         ▼           ├──→ graphviz (dependency map)
                   research-to-      │
                   strategy          └──→ infographic / infocard
                         │
                         ▼
                    llm-council ──→ slide-narrative → marp
                    (pressure-test)
```

---

## Pipeline 1: Research → Knowledge Graph → Decomposition

**Goal:** Ingest research sources, build a knowledge graph, then decompose findings into mindmaps, canvases, and dependency graphs for different audiences.

**Topic:** "AI agents in enterprise software — market landscape, key players, and adoption patterns."

### Step 1 — Content ingestion
**Skill:** `content-research` (global)

> Ingest and analyze these sources on AI agents in enterprise:
> - A YouTube video on AI agent frameworks (e.g., LangChain, CrewAI, AutoGen)
> - A LinkedIn post from an enterprise CTO about agent adoption challenges
> - A GitHub repo README for a popular agent framework
>
> Save structured notes to the Obsidian vault with wikilinks and tags.

**Grade:**
- [ ] Each source type correctly identified and ingested
- [ ] Structured notes with hook, key points, authority assessment
- [ ] Obsidian-compatible wikilinks (`[[concept]]`) and tags (`#ai-agents`)
- [ ] Map of Concepts (MOC) updated

### Step 2 — Knowledge graph
**Skill:** `graphify` (global)

> Build a knowledge graph from the research notes in Step 1. Extract entities: companies, products, technologies, concepts, people. Detect communities (e.g., "LLM frameworks," "enterprise platforms," "research labs"). Generate the interactive HTML visualization.

**Grade:**
- [ ] Entities extracted with types (company, product, technology, person)
- [ ] Edges with relationship labels (e.g., "develops," "competes with," "integrates")
- [ ] Community detection groups related entities
- [ ] Interactive HTML with hover/click behavior
- [ ] GraphRAG-ready JSON exported
- [ ] GRAPH_REPORT.md summarizing communities

### Step 3 — Mindmap decomposition
**Skill:** `mindmap`

> Use the mindmap skill to decompose the AI agents landscape into a hierarchical map:
>
> **Root:** AI Agents in Enterprise
>
> **Right side:**
> - Frameworks: LangChain, CrewAI, AutoGen, Claude Agent SDK
>   - Each with: strengths, weaknesses, adoption stage
> - Use Cases: Customer support, Code generation, Data analysis, Process automation
>   - Each with: maturity level (color-coded: green=production, yellow=pilot, red=research)
>
> **Left side:**
> - Challenges: Reliability, Cost, Security, Compliance, Integration
> - Risks: Hallucination in critical workflows, Vendor lock-in, Skill gap
>
> Use the RAG color palette (green/yellow/red) for maturity and the general-purpose pastel palette for categories.

**Grade:**
- [ ] `@startmindmap` / `@endmindmap`
- [ ] ` ```plantuml ` fence
- [ ] `*` markers with consistent depth (`*`, `**`, `***`, `****`)
- [ ] `left side` splits challenges/risks to the left
- [ ] `[#C8E6C9]` (green), `[#FFF9C4]` (yellow), `[#FFCDD2]` (red) for RAG colors
- [ ] Pastel palette from the skill's recommended palettes for category branches
- [ ] Content matches research findings from Steps 1-2

### Step 4 — Spatial canvas
**Skill:** `canvas`

> Create a JSON Canvas spatial board organizing the AI agents research:
>
> **Group: "Market Landscape"** (top-left, 800x400)
> - Text nodes for each framework (LangChain, CrewAI, AutoGen, Claude SDK) with 1-line descriptions
> - Edges connecting competing frameworks
>
> **Group: "Enterprise Use Cases"** (top-right, 800x400)
> - Text nodes for each use case with maturity label
> - Edges from frameworks to their strongest use cases
>
> **Group: "Decision Factors"** (bottom-center, 800x400)
> - Text nodes: Cost, Reliability, Security, Integration Ease, Community Size
> - Edges from use cases to relevant decision factors
>
> Color-code: frameworks = cyan (5), use cases = green (4), decision factors = orange (2).

**Grade:**
- [ ] Valid JSON in ` ```canvas ` fence
- [ ] Three `"type": "group"` nodes with labels
- [ ] Text nodes inside groups (positioned within group bounds)
- [ ] Edges with `fromNode`/`toNode` matching node IDs exactly
- [ ] `fromSide`/`toSide` specified for clean routing
- [ ] Color presets applied correctly (`"5"` = cyan, `"4"` = green, `"2"` = orange)
- [ ] 100px grid alignment
- [ ] IDs alphanumeric/dash/underscore only

### Step 5 — Dependency graph
**Skill:** `graphviz`

> Create a Graphviz dependency graph showing the technology stack relationships:
>
> - `digraph` (directed)
> - Cluster "LLM Providers": OpenAI, Anthropic, Google, Meta (open-source)
> - Cluster "Agent Frameworks": LangChain → depends on all LLM providers; CrewAI → depends on OpenAI + Anthropic; AutoGen → depends on OpenAI; Claude SDK → depends on Anthropic only
> - Cluster "Enterprise Platforms": Salesforce Einstein, ServiceNow, Microsoft Copilot → each depends on specific frameworks + providers
> - Edge labels show dependency type: "API", "SDK", "fine-tune"
>
> Use `rankdir=LR`, `splines=ortho` for clean routing.

**Grade:**
- [ ] ` ```dot ` fence (NOT ` ```graphviz `)
- [ ] `digraph` with `->` directed edges
- [ ] Cluster names start with `cluster_` (e.g., `subgraph cluster_llm_providers`)
- [ ] Node IDs with spaces quoted or underscored
- [ ] Attribute syntax comma-separated with semicolons
- [ ] `rankdir=LR`, `splines=ortho` set
- [ ] Edge labels: `[label="API"]`
- [ ] Dependency direction correct (framework → provider, platform → framework)

### Step 6 — Strategic recommendation
**Skill:** `llm-council` (global)

> Run the LLM Council on this decision: "Should our enterprise (500-person B2B SaaS company) build our AI agent platform on LangChain, CrewAI, or Claude Agent SDK? Context: we're an Anthropic-heavy shop, our use case is customer support automation, and we need production reliability within 6 months."
>
> Present the research from Steps 1-5 as context for the 5 advisors.

**Grade:**
- [ ] 5 advisors spawned in parallel (Killer, Rebuilder, Maximizer, Stranger, Operator)
- [ ] Each advisor references the research context (not generic advice)
- [ ] Peer review phase anonymized
- [ ] Chairman synthesis identifies: agreement points, clashes, blind spots
- [ ] Clear recommendation with first action
- [ ] HTML report + markdown transcript

### Step 7 — Presentation
**Skills:** `slide-narrative` → `marp`

> 1. Outline a 15-minute "AI Agent Strategy" presentation for the CTO. Include: market landscape (mindmap), technology stack (graphviz dependency graph), recommendation (council verdict), implementation roadmap.
> 2. Build the Marp deck with 10-12 slides.

**Grade:**
- [ ] Narrative references specific artifacts from earlier steps
- [ ] Mindmap visual for landscape slide
- [ ] Graphviz graph for tech stack slide
- [ ] Council recommendation as the climax
- [ ] Implementation roadmap as the closing ask
- [ ] Marp deck valid with speaker notes

---

## Pipeline 2: Product Planning — Brainstorm to Roadmap

**Goal:** Take a product idea from brainstorm through structured planning to a visual roadmap.

### Step 1 — Brainstorm mindmap
**Skill:** `mindmap`

> Brainstorm a new product: "AI-powered code review assistant for enterprise teams." Use bilateral layout:
>
> **Right side (Opportunities):**
> - Features: Auto-review PRs, Security scanning, Performance suggestions, Style consistency, Knowledge sharing
> - Markets: Enterprise DevOps teams, Open-source maintainers, Bootcamp students
> - Differentiators: Context-aware (understands your codebase), Team learning (shares patterns across reviewers)
>
> **Left side (Challenges):**
> - Technical: LLM cost per review, Latency requirements (<30s), False positive rate
> - Business: Crowded market (Copilot, CodeRabbit, Sourcery), Enterprise sales cycle
> - Adoption: Developer trust, Integration with existing CI/CD
>
> Use warm corporate color palette.

**Grade:**
- [ ] `@startmindmap` / `@endmindmap`
- [ ] Bilateral: `left side` keyword present
- [ ] Right side = opportunities, left side = challenges
- [ ] Warm corporate colors: `[#1565C0]` root, `[#FFB74D]` level 1, `[#4DB6AC]` level 2
- [ ] 3+ levels of depth on each side

### Step 2 — Feature dependency graph
**Skill:** `graphviz`

> Create a dependency graph for the code review assistant's features:
>
> - Core: `code_parser` → `ast_analyzer` → `context_builder`
> - Review: `context_builder` → `review_engine` → `suggestion_generator`
> - Security: `ast_analyzer` → `security_scanner` (depends on OWASP rules DB)
> - Performance: `ast_analyzer` → `perf_analyzer` (depends on benchmark DB)
> - Learning: `review_engine` → `pattern_extractor` → `team_knowledge_base`
> - Integration: `suggestion_generator` → `github_integration`, `gitlab_integration`, `bitbucket_integration`
>
> Color nodes by module: core=lightblue, review=lightgreen, security=lightyellow, integration=lightsalmon.

**Grade:**
- [ ] `digraph` with correct `->` dependencies
- [ ] `subgraph cluster_core`, `cluster_review`, `cluster_security`, `cluster_integration`
- [ ] Node colors applied: `[style=filled, fillcolor=lightblue]`
- [ ] Dependency direction correct (dependencies point FROM dependent TO dependency)
- [ ] Clean layout with `rankdir=TB` or `LR`

### Step 3 — Planning board canvas
**Skill:** `canvas`

> Create a product planning canvas with four quadrant groups:
>
> **Group: "Now (Q3 2026)"** — top-left, green
> - Core parser, AST analyzer, GitHub integration, Basic review engine
>
> **Group: "Next (Q4 2026)"** — top-right, yellow
> - Security scanner, Performance analyzer, GitLab integration
>
> **Group: "Later (H1 2027)"** — bottom-left, orange
> - Team knowledge base, Pattern extractor, Bitbucket integration
>
> **Group: "Explore"** — bottom-right, purple
> - Auto-fix suggestions, Voice-controlled reviews, IDE live mode
>
> Edges from "Now" items to "Next" items they enable (dependencies).

**Grade:**
- [ ] Four `"type": "group"` nodes with correct labels and colors
- [ ] Items positioned inside their group bounds
- [ ] Edges show cross-group dependencies (Now → Next)
- [ ] Color presets: green (4), yellow (3), orange (2), purple (6)
- [ ] Valid JSON, IDs match in edges

### Step 4 — Competitive landscape infographic
**Skill:** `infographic`

> Create a comparison infographic of AI code review tools:
>
> - GitHub Copilot Code Review: $19/user/mo, basic suggestions, deep GitHub integration
> - CodeRabbit: $15/user/mo, comprehensive reviews, multi-platform
> - Sourcery: $12/user/mo, Python-focused, refactoring suggestions
> - Our Product: $25/user/mo, context-aware, team learning, enterprise security
>
> Use the `comparison` template.

**Grade:**
- [ ] `infographic comparison` template
- [ ] Space-separated syntax, 2-space indent
- [ ] Exactly 4 items with children (price, focus, differentiator)
- [ ] Our product clearly positioned against competitors

### Step 5 — Decision council
**Skill:** `llm-council` (global)

> "Should we price our AI code review assistant at $25/user/month (premium positioning) or $12/user/month (aggressive market entry)? We have 6 months of runway and need 500 paying users to hit break-even."

**Grade:**
- [ ] 5 advisors with distinct perspectives on pricing strategy
- [ ] Killer advisor challenges the $25 positioning
- [ ] Operator advisor calculates unit economics
- [ ] Clear recommendation with reasoning
- [ ] First action identified

---

## Pipeline 3: Knowledge Graph from Codebase

**Goal:** Use `graphify` on a codebase, then visualize the extracted graph with project-level skills.

### Step 1 — Extract knowledge graph from code
**Skill:** `graphify` (global)

> Run graphify on the `ticketforge` repository. Extract: skill names as entities, shared dependencies (PlantUML, mxgraph stencils, Marp), skill categories, cross-references between skill SKILL.md files.

**Grade:**
- [ ] Entities: 15 skill names extracted
- [ ] Relationships: shared stencil families, shared rendering engines
- [ ] Communities detected: PlantUML-based skills, HTML-based skills, presentation skills
- [ ] Interactive HTML graph
- [ ] GRAPH_REPORT.md summarizes findings

### Step 2 — Mindmap of skill categories
**Skill:** `mindmap`

> From the graphify output, create a mindmap of the skill ecosystem:
>
> Root: Markdown Viewer Skills
> - PlantUML-based (10): cloud, network, security, iot, data-analytics, uml, bpmn, archimate, mindmap, c4
> - HTML-based (3): architecture, infocard, infographic
> - Other (4): vega (JSON), canvas (JSON), graphviz (DOT), mermaid (Mermaid)
> - Presentation (3): marp, python-pptx, slide-narrative
> - Utility (2): diagram-export, repo-architecture
>
> Color by rendering engine.

**Grade:**
- [ ] Categories match actual skill groupings
- [ ] Color-coded by rendering engine (PlantUML = blue, HTML = green, JSON = purple, etc.)
- [ ] Counts accurate (cross-check with repo)
- [ ] `@startmindmap` / `@endmindmap`

### Step 3 — Dependency graph
**Skill:** `graphviz`

> Create a Graphviz dependency graph showing which skills depend on which rendering engines and shared resources:
>
> - Cluster "Rendering Engines": PlantUML, Marp CLI, Vega renderer, Graphviz dot, Browser (for HTML)
> - Cluster "Shared Resources": mxgraph stencils (9500+), ArchiMate stdlib, Marp themes
> - Individual skill nodes with edges to their engine and resources
>
> Show that mxgraph stencils are the most-depended-on resource (10 skills use them).

**Grade:**
- [ ] `cluster_engines`, `cluster_resources` subgraphs
- [ ] Each skill node connects to its rendering engine
- [ ] mxgraph stencils node has the most incoming edges (visually prominent)
- [ ] `rankdir=LR` or `TB` for clean layout
- [ ] Edge labels not needed (relationship is "depends on")

### Step 4 — Spatial canvas board
**Skill:** `canvas`

> Create a canvas board mapping the full skill ecosystem spatially:
>
> - Left column: Input formats (PlantUML, DOT, JSON, Markdown, HTML)
> - Center column: Skills (positioned near their input format)
> - Right column: Output formats (SVG, PNG, PDF, HTML, PPTX)
> - Edges from input → skill → output
>
> Group by rendering pipeline.

**Grade:**
- [ ] Three visual columns (input, skills, output)
- [ ] Skills positioned near their input format
- [ ] Edges trace the full pipeline path
- [ ] Groups for each rendering pipeline
- [ ] Valid JSON canvas spec

---

## Pipeline 4: Mindmap Deep-Dive — Pattern Coverage

**Goal:** Test all mindmap patterns from the skill's examples.

### Step 1 — Basic hierarchy
> Use the mindmap skill. Decompose "Machine Learning" into: Supervised (Classification, Regression), Unsupervised (Clustering, Dimensionality Reduction), Reinforcement (Model-Based, Model-Free). Three levels deep.

**Grade:**
- [ ] `*` root, `**` categories, `***` subcategories
- [ ] Clean hierarchy, no skipped levels

### Step 2 — Bilateral layout
> Create a pros/cons mindmap for "Migrating to Kubernetes." Pros on the right, cons on the left.

**Grade:**
- [ ] `left side` keyword splits the map
- [ ] Pros right, cons left (not mixed)
- [ ] Balanced depth on both sides

### Step 3 — Styled theme with RAG colors
> Create a project status mindmap for a product launch. Color-code each item: green (on track), yellow (at risk), red (blocked). Use `<style>` classes.

**Grade:**
- [ ] `<style>` block with `.green`, `.yellow`, `.red` classes
- [ ] `<<green>>` / `<<yellow>>` / `<<red>>` stereotypes on nodes
- [ ] Consistent color application
- [ ] RAG palette hex values from the skill's reference

### Step 4 — Rich text with multi-line nodes
> Create a mindmap where each leaf node has multi-line content (title + description). Use the `:..;` block syntax.

**Grade:**
- [ ] `***:Title\nDescription line 1\nDescription line 2;` syntax
- [ ] Trailing `;` present on every multi-line node
- [ ] No parser breaks

### Step 5 — Direction control
> Create a top-to-bottom mindmap (tree layout) for an org chart: CEO → VPs → Directors → Managers.

**Grade:**
- [ ] `top to bottom direction` specified
- [ ] Renders as vertical tree (not radial)
- [ ] 4 levels of hierarchy

---

## Pipeline 5: Adversarial & Edge Cases

### 5a — Mindmap: wrong fence
> Create a mindmap using ` ```mermaid ` fence with `mindmap` keyword.

**Expected:** Correction — mindmap skill uses PlantUML with `@startmindmap`, not Mermaid. Should use ` ```plantuml ` fence.

### 5b — Canvas: overlapping nodes
> Create a canvas with 10 nodes all at position (0, 0).

**Expected:** Pushback — all nodes will overlap. Should space them on 100px grid (e.g., 0, 100, 200, ...).

### 5c — Graphviz: missing cluster_ prefix
> Create a Graphviz diagram with `subgraph backend { }` (no `cluster_` prefix).

**Expected:** Correction — subgraphs must start with `cluster_` to render as boxes. Should fix to `subgraph cluster_backend`.

### 5d — Graphviz: wrong fence
> Wrap the DOT diagram in ` ```graphviz ` fence.

**Expected:** Correction — skill explicitly says use ` ```dot `, NOT ` ```graphviz `.

### 5e — Canvas: invalid node IDs
> Create a canvas with node ID `"my node #1"` (contains space and hash).

**Expected:** Correction — IDs must be alphanumeric, dash, underscore only. Should fix to `"my-node-1"`.

### 5f — Mindmap: mixed marker styles
> Create a mindmap using `*` for the root, `++` for level 1, `***` for level 2, `--` for level 3.

**Expected:** Correction — should not randomly mix `*` and `+/-` styles in the same branch. Pick one style and stay consistent.

### 5g — Graphify on empty input
> Run graphify with no input files or URLs.

**Expected:** Error handling — should ask for input source rather than producing an empty graph.

---

## Grading Summary

| Pipeline | Steps | What it proves |
|---|---|---|
| **1: Research → Knowledge Graph** | 7 | `content-research` → `graphify` → `mindmap` + `canvas` + `graphviz` → `llm-council` → presentation |
| **2: Product Planning** | 5 | Brainstorm → dependency graph → planning board → competitive infographic → decision council |
| **3: Codebase Knowledge Graph** | 4 | `graphify` on code → `mindmap` categories → `graphviz` dependencies → `canvas` ecosystem map |
| **4: Mindmap Deep-Dive** | 5 | Every pattern: basic, bilateral, styled/RAG, rich text, direction control |
| **5: Adversarial** | 7 | Wrong fences, overlapping nodes, missing prefixes, invalid IDs, mixed styles, empty input |

### Pass criteria
- **mindmap passes** when: `@startmindmap`/`@endmindmap` in ` ```plantuml ` fence, consistent marker style per branch, `left side` correctly splits bilateral layouts, colors use recommended palettes.
- **canvas passes** when: valid JSON, nodes don't overlap (100px minimum spacing), edge IDs match node IDs exactly, color presets 1-6, coordinates on grid.
- **graphviz passes** when: ` ```dot ` fence (not ` ```graphviz `), `cluster_` prefix on subgraphs, quoted IDs with spaces, comma-separated attributes, correct edge syntax (`->` for digraph, `--` for graph).
- **Global skills pass** when: `graphify` extracts meaningful entities with community detection, `content-research` produces Obsidian-compatible notes, `llm-council` runs 5 advisors with peer review, `research-to-strategy` chains the full pipeline.
- **Adversarial tests pass** when syntax errors are corrected and invalid patterns are caught before rendering.
