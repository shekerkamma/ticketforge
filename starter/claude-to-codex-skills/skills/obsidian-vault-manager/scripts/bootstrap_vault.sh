#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${1:-vault}"
VAULT_PATH="${VAULT_PATH/#\~/$HOME}"

mkdir -p "$VAULT_PATH/.obsidian/plugins"

for dir in _index _templates attachments archive daily evergreen projects research sources; do
  mkdir -p "$VAULT_PATH/$dir"
done

touch "$VAULT_PATH/.obsidian/app.json"
touch "$VAULT_PATH/.obsidian/appearance.json"
touch "$VAULT_PATH/.obsidian/community-plugins.json"

GITIGNORE="$VAULT_PATH/.gitignore"
touch "$GITIGNORE"
for line in   ".obsidian/cache/"   ".obsidian/workspace.json"   ".obsidian/workspaces.json"   ".obsidian/plugins/*/data.json"   ".trash/"   ".DS_Store"
do
  grep -qxF "$line" "$GITIGNORE" || echo "$line" >> "$GITIGNORE"
done

if [ ! -f "$VAULT_PATH/README.md" ]; then
  cat > "$VAULT_PATH/README.md" <<'EOF'
# Obsidian Vault

This vault is structured for Git-friendly, markdown-first knowledge work.

## Entry points

- `_index/Second Brain MOC.md`
- `projects/`
- `research/`
- `sources/`
EOF
fi

if [ ! -f "$VAULT_PATH/_index/Second Brain MOC.md" ]; then
  cat > "$VAULT_PATH/_index/Second Brain MOC.md" <<'EOF'
# Second Brain MOC

## Recent source notes

## Evergreen notes

## Active projects

## Research themes
EOF
fi

if [ ! -f "$VAULT_PATH/_templates/source-note.md" ]; then
  cat > "$VAULT_PATH/_templates/source-note.md" <<'EOF'
---
title:
created:
updated:
tags: []
source:
source_type:
---

# {{title}}

## TL;DR

## Key claims

## Evidence

## Why it matters

## Related notes
EOF
fi

if [ ! -f "$VAULT_PATH/_templates/evergreen-note.md" ]; then
  cat > "$VAULT_PATH/_templates/evergreen-note.md" <<'EOF'
---
title:
created:
updated:
tags: []
---

# {{title}}

## Claim

## Why it matters

## Supporting evidence

## Related notes
EOF
fi

if [ ! -f "$VAULT_PATH/_templates/meeting-note.md" ]; then
  cat > "$VAULT_PATH/_templates/meeting-note.md" <<'EOF'
---
title:
created:
updated:
tags: [meeting]
---

# {{title}}

## Context

## Decisions

## Action items

## Risks
EOF
fi

echo "bootstrapped vault at $VAULT_PATH"
