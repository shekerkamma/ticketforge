#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

REAL_HOME="$(getent passwd "$USER" 2>/dev/null | cut -d: -f6)"
if [[ -z "$REAL_HOME" ]]; then
  REAL_HOME="$HOME"
fi

GH_DIR_CANDIDATE="${REAL_HOME}/.config/gh"

if [[ -z "${GH_CONFIG_DIR:-}" && -d "$GH_DIR_CANDIDATE" ]]; then
  export GH_CONFIG_DIR="$GH_DIR_CANDIDATE"
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI is required. Install it first."
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated. Run: gh auth login"
  exit 1
fi

repo_name="$(gh repo view --json nameWithOwner -q .nameWithOwner)"

apply_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if gh api "repos/${repo_name}/labels/${name}" >/dev/null 2>&1; then
    gh api --method PATCH "repos/${repo_name}/labels/${name}" \
      -f new_name="$name" \
      -f color="$color" \
      -f description="$description" >/dev/null
    echo "updated label: $name"
  else
    gh api --method POST "repos/${repo_name}/labels" \
      -f name="$name" \
      -f color="$color" \
      -f description="$description" >/dev/null
    echo "created label: $name"
  fi
}

apply_label "bug" "d73a4a" "Something is broken"
apply_label "feature" "1d76db" "New product or engineering capability"
apply_label "codex" "5319e7" "Work intended for Codex-driven execution"
apply_label "frontend" "0e8a16" "Frontend or UI work"
apply_label "backend" "fbca04" "Backend or API work"
apply_label "docs" "0052cc" "Documentation work"
apply_label "blocked" "b60205" "Blocked by external dependency or decision"
apply_label "good first issue" "7057ff" "Good entry point for a new contributor"

echo "GitHub repo label bootstrap completed for ${repo_name}"
