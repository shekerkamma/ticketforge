---
name: time-tokyo
description: Display the current time in Japan Standard Time (JST, UTC+9). Use when the user asks for the current time in Tokyo, Japan time, or JST.
---

# Time Tokyo Skill

This skill displays the current date and time in Japan Standard Time (JST).

## Task

Display the current date and time in Japan Standard Time (UTC+9).

## Instructions

1. **Get Current Time**: Run the following bash command:
   ```
   TZ='Asia/Tokyo' date '+%Y-%m-%d %H:%M:%S %Z'
   ```

2. **Display Result**: Show the time in this format:
   ```
   Current Time in Tokyo (JST): YYYY-MM-DD HH:MM:SS JST
   ```

## Requirements

- Always use the `Asia/Tokyo` timezone (UTC+9)
- Use 24-hour format
- Include the date alongside the time
- Keep the output concise — no extra commentary
