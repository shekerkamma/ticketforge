#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REPORT_SLUG = "insurance-progressive-ai-usecases"
CREATED_AT = "2026-06-02T18:00:00Z"
DECISION_QUESTION = (
    "Which AI use cases are strongest in the insurance industry right now, "
    "and how should Progressive prioritize them as a named customer account?"
)

ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = ROOT / "research-notes" / REPORT_SLUG
ANALYTICS_DIR = ROOT / "analytics-comms" / REPORT_SLUG


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def build_source_notes() -> dict:
    sources = [
        {
            "source_id": "src-mck-future-ai-insurance-2025",
            "title": "The future of AI in the insurance industry",
            "source_type": "web",
            "locator": "https://www.mckinsey.com/industries/financial-services/our-insights/the-future-of-ai-in-the-insurance-industry",
            "captured_at": CREATED_AT,
            "author": "McKinsey",
            "published_at": "2025-07-15",
            "summary": "McKinsey argues that AI in insurance is moving from experimentation to enterprise rewiring across onboarding, service, and claims.",
            "raw_evidence": [
                {
                    "evidence_id": "e1",
                    "kind": "stat",
                    "text": "McKinsey says domain-level AI rewiring has already improved conversion, premium growth, onboarding cost, and claims accuracy for leading insurers.",
                    "locator": "turn4view2:L54",
                },
                {
                    "evidence_id": "e2",
                    "kind": "quote",
                    "text": "The report says customer onboarding can increasingly be handled by AI multiagent systems acting as virtual coworkers.",
                    "locator": "turn4view2:L41",
                },
            ],
            "claims": [
                {
                    "claim_id": "c1",
                    "statement": "Insurance AI value is strongest where workflows are repeated, document-heavy, and customer-facing.",
                    "confidence": "high",
                    "evidence_ids": ["e1", "e2"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "Customer onboarding automation",
                    "rationale": "The report explicitly highlights intake, document extraction, and service workflows.",
                },
                {
                    "label": "Claims accuracy improvement",
                    "rationale": "Claims is one of the functions with measured improvement in the report.",
                },
            ],
            "tags": ["industry", "ai", "insurance", "claims", "service"],
        },
        {
            "source_id": "src-mck-agentic-core-modernization-2026",
            "title": "Can agentic AI (finally) modernize core technologies in insurance?",
            "source_type": "web",
            "locator": "https://www.mckinsey.com/middle-east/our-insights/can-agentic-ai-finally-modernize-core-technologies-in-insurance",
            "captured_at": CREATED_AT,
            "author": "McKinsey",
            "published_at": "2026-04-29",
            "summary": "McKinsey frames agentic AI as a practical route for insurer core modernization, especially where legacy complexity blocks faster change.",
            "raw_evidence": [
                {
                    "evidence_id": "e3",
                    "kind": "quote",
                    "text": "The article says agentic AI can capture legacy knowledge, compress rework loops, and improve predictability across modernization work.",
                    "locator": "turn4view3:L13-L15",
                },
                {
                    "evidence_id": "e4",
                    "kind": "quote",
                    "text": "The article says software agents can interpret legacy artifacts, generate outputs, and coordinate work across the delivery life cycle.",
                    "locator": "turn4view3:L30-L31",
                },
            ],
            "claims": [
                {
                    "claim_id": "c2",
                    "statement": "Core modernization is now an AI use case, not just a background IT program.",
                    "confidence": "high",
                    "evidence_ids": ["e3", "e4"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "Core system modernization",
                    "rationale": "The piece directly frames agentic AI as a modernization factory.",
                }
            ],
            "tags": ["industry", "agentic-ai", "core-systems", "modernization"],
        },
        {
            "source_id": "src-mck-global-insurance-2025",
            "title": "Global Insurance Report 2025: The pursuit of growth",
            "source_type": "document",
            "locator": "https://www.mckinsey.com/~/media/mckinsey/industries/financial%20services/our%20insights/global%20insurance%20report%202025/global-insurance-report-2025-the-pursuit-of-growth.pdf",
            "captured_at": CREATED_AT,
            "author": "McKinsey",
            "published_at": "2025-01-01",
            "summary": "McKinsey argues that insurance growth will depend on distinctive operating models, stronger service capability, and AI-enabled relevance.",
            "raw_evidence": [
                {
                    "evidence_id": "e5",
                    "kind": "stat",
                    "text": "The report says personal P&C represented about 1.1 trillion dollars of gross written premiums in 2023.",
                    "locator": "turn4view4:L179-L181",
                },
                {
                    "evidence_id": "e6",
                    "kind": "quote",
                    "text": "The report says evolving technology, especially AI and gen AI, can be used to spur innovation and profitable growth.",
                    "locator": "turn4view4:L176-L177",
                },
                {
                    "evidence_id": "e7",
                    "kind": "quote",
                    "text": "McKinsey says around 60 percent of insurer performance is driven by how the company operates, not just which lines it participates in.",
                    "locator": "turn4view4:L1577-L1582",
                },
            ],
            "claims": [
                {
                    "claim_id": "c3",
                    "statement": "In insurance, operating model quality matters more than participation in any single product line.",
                    "confidence": "high",
                    "evidence_ids": ["e6", "e7"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "Operating-model-led AI",
                    "rationale": "The report links growth and profitability to distinctiveness in how insurers operate.",
                }
            ],
            "tags": ["industry", "growth", "operations", "p-and-c"],
        },
        {
            "source_id": "src-progressive-annual-report-2024",
            "title": "The Progressive Corporation 2024 Annual Report",
            "source_type": "document",
            "locator": "https://www.progressive.com/content/pdf/art/2024-annual-report.pdf",
            "captured_at": CREATED_AT,
            "author": "Progressive",
            "published_at": "2025-03-03",
            "summary": "Progressive's annual report shows a fast-growing carrier using pricing models, telematics, bundling, digital claims, and product iteration as core competitive levers.",
            "raw_evidence": [
                {
                    "evidence_id": "e8",
                    "kind": "stat",
                    "text": "Progressive ended 2024 with nearly 34 million personal-lines policies in force, up 18 percent year over year.",
                    "locator": "turn3view0:L867-L874",
                },
                {
                    "evidence_id": "e9",
                    "kind": "quote",
                    "text": "Progressive says model 8.9 adds expanded use of external data and new coverage features, with favorable conversion results.",
                    "locator": "turn3view0:L907-L920",
                },
                {
                    "evidence_id": "e10",
                    "kind": "quote",
                    "text": "Progressive says continuous monitoring in Snapshot was live in states representing about 75 percent of auto net premiums written, excluding California.",
                    "locator": "turn3view1:L925-L930",
                },
                {
                    "evidence_id": "e11",
                    "kind": "quote",
                    "text": "Progressive says its mobile app can detect major accidents, connect customers to help, and improve first notice of loss and claims resolution time.",
                    "locator": "turn3view0:L930-L937",
                },
                {
                    "evidence_id": "e12",
                    "kind": "quote",
                    "text": "Progressive identifies bundled home-and-auto customers as its largest under-penetrated property segment and says it is focusing on bundling most new business in many states.",
                    "locator": "turn3view0:L974-L979",
                },
            ],
            "claims": [
                {
                    "claim_id": "c4",
                    "statement": "Progressive already operates a real AI-ready workflow stack across pricing, telematics, claims intake, and bundle growth.",
                    "confidence": "high",
                    "evidence_ids": ["e8", "e9", "e10", "e11", "e12"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "Personalized pricing and underwriting",
                    "rationale": "The annual report highlights model upgrades, external data, and telematics coverage at scale.",
                },
                {
                    "label": "Claims intake and orchestration",
                    "rationale": "The report directly links app features to first notice of loss and shorter claims resolution time.",
                },
                {
                    "label": "Bundle growth and household expansion",
                    "rationale": "The report says bundling is a strategic growth priority.",
                },
            ],
            "tags": ["customer", "progressive", "telematics", "claims", "bundling"],
        },
        {
            "source_id": "src-progressive-june-2025-results",
            "title": "Progressive Reports June 2025 Results",
            "source_type": "web",
            "locator": "https://investors.progressive.com/financials/financial-news-releases/news-details/2025/Progressive-Reports-June-2025-Results/default.aspx",
            "captured_at": CREATED_AT,
            "author": "Progressive",
            "published_at": "2025-07-16",
            "summary": "Progressive's 2025 results show the current scale of the account and confirm that it remains one of the most important customer targets in personal and commercial auto insurance.",
            "raw_evidence": [
                {
                    "evidence_id": "e13",
                    "kind": "stat",
                    "text": "At June 30, 2025, Progressive reported 37.3 million companywide policies in force, including 36.1 million personal lines policies.",
                    "locator": "turn5view0:L241-L250",
                },
                {
                    "evidence_id": "e14",
                    "kind": "quote",
                    "text": "Progressive says it is the second largest personal auto insurer in the country and a leading seller of commercial auto insurance.",
                    "locator": "turn5view1:L256",
                },
                {
                    "evidence_id": "e15",
                    "kind": "quote",
                    "text": "Progressive says customers can buy and use insurance online, by phone, by mobile app, or through agents.",
                    "locator": "turn5view0:L254-L257",
                },
            ],
            "claims": [
                {
                    "claim_id": "c5",
                    "statement": "Progressive is a scaled, digitally distributed insurer where workflow improvements can move large policy and claims volumes.",
                    "confidence": "high",
                    "evidence_ids": ["e13", "e14", "e15"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "Omnichannel service automation",
                    "rationale": "The carrier already runs customer acquisition and servicing across multiple channels at large scale.",
                }
            ],
            "tags": ["customer", "progressive", "scale", "distribution"],
        },
        {
            "source_id": "src-progressive-telematics-page",
            "title": "How does car insurance with telematics work?",
            "source_type": "web",
            "locator": "https://www.progressive.com/answers/telematics-devices-car-insurance/",
            "captured_at": CREATED_AT,
            "author": "Progressive",
            "published_at": "2026-06-02",
            "summary": "Progressive presents Snapshot as a price-personalization engine with customer savings tied directly to driving behavior.",
            "raw_evidence": [
                {
                    "evidence_id": "e16",
                    "kind": "quote",
                    "text": "Progressive says Snapshot gives an automatic discount in most states, then a personalized rate after the first policy period.",
                    "locator": "turn4view1:L52-L55",
                },
                {
                    "evidence_id": "e17",
                    "kind": "stat",
                    "text": "Progressive says drivers who save with Snapshot save an average of 322 dollars per year.",
                    "locator": "turn4view1:L54-L55",
                },
            ],
            "claims": [
                {
                    "claim_id": "c6",
                    "statement": "Telematics is not a side product at Progressive; it is part of the pricing and retention operating model.",
                    "confidence": "high",
                    "evidence_ids": ["e16", "e17"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "Telematics-led risk selection",
                    "rationale": "The page ties driving data directly to personalized pricing.",
                }
            ],
            "tags": ["customer", "progressive", "snapshot", "pricing"],
        },
        {
            "source_id": "src-progressive-claims-page",
            "title": "Progressive claims",
            "source_type": "web",
            "locator": "https://www.progressive.com/claims/",
            "captured_at": CREATED_AT,
            "author": "Progressive",
            "published_at": "2026-06-02",
            "summary": "Progressive promotes digital claim reporting, guest claim flows, and trackable account-based claims access as part of its customer experience.",
            "raw_evidence": [
                {
                    "evidence_id": "e18",
                    "kind": "quote",
                    "text": "Progressive lets policyholders log in to report or view claims and also offers guest claim reporting.",
                    "locator": "turn4view0:L191-L205",
                }
            ],
            "claims": [
                {
                    "claim_id": "c7",
                    "statement": "Progressive already has digital claims access patterns that make claims automation and orchestration good AI candidates.",
                    "confidence": "high",
                    "evidence_ids": ["e18"],
                }
            ],
            "use_case_hints": [
                {
                    "label": "Claims self-service and orchestration",
                    "rationale": "The claim entry points are already digital and operationally structured.",
                }
            ],
            "tags": ["customer", "progressive", "claims", "self-service"],
        },
    ]

    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "decision_question": DECISION_QUESTION,
        "sources": sources,
    }


def build_analysis_pack() -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "decision_question": DECISION_QUESTION,
        "audience": "executive",
        "headline": (
            "In insurance, the most valuable AI programs are workflow-led rather than chatbot-led; "
            "for Progressive specifically, pricing and telematics, claims orchestration, bundle growth, "
            "service automation, and core modernization are the strongest executive priorities."
        ),
        "source_ids": [
            "src-mck-future-ai-insurance-2025",
            "src-mck-agentic-core-modernization-2026",
            "src-mck-global-insurance-2025",
            "src-progressive-annual-report-2024",
            "src-progressive-june-2025-results",
            "src-progressive-telematics-page",
            "src-progressive-claims-page",
        ],
        "findings": [
            {
                "finding_id": "f1",
                "title": "Insurance AI is becoming a workflow and operating-model decision",
                "statement": "Industry evidence points to onboarding, claims, underwriting, and modernization as the highest-value AI lanes because they are repeated, document-heavy, and measurable.",
                "implication": "Executives should fund AI where it improves throughput, loss economics, or service speed rather than only where it creates visible demos.",
                "confidence": "high",
                "source_ids": [
                    "src-mck-future-ai-insurance-2025",
                    "src-mck-global-insurance-2025",
                    "src-mck-agentic-core-modernization-2026",
                ],
            },
            {
                "finding_id": "f2",
                "title": "Progressive is already operating the raw ingredients for scaled AI",
                "statement": "Progressive combines model iteration, telematics, app-based service, omnichannel distribution, and large policy volume in a way that makes workflow AI economically meaningful.",
                "implication": "The right pitch to Progressive is not generic AI transformation; it is targeted operating leverage on top of existing digital flows.",
                "confidence": "high",
                "source_ids": [
                    "src-progressive-annual-report-2024",
                    "src-progressive-june-2025-results",
                    "src-progressive-telematics-page",
                    "src-progressive-claims-page",
                ],
            },
            {
                "finding_id": "f3",
                "title": "Telematics and product models are the clearest pricing-and-underwriting wedge",
                "statement": "Progressive's annual report and Snapshot materials show that external data, continuous monitoring, and personalized pricing are already central to the customer proposition.",
                "implication": "AI that sharpens risk selection, pricing segmentation, or conversion quality is directly aligned with Progressive's current model.",
                "confidence": "high",
                "source_ids": [
                    "src-progressive-annual-report-2024",
                    "src-progressive-telematics-page",
                ],
            },
            {
                "finding_id": "f4",
                "title": "Claims orchestration is a high-value lane because the claim journey is already digital",
                "statement": "Progressive already supports account-based claim access, guest flows, app-based accident response, and faster first notice of loss.",
                "implication": "Claims AI should focus on triage, routing, documentation, next-best action, and cycle-time reduction instead of generic summaries alone.",
                "confidence": "high",
                "source_ids": [
                    "src-progressive-annual-report-2024",
                    "src-progressive-claims-page",
                ],
            },
            {
                "finding_id": "f5",
                "title": "Bundle growth and customer-lifecycle AI are underappreciated executive opportunities",
                "statement": "Progressive explicitly calls bundled home-and-auto households its largest under-penetrated property segment and is pushing bundle-first growth motions.",
                "implication": "Cross-line recommendation, propensity, retention, and service orchestration use cases should be treated as strategic growth levers, not side analytics projects.",
                "confidence": "high",
                "source_ids": [
                    "src-progressive-annual-report-2024",
                    "src-progressive-june-2025-results",
                ],
            },
        ],
        "use_case_clusters": [
            {
                "cluster_id": "uc1",
                "name": "Telematics-led pricing and underwriting",
                "buyer": "Chief underwriting officer or head of personal auto",
                "workflow_owner": "Pricing, product, and telematics teams",
                "business_job": "Use behavioral and external data to price more accurately, improve conversion quality, and sharpen retention.",
                "value_prop": "Raises underwriting precision while preserving Progressive's direct-to-consumer growth engine.",
                "why_now": "Progressive already has continuous monitoring at scale and product models that expand external-data use.",
                "recommendation": "Position AI as an extension of Progressive's existing risk and pricing machine rather than as a new standalone platform.",
                "evidence_companies": [
                    {
                        "name": "Progressive",
                        "proof_line": "Snapshot continuous monitoring is live across most of Progressive's auto premium footprint and supports personalized pricing.",
                        "source_id": "src-progressive-annual-report-2024",
                    }
                ],
            },
            {
                "cluster_id": "uc2",
                "name": "Claims intake, triage, and resolution orchestration",
                "buyer": "Chief claims officer",
                "workflow_owner": "Claims operations, first notice of loss, and digital experience teams",
                "business_job": "Accelerate claim intake, evidence gathering, routing, and customer updates while improving resolution speed.",
                "value_prop": "Reduces cycle time and service friction in one of the most visible insurance workflows.",
                "why_now": "Progressive already has digital claim entry, app-triggered accident response, and explicit goals around faster first notice of loss.",
                "recommendation": "Lead with orchestration and cycle-time outcomes rather than general-purpose assistant messaging.",
                "evidence_companies": [
                    {
                        "name": "Progressive",
                        "proof_line": "The mobile app can detect major accidents and is intended to accelerate first notice of loss and reduce claims resolution time.",
                        "source_id": "src-progressive-annual-report-2024",
                    }
                ],
            },
            {
                "cluster_id": "uc3",
                "name": "Bundle growth and household expansion",
                "buyer": "Chief growth officer or head of property",
                "workflow_owner": "Cross-sell, marketing, and household product teams",
                "business_job": "Grow bundled relationships by identifying the right households, timing, and offer sequences across auto and property.",
                "value_prop": "Turns a large under-penetrated customer segment into a measurable growth program.",
                "why_now": "Progressive says bundled home-and-auto customers are its largest under-penetrated property segment and is focusing new business on bundling.",
                "recommendation": "Treat bundle AI as a revenue and lifetime-value use case, not just a marketing optimization exercise.",
                "evidence_companies": [
                    {
                        "name": "Progressive",
                        "proof_line": "The annual report explicitly prioritizes bundled home-and-auto growth in many states.",
                        "source_id": "src-progressive-annual-report-2024",
                    }
                ],
            },
            {
                "cluster_id": "uc4",
                "name": "Service automation across direct, app, and agent channels",
                "buyer": "Chief operating officer or head of customer experience",
                "workflow_owner": "Service operations, digital experience, and contact center teams",
                "business_job": "Automate routine service interactions, route work intelligently, and keep service quality consistent across channels.",
                "value_prop": "Improves service cost-to-serve and customer convenience without disrupting channel choice.",
                "why_now": "Progressive serves customers through web, phone, mobile app, and agents, making consistent orchestration increasingly valuable.",
                "recommendation": "Frame AI here as channel orchestration and service productivity, not just chatbot containment.",
                "evidence_companies": [
                    {
                        "name": "Progressive",
                        "proof_line": "Progressive highlights online, phone, mobile-app, and agent access as core parts of the customer model.",
                        "source_id": "src-progressive-june-2025-results",
                    }
                ],
            },
            {
                "cluster_id": "uc5",
                "name": "Core technology and product-model modernization",
                "buyer": "Chief information officer or chief technology officer",
                "workflow_owner": "Platform engineering, rating, and legacy modernization teams",
                "business_job": "Use AI and agentic workflows to upgrade product logic, documentation, testing, and release processes without full-stop replacement programs.",
                "value_prop": "Shortens modernization cycles and makes product iteration more repeatable.",
                "why_now": "Industry research increasingly treats agentic AI as a modernization tool, and Progressive is already iterating product models quickly.",
                "recommendation": "Tie modernization AI to concrete release, documentation, testing, and rework metrics so it lands as an executive operating program.",
                "evidence_companies": [
                    {
                        "name": "Progressive",
                        "proof_line": "Progressive is already running successive product-model versions and expanding external-data use in auto product releases.",
                        "source_id": "src-progressive-annual-report-2024",
                    }
                ],
            },
        ],
        "risks": [
            "Public sources are stronger on strategic signals than on internal failure modes or system constraints.",
            "Insurance AI still faces regulatory, fairness, and model-governance scrutiny, especially in pricing and claims.",
            "Progressive may already be building internally in some lanes, so external pitches need a differentiated workflow angle rather than generic transformation language.",
        ],
        "recommendations": [
            {
                "title": "Lead with workflow economics, not AI novelty",
                "why": "The strongest case for insurance AI is cycle time, pricing precision, service productivity, and growth conversion.",
                "priority": "high",
            },
            {
                "title": "Anchor the account around Progressive's existing digital assets",
                "why": "Snapshot, product models, app-based claims, and bundling priorities already define where the customer is prepared to act.",
                "priority": "high",
            },
            {
                "title": "Package claims and service as orchestration programs",
                "why": "Progressive already has digital entry points, so AI should improve routing, documentation, and next-step execution.",
                "priority": "high",
            },
            {
                "title": "Treat modernization as a business-use-case enabler",
                "why": "Core-system and product-model velocity determine how quickly insurance AI can scale beyond pilots.",
                "priority": "medium",
            },
        ],
        "chart_briefs": [
            {
                "title": "Highest-value AI lanes for Progressive",
                "best_chart_type": "bar",
                "why_this_fits": "The audience needs a simple ranked view of where the account is most likely to create value.",
                "narrative_takeaway": "Pricing and telematics, claims orchestration, bundle growth, service automation, and modernization are the strongest lanes.",
                "encoding_guidance": "Rank the lanes from highest executive value to lower near-term value and highlight the top two.",
                "annotation_plan": "Annotate each bar with the Progressive proof point: Snapshot scale, FNOL acceleration, bundling priority, omnichannel service, or model iteration.",
            },
            {
                "title": "Industry AI hype versus insurance workflow value",
                "best_chart_type": "comparison",
                "why_this_fits": "Executives need to see why generic assistants are weaker than workflow-led use cases.",
                "narrative_takeaway": "Insurance value comes from underwriting, claims, service, and modernization workflows, not generic chatbot rollouts alone.",
                "encoding_guidance": "Contrast broad assistant narratives with operating-model-led programs tied to measurable economics.",
                "annotation_plan": "Call out revenue, loss ratio, cycle time, and cost-to-serve as the decisive metrics.",
            },
            {
                "title": "Customer fit: Progressive's readiness by use-case cluster",
                "best_chart_type": "bar",
                "why_this_fits": "The audience needs a customer-specific fit view rather than a generic industry taxonomy.",
                "narrative_takeaway": "Progressive is strongest where digital flow, product iteration, and policy scale already exist.",
                "encoding_guidance": "Show relative readiness across the five clusters using a simple ordinal score.",
                "annotation_plan": "Use short labels tied to policy scale, digital entry points, or strategic emphasis in public materials.",
            },
        ],
        "methodology": {
            "approach": "Cross-source synthesis using current McKinsey insurance AI research and Progressive official investor, annual-report, claims, and telematics materials, framed as an executive account strategy and use-case prioritization readout.",
            "limitations": [
                "This is a public-source strategic account readout, not an internal due-diligence package or live customer interview synthesis.",
                "The deck prioritizes executive decisions and use-case selection rather than vendor-level product mapping or implementation architecture.",
            ],
        },
    }


def slide(slide_id: str, section: str, slide_type: str, title: str, objective: str, layout: str, content_blocks: list[dict], source_ids: list[str]) -> dict:
    return {
        "slide_id": slide_id,
        "section": section,
        "slide_type": slide_type,
        "title": title,
        "objective": objective,
        "audience": "executive",
        "layout": layout,
        "content_blocks": content_blocks,
        "source_ids": source_ids,
    }


def build_deck_plan() -> dict:
    slides = [
        slide("s1", "Opening", "hero", "Insurance AI Use Cases For Progressive", "Lead with the main thesis.", "hero", [
            {"kind": "summary", "label": "Subtitle", "body": "Industry + customer + executive action"},
            {"kind": "summary", "label": "Strapline", "body": "For insurance, the most valuable AI programs are workflow-led. For Progressive, the strongest priorities are pricing and telematics, claims orchestration, bundle growth, service automation, and core modernization."},
        ], ["src-mck-future-ai-insurance-2025", "src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s2", "Agenda", "agenda", "What This Deck Covers", "Set the readout sequence.", "list", [
            {"kind": "agenda-item", "label": "Market shift", "body": "Why insurance AI has moved from experimentation to workflow and operating-model change."},
            {"kind": "agenda-item", "label": "Customer lens", "body": "Why Progressive is a strong named-customer target."},
            {"kind": "agenda-item", "label": "Use-case priorities", "body": "Which AI programs map best to Progressive's economics and workflows."},
            {"kind": "agenda-item", "label": "Executive action", "body": "What to fund, what to defer, and what to measure."},
        ], ["src-mck-future-ai-insurance-2025", "src-progressive-june-2025-results"]),
        slide("s3", "Market Shift", "section-divider", "Insurance AI Is An Operating Model Decision", "Open the industry section.", "section", [
            {"kind": "callout", "label": "Section note", "body": "The strongest insurance AI programs are no longer side pilots. They sit in underwriting, claims, service, growth, and modernization workflows that move real economics."},
        ], ["src-mck-future-ai-insurance-2025", "src-mck-global-insurance-2025", "src-mck-agentic-core-modernization-2026"]),
        slide("s4", "Executive Summary", "summary-cards", "Four Executive Conclusions", "Summarize the top takeaways.", "2x2-card-grid", [
            {"kind": "summary", "label": "Workflow AI beats chatbot AI", "body": "Insurance value comes from underwriting, claims, service, and modernization workflows with measurable economics."},
            {"kind": "summary", "label": "Progressive is already AI-ready", "body": "The account already runs telematics, product-model iteration, digital claims, and omnichannel service at scale."},
            {"kind": "summary", "label": "Pricing and claims are the top wedges", "body": "These lanes map best to Progressive's current model and to the industry's highest-value patterns."},
            {"kind": "summary", "label": "Bundle growth is the hidden opportunity", "body": "Progressive explicitly treats bundled home-and-auto households as an under-penetrated strategic segment."},
        ], ["src-mck-future-ai-insurance-2025", "src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s5", "Industry Metrics", "kpi-grid", "Why The Insurance Market Supports This Bet", "Compress the market signal.", "four-metric-grid", [
            {"kind": "metric", "label": "Personal P&C premiums", "body": "$1.1T|McKinsey says personal P&C represented about 1.1 trillion dollars of GWP in 2023."},
            {"kind": "metric", "label": "Claims accuracy uplift", "body": "3-5%|McKinsey cites claims accuracy improvement from domain-level AI rewiring."},
            {"kind": "metric", "label": "Onboarding cost reduction", "body": "20-40%|McKinsey cites lower onboarding cost in leading AI programs."},
            {"kind": "metric", "label": "Operations drive performance", "body": "60%|McKinsey says around 60 percent of insurer performance is driven by how the company operates."},
            {"kind": "callout", "label": "Takeaway", "body": "This is a large market where process quality and operating-model quality dominate outcomes."},
        ], ["src-mck-global-insurance-2025", "src-mck-future-ai-insurance-2025"]),
        slide("s6", "Interpretation", "comparison", "Insurance AI: Old Framing Versus Executive Reality", "Contrast hype with operating reality.", "two-column-comparison", [
            {"kind": "comparison-column", "label": "Weak framing", "body": "Generic chatbot launch|Small copilots with no owner|Innovation theater|No tie to pricing, claims, or growth"},
            {"kind": "comparison-column", "label": "Strong framing", "body": "Workflow automation with owners|AI inside underwriting and claims|Measured economics|Modernization that enables repeated change"},
        ], ["src-mck-future-ai-insurance-2025", "src-mck-agentic-core-modernization-2026", "src-mck-global-insurance-2025"]),
        slide("s7", "Industry Thesis", "bullets", "What Actually Creates Value In Insurance", "State the operating thesis.", "bullet-list", [
            {"kind": "bullet", "label": "Repeated workflow", "body": "The best lanes are repeated, high-volume, document-heavy, and already instrumented."},
            {"kind": "bullet", "label": "Decision quality", "body": "Value comes from better pricing, faster claims, sharper routing, and lower cost-to-serve."},
            {"kind": "bullet", "label": "Data loop", "body": "The strongest insurers connect customer, policy, claims, and servicing data into one feedback loop."},
            {"kind": "bullet", "label": "Operating system", "body": "AI becomes durable when it changes how the insurer operates, not just how it communicates."},
        ], ["src-mck-future-ai-insurance-2025", "src-mck-global-insurance-2025"]),
        slide("s8", "Customer Lens", "section-divider", "Why Progressive Is The Right Customer To Anchor", "Transition into the account section.", "section", [
            {"kind": "callout", "label": "Section note", "body": "Progressive is not a generic insurance target. It is a scaled, digitally distributed carrier already optimized around pricing, telematics, and workflow speed."},
        ], ["src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s9", "Customer Summary", "summary-cards", "Progressive In One Slide", "Summarize customer context.", "2x2-card-grid", [
            {"kind": "summary", "label": "Scaled carrier", "body": "Progressive reported 37.3 million companywide policies in force at June 30, 2025."},
            {"kind": "summary", "label": "Digital distribution", "body": "Customers buy and use insurance online, by phone, by app, or through agents."},
            {"kind": "summary", "label": "Usage-based edge", "body": "Snapshot and continuous monitoring are part of the current operating model, not a side experiment."},
            {"kind": "summary", "label": "Growth agenda", "body": "Progressive is pushing product iteration, new business growth, and bundling in under-penetrated segments."},
        ], ["src-progressive-june-2025-results", "src-progressive-annual-report-2024", "src-progressive-telematics-page"]),
        slide("s10", "Customer Metrics", "kpi-grid", "Progressive Signals That Matter", "Quantify the customer.", "four-metric-grid", [
            {"kind": "metric", "label": "Companywide policies in force", "body": "37.3M|June 30, 2025 results"},
            {"kind": "metric", "label": "Total personal lines PIF", "body": "36.1M|June 30, 2025 results"},
            {"kind": "metric", "label": "Snapshot average savings", "body": "$322|Progressive telematics page"},
            {"kind": "metric", "label": "Snapshot continuous monitoring footprint", "body": "75%|Of auto net premiums written, excluding California"},
            {"kind": "callout", "label": "Takeaway", "body": "Progressive already has the scale and digital instrumentation to justify workflow-led AI investment."},
        ], ["src-progressive-june-2025-results", "src-progressive-telematics-page", "src-progressive-annual-report-2024"]),
        slide("s11", "Customer Interpretation", "comparison", "Why Progressive Is Different From A Generic Carrier", "Clarify account fit.", "two-column-comparison", [
            {"kind": "comparison-column", "label": "Generic insurer pitch", "body": "Broad transformation story|High-level service bot demos|No clear account wedge|Weak tie to current workflows"},
            {"kind": "comparison-column", "label": "Progressive-specific pitch", "body": "Pricing and telematics leverage|Claims orchestration|Bundle growth expansion|Service and modernization tied to scale economics"},
        ], ["src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s12", "Use Case Ranking", "section-divider", "Where Progressive Should Prioritize AI", "Transition into ranked use cases.", "section", [
            {"kind": "callout", "label": "Section note", "body": "The right ordering is not based on novelty. It is based on account fit, measurable economics, and readiness of the existing workflow."},
        ], ["src-progressive-annual-report-2024", "src-progressive-telematics-page", "src-progressive-claims-page"]),
        slide("s13", "Ranking", "bar-chart", "Highest-Value AI Lanes For Progressive", "Rank use-case clusters.", "horizontal-bar", [
            {"kind": "chart-brief", "label": "Telematics-led pricing and underwriting", "body": "98"},
            {"kind": "chart-brief", "label": "Claims intake and resolution orchestration", "body": "95"},
            {"kind": "chart-brief", "label": "Bundle growth and household expansion", "body": "90"},
            {"kind": "chart-brief", "label": "Service automation across channels", "body": "86"},
            {"kind": "chart-brief", "label": "Core technology and product-model modernization", "body": "82"},
        ], ["src-progressive-annual-report-2024", "src-progressive-telematics-page", "src-progressive-claims-page", "src-mck-agentic-core-modernization-2026"]),
        slide("s14", "Use Cases", "use-case-card-grid", "Business Use Cases That Matter Most", "Summarize the use cases in one table.", "two-column-table", [
            {"kind": "table-row", "label": "Telematics pricing and underwriting", "body": "Use behavioral and external data to improve risk selection, conversion quality, and retention."},
            {"kind": "table-row", "label": "Claims orchestration", "body": "Automate intake, evidence routing, next-best action, and customer updates to cut cycle time."},
            {"kind": "table-row", "label": "Bundle growth", "body": "Identify the right households and moments for home-plus-auto expansion and retention."},
            {"kind": "table-row", "label": "Service automation", "body": "Improve routing and routine issue handling across web, app, phone, and agent channels."},
            {"kind": "table-row", "label": "Modernization factory", "body": "Use agentic workflows to accelerate product logic, testing, documentation, and release work."},
        ], ["src-progressive-annual-report-2024", "src-progressive-june-2025-results", "src-mck-future-ai-insurance-2025", "src-mck-agentic-core-modernization-2026"]),
        slide("s15", "Use Cases", "customer-fit", "Industry Need Versus Progressive Fit", "Tie general industry need to customer-specific fit.", "two-column-comparison", [
            {"kind": "comparison-column", "label": "Industry need", "body": "Better pricing|Faster claims|Cheaper service|Smarter growth|Faster change"},
            {"kind": "comparison-column", "label": "Progressive fit", "body": "Snapshot and external data|Digital FNOL and accident response|Omnichannel servicing|Bundle-first expansion|Rapid product-model iteration"},
        ], ["src-mck-future-ai-insurance-2025", "src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s16", "Deep Dives", "section-divider", "Five Priority Programs", "Open the deep-dive section.", "section", [
            {"kind": "callout", "label": "Section note", "body": "Each of these programs already has an owner, a measurable business job, and evidence that Progressive is ready to act."},
        ], ["src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s17", "Deep Dive", "use-case-deep-dive", "Use Case 01: Telematics-Led Pricing", "Explain the pricing wedge.", "case-study", [
            {"kind": "company-card", "label": "Current account signal", "body": "Snapshot provides automatic discounting and personalized pricing, while continuous monitoring covers most of Progressive's auto premium base."},
            {"kind": "company-card", "label": "Executive logic", "body": "This is already core to Progressive's customer proposition, so incremental AI here maps directly to underwriting and growth economics."},
            {"kind": "company-card", "label": "What to sell", "body": "Risk segmentation, quote quality, pricing optimization, and retention interventions tied to telematics behavior."},
            {"kind": "bullet-list", "label": "Implications", "body": "Lead with measurable lift in risk selection|Tie the program to conversion and retention|Do not pitch this as a generic personalization layer"},
        ], ["src-progressive-telematics-page", "src-progressive-annual-report-2024"]),
        slide("s18", "Deep Dive", "use-case-deep-dive", "Use Case 02: Claims Orchestration", "Explain the claims wedge.", "case-study", [
            {"kind": "company-card", "label": "Current account signal", "body": "Progressive already supports digital claim access, guest claim reporting, app-based accident response, and faster FNOL goals."},
            {"kind": "company-card", "label": "Executive logic", "body": "Claims is a visible customer workflow where cycle time, routing quality, and service quality all matter financially."},
            {"kind": "company-card", "label": "What to sell", "body": "Triage, document extraction, claim summarization, next-best action, and claimant communication orchestration."},
            {"kind": "bullet-list", "label": "Implications", "body": "Anchor on cycle time and service metrics|Stay close to existing digital entry points|Frame AI as workflow execution, not just summarization"},
        ], ["src-progressive-annual-report-2024", "src-progressive-claims-page"]),
        slide("s19", "Deep Dive", "use-case-deep-dive", "Use Case 03: Bundle Growth", "Explain the growth wedge.", "case-study", [
            {"kind": "company-card", "label": "Current account signal", "body": "Progressive says bundled home-and-auto households are its largest under-penetrated property segment and is actively prioritizing bundles."},
            {"kind": "company-card", "label": "Executive logic", "body": "This is a revenue and lifetime-value program, not just a marketing optimization problem."},
            {"kind": "company-card", "label": "What to sell", "body": "Household propensity models, timing recommendations, agent prompts, and cross-channel offer orchestration."},
            {"kind": "bullet-list", "label": "Implications", "body": "Position this as growth infrastructure|Tie the motion to household expansion and retention|Connect service and distribution data"},
        ], ["src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s20", "Deep Dive", "use-case-deep-dive", "Use Case 04: Service Automation", "Explain the service wedge.", "case-study", [
            {"kind": "company-card", "label": "Current account signal", "body": "Progressive serves customers online, by app, by phone, and through agents, making orchestration a real operational challenge."},
            {"kind": "company-card", "label": "Executive logic", "body": "The value is lower cost-to-serve and more consistent issue resolution across channels."},
            {"kind": "company-card", "label": "What to sell", "body": "Routing, service summarization, task automation, and agent-assist flows that preserve channel choice."},
            {"kind": "bullet-list", "label": "Implications", "body": "Do not over-index on chatbot containment|Show how orchestration lowers handling time|Keep human escalation explicit"},
        ], ["src-progressive-june-2025-results", "src-mck-future-ai-insurance-2025"]),
        slide("s21", "Deep Dive", "use-case-deep-dive", "Use Case 05: Core Modernization", "Explain the modernization wedge.", "case-study", [
            {"kind": "company-card", "label": "Current account signal", "body": "Progressive is already iterating product models and external-data logic, which makes faster documentation, testing, and release work economically relevant."},
            {"kind": "company-card", "label": "Executive logic", "body": "Modernization is a business enabler because it determines how quickly the carrier can scale other AI programs."},
            {"kind": "company-card", "label": "What to sell", "body": "Agentic documentation, legacy knowledge capture, test generation, and release orchestration."},
            {"kind": "bullet-list", "label": "Implications", "body": "Tie this to throughput and rework|Frame it as a modernization factory|Keep controls and auditability explicit"},
        ], ["src-mck-agentic-core-modernization-2026", "src-progressive-annual-report-2024"]),
        slide("s22", "Executive Action", "section-divider", "What Executives Should Do Now", "Open the action section.", "section", [
            {"kind": "callout", "label": "Section note", "body": "The main executive job is sequencing: invest where Progressive already has data, workflow ownership, and measurable value pools."},
        ], ["src-progressive-annual-report-2024", "src-mck-global-insurance-2025"]),
        slide("s23", "Recommendations", "summary-cards", "Four Executive Moves", "Condense the recommended actions.", "2x2-card-grid", [
            {"kind": "summary", "label": "Fund pricing and telematics first", "body": "This is the cleanest fit with Progressive's current model and strongest economics."},
            {"kind": "summary", "label": "Package claims as orchestration", "body": "Lead with FNOL, routing, documentation, and service quality, not generic AI claims summaries."},
            {"kind": "summary", "label": "Treat bundle AI as a growth program", "body": "Use household and cross-line orchestration to attack a segment Progressive has already named as strategic."},
            {"kind": "summary", "label": "Use modernization to unlock scale", "body": "Support all other AI programs with faster product, testing, and documentation cycles."},
        ], ["src-progressive-annual-report-2024", "src-progressive-telematics-page", "src-progressive-claims-page", "src-mck-agentic-core-modernization-2026"]),
        slide("s24", "Roadmap", "executive-action", "Suggested Sequencing", "Show an execution order.", "roadmap", [
            {"kind": "roadmap-step", "label": "1", "body": "Land pricing and claims pilots|Start with the two workflows that already have strong digital exhaust and obvious financial metrics."},
            {"kind": "roadmap-step", "label": "2", "body": "Expand into bundle growth and service orchestration|Use the first wave to unify household and service data across channels."},
            {"kind": "roadmap-step", "label": "3", "body": "Stand up modernization factory capabilities|Use agentic delivery patterns to accelerate the product and platform layer underneath the business use cases."},
            {"kind": "roadmap-step", "label": "4", "body": "Institutionalize governance and KPI review|Track lift in pricing quality, claims cycle time, bundle conversion, and service cost-to-serve."},
        ], ["src-progressive-annual-report-2024", "src-mck-agentic-core-modernization-2026", "src-mck-future-ai-insurance-2025"]),
        slide("s25", "Risks", "bar-chart", "Where Execution Can Fail", "Rank the main risks.", "horizontal-bar", [
            {"kind": "chart-brief", "label": "Pitching generic AI instead of workflow AI", "body": "95"},
            {"kind": "chart-brief", "label": "Ignoring regulatory and model-governance needs", "body": "90"},
            {"kind": "chart-brief", "label": "Treating modernization as separate from use cases", "body": "84"},
            {"kind": "chart-brief", "label": "Overpromising without account-specific differentiation", "body": "80"},
        ], ["src-mck-future-ai-insurance-2025", "src-mck-agentic-core-modernization-2026", "src-progressive-annual-report-2024"]),
        slide("s26", "Caveats", "comparison", "What To Fund Versus What To Defer", "Clarify prioritization discipline.", "two-column-comparison", [
            {"kind": "comparison-column", "label": "Fund now", "body": "Pricing and telematics|Claims orchestration|Bundle growth|Service workflow automation"},
            {"kind": "comparison-column", "label": "Defer or narrow", "body": "Generic enterprise chatbots|Unowned copilots|Broad transformation programs with no workflow metrics|Standalone innovation pilots"},
        ], ["src-mck-future-ai-insurance-2025", "src-progressive-annual-report-2024", "src-progressive-june-2025-results"]),
        slide("s27", "Methodology", "bullets", "Methodology And Source Coverage", "Close with evidence and limits.", "bullet-list", [
            {"kind": "bullet", "label": "Industry sources", "body": "McKinsey insurance AI and insurance growth research from July 2025, January 2025, and April 2026."},
            {"kind": "bullet", "label": "Customer sources", "body": "Progressive annual report, June 2025 results, telematics page, and claims page."},
            {"kind": "bullet", "label": "What this is", "body": "A public-source executive account and use-case prioritization readout."},
            {"kind": "bullet", "label": "What this is not", "body": "It is not a vendor bake-off, implementation plan, or internal systems assessment."},
        ], ["src-mck-future-ai-insurance-2025", "src-mck-global-insurance-2025", "src-mck-agentic-core-modernization-2026", "src-progressive-annual-report-2024", "src-progressive-june-2025-results", "src-progressive-telematics-page", "src-progressive-claims-page"]),
    ]

    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "audience": "executive",
        "deck_goal": "Produce a research-backed executive deck on AI use cases in insurance, anchored on Progressive as the named customer.",
        "theme_reference": "Use the branded executive slide system already established in this repo.",
        "story_arc": [
            "Why the market has shifted",
            "Why Progressive is the right customer lens",
            "Which use cases matter most",
            "What executives should do next",
        ],
        "slides": slides,
        "export_targets": ["pptx", "html", "memo"],
    }

def build_strategy_brief() -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "decision": "Prioritize pricing and telematics, claims orchestration, bundle growth, service automation, and modernization as Progressive's top AI programs.",
        "why_this_matters": "Insurance AI is now an operating-model question tied to pricing precision, claims speed, service productivity, and product-change velocity.",
        "executive_view": "Progressive is a strong named customer because it already combines large policy volume, telematics, digital claims, omnichannel service, and explicit growth priorities.",
        "strategic_implications": [
            "The best AI opportunities are acceleration opportunities on top of existing workflows, not greenfield experiments.",
            "Pricing and claims should lead because they are closest to measurable economics and already have digital exhaust and workflow ownership.",
            "Bundle growth is a real cross-line growth wedge because Progressive has already named it as strategic.",
            "Modernization is the multiplier because it determines how quickly every other AI program compounds."
        ],
        "recommended_actions": [
            {
                "title": "Fund pricing and claims first",
                "why": "These two lanes map most directly to measurable economics and workflow readiness.",
                "priority": "high"
            },
            {
                "title": "Package bundle growth as a revenue and retention program",
                "why": "Household expansion is already a named strategic priority.",
                "priority": "high"
            },
            {
                "title": "Treat service AI as orchestration, not only containment",
                "why": "Progressive already serves customers across multiple channels, so routing and task execution matter more than generic chat.",
                "priority": "medium"
            },
            {
                "title": "Tie modernization to release speed, documentation, and test throughput",
                "why": "Modernization is the enabler that lets the other AI programs scale beyond pilots.",
                "priority": "medium"
            }
        ],
        "kpis": [
            "pricing lift and conversion quality",
            "claims cycle time",
            "bundle conversion and household retention",
            "service cost-to-serve",
            "release and testing throughput"
        ],
        "bottom_line": "The right executive story for Progressive is AI that improves the insurance operating system, not AI that sits on top of it."
    }


def build_customer_brief() -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "customer_scope": "named-customer",
        "customer_label": "The Progressive Corporation",
        "why_this_customer_matters": "Progressive combines scale, digital distribution, telematics, claims workflow instrumentation, and a clear growth agenda.",
        "public_signals": [
            "Second largest personal auto insurer in the United States",
            "Leading seller of commercial auto insurance",
            "37.3 million companywide policies in force as of June 30, 2025",
            "Snapshot telematics and continuous monitoring at scale",
            "App-based accident response and digital claim access",
            "Explicit bundle-growth focus in property"
        ],
        "executive_priorities": [
            "pricing precision and conversion quality",
            "claims experience and cycle time",
            "growth in bundled households",
            "cost-to-serve discipline across channels",
            "faster product and platform iteration"
        ],
        "workflow_owners": [
            "underwriting and product leaders",
            "claims operations leadership",
            "growth and household / bundle teams",
            "digital experience and service operations",
            "platform and modernization leaders"
        ],
        "best_entry_points": [
            "chief underwriting and product leaders",
            "claims operations leadership",
            "growth and household / bundle teams",
            "digital experience and service operations",
            "platform and modernization leaders"
        ],
        "best_use_case_angles": [
            "telematics-driven underwriting",
            "claims orchestration",
            "bundle propensity and household expansion",
            "service routing and automation",
            "modernization factory workflows"
        ]
    }


def build_executive_angle() -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "primary_audience": "business executives",
        "lead_with": [
            "measurable economics",
            "workflow ownership",
            "sequencing",
            "what to fund now"
        ],
        "avoid_leading_with": [
            "abstract transformation language",
            "generic copilots",
            "vendor taxonomy",
            "speculative moonshots without operating ownership"
        ],
        "decision_frame": "Frame the deck as an operating-model and prioritization decision, not as a tour of AI features."
    }


def build_use_case_priorities() -> dict:
    return {
        "report_slug": REPORT_SLUG,
        "created_at": CREATED_AT,
        "prioritization_basis": "account fit, measurable economics, and workflow readiness",
        "tiers": {
            "tier_1": [
                "telematics-led pricing and underwriting",
                "claims intake and resolution orchestration"
            ],
            "tier_2": [
                "bundle growth and household expansion",
                "service automation across channels"
            ],
            "tier_3": [
                "modernization factory workflows that accelerate the other tiers"
            ]
        },
        "rationale": "The order follows account fit, measurable economics, and workflow readiness rather than novelty."
    }


def main() -> int:
    write_json(RESEARCH_DIR / "source-notes.json", build_source_notes())
    write_json(ANALYTICS_DIR / "analysis-pack.json", build_analysis_pack())
    write_json(ANALYTICS_DIR / "deck-plan.json", build_deck_plan())
    write_json(ANALYTICS_DIR / "strategy-brief.json", build_strategy_brief())
    write_json(ANALYTICS_DIR / "customer-brief.json", build_customer_brief())
    write_json(ANALYTICS_DIR / "executive-angle.json", build_executive_angle())
    write_json(ANALYTICS_DIR / "use-case-priorities.json", build_use_case_priorities())
    print(REPORT_SLUG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
