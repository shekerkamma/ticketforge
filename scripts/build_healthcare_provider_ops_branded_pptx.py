#!/usr/bin/env python3
"""Build a branded, PowerPoint-native healthcare provider-ops AI deck.

This uses the local branded-pptx-deck toolkit instead of the generic deck-plan
renderer so the output is authored as a real PPTX with slide-specific layouts.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for candidate in [
    ROOT / ".claude" / "skills" / "branded-pptx-deck" / "scripts",
    Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts"),
    Path.home() / ".claude" / "skills" / "branded-pptx-deck" / "scripts",
]:
    if candidate.exists():
        sys.path.insert(0, str(candidate))

from pptxkit import Deck, Inches, MSO_ANCHOR, PP_ALIGN, hx  # type: ignore

ANALYSIS = ROOT / "analytics-comms" / "healthcare-provider-ops-ai-usecases" / "analysis-pack.json"
SOURCE_NOTES = ROOT / "research-notes" / "healthcare-provider-ops-ai-usecases" / "source-notes.json"
OUT = ROOT / "docs" / "reports" / "healthcare-provider-ops-ai-usecases-branded.pptx"
CHART_DIR = ROOT / "docs" / "reports" / "_chart_assets" / "healthcare-provider-ops"
FOOTER_TEXT = "Healthcare Provider Operations AI Use Cases  |  Research-backed executive deck  |  June 2026"
TOTAL = 29


with ANALYSIS.open() as fh:
    analysis = json.load(fh)
with SOURCE_NOTES.open() as fh:
    source_notes = json.load(fh)

d = Deck(footer=FOOTER_TEXT)
b = d.b

CORAL = b.CORAL
AMBER = b.AMBER
LIGHT_TEAL = b.LIGHT_TEAL
NAVY_2 = b.NAVY_2

sources_by_id = {item["source_id"]: item for item in source_notes["sources"]}
clusters = analysis["use_case_clusters"]
findings = analysis["findings"]
recommendations = analysis["recommendations"]


def compact(text: str, limit: int) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[:limit].rsplit(" ", 1)[0] + "..."


def divider(num: str, title: str, sub: str, page: int) -> None:
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {num}", d.M, Inches(2.0), Inches(4.5), Inches(0.4), size=14, color=b.TEAL, bold=True)
    d.text(
        s,
        title,
        d.M,
        Inches(2.55),
        Inches(11.5),
        Inches(1.15),
        size=38,
        color=b.WHITE,
        bold=True,
        font=b.FONT_H,
        shrink=True,
    )
    d.rect(s, d.M, Inches(3.8), Inches(1.5), Inches(0.06), b.TEAL)
    d.text(s, sub, d.M, Inches(4.08), Inches(10.8), Inches(0.8), size=17, color=LIGHT_TEAL, shrink=True)
    d.footer(s, page, TOTAL, dark=True)


def exec_summary_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "Executive Summary", "What matters most if you only read one page")
    d.rect(s, d.M, Inches(1.58), d.CW, Inches(0.98), b.NAVY, radius=0.06, shadow=True)
    d.rect(s, d.M, Inches(1.58), Inches(0.12), Inches(0.98), b.TEAL)
    d.text(s, "BOTTOM LINE", d.M + Inches(0.35), Inches(1.7), Inches(2.2), Inches(0.24), size=11, color=b.TEAL, bold=True)
    d.text(
        s,
        "Healthcare provider-ops AI is strongest where the system reduces manual coordination, accelerates revenue, or returns clinician time inside existing workflows.",
        d.M + Inches(0.35),
        Inches(1.97),
        d.CW - Inches(0.7),
        Inches(0.54),
        size=13.4,
        color=b.WHITE,
        bold=True,
        shrink=True,
    )
    cards = [
        (
            "MARKET SHIFT",
            b.TEAL,
            [
                "Provider AI has moved beyond experimentation and into operating workflows.",
                "The strongest value is showing up in admin-heavy, measurable domains.",
            ],
        ),
        (
            "WHERE VALUE IS CLEAREST",
            b.GOLD,
            [
                "Documentation, access, coding, RCM, and perioperative flow now have public proof.",
                "Workflow economics are clearer than broad enterprise-copilot narratives.",
            ],
        ),
        (
            "HOW TO START",
            b.ACCENT,
            [
                "Pick one workflow, one owner, and one hard operating scorecard.",
                "Require EHR-adjacent execution before expanding beyond pilot mode.",
            ],
        ),
        (
            "GOVERNANCE NOTE",
            CORAL,
            [
                "Assistive and more autonomous workflows should not use the same control model.",
                "Sequence proof first; scale only after quality and exception handling are stable.",
            ],
        ),
    ]
    gap_x = Inches(0.28)
    gap_y = Inches(0.22)
    cw = (d.CW - gap_x) / 2
    ch = Inches(1.46)
    top = Inches(2.75)
    for idx, (title, accent, items) in enumerate(cards):
        row, col = divmod(idx, 2)
        x = d.M + col * (cw + gap_x)
        y = top + row * (ch + gap_y)
        d.rect(s, x, y, cw, ch, b.SOFT, line=b.GRID, radius=0.05)
        d.rect(s, x, y, cw, Inches(0.48), b.NAVY, radius=0.05)
        d.rect(s, x, y, Inches(0.1), Inches(0.48), accent)
        d.text(s, title, x + Inches(0.22), y + Inches(0.1), cw - Inches(0.34), Inches(0.26), size=12, color=accent, bold=True)
        d.text(
            s,
            [{"text": item, "size": 9.7, "color": b.INK, "bullet": True, "space_before": 4} for item in items],
            x + Inches(0.24),
            y + Inches(0.58),
            cw - Inches(0.46),
            ch - Inches(0.72),
            shrink=True,
            ls=0.98,
        )
    d.rect(s, d.M, Inches(6.03), d.CW, Inches(0.62), b.TEAL, radius=0.06)
    d.text(s, "THE ASK", d.M + Inches(0.4), Inches(6.03), Inches(2.0), Inches(0.62), size=13.2, color=b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    d.text(
        s,
        "Approve one workflow-led pilot with a named owner and a hard operating scorecard before expanding into broader AI initiatives.",
        d.M + Inches(1.95),
        Inches(6.03),
        d.CW - Inches(2.35),
        Inches(0.62),
        size=13.2,
        color=b.NAVY,
        bold=True,
        anchor=MSO_ANCHOR.MIDDLE,
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def storyboard_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "The Story In Five Beats", "The argument should read by slide titles alone")
    beats = [
        ("SITUATION", "Healthcare AI has moved past experimentation.", b.TEAL),
        ("COMPLICATION", "Not every AI workflow deserves the same priority.", AMBER),
        ("QUESTION", "Which provider-ops use cases have the cleanest economic proof?", b.GOLD),
        ("ANSWER", "Workflow-embedded admin domains win first.", b.ACCENT),
        ("ACTION", "Pilot one high-pain domain with an operating scorecard.", b.TEAL),
    ]
    gap = Inches(0.22)
    cw = (d.CW - gap * 4) / 5
    top = Inches(2.08)
    h = Inches(2.9)
    for i, (label, line, accent) in enumerate(beats):
        x = d.M + i * (cw + gap)
        d.rect(s, x, top, cw, h, b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.rect(s, x, top, cw, Inches(0.7), b.NAVY, radius=0.06)
        d.text(s, f"0{i + 1}", x, top + Inches(0.12), cw, Inches(0.45), size=22, color=accent, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.12), top + Inches(0.85), cw - Inches(0.24), Inches(0.3), size=11.3, color=accent, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, line, x + Inches(0.18), top + Inches(1.23), cw - Inches(0.36), Inches(1.55), size=12.8, color=b.INK, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        if i < 4:
            d.text(s, "→", x + cw - Inches(0.03), top + Inches(1.0), gap + Inches(0.1), Inches(0.6), size=19, color=b.ACCENT, bold=True, align=PP_ALIGN.CENTER)
    d.rect(s, d.M, Inches(5.33), d.CW, Inches(0.85), b.NAVY, radius=0.06)
    d.text(
        s,
        "The deck moves from market proof to workflow prioritization to real operating examples and then to the implementation ask.",
        d.M,
        Inches(5.33),
        d.CW,
        Inches(0.85),
        size=14.5,
        color=b.WHITE,
        bold=True,
        italic=True,
        align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE,
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def kpi_grid_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "Why The Market Is Moving", "Adoption and implementation are now strong enough to force prioritization decisions")
    kpis = [
        ("50%", "Organizations implemented gen AI", "McKinsey 2026 survey"),
        ("80%+", "Organizations with end-user use cases", "McKinsey 2026 survey"),
        ("66%", "Physicians using health AI", "AMA 2025 survey"),
        ("54%", "Care orgs implementing clinical-productivity AI", "McKinsey 2026 survey"),
    ]
    gap = Inches(0.25)
    cw = (d.CW - gap * 3) / 4
    top = Inches(1.9)
    h = Inches(2.3)
    for i, (stat, label, note) in enumerate(kpis):
        x = d.M + i * (cw + gap)
        d.rect(s, x, top, cw, h, b.NAVY, radius=0.06, shadow=True)
        d.text(s, stat, x, top + Inches(0.22), cw, Inches(0.62), size=34, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.15), top + Inches(0.93), cw - Inches(0.3), Inches(0.68), size=12.3, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, note, x + Inches(0.15), top + Inches(1.7), cw - Inches(0.3), Inches(0.4), size=10.2, color=LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, d.M, Inches(4.55), d.CW, Inches(0.74), b.SOFT, line=b.GRID, radius=0.04)
    d.text(
        s,
        "This is now an execution problem: the question is which workflow gets implementation attention first, not whether AI belongs in provider operations.",
        d.M + Inches(0.25),
        Inches(4.55),
        d.CW - Inches(0.5),
        Inches(0.74),
        size=13.6,
        color=b.INK,
        bold=True,
        italic=True,
        anchor=MSO_ANCHOR.MIDDLE,
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def frontline_adoption_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "Adoption Rises Where AI Removes Clerical Work", "Physicians adopt AI fastest when it reduces friction in their current workflow")
    col_w = Inches(5.88)
    lx = d.M
    rx = d.W - d.M - col_w
    d.rect(s, lx, Inches(1.75), col_w, Inches(4.55), b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, lx, Inches(1.75), col_w, Inches(0.58), b.NAVY, radius=0.05)
    d.rect(s, lx, Inches(1.75), Inches(0.1), Inches(0.58), b.TEAL)
    d.text(s, "WHERE ADOPTION SHOWS UP", lx + Inches(0.25), Inches(1.86), col_w - Inches(0.5), Inches(0.3), size=15, color=b.TEAL, bold=True)
    left_points = [
        "Documentation of billing codes, charts, and visit notes.",
        "Drafting discharge instructions, care plans, and progress notes.",
        "Chart summaries and customer-service tasks near the patient workflow.",
        "Ambient documentation scaled from pilot to broad provider deployment.",
    ]
    d.text(
        s,
        [{"text": item, "size": 12.3, "color": b.INK, "bullet": True, "space_before": 10} for item in left_points],
        lx + Inches(0.3),
        Inches(2.55),
        col_w - Inches(0.6),
        Inches(3.2),
        shrink=True,
    )
    d.rect(s, rx, Inches(1.75), col_w, Inches(4.55), b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, rx, Inches(1.75), col_w, Inches(0.58), b.NAVY, radius=0.05)
    d.rect(s, rx, Inches(1.75), Inches(0.1), Inches(0.58), b.GOLD)
    d.text(s, "MANAGEMENT IMPLICATION", rx + Inches(0.25), Inches(1.86), col_w - Inches(0.5), Inches(0.3), size=15, color=b.GOLD, bold=True)
    right_points = [
        "Start where AI supports staff inside the existing system rather than forcing workflow redesign first.",
        "Treat documentation and clerical load as operating problems with measurable time recovery.",
        "Use adoption evidence as a proxy for workflow fit, not as blanket permission for any AI deployment.",
    ]
    d.text(
        s,
        [{"text": item, "size": 12.4, "color": b.INK, "bullet": True, "space_before": 11} for item in right_points],
        rx + Inches(0.3),
        Inches(2.55),
        col_w - Inches(0.6),
        Inches(3.15),
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def comparison_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "What Tends To Win Versus What Tends To Stall", "Workflow fit matters more than generic AI capability")
    col_w = Inches(5.9)
    lx = d.M
    rx = d.W - d.M - col_w
    for x, accent, title, items in [
        (
            lx,
            b.TEAL,
            "WHAT TENDS TO WIN",
            [
                "EHR-embedded workflow steps with one operational owner.",
                "Direct cost, cash, capacity, or clinician-time metrics.",
                "High-volume repetitive tasks with clear exception handling.",
                "Solutions that complete work, not just summarize work.",
            ],
        ),
        (
            rx,
            CORAL,
            "WHAT TENDS TO STALL",
            [
                "Generic enterprise copilots with unclear day-to-day ownership.",
                "No baseline metric for value or no downstream system integration.",
                "Workflows driven mostly by governance theater instead of operational pain.",
                "Point tools detached from registration, revenue cycle, or clinical operations.",
            ],
        ),
    ]:
        d.rect(s, x, Inches(1.82), col_w, Inches(4.4), b.SOFT, line=b.GRID, radius=0.05, shadow=True)
        d.rect(s, x, Inches(1.82), col_w, Inches(0.62), b.NAVY, radius=0.05)
        d.rect(s, x, Inches(1.82), Inches(0.12), Inches(0.62), accent)
        d.text(s, title, x + Inches(0.28), Inches(1.95), col_w - Inches(0.56), Inches(0.28), size=15, color=accent, bold=True)
        d.text(
            s,
            [{"text": item, "size": 12.1, "color": b.INK, "bullet": True, "space_before": 10} for item in items],
            x + Inches(0.3),
            Inches(2.68),
            col_w - Inches(0.6),
            Inches(3.2),
            shrink=True,
        )
    d.footer(s, page, TOTAL)


def proof_model_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "ROI Is Easiest To Defend One Workflow At A Time", "The source set keeps proving the same operating model")
    cols = [
        ("CLINICIAN TIME", b.TEAL, [
            "Ambient documentation reduces after-hours note work.",
            "Better patient interaction is a real outcome, not a soft side benefit.",
            "Measure reclaimed time and documentation completeness together.",
        ]),
        ("CASH + COST", b.GOLD, [
            "Revenue-cycle and coding workflows map to A/R days, denials, and cost-to-collect.",
            "These domains create the cleanest hard-dollar proof for finance leaders.",
            "Measure cash conversion and coding turnaround before scaling.",
        ]),
        ("CAPACITY + ACCESS", b.ACCENT, [
            "Access and perioperative workflows create visible throughput and queue relief.",
            "The economic value comes from avoided cancellations and better constrained capacity usage.",
            "Measure queue leakage, cancellations, utilization, and release velocity.",
        ]),
    ]
    gap = Inches(0.28)
    cw = (d.CW - gap * 2) / 3
    top = Inches(1.88)
    h = Inches(3.95)
    for i, (title, accent, items) in enumerate(cols):
        x = d.M + i * (cw + gap)
        d.rect(s, x, top, cw, h, b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.rect(s, x, top, cw, Inches(0.56), b.NAVY, radius=0.06)
        d.rect(s, x, top, Inches(0.12), Inches(0.56), accent)
        d.text(s, title, x + Inches(0.24), top + Inches(0.12), cw - Inches(0.48), Inches(0.3), size=14, color=accent, bold=True)
        d.text(
            s,
            [{"text": item, "size": 12, "color": b.INK, "bullet": True, "space_before": 10} for item in items],
            x + Inches(0.28),
            top + Inches(0.8),
            cw - Inches(0.56),
            Inches(2.7),
            shrink=True,
        )
        d.rect(s, x + Inches(0.24), top + Inches(3.15), cw - Inches(0.48), Inches(0.58), b.NAVY, radius=0.04)
        d.text(
            s,
            f"Best first metric: {['time reclaimed', 'cost / cash', 'throughput / cancellations'][i]}",
            x + Inches(0.3),
            top + Inches(3.15),
            cw - Inches(0.6),
            Inches(0.58),
            size=11.2,
            color=b.WHITE,
            bold=True,
            anchor=MSO_ANCHOR.MIDDLE,
            align=PP_ALIGN.CENTER,
            shrink=True,
        )
    d.footer(s, page, TOTAL)


def ranking_chart_slide(page: int) -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    labels = [
        "Patient access + prior auth",
        "Revenue cycle status work",
        "Coding automation",
        "Ambient documentation",
        "Perioperative + capacity",
    ]
    values = [9.4, 9.0, 8.8, 8.4, 8.2]
    chart = d.chart_barh(labels, values, CHART_DIR / "healthcare_rank.png", highlight_at=8)
    s = d.slide(fill=b.WHITE)
    d.header(s, "Highest-Value Provider-Ops AI Domains", "Near-term priority is strongest where workflow pain and measurable proof already exist")
    d.picture_centered(s, chart, top=Inches(1.65), width=Inches(9.4), max_bottom=Inches(6.0))
    d.text(
        s,
        "The strongest stack clusters around access, revenue cycle, coding, documentation, and perioperative operations — all repetitive workflows with clear owners and visible economic metrics.",
        d.M,
        Inches(6.22),
        d.CW,
        Inches(0.5),
        size=14,
        color=b.NAVY,
        bold=True,
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def matrix_slide(page: int) -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    points = [
        ("Access + prior auth", 0.90, 0.93, b.HX_TEAL),
        ("Revenue cycle", 0.87, 0.90, b.HX_TEAL),
        ("Coding automation", 0.83, 0.88, b.HX_TEALD),
        ("Ambient documentation", 0.80, 0.78, b.HX_TEALD),
        ("Periop capacity", 0.75, 0.84, b.HX_GOLD),
    ]
    chart = d.chart_matrix(
        points,
        CHART_DIR / "healthcare_matrix.png",
        xlabel="Generic assistant  →  Workflow embeddedness",
        ylabel="Weak proof  →  Hard economic proof",
        note="Best first bets sit in the upper-right quadrant",
    )
    s = d.slide(fill=b.WHITE)
    d.header(s, "Embedded Workflows Win First", "Workflow-embedded administrative domains sit furthest from generic AI theater")
    d.picture_centered(s, chart, top=Inches(1.65), width=Inches(9.2), max_bottom=Inches(6.05))
    d.text(
        s,
        "Ambient documentation is already real, but access, revenue cycle, and coding sit even higher on immediate economic proof because the workflow economics are cleaner.",
        d.M,
        Inches(6.24),
        d.CW,
        Inches(0.46),
        size=13.8,
        color=b.NAVY,
        bold=True,
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def use_case_table_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "Five High-Value Workflow Families", "This is the prioritized operating map, not just a vendor list")
    top = Inches(1.76)
    d.rect(s, d.M, top, d.CW, Inches(0.48), b.NAVY, radius=0.04)
    headers = [("Workflow family", Inches(3.2)), ("Buyer / owner", Inches(2.9)), ("Business job", Inches(5.0))]
    x = d.M + Inches(0.2)
    for label, width in headers:
        d.text(s, label, x, top, width, Inches(0.48), size=12.2, color=b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        x += width
    y = top + Inches(0.52)
    row_h = Inches(0.86)
    for idx, cluster in enumerate(clusters):
        if idx % 2 == 0:
            d.rect(s, d.M, y, d.CW, row_h, b.SOFT)
        d.text(s, cluster["name"], d.M + Inches(0.18), y + Inches(0.08), Inches(3.0), Inches(0.68), size=11.7, color=b.NAVY, bold=True, shrink=True)
        d.text(
            s,
            f'{cluster["buyer"]}\n{cluster["workflow_owner"]}',
            d.M + Inches(3.35),
            y + Inches(0.07),
            Inches(2.7),
            Inches(0.7),
            size=10.1,
            color=b.INK,
            shrink=True,
        )
        d.text(
            s,
            cluster["business_job"],
            d.M + Inches(6.2),
            y + Inches(0.07),
            Inches(5.55),
            Inches(0.72),
            size=10.4,
            color=b.INK,
            shrink=True,
        )
        y += row_h
    d.text(
        s,
        "The common pattern: each lane has a visible owner, repetitive workflow steps, and a measurable economic scorecard.",
        d.M,
        Inches(6.38),
        d.CW,
        Inches(0.42),
        size=13.4,
        color=b.NAVY,
        bold=True,
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def workflow_card(
    page: int,
    cluster: dict,
    display_title: str,
    stat: str,
    stat_label: str,
    systems: list[str],
    workflow_steps: list[tuple[str, str]],
    org_label: str,
) -> None:
    s = d.slide(fill=b.WHITE)
    pw = Inches(4.6)
    d.rect(s, 0, 0, pw, d.H, b.NAVY)
    d.rect(s, pw, 0, Inches(0.06), d.H, b.TEAL)
    d.text(s, "USE CASE", Inches(0.45), Inches(0.52), Inches(4), Inches(0.28), size=11, color=b.TEAL, bold=True)
    d.text(s, display_title, Inches(0.45), Inches(0.82), Inches(3.85), Inches(0.88), size=20.5, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, Inches(0.45), Inches(1.75), Inches(1.25), Inches(0.04), b.TEAL)

    d.rect(s, Inches(0.35), Inches(2.05), Inches(3.9), Inches(1.14), NAVY_2, radius=0.06)
    d.rect(s, Inches(0.35), Inches(2.05), Inches(0.08), Inches(1.14), CORAL)
    d.text(s, "BUSINESS JOB", Inches(0.6), Inches(2.18), Inches(3.7), Inches(0.22), size=10, color=CORAL, bold=True)
    d.text(s, compact(cluster["business_job"], 96), Inches(0.6), Inches(2.43), Inches(3.45), Inches(0.62), size=9.7, color=LIGHT_TEAL, shrink=True, ls=1.0)

    d.rect(s, Inches(0.35), Inches(3.48), Inches(1.95), Inches(1.12), NAVY_2, radius=0.06)
    d.text(s, stat, Inches(0.35), Inches(3.6), Inches(1.95), Inches(0.45), size=28, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, compact(stat_label, 28), Inches(0.45), Inches(4.1), Inches(1.75), Inches(0.34), size=8.7, color=b.WHITE, align=PP_ALIGN.CENTER, shrink=True)

    d.rect(s, Inches(2.52), Inches(3.48), Inches(1.93), Inches(1.12), NAVY_2, radius=0.06)
    d.text(s, "WHO OWNS IT", Inches(2.66), Inches(3.6), Inches(1.6), Inches(0.2), size=9, color=b.TEAL, bold=True)
    d.text(
        s,
        cluster["workflow_owner"],
        Inches(2.66),
        Inches(3.88),
        Inches(1.6),
        Inches(0.54),
        size=9.0,
        color=LIGHT_TEAL,
        shrink=True,
    )

    d.text(s, compact(cluster["value_prop"], 90), Inches(0.45), Inches(4.95), Inches(3.9), Inches(0.48), size=9.2, color=b.MUTED, italic=True, shrink=True)

    rx = pw + Inches(0.5)
    rw = d.W - pw - Inches(1.1)
    d.rect(s, rx, Inches(0.2), rw, Inches(0.16), b.TEAL)
    d.text(s, "HOW THE WORKFLOW GETS REALIZED", rx, Inches(0.55), rw, Inches(0.35), size=13, color=b.NAVY, bold=True)
    d.text(s, compact(cluster["recommendation"], 118), rx, Inches(0.88), rw, Inches(0.3), size=9.7, color=b.MUTED, shrink=True)
    step_top = Inches(1.33)
    step_h = Inches(0.68)
    step_gap = Inches(0.08)
    for i, (step_title, step_desc) in enumerate(workflow_steps):
        y = step_top + i * (step_h + step_gap)
        d.rect(s, rx, y, Inches(0.5), Inches(0.5), b.TEAL, radius=0.18)
        d.text(s, str(i + 1), rx, y + Inches(0.06), Inches(0.5), Inches(0.36), size=16, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, step_title, rx + Inches(0.65), y + Inches(0.01), rw - Inches(0.72), Inches(0.22), size=11.4, color=b.NAVY, bold=True, shrink=True)
        d.text(s, compact(step_desc, 92), rx + Inches(0.65), y + Inches(0.25), rw - Inches(0.72), Inches(0.34), size=9.7, color=b.INK, shrink=True)
        if i < len(workflow_steps) - 1:
            d.text(s, "↓", rx + Inches(0.15), y + step_h - Inches(0.06), Inches(0.5), Inches(0.24), size=13, color=b.ACCENT, bold=True, align=PP_ALIGN.CENTER)

    evidence = cluster["evidence_companies"][0]
    d.rect(s, rx, Inches(5.7), rw, Inches(0.68), b.SOFT, line=b.GRID, radius=0.04)
    d.text(s, org_label, rx + Inches(0.2), Inches(5.82), Inches(1.8), Inches(0.2), size=10, color=b.ACCENT, bold=True)
    d.text(s, compact(evidence["proof_line"], 96), rx + Inches(1.75), Inches(5.78), rw - Inches(1.95), Inches(0.26), size=8.4, color=b.INK, shrink=True)
    d.rect(s, rx, Inches(6.48), rw, Inches(0.34), b.NAVY, radius=0.04)
    d.text(
        s,
        "SYSTEMS:  " + "  ·  ".join(systems),
        rx + Inches(0.18),
        Inches(6.48),
        rw - Inches(0.36),
        Inches(0.34),
        size=8.0,
        color=b.WHITE,
        bold=True,
        anchor=MSO_ANCHOR.MIDDLE,
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def case_study_slide(page: int, title: str, cards: list[tuple[str, str]], implications: list[str], takeaway: str) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, title, "Evidence and implication from a real provider-operations deployment")
    left_w = Inches(5.9)
    right_w = Inches(6.15)
    lx = d.M
    rx = d.W - d.M - right_w
    y = Inches(1.82)
    for label, body in cards:
        d.rect(s, lx, y, left_w, Inches(1.12), b.SOFT, line=b.GRID, radius=0.05, shadow=True)
        d.rect(s, lx, y, Inches(0.12), Inches(1.12), b.TEAL)
        d.text(s, label, lx + Inches(0.22), y + Inches(0.12), left_w - Inches(0.4), Inches(0.22), size=11.2, color=b.ACCENT, bold=True)
        d.text(s, body, lx + Inches(0.22), y + Inches(0.38), left_w - Inches(0.38), Inches(0.6), size=11.3, color=b.INK, shrink=True)
        y += Inches(1.28)
    d.rect(s, rx, Inches(1.82), right_w, Inches(4.1), b.NAVY, radius=0.06, shadow=True)
    d.text(s, "WHAT THIS MEANS", rx + Inches(0.28), Inches(1.96), right_w - Inches(0.56), Inches(0.26), size=13, color=b.TEAL, bold=True)
    d.text(
        s,
        [{"text": item, "size": 12.3, "color": LIGHT_TEAL, "bullet": True, "space_before": 11} for item in implications],
        rx + Inches(0.28),
        Inches(2.42),
        right_w - Inches(0.56),
        Inches(2.78),
        shrink=True,
    )
    d.rect(s, rx + Inches(0.25), Inches(5.35), right_w - Inches(0.5), Inches(0.52), b.TEAL, radius=0.04)
    d.text(s, takeaway, rx + Inches(0.38), Inches(5.35), right_w - Inches(0.76), Inches(0.52), size=10.8, color=b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.footer(s, page, TOTAL)


def governance_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "Governance Should Follow Workflow Economics", "Different workflow classes need different controls and scorecards")
    rows = [
        ("Assistive documentation", "Clinician experience, note quality, and downstream completeness", "Clinical leader + informatics owner", "Human review stays in-loop"),
        ("Access + prior auth", "Queue relief, cancellations, digital completion", "Patient access leader", "Exception queue + policy check"),
        ("Revenue-cycle status work", "A/R days, cost-to-collect, staff productivity", "RCM operations leader", "Write-back controls + audit trail"),
        ("Coding automation", "Coding cost, denial rates, turnaround time", "Coding / HIM leader", "Quality sampling + compliance controls"),
        ("Capacity orchestration", "Utilization, case throughput, release velocity", "Periop operations leader", "Escalation rules + release governance"),
    ]
    top = Inches(1.76)
    d.rect(s, d.M, top, d.CW, Inches(0.48), b.NAVY, radius=0.04)
    cols = [
        ("Workflow", Inches(2.65)),
        ("Primary scorecard", Inches(3.7)),
        ("Owner", Inches(2.35)),
        ("Control model", Inches(3.0)),
    ]
    x = d.M + Inches(0.16)
    for label, width in cols:
        d.text(s, label, x, top, width, Inches(0.48), size=12, color=b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        x += width
    y = top + Inches(0.5)
    row_h = Inches(0.82)
    for i, row in enumerate(rows):
        if i % 2 == 0:
            d.rect(s, d.M, y, d.CW, row_h, b.SOFT)
        x = d.M + Inches(0.16)
        widths = [Inches(2.55), Inches(3.6), Inches(2.25), Inches(2.95)]
        sizes = [11.2, 10.6, 10.4, 10.4]
        colors = [b.NAVY, b.INK, b.INK, b.ACCENT]
        bolds = [True, False, False, True]
        for idx, cell in enumerate(row):
            d.text(s, cell, x, y + Inches(0.07), widths[idx], Inches(0.68), size=sizes[idx], color=colors[idx], bold=bolds[idx], shrink=True)
            x += widths[idx] + Inches(0.1)
        y += row_h
    d.footer(s, page, TOTAL)


def roadmap_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "A 90-Day Provider-Ops AI Pilot Plan", "The goal is hard workflow proof, not broad AI theater")
    steps = [
        ("01", "Choose one workflow family", "Pick a high-pain domain such as prior auth, coding, or OR scheduling — not a vague enterprise AI mandate."),
        ("02", "Name the operating owner", "Give one leader the workflow, baseline, and escalation path before vendor configuration begins."),
        ("03", "Set 2–3 operating metrics", "Use cancellations, A/R days, denials, coding turnaround, or clinician-time recovery — not vanity metrics."),
        ("04", "Require EHR / system integration", "If the workflow is not embedded in the EHR or downstream process, it is not ready to scale."),
        ("05", "Scale only after durable proof", "Move from pilot to expansion only after the operating scorecard improves and exception handling is stable."),
    ]
    top = Inches(1.95)
    for idx, (num, title, body) in enumerate(steps):
        y = top + idx * Inches(0.87)
        d.rect(s, d.M, y, Inches(0.68), Inches(0.68), b.TEAL, radius=0.18)
        d.text(s, num, d.M, y + Inches(0.11), Inches(0.68), Inches(0.42), size=20, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, title, d.M + Inches(0.95), y + Inches(0.02), Inches(3.5), Inches(0.24), size=12.2, color=b.NAVY, bold=True)
        d.text(s, body, d.M + Inches(0.95), y + Inches(0.26), d.CW - Inches(1.1), Inches(0.38), size=9.8, color=b.INK, shrink=True)
        if idx < len(steps) - 1:
            d.text(s, "↓", d.M + Inches(0.15), y + Inches(0.66), Inches(0.4), Inches(0.26), size=13, color=b.ACCENT, bold=True, align=PP_ALIGN.CENTER)
    d.rect(s, d.M, Inches(6.45), d.CW, Inches(0.4), b.NAVY, radius=0.04)
    d.text(s, "The sequence matters: workflow first, owner second, metrics third, scale last.", d.M, Inches(6.45), d.CW, Inches(0.4), size=11.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.footer(s, page, TOTAL)


def decision_slide(page: int) -> None:
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(8.9), 0, d.W - Inches(8.9), d.H, NAVY_2)
    d.rect(s, Inches(8.9), 0, Inches(0.06), d.H, b.TEAL)
    d.text(s, "DECISION REQUIRED", d.M, Inches(0.95), Inches(6), Inches(0.32), size=14, color=b.TEAL, bold=True)
    d.text(
        s,
        "Pick The First\nWorkflow",
        d.M,
        Inches(1.45),
        Inches(6.7),
        Inches(1.1),
        size=34,
        color=b.WHITE,
        bold=True,
        font=b.FONT_H,
        shrink=True,
    )
    d.rect(s, d.M, Inches(3.2), Inches(1.5), Inches(0.06), b.TEAL)
    d.text(
        s,
        "The strongest provider-ops AI opportunities are already visible. The decision is whether to own one operational workflow with measurable proof before widening the platform narrative.",
        d.M,
        Inches(3.52),
        Inches(7.3),
        Inches(0.78),
        size=13.2,
        color=b.WHITE,
        shrink=True,
    )
    asks = [
        "Approve one workflow-led pilot in access, revenue cycle, coding, documentation, or periop operations.",
        "Require a named owner, baseline metrics, and EHR-adjacent execution design.",
        "Review expansion only after hard operating gains are visible.",
    ]
    d.text(
        s,
        [{"text": ask, "size": 13.5, "color": b.WHITE, "bullet": True, "space_before": 11} for ask in asks],
        d.M,
        Inches(4.8),
        Inches(7.6),
        Inches(1.55),
        shrink=True,
    )
    sx = Inches(9.35)
    d.text(s, "START HERE", sx, Inches(1.9), Inches(3.2), Inches(0.22), size=11, color=b.GOLD, bold=True)
    chips = [
        "Prior auth / access",
        "Revenue-cycle status",
        "Coding automation",
        "Ambient documentation",
        "Periop scheduling",
    ]
    y = Inches(2.35)
    for chip in chips:
        d.rect(s, sx, y, Inches(2.9), Inches(0.5), b.ACCENT, radius=0.5)
        d.text(s, chip, sx, y + Inches(0.08), Inches(2.9), Inches(0.3), size=10.6, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        y += Inches(0.68)
    d.footer(s, page, TOTAL, dark=True)


def methodology_slide(page: int) -> None:
    s = d.slide(fill=b.WHITE)
    d.header(s, "Methodology And Source Coverage", "How to interpret this deck and where the evidence comes from")
    lx = d.M
    rx = d.W - d.M - Inches(5.7)
    d.rect(s, lx, Inches(1.8), Inches(6.0), Inches(4.6), b.SOFT, line=b.GRID, radius=0.05, shadow=True)
    d.rect(s, lx, Inches(1.8), Inches(6.0), Inches(0.56), b.NAVY, radius=0.05)
    d.rect(s, lx, Inches(1.8), Inches(0.1), Inches(0.56), b.TEAL)
    d.text(s, "HOW TO READ THIS", lx + Inches(0.25), Inches(1.93), Inches(5.5), Inches(0.24), size=14, color=b.TEAL, bold=True)
    bullets = [
        "This is a research-backed synthesis of market surveys, provider case evidence, and vendor case evidence.",
        "The goal is workflow prioritization, not vendor procurement ranking.",
        "Outcome figures come from heterogeneous sources and need local baseline validation before purchase decisions.",
        "The strongest conclusions are about which workflow families are most investable right now.",
    ]
    d.text(
        s,
        [{"text": item, "size": 12, "color": b.INK, "bullet": True, "space_before": 10} for item in bullets],
        lx + Inches(0.28),
        Inches(2.5),
        Inches(5.45),
        Inches(2.9),
        shrink=True,
    )
    d.rect(s, rx, Inches(1.8), Inches(5.7), Inches(4.6), b.NAVY, radius=0.05, shadow=True)
    d.text(s, "SOURCE SET", rx + Inches(0.28), Inches(1.94), Inches(4.8), Inches(0.24), size=14, color=b.TEAL, bold=True)
    source_lines = []
    for source_id in analysis["source_ids"]:
        item = sources_by_id[source_id]
        source_lines.append(f'{item["author"]} — {item["title"]}')
    d.text(
        s,
        [{"text": line, "size": 11, "color": LIGHT_TEAL, "bullet": True, "space_before": 8} for line in source_lines],
        rx + Inches(0.28),
        Inches(2.42),
        Inches(5.1),
        Inches(3.35),
        shrink=True,
    )
    d.footer(s, page, TOTAL)


def cover_slide() -> None:
    s = d.slide(fill=b.NAVY)
    panel_w = Inches(9.05)
    d.rect(s, panel_w, 0, d.W - panel_w, d.H, NAVY_2)
    d.rect(s, panel_w, 0, Inches(0.06), d.H, b.TEAL)
    d.text(s, "EXECUTIVE DECK", d.M, Inches(0.95), Inches(6), Inches(0.32), size=15, color=b.TEAL, bold=True)
    d.text(s, "Healthcare Provider-Ops\nAI Use Cases", d.M, Inches(1.45), Inches(7.6), Inches(1.26), size=36, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
    d.text(s, "Where Provider-Ops Value Is Strongest", d.M, Inches(3.15), Inches(7.4), Inches(0.58), size=21.5, color=b.TEAL, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(3.98), Inches(1.5), Inches(0.06), b.TEAL)
    d.text(
        s,
        "A research-backed point of view on the workflows that deserve priority, the case evidence behind them, and the implementation model a health system should use.",
        d.M,
        Inches(4.28),
        Inches(7.85),
        Inches(1.0),
        size=16,
        color=b.WHITE,
        shrink=True,
    )
    sx = panel_w + Inches(0.45)
    d.text(s, "READOUT FOCUS", sx, Inches(1.88), Inches(3.5), Inches(0.24), size=11, color=b.GOLD, bold=True)
    for i, (head, detail) in enumerate([
        ("Why now", "Adoption has moved into real provider operations."),
        ("Where value is strongest", "Administrative domains create the clearest proof."),
        ("What to do", "Pilot one workflow with a hard scorecard."),
    ]):
        y = Inches(2.34) + i * Inches(1.2)
        d.text(s, head.upper(), sx, y, Inches(3.2), Inches(0.22), size=10.5, color=b.TEAL, bold=True)
        d.text(s, detail, sx, y + Inches(0.26), Inches(3.15), Inches(0.64), size=12.0, color=b.WHITE, bold=True, shrink=True)
    d.text(s, FOOTER_TEXT, d.M, Inches(6.7), Inches(9), Inches(0.3), size=11, color=hx("6B7C8C"))


cover_slide()
exec_summary_slide(2)
storyboard_slide(3)
divider("01", "Why The Market Has Shifted", "Healthcare AI is now an operating-model question, not a speculative future bet.", 4)
kpi_grid_slide(5)
frontline_adoption_slide(6)
comparison_slide(7)
proof_model_slide(8)
divider("02", "Where The Value Is Strongest", "The best use cases are workflow-embedded, measurable, and operationally owned.", 9)
ranking_chart_slide(10)
matrix_slide(11)
use_case_table_slide(12)
divider("03", "Workflow Deep Dives", "The question is not only what the use case is, but how it gets realized in a provider workflow.", 13)
workflow_card(
    14,
    clusters[0],
    "Ambient\ndocumentation",
    "1/3+",
    "UCHealth providers on platform",
    ["EHR", "Ambient note engine", "Clinical chart", "Audit trail"],
    [
        ("Capture encounter context", "Listen to the visit and produce draft documentation in the chart."),
        ("Keep the provider in the workflow", "Reduce typing and after-hours documentation burden without leaving the EHR."),
        ("Improve downstream quality", "Preserve documentation completeness while improving patient interaction."),
        ("Scale when adoption proves durable", "Treat it as workflow infrastructure rather than a novelty point tool."),
    ],
    "PROOF LINE",
)
workflow_card(
    15,
    clusters[1],
    "Access,\nregistration,\nand prior auth",
    "91%",
    "authorization success in case",
    ["Scheduling", "Registration", "Auth workflow", "Call / queue system"],
    [
        ("Surface queue pain", "Start where staff capacity is already failing against intake or auth demand."),
        ("Digitize repetitive intake work", "Use AI to automate repetitive registration and authorization steps."),
        ("Route exceptions to staff", "Keep unresolved cases in a managed exception queue."),
        ("Measure avoided leakage", "Tie the pilot to cancellations, queue relief, and digital completion."),
    ],
    "CASE EVIDENCE",
)
workflow_card(
    16,
    clusters[2],
    "RCM status\nwork",
    "A/R↓",
    "cash conversion focus",
    ["Payer portals", "Claim systems", "Auth status", "RCM queue"],
    [
        ("Target status-heavy tasks", "Start with claim, auth, and documentation research that consumes analyst time."),
        ("Pull context into one operating pane", "Retrieve status, policy, and document context before staff review."),
        ("Write back with controls", "Complete research work into the system of record with traceability."),
        ("Manage by cash metrics", "Use A/R days, cost-to-collect, and staff productivity as the scorecard."),
    ],
    "CASE EVIDENCE",
)
workflow_card(
    17,
    clusters[3],
    "Coding\nautomation",
    "5:1",
    "ROI signal in case proof",
    ["Coding queue", "Revenue integrity", "Claim edits", "Audit trail"],
    [
        ("Choose a narrow coding lane", "Pilot on a service line with coding delay or denial pain."),
        ("Automate repetitive coding work", "Use structured context to assist or automate code generation."),
        ("Sample for quality and denials", "Keep auditability and human oversight on sensitive edge cases."),
        ("Scale by hard-dollar proof", "Expand only when coding speed, cost, and denials improve together."),
    ],
    "CASE EVIDENCE",
)
workflow_card(
    18,
    clusters[4],
    "Perioperative\ncapacity",
    "7%",
    "more cases despite 20% fewer ORs",
    ["OR scheduling", "Block release rules", "Capacity queue", "Escalation workflow"],
    [
        ("Find constrained capacity", "Start with manual scheduling or release processes that bottleneck access."),
        ("Automate release and orchestration", "Use workflow automation to recover usable block time."),
        ("Coordinate downstream actions", "Treat scheduling changes as real workflow actions with owners."),
        ("Measure throughput, not novelty", "Judge value by cases, utilization, and release velocity."),
    ],
    "CASE EVIDENCE",
)
divider("04", "What The Case Evidence Shows", "Provider AI is strongest when the workflow pain is visible and the economics are explicit.", 19)
case_study_slide(
    20,
    "Case: Ambient Documentation At Scale",
    [
        ("Pilot-to-scale path", "UCHealth expanded Abridge after a nine-month pilot covering 250 providers."),
        ("Scaled usage", "The rollout now covers more than one-third of UCHealth's roughly 6,000 physicians, NPs, and PAs."),
        ("Operational outcome", "Providers reported stronger patient interactions and lower administrative burden."),
    ],
    [
        "Documentation AI is no longer a novelty wedge; it can become a system-wide workflow platform.",
        "The proof model is clinician time and interaction quality, not only note generation speed.",
        "This is a strong first bet when provider burden is already measurable and leadership wants visible frontline adoption.",
    ],
    "Use ambient documentation as workflow infrastructure when provider documentation burden is already material.",
)
case_study_slide(
    21,
    "Case: Access And Prior Auth ROI",
    [
        ("Queue pain", "Fort HealthCare had roughly double the prior-auth work volume relative to staff capacity."),
        ("Call leakage", "Thirty-eight percent of calls to a busy clinic were going to voicemail before automation."),
        ("Operational result", "The system reached 74% digital completion, over 5% fewer cancellations, and 91% successful authorizations."),
    ],
    [
        "This is not a convenience use case; it directly affects delayed care, cancellation leakage, and staff overload.",
        "Access workflows are attractive first pilots because the pain is visible and the baseline is operationally concrete.",
        "Management should measure queue relief and cancellation avoidance rather than chatbot activity or message counts.",
    ],
    "Access workflows win because they convert obvious queue pain into visible operational relief.",
)
case_study_slide(
    22,
    "Case: RCM And Coding Hard-Dollar Proof",
    [
        ("Revenue-cycle lane", "AKASA emphasizes automated claim status, auth status, and research-heavy workflows inside RCM operations."),
        ("Finance-facing outcomes", "The proof story centers on lower A/R days, staff time savings, and gross yield improvement."),
        ("Coding lane", "CodaMetrix cites lower coding cost, faster turnaround, reduced denials, and a 5:1 ROI profile."),
    ],
    [
        "Finance leaders can govern these pilots against cost-to-collect, A/R days, denial rates, and coding productivity.",
        "These workflows are easier to defend because the economics are direct, repetitive, and auditable.",
        "The right rollout is narrow and scorecard-led, not a broad promise of full back-office autonomy.",
    ],
    "Treat revenue cycle and coding as operating-model redesign, not just AI procurement.",
)
case_study_slide(
    23,
    "Case: Capacity Gains Without New Staffing",
    [
        ("Structural constraint", "Saint Luke's faced staffing pressure that reduced available OR capacity."),
        ("Workflow issue", "Manual release and scheduling processes left usable block time unused and slowed access."),
        ("Outcome", "The flagship hospital accommodated 7% more surgical cases despite 20% fewer ORs."),
    ],
    [
        "Capacity and perioperative workflows create a different kind of value: throughput and margin rather than direct labor removal.",
        "These pilots need strong release rules, escalation paths, and downstream scheduling ownership to avoid chaos.",
        "The scorecard should focus on throughput, release velocity, and utilization — not generic AI activity.",
    ],
    "Capacity workflows matter because they recover access and margin from constrained systems.",
)
divider("05", "What To Do Next", "The operating model matters as much as the vendor choice.", 24)
governance_slide(25)
roadmap_slide(26)
decision_slide(27)
methodology_slide(28)
divider("06", "Closing View", "Start where the workflow is repetitive, measurable, and operationally owned — then scale on proof.", 29)

assert d.n == TOTAL, f"Expected {TOTAL} slides, got {d.n}"
d.save(OUT)
