#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

REAL_HOME="$(getent passwd "$USER" 2>/dev/null | cut -d: -f6)"
if [[ -z "$REAL_HOME" ]]; then
  REAL_HOME="$HOME"
fi

GH_DIR_CANDIDATE="${REAL_HOME}/.config/gh"
SSH_DIR_CANDIDATE="${REAL_HOME}/.ssh"

if [[ -z "${GH_CONFIG_DIR:-}" && -d "$GH_DIR_CANDIDATE" ]]; then
  export GH_CONFIG_DIR="$GH_DIR_CANDIDATE"
fi

ok() {
  printf '[ok] %s\n' "$1"
}

warn() {
  printf '[warn] %s\n' "$1"
}

info() {
  printf '[info] %s\n' "$1"
}

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ok "git repository detected"
else
  warn "not inside a git repository"
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  ok "origin remote configured: $(git remote get-url origin)"
else
  warn "origin remote is missing"
fi

current_branch="$(git branch --show-current)"
if [[ -n "$current_branch" ]]; then
  info "current branch: $current_branch"
fi

if git config --get user.name >/dev/null 2>&1; then
  ok "git user.name configured: $(git config --get user.name)"
else
  warn "git user.name is not configured"
fi

if git config --get user.email >/dev/null 2>&1; then
  ok "git user.email configured: $(git config --get user.email)"
else
  warn "git user.email is not configured"
fi

if command -v gh >/dev/null 2>&1; then
  ok "GitHub CLI installed"
  if gh auth status >/dev/null 2>&1; then
    ok "GitHub CLI authenticated"
  else
    warn "GitHub CLI is not authenticated"
    info "run: gh auth login"
  fi
else
  warn "GitHub CLI is not installed"
fi

if command -v codex >/dev/null 2>&1; then
  ok "Codex CLI installed"
else
  warn "Codex CLI is not installed"
fi

if [[ -f "$SSH_DIR_CANDIDATE/id_ed25519.pub" || -f "$SSH_DIR_CANDIDATE/id_rsa.pub" ]]; then
  ok "SSH public key found"
else
  warn "no SSH public key found in ${SSH_DIR_CANDIDATE}"
fi

if [[ -f ".devcontainer/devcontainer.json" ]]; then
  ok "devcontainer configured for remote/cloud work"
else
  warn "devcontainer is missing"
fi

info "next step: run Codex from the repo root after your GitHub foundation is clean"
