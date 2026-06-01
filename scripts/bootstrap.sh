#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR/backend"

if ! python3 -m pip --version >/dev/null 2>&1; then
  echo "Bootstrapping pip..."
  python3 - <<'PY'
import urllib.request
urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "/tmp/get-pip.py")
PY
  python3 /tmp/get-pip.py --break-system-packages
fi

echo "Installing backend dependencies..."
python3 -m pip install -e .[dev] --break-system-packages

cd "$ROOT_DIR/frontend"
echo "Installing frontend dependencies..."
npm install

echo "Bootstrap complete."
