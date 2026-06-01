---
name: ss
description: Load the most recent screenshots from a screenshot inbox and act on them quickly. Use when the user invokes `/ss`-style screenshot workflows, wants recent screenshots explained, compared, transcribed, remixed, or used as visual context for a task.
---

# Screenshot Inbox

Treat recent local screenshots as structured visual input.

## Configuration

Determine the screenshot folder in this order:

1. `SCREENSHOT_INBOX`
2. `~/Pictures/Screenshots`
3. `~/Pictures/Screen Shots`
4. `~/Desktop`

If none of these exist or no screenshots are found, say so directly.

## Parsing

Interpret the arguments this way:

- no args -> `N=1`, action=`explain`
- first token is a positive integer -> that is `N`
- first token is `diff` -> `N=2`, action=`compare`
- otherwise -> `N=1`, action=`<full arg string>`

## Load the images

List the most recent PNG, JPG, or JPEG files:

```bash
find "<folder>" -maxdepth 1 -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) -printf '%T@ %p
' | sort -nr | head -N
```

Then inspect each returned image path with the local image-viewing tool available in the environment.

## Actions

- `explain`: describe the screenshot concretely and transcribe key visible text
- `compare`: compare multiple screenshots and call out what changed
- `transcribe`: extract visible text faithfully
- `fix`: treat the screenshot as a bug report or UI defect and connect it to the repo when possible
- `remix` or freeform: extract the pattern and adapt it to the user's context
- `infographic`: synthesize multiple screenshots into one HTML artifact saved in the current working directory

## Rules

- Confirm which screenshots were loaded before acting on them.
- Keep outputs tight; this workflow is for speed.
- If the user wants non-inbox images, ask for explicit file paths instead of guessing.
