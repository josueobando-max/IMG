#!/usr/bin/env bash
# Bake the public GitHub Pages URL into the manifest, then push to GitHub.
# Usage: bash deploy.sh <github-username> [repo-name]
set -euo pipefail

USER="${1:-}"
REPO="${2:-stock-seo}"

if [ -z "$USER" ]; then
  echo "usage: bash deploy.sh <github-username> [repo-name]" >&2
  echo "  the repo must already exist and be empty: https://github.com/new" >&2
  exit 1
fi

cd "$(dirname "$0")"
BASE="https://${USER}.github.io/${REPO}"

echo "==> baking base URL: $BASE"
python tools/set-base-url.py "$BASE"

echo "==> committing"
git add -A
git commit -q -m "Set public base URL to ${BASE}" || echo "    (nothing to commit)"

echo "==> pushing to github.com/${USER}/${REPO}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${USER}/${REPO}.git"
git push -u origin main

cat <<EOF

==> pushed.

Last step, in the browser:
  https://github.com/${USER}/${REPO}/settings/pages
  Source: "Deploy from a branch"  ->  Branch: main / (root)  ->  Save

In 1-2 minutes your gallery is live at:
  ${BASE}/

Send the AI this:
  ${BASE}/            (gallery)
  ${BASE}/manifest.json   (machine-readable index of all 389 images)
EOF
