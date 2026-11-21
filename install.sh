#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO AI Agent Toolkit Installer (LEGACY)
# Skills are distributed only by pinned `npx skills@1.9.0 add`.
# This script no longer deploys skills; Todo 16 will fully rewrite it
# as an npx-first quick start. Kept here only as a legacy skeleton.
# ============================================================

REPO_URL="https://github.com/D0wn10ad/geo-seo-ai-agent.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
INSTALL_DIR="${SKILLS_DIR}/geo"
VENV_DIR="${INSTALL_DIR}/.venv"
# Windows venvs (Git Bash / MSYS / Cygwin) put the interpreter at
# Scripts/python.exe instead of bin/python3.
case "${OSTYPE:-}" in
    msys*|cygwin*|win32*) VENV_PY_REL="Scripts/python.exe" ;;
    *)                    VENV_PY_REL="bin/python3" ;;
esac
VENV_PY="${VENV_DIR}/${VENV_PY_REL}"
TEMP_DIR=$(mktemp -d)

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   GEO-SEO AI Agent Toolkit Installer        ║${NC}"
    echo -e "${BLUE}║   Claude Code + OpenCode                    ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error()   { echo -e "${RED}✗ $1${NC}"; }
print_info()    { echo -e "${BLUE}→ $1${NC}"; }

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Cross-platform in-place sed
sed_inplace() {
    local pattern="$1"
    local file="$2"
    sed -i.bak "$pattern" "$file" && rm -f "${file}.bak"
}

main() {
    # ---- Parse arguments ----
    BRANCH="main"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -b|--branch)
                BRANCH="$2"
                shift 2
                ;;
            *)
                print_error "Unknown option: $1"
                echo "  Usage: bash install.sh [-b|--branch <branch>]"
                exit 1
                ;;
        esac
    done

    print_header

    # ---- Check Prerequisites ----
    print_info "Checking prerequisites..."

    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed."
        echo "  Install: https://git-scm.com/downloads"
        exit 1
    fi
    print_success "Git found: $(git --version)"

    # Require Python >= 3.10 (requirements.txt pins lxml that drop 3.9).
    # Don't trust the first `python3` on PATH: macOS ships system python3 3.9.x,
    # and Homebrew often exposes a newer Python only as pythonX.Y with no
    # `python3` symlink, so probe versioned names too and pick the first that
    # meets the minimum.
    PYTHON_CMD=""
    for cmd in python3 python3.15 python3.14 python3.13 python3.12 python3.11 python3.10 python; do
        command -v "$cmd" &> /dev/null || continue
        # A candidate can exist on PATH and still fail to run: a pyenv shim for
        # a version that is installed but not active, or the Windows Store alias
        # for python3. Under `set -euo pipefail` an unguarded failure here would
        # end the installer with no message, so discard the candidate's stderr
        # and fall through to the next name instead.
        PY_VERSION=$("$cmd" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1 || true)
        [ -n "$PY_VERSION" ] || continue
        MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
        MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
        if [ "$MAJOR" -gt 3 ] || { [ "$MAJOR" -eq 3 ] && [ $MINOR -ge 10 ]; }; then
            PYTHON_CMD="$cmd"
            break
        fi
    done

    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python 3.10+ is required but not found."
        echo "  Install: https://www.python.org/downloads/"
        exit 1
    fi
    print_success "Python found: $($PYTHON_CMD --version)"

    # Detect uv for faster venv/install
    USE_UV=false
    if command -v uv &> /dev/null; then
        USE_UV=true
        print_success "'uv' detected"
    fi

    # ---- Early venv feasibility check ----
    if [ "$USE_UV" = false ]; then
        if ! $PYTHON_CMD -m venv "$TEMP_DIR/.test-venv" 2>/dev/null; then
            print_error "Python venv module not available."
            echo ""
            echo "  Debian/Ubuntu:  sudo apt install python3-venv"
            echo "  Fedora/RHEL:    sudo dnf install python3-virtualenv"
            echo "  Or install 'uv' (no system packages needed):"
            echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
            exit 1
        fi
        rm -rf "$TEMP_DIR/.test-venv"
    fi

    # ---- Resolve source directory ----
    print_info "Fetching source files..."

    SCRIPT_DIR=""
    if [ -n "${BASH_SOURCE[0]:-}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || true
    fi

    if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/geo/SKILL.md" ]; then
        print_info "Installing from local directory..."
        SOURCE_DIR="$SCRIPT_DIR"
    else
        print_info "Cloning from repository (branch: ${BRANCH})..."
        git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TEMP_DIR/repo" || {
            print_error "Failed to clone repository."
            exit 1
        }
        SOURCE_DIR="${TEMP_DIR}/repo"
    fi

    # ---- Create Virtual Environment (before deployment) ----
    print_info "Creating isolated Python environment → ${VENV_DIR}"
    rm -rf "$VENV_DIR"

    VENV_OK=false
    if [ "$USE_UV" = true ]; then
        if uv venv "$VENV_DIR" --python "$PYTHON_CMD" --quiet 2>/dev/null; then
            VENV_OK=true
        else
            print_warning "uv venv failed — falling back to stdlib venv."
        fi
    fi

    if [ "$VENV_OK" = false ]; then
        if $PYTHON_CMD -m venv "$VENV_DIR" 2>/dev/null; then
            VENV_OK=true
        elif $PYTHON_CMD -m venv --without-pip "$VENV_DIR" 2>/dev/null; then
            print_info "Venv created without pip — bootstrapping..."
            if "$VENV_PY" -m ensurepip --upgrade 2>/dev/null || \
               "$PYTHON_CMD" -m ensurepip --upgrade --root "$VENV_DIR" 2>/dev/null; then
                VENV_OK=true
            else
                print_info "Downloading get-pip.py to bootstrap pip..."
                if command -v curl &>/dev/null; then
                    curl -fsSLo "$TEMP_DIR/get-pip.py" https://bootstrap.pypa.io/get-pip.py
                elif command -v wget &>/dev/null; then
                    wget -qO "$TEMP_DIR/get-pip.py" https://bootstrap.pypa.io/get-pip.py
                fi
                if [ -f "$TEMP_DIR/get-pip.py" ]; then
                    "$VENV_PY" "$TEMP_DIR/get-pip.py" --quiet 2>/dev/null && VENV_OK=true
                fi
            fi
        fi
    fi

    if [ "$VENV_OK" = true ]; then
        # Verify the actual python binary exists in the venv.
        # Some systems create bin/python instead of bin/python3.
        if [ ! -x "$VENV_PY" ]; then
            VENV_DIR_BIN="$(dirname "$VENV_PY")"
            if [ -x "${VENV_DIR_BIN}/python" ]; then
                VENV_PY="${VENV_DIR_BIN}/python"
                # Also update the tilde-form path used for markdown rewriting
                VENV_MD_PY='~/.claude/skills/geo/.venv/bin/python'
            else
                print_warning "Virtual environment created but python binary not found."
                VENV_OK=false
            fi
        fi
    fi

    if [ "$VENV_OK" = false ]; then
        print_warning "Could not create virtual environment."
        print_warning "Installing dependencies system-wide with --user flag."
        print_warning "  Fix: sudo apt install python3-venv && $0"
        USER_INSTALL=true
    else
        print_success "Virtual environment created"
        USER_INSTALL=false
    fi

    # ---- Legacy distribution disabled ----
    print_warning "This legacy installer no longer deploys skills."
    print_warning "Install with: npx skills@1.9.0 add -a claude-code -a opencode -y ${REPO_URL}"
    print_warning "Todo 16 will replace this script with the npx-first quick start."

    # ---- Install Python Dependencies ----
    DEPS_OK=true
    if [ -f "$SOURCE_DIR/requirements.txt" ]; then
        if [ "$USER_INSTALL" = true ]; then
            print_info "Python dependency mode: system --user"
            if ! $PYTHON_CMD -m pip install --user -r "$SOURCE_DIR/requirements.txt"; then
                print_error "Python dependency installation failed."
                print_error "See pip output above for the exact error."
                exit 1
            fi
        elif [ "$USE_UV" = true ]; then
            print_info "Python dependency mode: isolated venv via uv"
            if ! uv pip install --python "$VENV_PY" -r "$SOURCE_DIR/requirements.txt"; then
                print_warning "uv pip install failed — falling back to pip."
                if ! "$VENV_PY" -m pip install -r "$SOURCE_DIR/requirements.txt"; then
                    print_error "Python dependency installation failed."
                    print_error "See pip output above for the exact error."
                    exit 1
                fi
            fi
        else
            print_info "Python dependency mode: isolated venv via pip"
            "$VENV_PY" -m pip install --upgrade pip || true
            if ! "$VENV_PY" -m pip install -r "$SOURCE_DIR/requirements.txt"; then
                print_error "Python dependency installation failed."
                print_error "See pip output above for the exact error."
                exit 1
            fi
        fi
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt missing — skipping dependency install."
    fi
    cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/" 2>/dev/null || true

    # ---- Verify ----
    echo ""
    print_info "Verifying installation..."
    agent_count=0
    for f in "${HOME}/.claude/agents/"geo-*.md; do
        [ -f "$f" ] && agent_count=$((agent_count + 1))
    done

    test -f "$INSTALL_DIR/SKILL.md"        && print_success "Main skill"     || print_error "Main skill missing"
    test -d "$SKILLS_DIR/geo-audit"        && print_success "Sub-skills"     || print_error "Sub-skills missing"
    [ "$agent_count" -gt 0 ]               && print_success "Claude agents"  || print_warning "No Claude agents"
    test -d "$INSTALL_DIR/scripts"         && print_success "Scripts"        || print_error "Scripts missing"
    test -x "$VENV_PY"                     && print_success "Venv"           || print_error "Venv missing"
    test -d "$INSTALL_DIR/regions"         && print_success "Region profiles"|| print_info "No region profiles (feature branch only)"

    # ---- Summary ----
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║        Installation Complete!             ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
    echo ""
    echo "  Skills:   ${INSTALL_DIR}"
    echo "  Venv:     ${VENV_DIR}"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    echo "  Claude Code:  /geo audit https://example.com"
    echo "  OpenCode:     /geo-audit https://example.com"
    echo ""
    echo -e "${BLUE}Region-Specific Audit:${NC}"
    echo "  Claude Code:  /geo audit https://example.com --region cn"
    echo "  OpenCode:     /geo-audit https://example.com --region cn"
    echo ""
    echo -e "${BLUE}Available Commands:${NC}"
    echo "    /geo audit <url>      Full GEO + SEO audit"
    echo "    /geo quick <url>      60-second visibility snapshot"
    echo "    /geo citability <url> AI citation readiness score"
    echo "    /geo crawlers <url>   AI crawler access check"
    echo "    /geo llmstxt <url>    Analyze/generate llms.txt"
    echo "    /geo brands <url>     Brand mention scan"
    echo "    /geo platforms <url>  Platform-specific optimization"
    echo "    /geo schema <url>     Structured data analysis"
    echo "    /geo technical <url>  Technical SEO audit"
    echo "    /geo content <url>    Content quality & E-E-A-T"
    echo "    /geo report <url>     Client-ready GEO report"
    echo "    /geo report-pdf       Generate PDF report from audit data"
    echo ""
    echo -e "${BLUE}Tip:${NC} Add '--region <code>' to any audit command for"
    echo "  region-specific analysis (e.g., --region cn for China market)."
    echo ""
}

main "$@"
