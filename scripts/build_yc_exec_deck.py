#!/usr/bin/env python3
"""Executive edition — a decision-grade deck for business executives.

Wraps the use-case realization depth in an executive story layer:
  * BLUF / executive summary one-pager
  * a five-beat storyboard (the argument reads by titles alone)
  * a point-of-view statement
  * an Executive Decision Scorecard (10 lanes x 5 factors heatmap + priority)
  * Where to Play / How to Win + The Decision Required
  * action titles throughout

Reuses the realization slide builders from build_yc_usecase_deck.

Run from repo root:  python3 scripts/build_yc_exec_deck.py
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

# ── import the realization module as a library ───────────────────────────────
_spec = importlib.util.spec_from_file_location("uc", str(Path(__file__).with_name("build_yc_usecase_deck.py")))
uc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uc)

# pull names
rect, text, slide, head, footer = uc.rect, uc.text, uc.slide, uc.head, uc.footer
TEAL, NAVY, NAVY_2, WHITE, LIGHT_TEAL = uc.TEAL, uc.NAVY, uc.NAVY_2, uc.WHITE, uc.LIGHT_TEAL
ACCENT, DARK_TEAL, SOFT, INK, MUTED, GRID, GOLD = uc.ACCENT, uc.DARK_TEAL, uc.SOFT, uc.INK, uc.MUTED, uc.GRID, uc.GOLD
CORAL = uc.RGBColor(0xE0, 0x5A, 0x6B)
AMBER = uc.RGBColor(0xF2, 0xA8, 0x3B)
SLIDE_W, SLIDE_H, MARGIN, CONTENT_W = uc.SLIDE_W, uc.SLIDE_H, uc.MARGIN, uc.CONTENT_W
FONT, FONT_H = uc.FONT, uc.FONT_H

OUT = Path("docs/reports/yc-agent-usecases-executive.pptx")
FOOTER = "Agentic AI · Executive Briefing  |  Strictly Confidential  |  June 2026"


def foot(s, page, total, *, dark=False):
    col = uc.RGBColor(0x88, 0x90, 0x98) if dark else MUTED
    text(s, FOOTER, MARGIN, Inches(7.08), Inches(9), Inches(0.3), size=9, color=col)
    text(s, f"{page} / {total}", SLIDE_W - Inches(1.3), Inches(7.06), Inches(0.7), Inches(0.3),
         size=10, color=col, align=PP_ALIGN.RIGHT, bold=True)


# ── executive slides ─────────────────────────────────────────────────────────


def s_cover(prs, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    rect(s, uc.PANEL_W, 0, SLIDE_W - uc.PANEL_W, SLIDE_H, NAVY_2)
    rect(s, uc.PANEL_W, 0, Inches(0.06), SLIDE_H, TEAL)
    text(s, "EXECUTIVE BRIEFING", MARGIN, Inches(0.95), Inches(7.5), Inches(0.4), size=15, color=TEAL, bold=True)
    text(s, "Winning In Agentic AI", MARGIN, Inches(1.5), Inches(8.0), Inches(1.05), size=46, color=WHITE, bold=True, font=FONT_H, shrink=True)
    text(s, "Where The Value Is — And Where To Place Our Bets", MARGIN, Inches(2.5), Inches(7.9), Inches(0.8), size=26, color=TEAL, bold=True, font=FONT_H, shrink=True)
    rect(s, MARGIN, Inches(3.45), Inches(1.5), Inches(0.06), TEAL)
    text(s, [
        {"text": "A decision-grade read of the agent market: ten operational use cases, the", "size": 16, "color": WHITE},
        {"text": "organizations proving them out, and a scored view of where to invest first.", "size": 16, "color": WHITE, "space_before": 3},
    ], MARGIN, Inches(3.75), Inches(7.7), Inches(1.0), shrink=True)
    # right strip: the decision framing
    sx = uc.PANEL_W + Inches(0.45)
    text(s, "FOR THE EXECUTIVE TEAM", sx, Inches(1.9), Inches(3.7), Inches(0.3), size=11, color=TEAL, bold=True)
    for i, (h, d) in enumerate([
        ("The question", "Where do agents create durable value?"),
        ("The answer", "In owned operational workflows."),
        ("The ask", "Approve a 90-day wedge bet."),
    ]):
        y = Inches(2.4) + i * Inches(1.25)
        text(s, h.upper(), sx, y, Inches(3.6), Inches(0.3), size=11, color=GOLD, bold=True)
        text(s, d, sx, y + Inches(0.28), Inches(3.6), Inches(0.8), size=15, color=WHITE, bold=True, shrink=True)
    text(s, FOOTER, MARGIN, Inches(6.7), Inches(9), Inches(0.3), size=11, color=uc.RGBColor(0x6B, 0x7C, 0x8C))


def s_exec_summary(prs, page, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    head(s, "Executive Summary", "If you read one slide, read this one")
    # BLUF banner
    rect(s, MARGIN, Inches(1.6), CONTENT_W, Inches(0.95), NAVY, radius=0.06, shadow=True)
    rect(s, MARGIN, Inches(1.6), Inches(0.12), Inches(0.95), TEAL)
    text(s, "BOTTOM LINE", MARGIN + Inches(0.35), Inches(1.72), Inches(2), Inches(0.25), size=11, color=TEAL, bold=True)
    text(s, "In agentic AI, winners are defined by workflow ownership — not model novelty — and the value concentrates in a handful of operational lanes.",
         MARGIN + Inches(0.35), Inches(1.98), CONTENT_W - Inches(0.7), Inches(0.5), size=16.5, color=WHITE, bold=True, shrink=True)
    # three columns
    cols = [
        ("THE SITUATION", TEAL, [
            "Agents are moving from demos to systems of action that complete real work.",
            "Activity clusters in operational lanes: workflow, customer ops, analytics, testing, infra.",
            "The market is crowded with generic 'agent platform' positioning.",
        ]),
        ("THE INSIGHT", GOLD, [
            "The durable wedge is owning a workflow end-to-end, not summarizing it.",
            "Value is highest where workflow ownership meets willingness to pay.",
            "Healthcare ops and finance are the strongest vertical lanes.",
        ]),
        ("THE RECOMMENDATION", ACCENT, [
            "Pick one workflow-heavy lane and own context, actuation, and governance.",
            "Treat healthcare operations as a priority wedge.",
            "Avoid generic agent-platform messaging entirely.",
        ]),
    ]
    gap = Inches(0.3)
    cw = (CONTENT_W - gap * 2) / 3
    top = Inches(2.75)
    h = Inches(2.6)
    for i, (title, accent, items) in enumerate(cols):
        x = MARGIN + i * (cw + gap)
        rect(s, x, top, cw, h, SOFT, line=GRID, radius=0.05)
        rect(s, x, top, cw, Inches(0.5), NAVY, radius=0.05)
        rect(s, x, top, Inches(0.1), Inches(0.5), accent)
        text(s, title, x + Inches(0.25), top + Inches(0.1), cw - Inches(0.4), Inches(0.3), size=13, color=accent, bold=True)
        text(s, [{"text": it, "size": 12, "color": INK, "bullet": True, "space_before": 9} for it in items],
             x + Inches(0.28), top + Inches(0.68), cw - Inches(0.56), h - Inches(0.85), shrink=True, ls=1.05)
    # the ask strip
    rect(s, MARGIN, Inches(5.6), CONTENT_W, Inches(0.85), TEAL, radius=0.06)
    text(s, [
        {"text": "THE ASK:  ", "size": 14, "color": NAVY, "bold": True},
    ], MARGIN + Inches(0.4), Inches(5.6), Inches(2), Inches(0.85), anchor=MSO_ANCHOR.MIDDLE)
    text(s, "Approve a 90-day bet on one owned workflow lane — starting with healthcare operations or workflow automation.",
         MARGIN + Inches(1.9), Inches(5.6), CONTENT_W - Inches(2.2), Inches(0.85), size=14.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    foot(s, page, total)


def s_storyboard(prs, page, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    head(s, "The Story In Five Beats", "Read left to right — this is the argument, in order")
    beats = [
        ("SITUATION", "Agents are becoming systems of action.", TEAL),
        ("COMPLICATION", "But generic agent platforms don't defend.", AMBER),
        ("QUESTION", "So where does durable value actually sit?", GOLD),
        ("ANSWER", "In owned operational workflows.", ACCENT),
        ("ACTION", "Bet on one lane for 90 days.", TEAL),
    ]
    n = 5
    gap = Inches(0.22)
    cw = (CONTENT_W - gap * (n - 1)) / n
    top = Inches(2.1)
    h = Inches(2.9)
    for i, (label, line, accent) in enumerate(beats):
        x = MARGIN + i * (cw + gap)
        rect(s, x, top, cw, h, SOFT, line=GRID, radius=0.06, shadow=True)
        rect(s, x, top, cw, Inches(0.7), NAVY, radius=0.06)
        text(s, f"0{i+1}", x, top + Inches(0.12), cw, Inches(0.45), size=22, color=accent, bold=True, align=PP_ALIGN.CENTER)
        text(s, label, x + Inches(0.1), top + Inches(0.85), cw - Inches(0.2), Inches(0.3), size=11.5, color=accent, bold=True, align=PP_ALIGN.CENTER)
        text(s, line, x + Inches(0.18), top + Inches(1.25), cw - Inches(0.36), Inches(1.5), size=13.5, color=INK, bold=True, align=PP_ALIGN.CENTER, shrink=True, ls=1.1)
        if i < n - 1:
            text(s, "→", x + cw - Inches(0.05), top + Inches(1.0), gap + Inches(0.12), Inches(0.6), size=20, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
    # spine
    rect(s, MARGIN, Inches(5.35), CONTENT_W, Inches(0.85), NAVY, radius=0.06)
    text(s, "Every slide that follows develops one of these five beats — and nothing else.",
         MARGIN, Inches(5.35), CONTENT_W, Inches(0.85), size=15, color=WHITE, bold=True, italic=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    foot(s, page, total)


def s_pov(prs, page, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    rect(s, 0, 0, Inches(0.18), SLIDE_H, TEAL)
    text(s, "OUR POINT OF VIEW", MARGIN, Inches(0.85), Inches(6), Inches(0.4), size=14, color=TEAL, bold=True)
    text(s, "Don't buy the agent hype. Buy the workflow.",
         MARGIN, Inches(1.35), Inches(11.8), Inches(1.1), size=36, color=WHITE, bold=True, font=FONT_H, shrink=True)
    pillars = [
        ("Own the workflow", "The defensible position is completing a job end-to-end inside the systems of record — not chatting about it."),
        ("Pick where pain meets pay", "Concentrate where workflow ownership and willingness to pay are both high: healthcare ops, finance, customer ops."),
        ("Prove it in 90 days", "Ship one narrow lane, instrument the baseline, and show a measurable cycle-time or error-rate delta."),
    ]
    gap = Inches(0.35)
    cw = (CONTENT_W - gap * 2) / 3
    top = Inches(3.2)
    h = Inches(3.0)
    for i, (t, d) in enumerate(pillars):
        x = MARGIN + i * (cw + gap)
        rect(s, x, top, cw, h, NAVY_2, line=uc.RGBColor(0x21, 0x35, 0x4A), radius=0.06)
        rect(s, x, top, Inches(0.7), Inches(0.7), TEAL, radius=0.16)
        text(s, f"0{i+1}", x, top + Inches(0.12), Inches(0.7), Inches(0.45), size=20, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
        text(s, t, x + Inches(0.25), top + Inches(0.95), cw - Inches(0.5), Inches(0.6), size=19, color=TEAL, bold=True, shrink=True)
        text(s, d, x + Inches(0.25), top + Inches(1.6), cw - Inches(0.5), Inches(1.3), size=13.5, color=LIGHT_TEAL, shrink=True, ls=1.1)
    foot(s, page, total, dark=True)


# ── Executive Decision Scorecard ─────────────────────────────────────────────
# Honest qualitative scoring derived from org activity + the workflow/WTP map.
# H (teal) good, M (amber) mixed, L (gray) weak. Higher = more attractive.
SCORECARD = [
    # lane, demand, ownership, willingness_to_pay, defensibility, time_to_value, priority
    ("Healthcare operations", "M", "H", "H", "H", "M", "PRIORITY"),
    ("Workflow automation",   "H", "H", "M", "M", "H", "PRIORITY"),
    ("Finance & trading",     "M", "H", "H", "H", "M", "PRIORITY"),
    ("Sales & customer ops",  "H", "M", "M", "M", "H", "STRONG"),
    ("Security & governance", "M", "M", "H", "H", "M", "STRONG"),
    ("Data & agent infra",    "M", "M", "M", "H", "M", "STRONG"),
    ("Developer tools & test","H", "L", "M", "M", "M", "WATCH"),
    ("Analytics & reporting", "H", "M", "L", "L", "H", "WATCH"),
    ("Legal & compliance",    "L", "H", "M", "M", "L", "WATCH"),
    ("General AI apps",       "L", "L", "L", "L", "M", "LOWER"),
]
PRIORITY_COLOR = {"PRIORITY": TEAL, "STRONG": ACCENT, "WATCH": AMBER, "LOWER": uc.RGBColor(0x9A, 0xA6, 0xB2)}
HML_COLOR = {"H": TEAL, "M": AMBER, "L": uc.RGBColor(0xC4, 0xCD, 0xD6)}
HML_TEXT = {"H": NAVY, "M": NAVY, "L": uc.RGBColor(0x55, 0x60, 0x6B)}


def s_scorecard(prs, page, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    head(s, "The Value Concentrates In A Few Lanes", "Executive decision scorecard — ten lanes scored on what determines payoff")
    cols = ["Use-case lane", "Demand", "Workflow\nownership", "Willingness\nto pay", "Defensi-\nbility", "Time to\nvalue", "Priority"]
    lane_w = Inches(2.85)
    score_w = Inches(1.32)
    pr_w = Inches(1.55)
    x0 = MARGIN
    xs = [x0]
    xs.append(x0 + lane_w)
    for k in range(4):
        xs.append(xs[-1] + score_w)
    xs.append(xs[-1] + score_w)  # priority start
    # header
    hy = Inches(1.7)
    hh = Inches(0.5)
    text(s, cols[0], xs[0] + Inches(0.1), hy, lane_w - Inches(0.2), hh, size=12, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    for k in range(5):
        text(s, cols[k + 1].replace("\n", " "), xs[1 + k], hy, score_w, hh, size=10.5, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    text(s, "Priority", xs[6], hy, pr_w, hh, size=12, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, MARGIN, hy + Inches(0.5), CONTENT_W, Pt(2), NAVY)
    # rows
    y = Inches(2.28)
    rh = Inches(0.4)
    for r, row in enumerate(SCORECARD):
        lane = row[0]
        if r % 2 == 0:
            rect(s, MARGIN, y, CONTENT_W, rh, SOFT)
        text(s, lane, xs[0] + Inches(0.1), y, lane_w - Inches(0.2), rh, size=12, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
        for k in range(5):
            v = row[1 + k]
            cx = xs[1 + k] + Inches(0.12)
            rect(s, cx, y + Inches(0.05), score_w - Inches(0.24), rh - Inches(0.1), HML_COLOR[v], radius=0.25)
            text(s, v, cx, y + Inches(0.05), score_w - Inches(0.24), rh - Inches(0.1), size=12, color=HML_TEXT[v], bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        pr = row[6]
        prx = xs[6] + Inches(0.1)
        rect(s, prx, y + Inches(0.05), pr_w - Inches(0.2), rh - Inches(0.1), PRIORITY_COLOR[pr], radius=0.4)
        text(s, pr, prx, y + Inches(0.05), pr_w - Inches(0.2), rh - Inches(0.1), size=10, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        y += rh
    # legend
    text(s, "H = high / attractive   ·   M = mixed   ·   L = weak    |    Scoring is a strategic judgment from builder activity and the ownership-vs-willingness-to-pay map.",
         MARGIN, Inches(6.45), CONTENT_W, Inches(0.4), size=10.5, color=MUTED, italic=True)
    foot(s, page, total)


def s_where_how(prs, page, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, WHITE)
    head(s, "Where To Play, And How To Win", "The two questions every executive bet has to answer")
    col_w = Inches(5.85)
    lx, rx = MARGIN, SLIDE_W - MARGIN - col_w
    rect(s, lx, Inches(1.75), col_w, Inches(4.55), SOFT, line=GRID, radius=0.04)
    rect(s, lx, Inches(1.75), col_w, Inches(0.6), NAVY, radius=0.04)
    rect(s, lx, Inches(1.75), Inches(0.1), Inches(0.6), TEAL)
    text(s, "WHERE TO PLAY", lx + Inches(0.3), Inches(1.75), col_w - Inches(0.6), Inches(0.6), size=16, color=TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, [{"text": t, "size": 13.5, "color": INK, "bullet": True, "space_before": 13} for t in [
        "Healthcare operations — deep workflow, high willingness to pay.",
        "Workflow automation — broadest builder activity, fast time-to-value.",
        "Finance & trading — error/cycle-time maps straight to money.",
        "Customer ops — structured data and clear SLAs to exploit.",
    ]], lx + Inches(0.35), Inches(2.6), col_w - Inches(0.7), Inches(3.5), shrink=True)
    rect(s, rx, Inches(1.75), col_w, Inches(4.55), SOFT, line=GRID, radius=0.04)
    rect(s, rx, Inches(1.75), col_w, Inches(0.6), NAVY, radius=0.04)
    rect(s, rx, Inches(1.75), Inches(0.1), Inches(0.6), GOLD)
    text(s, "HOW TO WIN", rx + Inches(0.3), Inches(1.75), col_w - Inches(0.6), Inches(0.6), size=16, color=GOLD, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, [{"text": t, "size": 13.5, "color": INK, "bullet": True, "space_before": 13} for t in [
        "Own context + actuation — write back into the system of record.",
        "Wrap it in governance — identity, scoping, audit, human-in-the-loop.",
        "Complete the job — don't stop at a summary.",
        "Instrument the ROI — prove the delta vs. the manual baseline.",
    ]], rx + Inches(0.35), Inches(2.6), col_w - Inches(0.7), Inches(3.5), shrink=True)
    foot(s, page, total)


def s_decision(prs, page, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    rect(s, 0, 0, SLIDE_W, Inches(0.16), TEAL)
    text(s, "The Decision In Front Of Us", MARGIN, Inches(0.42), CONTENT_W, Inches(0.7), size=30, color=WHITE, bold=True, font=FONT_H)
    rect(s, MARGIN, Inches(1.12), Inches(1.45), Inches(0.05), TEAL)
    text(s, "Three paths — one recommendation", MARGIN, Inches(1.26), CONTENT_W, Inches(0.4), size=14.5, color=LIGHT_TEAL)
    options = [
        ("OPTION A", "Own a vertical workflow", "Pick healthcare ops or finance and own the workflow end-to-end.", "Highest defensibility & willingness to pay.", True),
        ("OPTION B", "Build horizontal infra", "Provide the context / governance layer agents depend on.", "Stickier, but slower to revenue and more crowded.", False),
        ("OPTION C", "Wait and watch", "Hold until the lanes consolidate.", "Lowest cost today, highest opportunity cost.", False),
    ]
    gap = Inches(0.3)
    cw = (CONTENT_W - gap * 2) / 3
    top = Inches(2.0)
    h = Inches(3.2)
    for i, (tag, title, body, note, rec) in enumerate(options):
        x = MARGIN + i * (cw + gap)
        bg = TEAL if rec else NAVY_2
        rect(s, x, top, cw, h, bg, line=(TEAL if not rec else TEAL), radius=0.06, shadow=rec)
        text(s, tag, x + Inches(0.28), top + Inches(0.22), cw - Inches(0.5), Inches(0.3), size=12, color=(NAVY if rec else TEAL), bold=True)
        text(s, title, x + Inches(0.28), top + Inches(0.58), cw - Inches(0.56), Inches(0.7), size=20, color=(NAVY if rec else WHITE), bold=True, shrink=True)
        text(s, body, x + Inches(0.28), top + Inches(1.35), cw - Inches(0.56), Inches(0.9), size=13, color=(NAVY if rec else LIGHT_TEAL), shrink=True, ls=1.1)
        text(s, note, x + Inches(0.28), top + Inches(2.35), cw - Inches(0.56), Inches(0.7), size=11.5, color=(uc.RGBColor(0x0A,0x40,0x38) if rec else MUTED), italic=True, shrink=True)
        if rec:
            rect(s, x, top + h - Inches(0.42), cw, Inches(0.42), NAVY)
            text(s, "✓  RECOMMENDED", x, top + h - Inches(0.42), cw, Inches(0.42), size=12, color=TEAL, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, MARGIN, Inches(5.5), CONTENT_W, Inches(0.85), GOLD, radius=0.06)
    text(s, "THE ASK:  approve a 90-day, single-lane wedge bet — scoped, instrumented, and reviewed against a hard baseline.",
         MARGIN + Inches(0.4), Inches(5.5), CONTENT_W - Inches(0.8), Inches(0.85), size=15, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    foot(s, page, total, dark=True)


def s_section(prs, page, total, num, title, sub):
    uc.s_divider(prs, page, total, num, title, sub)


def main():
    a = uc.json.loads(uc.ANALYSIS.read_text(encoding="utf-8"))
    clusters = a["use_case_clusters"]
    sync2 = a["adjacency"]["sync2_matches"]
    reprises = a["adjacency"]["reprisesai_matches"]
    recs = a["recommendations"]

    uc.CHARTS.mkdir(parents=True, exist_ok=True)
    p_orgcount = uc.CHARTS / "orgcount.png"
    p_matrix = uc.CHARTS / "matrix_uc.png"
    uc.chart_orgcount(clusters, p_orgcount)
    uc.chart_matrix(p_matrix)

    prs = Presentation()
    prs.slide_width, prs.slide_height = SLIDE_W, SLIDE_H
    uc.wipe(prs)

    # patch the realization module footer text so reused slides share branding
    uc.FOOTER = FOOTER

    slides = []  # list of callables(page, total)

    # ---- SECTION 1: EXECUTIVE STORY ----
    slides.append(lambda p, t: s_section(prs, p, t, "01", "The Executive Read", "The market, the value, and the bet — in ten slides."))
    slides.append(lambda p, t: s_exec_summary(prs, p, t))
    slides.append(lambda p, t: s_storyboard(prs, p, t))
    slides.append(lambda p, t: s_pov(prs, p, t))
    slides.append(lambda p, t: uc.s_chart(prs, p, t, "Builder Activity Concentrates In Five Operational Lanes",
                                          "Number of organizations active in each use case", p_orgcount,
                                          "The market is voting with its feet: operational workflows, not generic assistants."))
    slides.append(lambda p, t: s_scorecard(prs, p, t))
    slides.append(lambda p, t: uc.s_chart(prs, p, t, "The Payoff Sits Where Ownership Meets Willingness To Pay",
                                          "Workflow ownership vs. willingness to pay, by use case", p_matrix,
                                          "Healthcare ops and finance occupy the top-right — deep ownership and strong willingness to pay.",
                                          img_w=Inches(9.0)))
    slides.append(lambda p, t: s_where_how(prs, p, t))
    slides.append(lambda p, t: s_decision(prs, p, t))

    # ---- SECTION 2: HOW THE VALUE GETS REALIZED (proof) ----
    slides.append(lambda p, t: s_section(prs, p, t, "02", "How The Value Gets Realized", "The same agent loop, wrapped around ten different operational jobs."))
    slides.append(lambda p, t: uc.s_landscape(prs, p, t, clusters))
    slides.append(lambda p, t: uc.s_pipeline(prs, p, t))
    slides.append(lambda p, t: uc.s_stack(prs, p, t))
    for ucase in uc.USE_CASES:
        slides.append(lambda p, t, _u=ucase: uc.s_usecase(prs, p, t, _u))

    # ---- SECTION 3: STRATEGIC DEEP DIVES ----
    slides.append(lambda p, t: s_section(prs, p, t, "03", "Two Bets Worth A Closer Look", "Where the pattern is strongest — and where it is most at risk."))
    slides.append(lambda p, t: uc.s_strategic(prs, p, t, "Healthcare Operations Is The Strongest Vertical Wedge", sync2,
        ["The lane is real; the strong names own deep workflow, not a front-desk wrapper.",
         "Scheduling, claims, billing, intake, and patient comms are the system-of-action wedges.",
         "Winners capture more of the actual clinic workflow end to end."],
        ["Own the EHR / RCM write-back, not just the conversation.",
         "Instrument collections and staffing ROI from day one."],
        "Does the product own enough of the clinic workflow to become system-of-action software?"))
    slides.append(lambda p, t: uc.s_strategic(prs, p, t, "Implementation Automation Is The Biggest Realization Risk", reprises,
        ["Fewer direct 'AI agency' clones than expected.",
         "The real risk: productized implementation software absorbing repeatable service work.",
         "Generic AI delivery is easily copied; a narrow owned workflow is not."],
        ["Specialize the wedge around one repeatable, painful workflow.",
         "Turn the service motion into owned product before someone else does."],
        "Can a service motion defend a wedge before software productizes the work?"))
    slides.append(lambda p, t: uc.s_risks(prs, p, t))
    slides.append(lambda p, t: uc.s_roadmap(prs, p, t))
    slides.append(lambda p, t: uc.s_reco(prs, p, t, recs[:4]))
    slides.append(lambda p, t: s_closing_exec(prs, p, t))

    total = len(slides) + 1  # + cover
    s_cover(prs, total)
    for i, fn in enumerate(slides, start=2):
        fn(i, total)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print(f"Saved {OUT} with {len(prs.slides._sldIdLst)} slides")


def s_closing_exec(prs, page, total):
    s = slide(prs)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    rect(s, 0, 0, Inches(0.18), SLIDE_H, TEAL)
    text(s, "THE BOTTOM LINE", MARGIN, Inches(0.9), Inches(6), Inches(0.4), size=14, color=TEAL, bold=True)
    text(s, "Buy the workflow, not the hype — and prove it in 90 days.",
         MARGIN, Inches(1.4), Inches(11.8), Inches(1.1), size=32, color=WHITE, bold=True, font=FONT_H, shrink=True)
    take = [
        ("Winners own workflows end-to-end", "Model novelty is not the moat; completing the job inside the system of record is."),
        ("Concentrate where pain meets pay", "Healthcare ops, finance, workflow automation, and customer ops lead the scorecard."),
        ("Make a single, scoped bet", "One lane, owned context + actuation + governance — not a broad platform."),
        ("Decide now, review in 90 days", "Approve the wedge, instrument the baseline, and judge it on a measurable delta."),
    ]
    top = Inches(3.05)
    for i, (t, d) in enumerate(take, 1):
        rect(s, MARGIN, top, Inches(0.55), Inches(0.55), TEAL, radius=0.18)
        text(s, str(i), MARGIN, top + Inches(0.06), Inches(0.55), Inches(0.4), size=18, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
        text(s, t, Inches(1.35), top - Inches(0.02), Inches(11), Inches(0.4), size=17, color=WHITE, bold=True)
        text(s, d, Inches(1.35), top + Inches(0.4), Inches(11), Inches(0.45), size=13, color=LIGHT_TEAL, shrink=True)
        top += Inches(0.97)
    foot(s, page, total, dark=True)


if __name__ == "__main__":
    main()
