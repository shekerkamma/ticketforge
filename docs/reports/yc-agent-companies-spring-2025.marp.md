---
marp: true
theme: analytics
size: 16:9
paginate: true
html: true
footer: "TicketForge | YC Agent Companies | June 2026"
---

<!-- _class: title -->

# Y Combinator Agent Companies

**What Spring 2025 small-team YC companies are building, and which use cases they are actually focused on**
June 2026

<div class="accent-bar"></div>

---

<!-- _class: section-opener -->

## Scope

- Live source tested on **June 2, 2026**
- Website entry point: `https://www.ycombinator.com/companies`
- Backend discovered from the page: YC's public company search index
- Cohort analyzed for comparability with the demo: **Spring 2025**
- Screen used in this report:
  - query anchored on **agent / agentic**
  - **team size <= 10**
  - **27-company** full cohort after filtering

---

<!-- _class: kpi -->

## Cohort snapshot

<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-value accent">27</div>
    <div class="kpi-label">Agent-related companies</div>
    <div class="kpi-delta flat">Spring 2025 · team size <= 10</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">2</div>
    <div class="kpi-label">Median team size</div>
    <div class="kpi-delta flat">very early-stage cohort</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">13</div>
    <div class="kpi-label">Teams with 1-2 people</div>
    <div class="kpi-delta up">48% of the cohort</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value positive">8</div>
    <div class="kpi-label">Workflow automation names</div>
    <div class="kpi-delta up">largest focus area</div>
  </div>
</div>

---

<!-- _class: takeaway -->

## The cohort is more practical than abstract

<div class="so-what">The center of gravity is not “general agents.” It is operational software: workflow automation, customer-facing ops, analytics, developer tooling, and narrow vertical execution.</div>

<div class="finding">
  <div class="finding-headline">The YC small-team agent cohort is deployment-focused</div>
  <div class="finding-detail">Top cluster counts: workflow automation (8), sales/customer ops (7), analytics/reporting (6), developer tools/testing (6), and data/agent infrastructure (5).</div>
  <div class="finding-impact">Interpretation: founders are packaging agents around jobs, not around generic AI claims.</div>
</div>

---

<!-- _class: recommendation -->

## Highest-density use-case clusters

<div class="rec-row">
  <div class="rec-number">1</div>
  <div class="rec-content">
    <div class="rec-action">Workflow automation</div>
    <div class="rec-rationale">Examples: Anana, Third Chair, MindFort, Cotool, Sim. These companies wrap agents around concrete operational flows instead of open-ended chat.</div>
  </div>
  <div class="rec-confidence high">8</div>
</div>

<div class="rec-row">
  <div class="rec-number">2</div>
  <div class="rec-content">
    <div class="rec-action">Sales / customer-facing operations</div>
    <div class="rec-rationale">Examples: stratify, Cohesive, Anana, Galen AI. The recurring pattern is “use agents where human teams already have repetitive customer-facing work.”</div>
  </div>
  <div class="rec-confidence high">7</div>
</div>

<div class="rec-row">
  <div class="rec-number">3</div>
  <div class="rec-content">
    <div class="rec-action">Analytics, reporting, and knowledge work</div>
    <div class="rec-rationale">Examples: Alpha Research, BitBoard, nao Labs. These are tools that let agents summarize, monitor, report, or structure information for operators.</div>
  </div>
  <div class="rec-confidence medium">6</div>
</div>

<div class="rec-row">
  <div class="rec-number">4</div>
  <div class="rec-content">
    <div class="rec-action">Developer tooling, testing, and agent infrastructure</div>
    <div class="rec-rationale">Examples: Propolis, Docket, Kaelio, Airweave, Capacitive. This is the “make agents usable” layer: QA, testing, context, retrieval, and data access.</div>
  </div>
  <div class="rec-confidence medium">5-6</div>
</div>

---

<!-- _class: insight -->

## Representative companies: what they are actually doing

- **Anana**: agentic operating layer for hospitality revenue, sales, and ops teams.
- **Third Chair**: IP-enforcement workflow agent for legal/compliance work.
- **Propolis**: browser-agent QA and web testing automation.
- **Kaelio**: open-source context layer for data agents.
- **Pelica**: healthcare operations OS with copilots for care and provider workflows.
- **MindFort**: autonomous security agents for security teams.

<div class="finding">
  <div class="finding-headline">The pattern is “job-specific agent software”</div>
  <div class="finding-detail">Even when companies use the word agent, the product is usually a focused application layer: testing, compliance, support, analytics, scheduling, or internal operations.</div>
</div>

---

<!-- _class: takeaway -->

## Sync2-style adjacency: clinic and patient operations are real

<div class="so-what">The medical front-office / clinic-ops lane is active. The overlap is strongest around scheduling, healthcare operations, patient communication, and admin-heavy workflows.</div>

<div class="finding">
  <div class="finding-headline">Closest live YC matches for the Sync2 prompt</div>
  <div class="finding-detail">Pelica (healthcare operations with AI agents), Simbie AI (patients to next appointment), Prosper (AI phone agents for healthcare ops), Toothy AI (clinic billing / verification), Sully.ai (hospital operations).</div>
  <div class="finding-impact">Takeaway: the opportunity is real, but the market is drifting toward deeper operational ownership, not just thin front-desk wrappers.</div>
</div>

---

<!-- _class: takeaway -->

## ReprisesAI-style adjacency: the risk is verticalized implementation

<div class="so-what">There are fewer direct “AI agency” analogues. The stronger signal is companies turning implementation and process automation into productized software.</div>

<div class="finding">
  <div class="finding-headline">Closest live YC matches for the ReprisesAI prompt</div>
  <div class="finding-detail">flowscope (AI-native process consulting), Unisson (B2B software implementation agents), Lua Global (mid-market agent platform), Contour (voice-driven operational automation).</div>
  <div class="finding-impact">Takeaway: the competitive risk is not another generic agency. It is vertical tools and implementation platforms absorbing repeatable delivery work.</div>
</div>

---

<!-- _class: recommendation -->

## If you need to choose use cases, start here

<div class="rec-row">
  <div class="rec-number">1</div>
  <div class="rec-content">
    <div class="rec-action">Pick workflow automation where a team already exists</div>
    <div class="rec-rationale">This is the densest YC pattern. The winning posture is to remove repetitive work for an existing ops team, not to invent a new abstract AI category.</div>
  </div>
  <div class="rec-confidence high">HIGH</div>
</div>

<div class="rec-row">
  <div class="rec-number">2</div>
  <div class="rec-content">
    <div class="rec-action">Prefer strong data or context moats</div>
    <div class="rec-rationale">The more durable names are not just “agent wrappers.” They own context, infra, retrieval, compliance, or embedded workflow position.</div>
  </div>
  <div class="rec-confidence high">HIGH</div>
</div>

<div class="rec-row">
  <div class="rec-number">3</div>
  <div class="rec-content">
    <div class="rec-action">Treat vertical healthcare and implementation as serious lanes</div>
    <div class="rec-rationale">Healthcare ops is recurring. Productized implementation is recurring. Both point to high-friction workflows with strong willingness to pay.</div>
  </div>
  <div class="rec-confidence medium">MEDIUM</div>
</div>

<div class="rec-row">
  <div class="rec-number">4</div>
  <div class="rec-content">
    <div class="rec-action">Be cautious with generic “agent platform” positioning</div>
    <div class="rec-rationale">The live YC cohort shows better traction in job-shaped products than in broad agent claims with weak functional ownership.</div>
  </div>
  <div class="rec-confidence low">LOW</div>
</div>

---

<!-- _class: appendix -->

## Appendix: Methodology & Commands

- **Website tested:** `https://www.ycombinator.com/companies`
- **Backend discovered live from page:** public Algolia config embedded by YC
- **Current website batch on June 2, 2026:** `Spring 2026`
- **Analyzed cohort:** `Spring 2025` to mirror the original demo
- **Key commands:**
  - `./yc-companies discover`
  - `./yc-companies prompt --batch "Spring 2025" "Read every company in Y Combinator and show me the AI agent startups under 10 people."`
  - `./yc-companies analyze --query agent --batch "Spring 2025" --limit 20 --agentish`
- `./yc-companies use-cases --query agent --batch "Spring 2025" --limit 20 --agentish`
- **Important caveat:** use-case buckets are heuristic labels derived from live company text, not official YC categories.

<div class="finding">
  <div class="finding-headline">Reproducible from the repo</div>
  <div class="finding-detail">The local `yc-companies` CLI discovers the live YC backend from the public companies page each run, so the workflow can be rerun without hard-coding a private API.</div>
</div>
