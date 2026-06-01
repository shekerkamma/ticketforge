---
name: presentation-accessibility
description: WCAG accessibility audit for HTML presentations. Checks contrast ratios, font sizes, keyboard navigation, screen reader compatibility, and motion sensitivity. Use when preparing slides for conferences, public talks, or inclusive audiences.
---

# Presentation Accessibility Skill

Audits and fixes accessibility issues in HTML presentations following WCAG 2.1 AA guidelines.

## Audit Checklist

### 1. Color Contrast (WCAG 1.4.3)

Check all text elements against their backgrounds:

| Element | Minimum Ratio | Standard |
|---|---|---|
| Body text (< 18px) | 4.5:1 | AA |
| Large text (>= 18px bold or >= 24px) | 3:1 | AA |
| UI components & graphics | 3:1 | AA |

**How to check:**
- Extract all CSS color/background-color pairs
- Calculate contrast ratios using the relative luminance formula
- Flag any pairs below the minimum ratio
- Pay special attention to: light text on gradients, colored text on colored backgrounds, text over images

**Common presentation issues:**
- Light gray text on white backgrounds (subtitle text, captions)
- Low contrast syntax highlighting in code blocks
- Journey bar labels against colored fill
- Badge text against colored pill backgrounds

### 2. Font Sizes (WCAG 1.4.4)

Minimum readable sizes for presentation context (projected/shared screen):

| Element | Minimum Size |
|---|---|
| Slide titles (h1) | 28px / 1.75rem |
| Subtitles (h2, h3) | 20px / 1.25rem |
| Body text | 16px / 1rem |
| Code blocks | 14px / 0.875rem |
| Captions / labels | 12px / 0.75rem |

Flag any text below these thresholds.

### 3. Keyboard Navigation (WCAG 2.1.1)

Verify all interactive elements work without a mouse:

- [ ] Arrow keys navigate between slides
- [ ] Tab key reaches all interactive elements (links, buttons)
- [ ] Focus indicators are visible on focused elements
- [ ] No keyboard traps (can always navigate away)
- [ ] Escape key closes any modals or overlays
- [ ] TOC links are keyboard-accessible
- [ ] Skip-to-content link exists or first Tab reaches main content

### 4. Screen Reader Compatibility (WCAG 1.3.1, 4.1.2)

- [ ] Slides have proper heading hierarchy (h1 > h2 > h3, no skipped levels)
- [ ] Images have alt text (or are marked decorative with `alt=""`)
- [ ] ARIA landmarks exist (`role="main"`, `role="navigation"`)
- [ ] Current slide is announced (aria-live region or aria-current)
- [ ] Slide counter is accessible (not just visual)
- [ ] Code blocks have `role="code"` or are in `<code>` elements
- [ ] Lists use proper `<ul>`/`<ol>` markup, not styled divs

### 5. Motion & Animation (WCAG 2.3.1, 2.3.3)

- [ ] Respect `prefers-reduced-motion` media query
- [ ] No auto-playing animations longer than 5 seconds
- [ ] No flashing content (> 3 flashes per second)
- [ ] Slide transitions can be disabled
- [ ] Journey bar animation respects reduced motion preference

```css
/* Required: respect user motion preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 6. Semantic Structure (WCAG 1.3.1)

- [ ] Each slide is a `<section>` or has `role="region"` with aria-label
- [ ] Heading levels don't skip (no h1 → h4)
- [ ] Lists are semantic (`<ul>`, `<ol>`) not visual-only
- [ ] Tables have `<th>` headers with scope attributes
- [ ] Code examples use `<pre><code>` not just styled divs

### 7. Responsive & Zoom (WCAG 1.4.10)

- [ ] Content readable at 200% zoom without horizontal scrolling
- [ ] Text reflows properly when viewport narrows
- [ ] No content clipped or hidden at larger font sizes
- [ ] Touch targets are at least 44x44px on mobile

## Workflow

### Step 1: Read the Presentation

```bash
# Read the HTML file
```

Parse all CSS (inline `<style>` blocks and any linked stylesheets).

### Step 2: Automated Checks

Run each checklist category against the parsed HTML/CSS:

1. Extract all color pairs → calculate contrast ratios
2. Extract all font-size declarations → check minimums
3. Search for keyboard event handlers → verify completeness
4. Check semantic HTML elements → flag missing ARIA
5. Search for animation/transition CSS → check reduced-motion support
6. Validate heading hierarchy → flag skipped levels

### Step 3: Generate Report

Output a structured accessibility report:

```markdown
# Accessibility Audit Report

## Score: X/7 categories passing

### Critical Issues (must fix)
- [Issue]: [Location] — [Fix]

### Warnings (should fix)
- [Issue]: [Location] — [Fix]

### Passing
- [Category]: All checks passed
```

### Step 4: Fix Issues

For each critical issue, apply the fix:
- Add `prefers-reduced-motion` media query if missing
- Adjust contrast ratios by darkening/lightening colors
- Add missing ARIA attributes
- Fix heading hierarchy
- Add alt text placeholders for images

Delegate HTML changes to the `presentation-curator` agent if the presentation structure needs modification.

## Quick Fix Reference

| Issue | Fix |
|---|---|
| Low contrast text | Darken text color or lighten background |
| Missing alt text | Add descriptive `alt` attribute to `<img>` |
| No reduced-motion | Add `@media (prefers-reduced-motion)` block |
| Missing focus styles | Add `:focus-visible` outline styles |
| Skipped heading | Insert intermediate heading or adjust level |
| No ARIA landmarks | Add `role` attributes to main containers |
| No slide announcements | Add `aria-live="polite"` to slide counter |
