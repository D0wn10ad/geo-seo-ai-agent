#!/usr/bin/env bash
set -euo pipefail

UV_VERSION="0.13.9"

uv_is_present() {
    command -v uv >/dev/null 2>&1
}

report_already_present() {
    existing_version="$(uv --version 2>/dev/null || true)"
    if [ -n "$existing_version" ]; then
        printf 'uv already present (%s); no-op - not reinstalling or downgrading.\n' "$existing_version"
    else
        printf 'uv already present on PATH; no-op - not reinstalling or downgrading.\n'
    fi
}

install_pinned_uv() {
    printf 'uv absent; installing pinned version %s.\n' "$UV_VERSION"
    env UV_VERSION="$UV_VERSION" curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | sh
}

main() {
    if uv_is_present; then
        report_already_present
        return 0
    fi
    install_pinned_uv
}

main "$@"
