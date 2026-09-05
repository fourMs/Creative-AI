#!/usr/bin/env bash
# Full HTML build with notebook execution — matches .github/workflows/deploy.yml.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v myst >/dev/null 2>&1; then
  echo "myst not found. Install: pip install -r requirements.txt" >&2
  exit 1
fi

echo "Checking chapter template, citations, and figures..."
python scripts/check-chapters.py

cd book
echo "Running: myst build --html --execute (same as CI deploy)..."
myst build --html --execute
# Mirror the deploy workflow: copy bundled web apps to a stable top-level path.
cp -r apps _build/html/apps
echo "OK: book built with all notebooks executed."
