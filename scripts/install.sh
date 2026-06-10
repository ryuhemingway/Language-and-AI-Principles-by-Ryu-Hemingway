#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "${BIN_DIR}"
chmod +x "${ROOT}/brief.py"
ln -sf "${ROOT}/brief.py" "${BIN_DIR}/Learn"
ln -sf "${ROOT}/brief.py" "${BIN_DIR}/learn"
ln -sf "${ROOT}/brief.py" "${BIN_DIR}/brief"

if [[ ! -f "${ROOT}/config.json" ]]; then
  cp "${ROOT}/config.example.json" "${ROOT}/config.json"
fi

echo "Installed:"
echo "  ${BIN_DIR}/Learn"
echo "  ${BIN_DIR}/learn"
echo "  ${BIN_DIR}/brief"
echo
echo "Make sure ${BIN_DIR} is on your PATH, then run: Learn"

