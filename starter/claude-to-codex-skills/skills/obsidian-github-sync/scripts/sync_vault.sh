#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${1:-.}"
MESSAGE="${2:-vault snapshot}"
VAULT_PATH="${VAULT_PATH/#\~/$HOME}"

cd "$VAULT_PATH"

git add -A
if git diff --cached --quiet; then
  echo "nothing to commit"
  exit 0
fi

git commit -m "$MESSAGE"

if git remote get-url origin >/dev/null 2>&1; then
  branch=$(git branch --show-current)
  git push -u origin "$branch"
else
  echo "committed locally; origin is not configured"
fi
