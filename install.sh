#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO AI Agent Toolkit — LEGACY installer (RETIRED)
# This script intentionally deploys nothing. Skills are distributed
# only by the pinned npx command below. It performs no repository
# download, no dependency installation, and no environment setup.
# Kept solely as an honest signpost for older setups.
# ============================================================

cat <<'EOF'

  GEO-SEO AI Agent Toolkit — LEGACY installer (RETIRED)

  This legacy script no longer deploys skills. It does not download,
  clone, or install anything. Install with the pinned command:

    npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git

  Cleaning up an older LEGACY install:

    bash uninstall.sh

  uninstall.sh removes legacy-only artifacts and preserves
  ~/.geo-prospects/ — your prospects, proposals and reports are
  never deleted.

EOF
