#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ_FILE="${1:-${SCRIPT_DIR}/../../requirements.txt}"

if [ ! -f "$REQ_FILE" ]; then
    printf 'error: requirements.txt not found: %s\n' "$REQ_FILE" >&2
    exit 1
fi

GEO_CACHE_DIR="${GEO_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/geo-seo-ai-agent}"
VENV_DIR="${GEO_CACHE_DIR}/venv"
SENTINEL="${GEO_CACHE_DIR}/.env-bootstrap-sentinel"

if command -v sha256sum >/dev/null 2>&1; then
    REQ_SHA="$(sha256sum "$REQ_FILE" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
    REQ_SHA="$(shasum -a 256 "$REQ_FILE" | awk '{print $1}')"
else
    printf 'error: sha256sum or shasum is required to checksum requirements.txt\n' >&2
    exit 1
fi

VENV_PY="${VENV_DIR}/bin/python3"
if [ ! -x "$VENV_PY" ] && [ -x "${VENV_DIR}/bin/python" ]; then
    VENV_PY="${VENV_DIR}/bin/python"
fi

if [ -f "$SENTINEL" ] && [ "$(cat "$SENTINEL")" = "$REQ_SHA" ] && [ -x "$VENV_PY" ]; then
    printf 'deps already bootstrapped for requirements sha %s; no-op\n' "$REQ_SHA"
    printf '%s\n' "$VENV_PY"
    exit 0
fi

if ! command -v uv >/dev/null 2>&1; then
    printf 'error: uv not found on PATH; run geo/scripts/install_uv.sh first\n' >&2
    exit 1
fi

mkdir -p "$GEO_CACHE_DIR"

if [ -n "${PYTHON_CMD:-${GEO_PYTHON:-}}" ]; then
    uv venv "$VENV_DIR" --python "${PYTHON_CMD:-${GEO_PYTHON:-}}"
else
    uv venv "$VENV_DIR"
fi

VENV_PY="${VENV_DIR}/bin/python3"
if [ ! -x "$VENV_PY" ] && [ -x "${VENV_DIR}/bin/python" ]; then
    VENV_PY="${VENV_DIR}/bin/python"
fi

uv pip install --python "$VENV_PY" -r "$REQ_FILE"

TMP_SENTINEL="${SENTINEL}.tmp.$$"
printf '%s\n' "$REQ_SHA" > "$TMP_SENTINEL"
mv "$TMP_SENTINEL" "$SENTINEL"

printf 'deps bootstrapped into venv for requirements sha %s\n' "$REQ_SHA"
printf '%s\n' "$VENV_PY"
