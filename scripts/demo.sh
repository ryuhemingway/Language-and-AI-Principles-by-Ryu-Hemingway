#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

cp "${ROOT}/config.example.json" "${TMP_DIR}/config.json"

NO_COLOR=1 \
LEARN_CONFIG_PATH="${TMP_DIR}/config.json" \
LEARN_PROGRESS_DIR="${TMP_DIR}/progress" \
python3 "${ROOT}/learn.py" learn <<'EOF'
1
1
1
1


store a value

name = "Ryu"
age = 21
print(name, age)
:done
b
q
EOF
