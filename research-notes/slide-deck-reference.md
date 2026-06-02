---
source_type: local-document
source_path: /mnt/c/Users/sheke/OneDrive/Desktop/slide deck-reference.pdf
title: slide deck-reference
---

# Slide Deck Reference

## Page 1

M A S T E R I N G CLAUDE CODE Complete Practical Guide — All Tips, Prompts & Workflows AGENTIC AI ALL PROMPTS PRO TIPS SDK & CLI Source: Anthropic — Boris, Member of Technical Staff | youtube.com/watch?v=AOfogJZ70OQ

## Page 2

What We'll Cover 10 sections • Every prompt, workflow, and configuration option from the video 01 What is Claude Code? Agentic AI, capabilities, installation 02 Initial Setup Terminal, theme, GitHub app, dictation 03 Tip 1 — Codebase Q&A Start here: explore before editing 04 Tip 2 — Editing Code Plan→code, commit/push/PR, workflows 05 Tip 3 — Integrate Tools Bash CLI tools + MCP servers 06 Tip 4 — Context (CLAUDE.md) Memory, slash commands, hierarchy 07 Configuration Hierarchy Project, global, enterprise policies 08 Key Bindings All shortcuts and terminal tricks 09 SDK & Pipeline Mode Headless, JSON, Unix pipes 10 Advanced: Parallel Sessions tmux, SSH, Git worktrees

## Page 3

S E C T I O N 0 1 What is Claude Code? A new kind of agentic AI coding assistant

## Page 4

Claude Code is NOT Line Completion Previous generation vs. the new generation Previous Gen (Copilot-style) ✗ Autocomplete one line at a time ✗ Suggests a few lines based on cursor context ✗ You guide every edit manually ✗ IDE plugin that watches you type Claude Code (Agentic) ✓ Builds entire features end-to-end ✓ Writes whole files and functions ✓ Fixes entire bugs autonomously ✓ Works across the whole repo

## Page 5

Key Capabilities What makes Claude Code different IDE-Agnostic Works with VS Code, Xcode, JetBrains, Vim, Emacs — any IDE, any terminal Code Stays Local No remote index, no upload to any database, not trained on your code Instant Start No indexing wait. Open Claude Code and use it immediately — zero setup General Purpose Coding, debugging, Q&A, CI pipelines, incident response — one tool Any Environment Local machine, remote SSH, tmux, Docker — wherever your terminal runs Fully Agentic Plans, explores, edits, tests, and iterates — all without hand-holding

## Page 6

Installation All you need is Node.js npm install -g @anthropic-ai/claude-code Requirement Node.js installed on your machine How to start Type claude in any terminal Works on macOS, Linux, Windows (WSL) IDE needed? No — works with any IDE or none Remote? Yes — SSH, tmux, any remote environment

## Page 7

S E C T I O N 0 2 Initial Setup Run these commands once — right after install

## Page 8

Setup Step 1 — /terminal-setup Make the terminal experience smoother /terminal-setup What it does Enables Shift+Enter for new lines inside Claude Code Without it You need to type backslash + enter for multiline prompts With it Press Shift+Enter to start a new line — much more natural Why it matters Longer, more detailed prompts are easier to write and edit

## Page 9

Setup Step 2 — /theme Choose your color theme /theme LIGHT Standard light mode Best for bright environments DARK Dark background, light text Best for low-light / night coding DALTONIZE Color-blind friendly palette Adjusted colors for accessibility

## Page 10

Setup Step 3 — /install-github-app Connect Claude Code to GitHub /install-github-app What it installs A GitHub App on your repos that Claude Code can interact with @-mention on Issues Tag Claude on any GitHub issue: "@claude investigate this bug" — Claude responds directly @-mention on PRs Tag Claude on any pull request — it will review, comment, or fix code GitHub Actions Pairs with CI pipelines — Claude can auto-label issues, summarize PRs, more

## Page 11

Setup Step 4 — Customize Allowed Tools Stop being prompted for every command you use regularly Problem: Claude asks permission for every bash command → constant approval interruptions → slow workflow Solution: Add frequently-used commands to your allowed tools list → auto-approved, no interruption E X A M P L E S T O A U T O - A P P R O V E Bash(git log) Bash(npm test) Bash(grep) Bash(cat) Bash(ls) Where to configure: • Project .claude/settings.json (shared) • ~/.claude/settings.json (personal global) • Enterprise policy file (org-wide) • Just tell Claude: 'remember to always allow this'

## Page 12

Setup Tip — macOS Dictation Talk to Claude Code instead of typing Boris: "I just hit the dictation key twice and speak my prompt — I talk to Claude like another engineer" 1 Step 1 Open System Settings on macOS 2 Step 2 Go to Accessibility → Dictation 3 Step 3 Enable Dictation 4 Step 4 Set a shortcut key (default: double-tap Fn or Mic key) 5 Step 5 In Claude Code, double-tap your dictation key and speak your prompt Works for detailed, specific prompts — speaking is faster than typing long context-rich instructions
