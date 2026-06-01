#!/usr/bin/env bash
set -euo pipefail

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to install Codex CLI"
  exit 1
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "Installing Codex CLI..."
  npm install -g @openai/codex
else
  echo "Codex CLI already installed"
fi
