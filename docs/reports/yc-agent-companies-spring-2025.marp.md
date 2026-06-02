---
marp: true
theme: analytics
size: 16:9
paginate: true
html: true
footer: "TicketForge | YC Agent Companies | June 2026"
---

# YC Agent Companies Are Job-Shaped

## Spring 2025 YC companies under 10 people

- Source tested live on June 2, 2026
- Website entry: `https://www.ycombinator.com/companies`
- Cohort used: 27 YC companies matching the "agent / agentic" pattern with team size `<= 10`

---

# Three Conclusions Matter Most

1. **Workflow automation leads.** YC founders are not mostly building generic assistants. They are wrapping agents around concrete operational jobs.
2. **Customer ops and tooling are next.** Sales ops, analytics, QA, testing, context, and infrastructure show up more often than broad "agent platform" claims.
3. **Vertical healthcare is real.** Clinic operations, claims, and patient workflow automation show enough density to treat healthcare ops as a serious lane.

---

# This Cohort Is Tiny But Focused

| Metric | What it says |
| --- | --- |
| 27 companies | Enough signal to see patterns, still early |
| Median team size: 2 | Very young companies, still choosing where to narrow |
| 13 teams with 1-2 people | Nearly half the cohort is extremely small |
| 8 teams at 5-8 people | A smaller group is already pushing beyond prototype stage |

**Interpretation:** the winners are likely being defined by use-case choice and workflow ownership, not by model novelty.

---

# Workflow Beats General Agents

| Highest-density use-case clusters | Count |
| --- | ---: |
| Workflow automation | 8 |
| Sales and customer ops | 7 |
| Analytics and reporting | 6 |
| Developer tools and testing | 6 |
| Data and agent infrastructure | 5 |

**What this means**

- The center of gravity is operational software.
- Founders are packaging agents around repetitive work, not around open-ended chat.
- The sharper the job boundary, the more credible the product.

---

# The Winning Pattern Is Narrow Ownership

**Representative examples**

- **Anana**: hotel revenue, sales, and ops workflow automation
- **Third Chair**: IP enforcement workflow agent
- **Propolis**: browser-agent QA and testing
- **BitBoard**: dashboards and reporting built by agents
- **Kaelio**: context layer for data agents
- **Pelica**: healthcare operations agents

**Takeaway:** even when the word "agent" appears, the product is usually a focused application layer with a clear owner and workflow.

---

# Tooling And Infra Are Real Wedges

| Company | Wedge |
| --- | --- |
| Propolis | QA via browser agents |
| Docket | Web testing agents |
| Capacitive | Data gateway for agents |
| Airweave | Context retrieval layer |
| Kaelio | Context layer for data agents |
| Golf | Agentic security and governance |

**Interpretation:** one durable path is enabling other agent products rather than competing as another broad app-layer assistant.

---

# Healthcare Ops Is A Serious Lane

| Company | Focus |
| --- | --- |
| Pelica | Healthcare operations with AI agents |
| Aegis | Denied claims workflow |
| Galen AI | Personal healthcare agent |
| Prosper | AI phone agents for healthcare ops |
| Toothy AI | Insurance verification and billing for clinics |

**Why it matters**

- The work is repetitive, regulated, and expensive.
- Buyers already feel the pain.
- Strong operational ownership creates clearer ROI than generic receptionist AI.

---

# Sync2 Has Real Adjacency

## Closest YC matches to the Sync2 prompt

- **Pelica**: healthcare operations agents
- **Simbie AI**: getting patients to the next appointment
- **Prosper**: AI phone agents for healthcare operations
- **Toothy AI**: insurance verification and billing at clinics
- **Sully.ai**: hospital operations agents

**Read-through for Sync2**

- The lane is real.
- The strongest YC pattern is deeper operational ownership, not a thin front-desk wrapper.
- The best opportunity is where the product can own scheduling, billing, claims, intake, or patient communication end to end.

---

# ReprisesAI Faces Productization Risk

## Closest YC matches to the ReprisesAI prompt

- **flowscope**: AI-native consulting for process automation
- **Unisson**: agents for B2B software implementation
- **Lua Global**: mid-market agent platform
- **Contour**: voice-driven operational automation

**Read-through for ReprisesAI**

- There are fewer direct "AI agency" clones.
- The bigger risk is productized implementation software absorbing repeatable service work.
- The safer posture is to specialize around a repeatable wedge, not remain a generic AI services layer.

---

# What To Learn From This Cohort

1. **Start where teams already work.** Ops, support, testing, claims, and reporting are more believable than broad agent positioning.
2. **Own context or workflow.** Data access, governance, embedded process, and vertical specificity are the moats that recur.
3. **Avoid vague platform language.** The YC signal favors job-shaped products over generic "agent OS" narratives unless there is a real infra wedge.

---

# Where I Would Focus Next

| Build direction | Why it fits the YC pattern |
| --- | --- |
| Healthcare operations | Dense adjacency, clear pain, strong willingness to pay |
| Workflow automation for existing teams | Largest cluster in the cohort |
| Tooling / context / infra | Durable enablement layer with repeatable need |
| Productized implementation | Strong hedge against agency commoditization |

**What I would avoid first:** generic "agent platform" positioning without a clear workflow owner, data moat, or vertical wedge.

---

# Method And Reproducibility

- Website tested: `https://www.ycombinator.com/companies`
- The local `yc-companies` CLI discovers the live YC backend from the public page each run
- Main demo command:
  - `./yc-companies prompt --batch "Spring 2025" --limit 100 --max-team-size 10 "Read every company in Y Combinator and show me the AI agent startups under 10 people."`
- Follow-up analysis:
  - `./yc-companies analyze --query agent --batch "Spring 2025" --limit 20 --agentish`
  - `./yc-companies use-cases --query agent --batch "Spring 2025" --limit 30 --agentish`

**Important caveat:** use-case labels are inferred from live company text. They are useful for pattern mapping, not official YC categories.
