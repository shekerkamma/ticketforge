#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${1:-.}"
REMOTE_URL="${2:-}"
VAULT_PATH="${VAULT_PATH/#\~/$HOME}"

mkdir -p "$VAULT_PATH"
cd "$VAULT_PATH"

if [ ! -d .git ]; then
  git init -b main >/dev/null 2>&1 || git init >/dev/null 2>&1
fi

current_branch=$(git branch --show-current 2>/dev/null || true)
if [ "$current_branch" = "master" ]; then
  git branch -M main >/dev/null 2>&1 || true
elif [ -z "$current_branch" ]; then
  git checkout -b main >/dev/null 2>&1 || git switch -c main >/dev/null 2>&1 || true
fi

GITIGNORE=".gitignore"
touch "$GITIGNORE"
for line in   ".obsidian/cache/"   ".obsidian/workspace.json"   ".obsidian/workspaces.json"   ".obsidian/plugins/*/data.json"   ".trash/"   ".DS_Store"
do
  grep -qxF "$line" "$GITIGNORE" || echo "$line" >> "$GITIGNORE"
done

if [ -n "$REMOTE_URL" ]; then
  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REMOTE_URL"
  else
    git remote add origin "$REMOTE_URL"
  fi
fi

echo "repo ready at $VAULT_PATH"
git status --short
if git remote get-url origin >/dev/null 2>&1; then
  echo "origin=$(git remote get-url origin)"
else
  echo "origin=unset"
fi
