#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import urllib.request

checks = [
    ("backend-health", "http://127.0.0.1:8000/api/health"),
    ("frontend-root", "http://127.0.0.1:3000"),
]

for name, url in checks:
    response = urllib.request.urlopen(url)
    print(f"{name}: {response.status} {url}")
PY
