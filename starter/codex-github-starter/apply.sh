#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./starter/codex-github-starter/apply.sh /path/to/repo owner/repo [--force]

Arguments:
  /path/to/repo   Target git repository
  owner/repo      GitHub repo slug used in template URLs
  --force         Overwrite existing files
EOF
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 1
fi

TARGET_DIR="$1"
REPO_SLUG="$2"
FORCE=0

if [[ "${3:-}" == "--force" ]]; then
  FORCE=1
elif [[ $# -eq 3 ]]; then
  usage
  exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory does not exist: $TARGET_DIR"
  exit 1
fi

if [[ ! -d "$TARGET_DIR/.git" ]]; then
  echo "Target directory is not a git repository: $TARGET_DIR"
  exit 1
fi

STARTER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="${STARTER_DIR}/template"
REPO_NAME="$(basename "$TARGET_DIR")"

escape_replacement() {
  printf '%s' "$1" | sed -e 's/[&|]/\\&/g'
}

escaped_slug="$(escape_replacement "$REPO_SLUG")"
escaped_name="$(escape_replacement "$REPO_NAME")"

copy_template() {
  local src="$1"
  local rel="${src#$TEMPLATE_DIR/}"
  local dst="${TARGET_DIR}/${rel}"

  mkdir -p "$(dirname "$dst")"

  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then
    echo "skip  $rel"
    return
  fi

  sed \
    -e "s|__REPO_SLUG__|${escaped_slug}|g" \
    -e "s|__REPO_NAME__|${escaped_name}|g" \
    "$src" >"$dst"

  if [[ -x "$src" ]]; then
    chmod +x "$dst"
  fi

  echo "write $rel"
}

while IFS= read -r src; do
  copy_template "$src"
done < <(find "$TEMPLATE_DIR" -type f | sort)

echo
echo "Starter applied to ${TARGET_DIR}"
echo "Next:"
echo "  cd ${TARGET_DIR}"
echo "  ./scripts/check_github_foundation.sh"
echo "  ./scripts/bootstrap_github_repo.sh"
