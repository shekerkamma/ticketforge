---
name: presentation-theme
description: Swap visual themes on HTML presentations — dark/light mode, corporate branding, conference themes, or custom color schemes. Preserves slide content while transforming the visual identity. Use when the user wants to restyle their presentation for a different audience or context.
---

# Presentation Theme Skill

Swaps the visual theme of an HTML presentation while preserving all content and structure.

## Built-in Themes

### Dark (default for most tech presentations)

```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #1a1a2e;
  --bg-card: #16213e;
  --text-primary: #e0e0e0;
  --text-secondary: #a0a0a0;
  --text-heading: #ffffff;
  --accent-primary: #4fc3f7;
  --accent-secondary: #81c784;
  --accent-warning: #ffb74d;
  --accent-danger: #ef5350;
  --border-color: #333;
  --code-bg: #1e1e1e;
  --code-text: #d4d4d4;
}
```

### Light (conferences with bright projectors)

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --bg-card: #fafafa;
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-heading: #1a1a1a;
  --accent-primary: #1976d2;
  --accent-secondary: #388e3c;
  --accent-warning: #f57c00;
  --accent-danger: #d32f2f;
  --border-color: #e0e0e0;
  --code-bg: #f5f5f5;
  --code-text: #333333;
}
```

### Corporate (neutral, professional)

```css
:root {
  --bg-primary: #1b2838;
  --bg-secondary: #2c3e50;
  --bg-card: #34495e;
  --text-primary: #ecf0f1;
  --text-secondary: #bdc3c7;
  --text-heading: #ffffff;
  --accent-primary: #3498db;
  --accent-secondary: #2ecc71;
  --accent-warning: #f39c12;
  --accent-danger: #e74c3c;
  --border-color: #4a6785;
  --code-bg: #1a252f;
  --code-text: #ecf0f1;
}
```

### High Contrast (accessibility-first)

```css
:root {
  --bg-primary: #000000;
  --bg-secondary: #1a1a1a;
  --bg-card: #262626;
  --text-primary: #ffffff;
  --text-secondary: #e0e0e0;
  --text-heading: #ffffff;
  --accent-primary: #00bfff;
  --accent-secondary: #00ff7f;
  --accent-warning: #ffd700;
  --accent-danger: #ff4444;
  --border-color: #555;
  --code-bg: #1a1a1a;
  --code-text: #ffffff;
}
```

## Workflow

### Step 1: Read Current Theme

1. Read the presentation HTML
2. Extract the current `<style>` block
3. Identify all color values (hex, rgb, hsl, named colors)
4. Map them to semantic categories (background, text, accent, border, code)

### Step 2: Build Color Map

Create a mapping from current colors → new theme colors:

```json
{
  "#0a0a0a": "--bg-primary",
  "#1a1a2e": "--bg-secondary",
  "#e0e0e0": "--text-primary",
  "#4fc3f7": "--accent-primary"
}
```

### Step 3: Apply Theme

Two approaches depending on current CSS structure:

#### If CSS uses custom properties (`:root` variables)
- Update the `:root` block with new values
- All references automatically update

#### If CSS uses hardcoded colors
1. Add a `:root` block with CSS custom properties
2. Replace hardcoded color values with `var(--property-name)` references
3. This is a one-time refactor that makes future theme swaps trivial

### Step 4: Handle Special Elements

Some elements need theme-aware adjustments beyond color swaps:

| Element | Dark Theme | Light Theme |
|---|---|---|
| Code blocks | Dark bg, light text | Light bg, dark text |
| Syntax highlighting | VS Code Dark+ colors | VS Code Light+ colors |
| Journey bar | Semi-transparent dark | Semi-transparent light |
| Box shadows | Subtle glow | Subtle drop shadow |
| Borders | Lighter than bg | Darker than bg |
| Good/bad cards | Green/red on dark | Green/red on light |

### Step 5: Verify Contrast

After applying the theme, verify all text/background combinations meet WCAG AA contrast ratios:
- Normal text: 4.5:1 minimum
- Large text: 3:1 minimum
- Flag any combinations below threshold

### Step 6: Syntax Highlighting Theme

Update code block syntax highlighting to match the overall theme:

**Dark themes:**
```css
.comment { color: #6a9955; }
.key     { color: #9cdcfe; }
.string  { color: #ce9178; }
.cmd     { color: #dcdcaa; }
```

**Light themes:**
```css
.comment { color: #008000; }
.key     { color: #0451a5; }
.string  { color: #a31515; }
.cmd     { color: #795e26; }
```

## Custom Themes

When the user provides brand colors or a custom palette:

1. Ask for or extract:
   - Primary brand color
   - Secondary color (optional)
   - Preferred background (dark/light)
2. Generate a full theme by:
   - Using the brand color as `--accent-primary`
   - Deriving complementary colors for secondary accents
   - Setting appropriate bg/text colors for the dark/light preference
   - Ensuring all contrast ratios pass WCAG AA

## Theme File (Optional)

For reusable themes, save to a standalone CSS file:

```
presentation/
├── index.html
├── themes/
│   ├── dark.css
│   ├── light.css
│   ├── corporate.css
│   └── custom.css
└── speaker-notes.json
```

The presentation can load themes via a `<link>` tag or inline injection.

## Rules

- Never modify slide content — only CSS/styling
- Always verify contrast ratios after applying a theme
- Preserve the journey bar color gradient logic (HSL interpolation from red to green)
- Keep syntax highlighting readable in the new theme
- If the presentation already uses CSS custom properties, only update `:root` values
- Report before/after comparison: old theme → new theme with key color changes
