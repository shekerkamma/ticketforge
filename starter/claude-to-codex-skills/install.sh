#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SOURCE_DIR="$SCRIPT_DIR/skills"
REAL_HOME=$(getent passwd "$(id -u)" | cut -d: -f6 2>/dev/null || true)

if [ -z "$REAL_HOME" ]; then
  REAL_HOME="$HOME"
fi

TARGET_DIR="${CODEX_HOME:-$REAL_HOME/.codex}/skills"

mkdir -p "$TARGET_DIR"

if [ $# -eq 0 ]; then
  set -- "$SOURCE_DIR"/*
  names=()
  for path in "$@"; do
    names+=("$(basename "$path")")
  done
else
  names=("$@")
fi

for name in "${names[@]}"; do
  src="$SOURCE_DIR/$name"
  dst="$TARGET_DIR/$name"

  if [ ! -d "$src" ]; then
    echo "Missing staged skill: $name" >&2
    exit 1
  fi

  rm -rf "$dst"
  cp -R "$src" "$dst"
  echo "installed $name -> $dst"
done
