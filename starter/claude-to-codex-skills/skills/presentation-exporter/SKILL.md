---
name: presentation-exporter
description: Export presentation slides to PDF, individual PNGs, or speaker notes markdown. Use when the user wants to share, print, or distribute their presentation in a portable format.
---

# Presentation Exporter Skill

Exports an HTML presentation to portable formats for sharing and distribution.

## Supported Formats

| Format | Output | Tool |
|--------|--------|------|
| `pdf` | Single PDF with all slides | Puppeteer / Chrome headless |
| `png` | One PNG per slide in `exports/slides/` | Puppeteer / Chrome headless |
| `notes` | Markdown file with speaker notes per slide | Text extraction |
| `all` | All of the above | Combined |

## Workflow

### Step 1: Locate the Presentation

Find the HTML presentation file. Common locations:
- `presentation/index.html`
- Any `.html` file the user specifies

Read the file to determine total slide count by counting `data-slide` attributes.

### Step 2: Export Based on Format

#### PDF Export

Use Puppeteer or Chrome headless to render each slide and print to PDF:

```bash
# Check if npx puppeteer is available
npx -y puppeteer --version 2>/dev/null

# Generate PDF via Node script
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: 'new'});
  const page = await browser.newPage();
  await page.setViewport({width: 1280, height: 720});
  await page.goto('file://$(pwd)/presentation/index.html');
  await page.pdf({path: 'exports/presentation.pdf', width: '1280px', height: '720px', printBackground: true});
  await browser.close();
})();
"
```

If Puppeteer is not available, fall back to `wkhtmltopdf` or suggest the user install it.

#### PNG Export (per slide)

Navigate to each slide and screenshot:

```bash
# Create output directory
mkdir -p exports/slides

# Screenshot each slide via Puppeteer
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: 'new'});
  const page = await browser.newPage();
  await page.setViewport({width: 1280, height: 720});
  await page.goto('file://$(pwd)/presentation/index.html');
  const totalSlides = await page.evaluate(() => document.querySelectorAll('[data-slide]').length);
  for (let i = 1; i <= totalSlides; i++) {
    await page.evaluate((n) => goToSlide(n), i);
    await page.waitForTimeout(300);
    await page.screenshot({path: 'exports/slides/slide-' + String(i).padStart(3, '0') + '.png'});
  }
  await browser.close();
})();
"
```

#### Notes Export

Parse the HTML to extract slide titles and any content marked as notes:

1. Read the presentation HTML
2. For each `data-slide` div, extract:
   - Slide number
   - `<h1>` title
   - Any element with class `speaker-notes` or `data-notes` attribute
   - Section name if it's a `section-slide`
3. Write to `exports/speaker-notes.md`

### Step 3: Report

After export, report:
- Format(s) generated
- File path(s) and sizes
- Total slides exported
- Any slides that failed to render

## Output Directory Structure

```
exports/
├── presentation.pdf          # Full deck as PDF
├── speaker-notes.md          # Extracted notes
└── slides/
    ├── slide-001.png
    ├── slide-002.png
    └── ...
```

## Fallback Options

If headless Chrome/Puppeteer is unavailable:
- **PDF**: Suggest `wkhtmltopdf` or opening in browser and using Print > Save as PDF
- **PNG**: Suggest the `/browse` skill to navigate and screenshot each slide
- **Notes**: Always works (pure text extraction, no browser needed)
