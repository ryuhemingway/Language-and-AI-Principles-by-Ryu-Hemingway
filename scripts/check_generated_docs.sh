#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

TARGETS=(docs/course-content docs/assets)
BEFORE="$(mktemp)"
AFTER="$(mktemp)"
trap 'rm -f "${BEFORE}" "${AFTER}"' EXIT

git diff -- "${TARGETS[@]}" > "${BEFORE}"
python3 scripts/export_course_content.py
python3 scripts/generate_docs_media.py
git diff -- "${TARGETS[@]}" > "${AFTER}"

if ! cmp -s "${BEFORE}" "${AFTER}"; then
  echo "Generated docs changed after regeneration." >&2
  echo "Run python3 scripts/export_course_content.py and python3 scripts/generate_docs_media.py, then commit the result." >&2
  git diff -- "${TARGETS[@]}"
  exit 1
fi
