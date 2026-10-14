#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [[ -n "${CHECK_PYTHON:-}" ]]; then
    PYTHON="$CHECK_PYTHON"
elif [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
    PYTHON="$REPO_ROOT/.venv/bin/python"
else
    PYTHON=python3
fi

for tool in black pytest; do
    if ! "$PYTHON" -m "$tool" --version >/dev/null 2>&1; then
        echo "Missing $tool for $PYTHON" >&2
        echo "Install: $PYTHON -m pip install black==25.1.0 pytest==8.3.4" >&2
        exit 2
    fi
done

echo "Checking Black formatting..."
"$PYTHON" -m black --check \
    src/handler/add_project_handler.py \
    src/github/repository_url.py \
    tests/test_repository_url.py

echo "Running unit tests..."
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" -m pytest -q -p no:cacheprovider tests
