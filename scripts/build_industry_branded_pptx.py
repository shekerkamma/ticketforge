#!/usr/bin/env python3
"""Generic branded PPTX builder from deck-plan contract files.

This renderer follows the user's Canva-style executive deck system.

Reference assets:
- starter/claude-to-codex-skills/skills/industry-research-analysis-branded-deck/assets/Prasad_Agentic_AI_Use_Cases_Across_Industries.pptx
- starter/claude-to-codex-skills/skills/industry-research-analysis-branded-deck/assets/slide deck-reference.pdf

Use-case-heavy sections should follow the Canva-adapted card/strip layout
already proven in scripts/build_yc_usecase_deck.py rather than plain tables.
"""
from __future__ import annotations

import argparse
import json
import re
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


SKILL_ASSETS_DIR = (
    ROOT
    / "starter"
    / "claude-to-codex-skills"
    / "skills"
    / "industry-research-analysis-branded-deck"
)
SKILL_REFERENCES_DIR = SKILL_ASSETS_DIR / "references"
SKILL_ASSETS_DIR = SKILL_ASSETS_DIR / "assets"
TEMPLATE_MANIFEST_PATH = SKILL_REFERENCES_DIR / "template-manifest.json"


def load_template_manifest() -> dict:
    return json.loads(TEMPLATE_MANIFEST_PATH.read_text(encoding="utf-8"))


TEMPLATE_MANIFEST = load_template_manifest()
REFERENCE_ASSETS = TEMPLATE_MANIFEST["reference_assets"]
PREFERRED_USE_CASE_LAYOUT = TEMPLATE_MANIFEST.get("preferred_use_case_layout", "canva-card-strip")
CANONICAL_SLIDE_FAMILIES = set(TEMPLATE_MANIFEST.get("canonical_slide_families", []))

REFERENCE_TEMPLATE_PPTX = SKILL_ASSETS_DIR / REFERENCE_ASSETS["pptx"]
REFERENCE_TEMPLATE_PDF = SKILL_ASSETS_DIR / REFERENCE_ASSETS["pdf"]


def nice_title(slug: str) -> str:
    return re.sub(r"\s+", " ", slug.replace("-", " ").replace("_", " ")).title()


def ensure_reference_assets() -> None:
    missing = [path for path in (REFERENCE_TEMPLATE_PPTX, REFERENCE_TEMPLATE_PDF, TEMPLATE_MANIFEST_PATH) if not path.exists()]
    if missing:
        missing_str = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Missing packaged presentation template assets: {missing_str}")


def bullets_from_text(body: str) -> list[str]:
    if "|" in body:
        return [chunk.strip() for chunk in body.split("|") if chunk.strip()]
    return [body.strip()]


def compact(text: str, limit: int) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[:limit].rsplit(" ", 1)[0] + "..."


def build_cover(d: Deck, slide: dict, total: int, page: int) -> None:
    b = d.b
    s = d.slide(fill=b.NAVY)
    panel_w = Inches(9.05)
    d.rect(s, panel_w, 0, d.W - panel_w, d.H, b.NAVY_2)
    d.rect(s, panel_w, 0, Inches(0.06), d.H, b.TEAL)
    d.text(s, "EXECUTIVE DECK", d.M, Inches(0.95), Inches(6), Inches(0.32), size=15, color=b.TEAL, bold=True)
    d.text(s, slide["title"], d.M, Inches(1.45), Inches(7.7), Inches(1.48), size=36, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
    strap = next((cb["body"] for cb in slide["content_blocks"] if cb.get("label") == "Subtitle"), "")
    body = next((cb["body"] for cb in slide["content_blocks"] if cb.get("label") != "Subtitle"), "")
    if strap:
        d.text(s, strap, d.M, Inches(3.0), Inches(7.8), Inches(0.6), size=22, color=b.TEAL, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(3.8), Inches(1.5), Inches(0.06), b.TEAL)
    if body:
        d.text(s, body, d.M, Inches(4.1), Inches(7.8), Inches(1.0), size=15.5, color=b.WHITE, shrink=True)
    sx = panel_w + Inches(0.45)
    d.text(s, "DECK FOCUS", sx, Inches(1.88), Inches(3.4), Inches(0.24), size=11, color=b.GOLD, bold=True)
    for i, item in enumerate(slide["content_blocks"][:3]):
        y = Inches(2.35) + i * Inches(1.15)
        d.text(s, item.get("label", "").upper(), sx, y, Inches(3.2), Inches(0.2), size=10.5, color=b.TEAL, bold=True)
        d.text(s, compact(item["body"], 74), sx, y + Inches(0.24), Inches(3.15), Inches(0.7), size=12.2, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, page, total, dark=True)


def build_agenda(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    top = Inches(1.95)
    for i, block in enumerate(slide["content_blocks"], start=1):
        d.rect(s, d.M, top, Inches(0.72), Inches(0.72), d.b.TEAL, radius=0.16)
        d.text(s, f"{i:02d}", d.M, top + Inches(0.12), Inches(0.72), Inches(0.46), size=22, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, block["label"], d.M + Inches(0.95), top + Inches(0.02), Inches(9.5), Inches(0.3), size=20, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, block["body"], d.M + Inches(0.95), top + Inches(0.38), Inches(10.7), Inches(0.34), size=13.5, color=d.b.MUTED, shrink=True)
        top += Inches(1.1)
    d.footer(s, page, total)


def build_divider(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, d.b.TEAL)
    d.text(s, slide.get("section", "").upper(), d.M, Inches(2.0), Inches(4), Inches(0.4), size=14, color=d.b.TEAL, bold=True)
    d.text(s, slide["title"], d.M, Inches(2.55), Inches(11.5), Inches(1.2), size=33, color=d.b.WHITE, bold=True, font=d.b.FONT_H, shrink=True)
    body = slide["content_blocks"][0]["body"] if slide["content_blocks"] else ""
    d.rect(s, d.M, Inches(3.82), Inches(1.5), Inches(0.06), d.b.TEAL)
    d.text(s, body, d.M, Inches(4.1), Inches(10.8), Inches(0.8), size=16.5, color=d.b.LIGHT_TEAL, shrink=True)
    d.footer(s, page, total, dark=True)


def build_summary_cards(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    gap = Inches(0.28)
    cw = (d.CW - gap) / 2
    ch = Inches(1.62)
    top = Inches(1.9)
    for i, block in enumerate(slide["content_blocks"][:4]):
        row, col = divmod(i, 2)
        x = d.M + col * (cw + gap)
        y = top + row * (ch + Inches(0.2))
        d.rect(s, x, y, cw, ch, d.b.SOFT, line=d.b.GRID, radius=0.05, shadow=True)
        d.rect(s, x, y, Inches(0.1), ch, d.b.TEAL)
        d.text(s, block["label"], x + Inches(0.2), y + Inches(0.12), cw - Inches(0.35), Inches(0.28), size=11.8, color=d.b.ACCENT, bold=True, shrink=True)
        d.text(s, compact(block["body"], 128), x + Inches(0.2), y + Inches(0.46), cw - Inches(0.36), Inches(0.95), size=10.5, color=d.b.INK, shrink=True)
    d.footer(s, page, total)


def build_kpi_grid(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    metrics = [block for block in slide["content_blocks"] if block["kind"] == "metric"][:4]
    gap = Inches(0.25)
    cw = (d.CW - gap * 3) / 4
    top = Inches(1.9)
    h = Inches(2.2)
    for i, block in enumerate(metrics):
        stat, note = (block["body"].split("|", 1) + [""])[:2]
        x = d.M + i * (cw + gap)
        d.rect(s, x, top, cw, h, d.b.NAVY, radius=0.06, shadow=True)
        d.text(s, stat, x, top + Inches(0.22), cw, Inches(0.6), size=32, color=d.b.GOLD, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, block["label"], x + Inches(0.15), top + Inches(0.92), cw - Inches(0.3), Inches(0.68), size=12, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, note, x + Inches(0.12), top + Inches(1.65), cw - Inches(0.24), Inches(0.35), size=10, color=d.b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    callout = next((b["body"] for b in slide["content_blocks"] if b["kind"] == "callout"), "")
    if callout:
        d.rect(s, d.M, Inches(4.45), d.CW, Inches(0.72), d.b.SOFT, line=d.b.GRID, radius=0.04)
        d.text(s, callout, d.M + Inches(0.25), Inches(4.45), d.CW - Inches(0.5), Inches(0.72), size=13.4, color=d.b.INK, bold=True, italic=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.footer(s, page, total)


def build_bar_chart(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    items = [(b["label"], float(b["body"])) for b in slide["content_blocks"] if b["kind"] == "chart-brief"]
    max_value = max(v for _, v in items) if items else 1.0
    top = Inches(1.8)
    label_w = Inches(4.4)
    bar_max = Inches(5.8)
    row_h = Inches(0.72)
    for i, (label, value) in enumerate(items):
        y = top + i * Inches(0.9)
        d.text(s, label, d.M, y + Inches(0.12), label_w, Inches(0.32), size=12.2, color=d.b.NAVY, bold=True, shrink=True)
        d.rect(s, d.M + label_w + Inches(0.2), y + Inches(0.08), bar_max, Inches(0.36), d.b.SOFT, line=d.b.GRID, radius=0.03)
        width = bar_max * (value / max_value)
        d.rect(s, d.M + label_w + Inches(0.2), y + Inches(0.08), width, Inches(0.36), d.b.TEAL if i == 0 else d.b.ACCENT, radius=0.03)
        d.text(s, f"{value:g}", d.M + label_w + Inches(0.25) + width, y + Inches(0.07), Inches(0.6), Inches(0.28), size=11, color=d.b.NAVY, bold=True)
    d.footer(s, page, total)


def build_comparison(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    cols = [b for b in slide["content_blocks"] if b["kind"] == "comparison-column"][:2]
    col_w = Inches(5.9)
    xs = [d.M, d.W - d.M - col_w]
    accents = [d.b.TEAL, d.b.CORAL]
    for x, accent, block in zip(xs, accents, cols):
        d.rect(s, x, Inches(1.82), col_w, Inches(4.35), d.b.SOFT, line=d.b.GRID, radius=0.05, shadow=True)
        d.rect(s, x, Inches(1.82), col_w, Inches(0.6), d.b.NAVY, radius=0.05)
        d.rect(s, x, Inches(1.82), Inches(0.12), Inches(0.6), accent)
        d.text(s, block["label"].upper(), x + Inches(0.24), Inches(1.95), col_w - Inches(0.48), Inches(0.28), size=14, color=accent, bold=True)
        items = bullets_from_text(block["body"])
        d.text(s, [{"text": item, "size": 12, "color": d.b.INK, "bullet": True, "space_before": 10} for item in items], x + Inches(0.28), Inches(2.68), col_w - Inches(0.56), Inches(3.0), shrink=True)
    d.footer(s, page, total)


def build_use_case_table(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    subtitle = (
        "Use-case cards work better here than a dense table because executives need a fast visual scan "
        "of workflow, business value, and prioritization."
    )
    d.rect(s, d.M, Inches(1.28), Inches(1.5), Inches(0.05), d.b.TEAL)
    d.text(s, subtitle, d.M, Inches(1.42), d.CW, Inches(0.42), size=13.2, color=d.b.MUTED, shrink=True)

    cards = slide["content_blocks"]
    cols = 2
    gap_x = Inches(0.28)
    gap_y = Inches(0.22)
    card_w = (d.CW - gap_x) / cols
    card_h = Inches(1.28)
    top0 = Inches(1.9)
    for idx, block in enumerate(cards):
        row, col = divmod(idx, cols)
        x = d.M + col * (card_w + gap_x)
        y = top0 + row * (card_h + gap_y)
        accent = d.b.TEAL if idx < 2 else d.b.ACCENT
        d.rect(s, x, y, card_w, card_h, d.b.SOFT, line=d.b.GRID, radius=0.06, shadow=True)
        d.rect(s, x, y, Inches(0.11), card_h, accent)
        d.rect(s, x + card_w - Inches(0.66), y + Inches(0.14), Inches(0.46), Inches(0.46), d.b.NAVY, radius=0.16)
        d.text(
            s,
            f"{idx + 1}",
            x + card_w - Inches(0.66),
            y + Inches(0.2),
            Inches(0.46),
            Inches(0.22),
            size=14,
            color=d.b.GOLD,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
        d.text(s, block["label"], x + Inches(0.24), y + Inches(0.14), card_w - Inches(1.05), Inches(0.26), size=13.2, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, block["body"], x + Inches(0.24), y + Inches(0.46), card_w - Inches(0.42), Inches(0.58), size=10.6, color=d.b.INK, shrink=True)

    d.rect(s, d.M, Inches(6.35), d.CW, Inches(0.5), d.b.NAVY, radius=0.04)
    d.text(
        s,
        "Prioritize the top two or three cards first; the point is sequencing by executive value, not parallelizing every use case.",
        d.M + Inches(0.2),
        Inches(6.35),
        d.CW - Inches(0.4),
        Inches(0.5),
        size=11.5,
        color=d.b.LIGHT_TEAL,
        bold=True,
        anchor=MSO_ANCHOR.MIDDLE,
        shrink=True,
    )
    d.footer(s, page, total)


def build_case_study(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.TEAL)
    panel_w = Inches(8.85)
    strip_w = d.W - panel_w
    d.rect(s, panel_w, 0, strip_w, d.H, d.b.NAVY)
    d.rect(s, panel_w, 0, Inches(0.06), d.H, d.b.GOLD)
    cards = [b for b in slide["content_blocks"] if b["kind"] == "company-card"]
    implication_items: list[str] = []
    for block in slide["content_blocks"]:
        if block["kind"] == "bullet-list":
            implication_items.extend(bullets_from_text(block["body"]))
    account_signal = cards[0]["body"] if len(cards) > 0 else ""
    what_to_sell = cards[1]["body"] if len(cards) > 1 else ""
    executive_logic = cards[2]["body"] if len(cards) > 2 else ""
    card_one_label = cards[0]["label"].upper() if len(cards) > 0 else "CURRENT ACCOUNT SIGNAL"
    card_two_label = cards[1]["label"].upper() if len(cards) > 1 else "WHAT TO SELL"
    card_three_label = cards[2]["label"].upper() if len(cards) > 2 else "EXECUTIVE LOGIC"
    title_tail = slide["title"].split(":", 1)[1].strip() if ":" in slide["title"] else slide["title"]

    d.text(s, slide["section"].upper(), d.M, Inches(0.28), Inches(3.5), Inches(0.25), size=11.5, color=d.b.NAVY, bold=True)
    d.text(s, title_tail, d.M, Inches(0.55), panel_w - Inches(1.0), Inches(0.62), size=22, color=d.b.WHITE, bold=True, font=d.b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(1.15), Inches(1.55), Inches(0.04), d.b.NAVY)

    left_card_w = Inches(3.82)
    lx = d.M
    rx = d.M + left_card_w + Inches(0.22)
    d.rect(s, lx, Inches(1.36), left_card_w, Inches(1.82), d.b.WHITE, radius=0.05, shadow=True)
    d.text(s, card_one_label, lx + Inches(0.2), Inches(1.47), left_card_w - Inches(0.4), Inches(0.22), size=10.8, color=d.b.ACCENT, bold=True, shrink=True)
    d.text(s, compact(account_signal, 165), lx + Inches(0.2), Inches(1.77), left_card_w - Inches(0.4), Inches(1.26), size=10.2, color=d.b.INK, shrink=True)

    d.rect(s, rx, Inches(1.36), left_card_w, Inches(1.82), d.b.WHITE, radius=0.05, shadow=True)
    d.text(s, card_two_label, rx + Inches(0.2), Inches(1.47), left_card_w - Inches(0.4), Inches(0.22), size=10.8, color=d.b.ACCENT, bold=True, shrink=True)
    d.text(s, compact(what_to_sell, 165), rx + Inches(0.2), Inches(1.77), left_card_w - Inches(0.4), Inches(1.26), size=10.2, color=d.b.INK, shrink=True)

    d.rect(s, d.M, Inches(3.42), panel_w - d.M * 2, Inches(0.88), d.b.NAVY, radius=0.05)
    d.text(s, card_three_label, d.M + Inches(0.2), Inches(3.52), Inches(3.2), Inches(0.2), size=10.4, color=d.b.TEAL, bold=True, shrink=True)
    d.text(
        s,
        compact(executive_logic, 215),
        d.M + Inches(0.2),
        Inches(3.78),
        panel_w - d.M * 2 - Inches(0.4),
        Inches(0.38),
        size=10.4,
        color=d.b.WHITE,
        bold=True,
        shrink=True,
    )

    d.rect(s, d.M, Inches(4.5), panel_w - d.M * 2, Inches(1.35), d.b.WHITE, radius=0.05, shadow=True)
    d.text(s, "HOW TO POSITION THIS", d.M + Inches(0.2), Inches(4.62), Inches(2.8), Inches(0.22), size=11, color=d.b.ACCENT, bold=True)
    d.text(
        s,
        [{"text": compact(bullet, 82), "size": 9.6, "color": d.b.INK, "bullet": True, "space_before": 3} for bullet in implication_items[:2]],
        d.M + Inches(0.2),
        Inches(4.9),
        panel_w - d.M * 2 - Inches(0.4),
        Inches(0.78),
        shrink=True,
    )

    sx = panel_w + Inches(0.28)
    d.text(s, "EXECUTIVE ACTION", sx, Inches(0.48), strip_w - Inches(0.42), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.rect(s, sx, Inches(0.82), Inches(1.0), Inches(0.04), d.b.GOLD)
    d.text(
        s,
        "This program matters when it improves a real automotive workflow with reusable data, clear ownership, and measurable operating leverage.",
        sx,
        Inches(1.0),
        strip_w - Inches(0.5),
        Inches(0.85),
        size=12.0,
        color=d.b.WHITE,
        bold=True,
        shrink=True,
    )
    d.text(s, "ACTION CHECKS", sx, Inches(2.18), strip_w - Inches(0.5), Inches(0.22), size=11.5, color=d.b.GOLD, bold=True)
    checks = [
        "Named workflow owner",
        "Clear business metric",
        "Uses existing data and system flow",
        "Can scale without a full replatform first",
    ]
    d.text(
        s,
        [{"text": item, "size": 11.2, "color": d.b.LIGHT_TEAL, "bullet": True, "space_before": 9} for item in checks],
        sx,
        Inches(2.48),
        strip_w - Inches(0.54),
        Inches(1.85),
        shrink=True,
    )
    d.text(s, "CUSTOMER FIT", sx, Inches(4.66), strip_w - Inches(0.5), Inches(0.22), size=11.5, color=d.b.GOLD, bold=True)
    fit_rows = [
        ("Data exhaust", "High"),
        ("Workflow ownership", "High"),
        ("Executive relevance", "High"),
        ("Time-to-value", "Medium/High"),
    ]
    y = Inches(4.96)
    for label, value in fit_rows:
        d.rect(s, sx, y, strip_w - Inches(0.55), Inches(0.34), d.b.NAVY_2, radius=0.04)
        d.text(s, label, sx + Inches(0.12), y, Inches(1.7), Inches(0.34), size=9.8, color=d.b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        d.text(s, value, sx + Inches(1.95), y, strip_w - Inches(2.6), Inches(0.34), size=9.8, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        y += Inches(0.43)
    d.footer(s, page, total)


def build_use_case_card_grid(d: Deck, slide: dict, total: int, page: int) -> None:
    build_use_case_table(d, slide, total, page)


def build_use_case_deep_dive(d: Deck, slide: dict, total: int, page: int) -> None:
    build_case_study(d, slide, total, page)


def build_customer_fit(d: Deck, slide: dict, total: int, page: int) -> None:
    build_comparison(d, slide, total, page)


def build_executive_action(d: Deck, slide: dict, total: int, page: int) -> None:
    build_roadmap(d, slide, total, page)


def build_roadmap(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    steps = [b for b in slide["content_blocks"] if b["kind"] == "roadmap-step"]
    top = Inches(1.95)
    for idx, block in enumerate(steps):
        title, body = (block["body"].split("|", 1) + [""])[:2]
        y = top + idx * Inches(0.92)
        d.rect(s, d.M, y, Inches(0.68), Inches(0.68), d.b.TEAL, radius=0.18)
        d.text(s, block["label"], d.M, y + Inches(0.11), Inches(0.68), Inches(0.42), size=20, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, title, d.M + Inches(0.95), y + Inches(0.02), Inches(3.8), Inches(0.24), size=13, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, d.M + Inches(0.95), y + Inches(0.28), d.CW - Inches(1.1), Inches(0.42), size=10.8, color=d.b.INK, shrink=True)
    d.footer(s, page, total)


def build_bullets(d: Deck, slide: dict, total: int, page: int) -> None:
    s = d.slide(fill=d.b.WHITE)
    d.header(s, slide["title"])
    bullets = []
    for block in slide["content_blocks"]:
        text = block["body"]
        if block.get("label"):
            text = f'{block["label"]}: {text}'
        bullets.append({"text": compact(text, 120), "size": 10.6, "color": d.b.INK, "bullet": True, "space_before": 7})
    d.text(s, bullets, d.M, Inches(1.9), d.CW, Inches(5.05), shrink=True)
    d.footer(s, page, total)


BUILDERS = {
    "hero": build_cover,
    "agenda": build_agenda,
    "section-divider": build_divider,
    "summary-cards": build_summary_cards,
    "kpi-grid": build_kpi_grid,
    "bar-chart": build_bar_chart,
    "comparison": build_comparison,
    "use-case-table": build_use_case_table,
    "use-case-card-grid": build_use_case_card_grid,
    "case-study": build_case_study,
    "use-case-deep-dive": build_use_case_deep_dive,
    "customer-fit": build_customer_fit,
    "executive-action": build_executive_action,
    "roadmap": build_roadmap,
    "bullets": build_bullets,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()

    ensure_reference_assets()

    slug = args.slug
    deck_plan_path = ROOT / "analytics-comms" / slug / "deck-plan.json"
    with deck_plan_path.open() as fh:
        deck_plan = json.load(fh)

    footer = f"{nice_title(slug)}  |  Research-backed executive deck  |  June 2026"
    d = Deck(footer=footer)
    slides = deck_plan["slides"]
    total = len(slides)
    for page, slide in enumerate(slides, start=1):
        if slide.get("slide_type") in {"use-case-table", "case-study"} and PREFERRED_USE_CASE_LAYOUT == "canva-card-strip":
            slide_type = "use-case-card-grid" if slide.get("slide_type") == "use-case-table" else "use-case-deep-dive"
        else:
            slide_type = slide.get("slide_type")
        if slide_type and CANONICAL_SLIDE_FAMILIES and slide_type not in CANONICAL_SLIDE_FAMILIES:
            slide_type = slide.get("slide_type")
        builder = BUILDERS.get(slide_type, build_bullets)
        builder(d, slide, total, page)

    out = ROOT / "docs" / "reports" / f"{slug}-branded.pptx"
    if total < 25:
        print(f"warning: deck-plan only has {total} slides; consider expanding to 25+ for executive depth")
    d.save(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
