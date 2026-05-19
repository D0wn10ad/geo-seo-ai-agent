#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO AI Agent Toolkit Installer — Windows (Git Bash)
# Run this script from Git Bash, NOT PowerShell or CMD.
# Delegates file copying to scripts/update_toolkit.py.
# ============================================================

REPO_URL="https://github.com/D0wn10ad/geo-seo-ai-agent.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
INSTALL_DIR="${SKILLS_DIR}/geo"
TEMP_DIR=$(mktemp -d)

INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}+------------------------------------------+${NC}"
    echo -e "${BLUE}|   GEO-SEO AI Agent Toolkit Installer     |${NC}"
    echo -e "${BLUE}|   Windows / Git Bash Edition             |${NC}"
    echo -e "${BLUE}|   Claude Code + OpenCode                 |${NC}"
    echo -e "${BLUE}+------------------------------------------+${NC}"
    echo ""
}
print_success() { echo -e "${GREEN}[OK] $1${NC}"; }
print_warning() { echo -e "${YELLOW}[!!] $1${NC}"; }
print_error()   { echo -e "${RED}[XX] $1${NC}"; }
print_info()    { echo -e "${BLUE}[>>] $1${NC}"; }

cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

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
                echo "  Usage: bash install-win.sh [-b|--branch <branch>]"
                exit 1
                ;;
        esac
    done

    print_header

    # ---- Verify Git Bash environment ----
    if [[ "$(uname -s 2>/dev/null)" != MINGW* ]] && \
       [[ "$(uname -s 2>/dev/null)" != CYGWIN* ]] && \
       [[ "$(uname -s 2>/dev/null)" != MSYS* ]] && \
       [[ -z "${WINDIR:-}" ]]; then
        print_info "Non-Windows detected — use install.sh instead on Linux/macOS."
    fi

    # ---- Check Prerequisites ----
    print_info "Checking prerequisites..."

    if ! command -v git &> /dev/null; then
        print_error "Git is required. Install: https://git-scm.com/downloads"
        exit 1
    fi
    print_success "Git found: $(git --version)"

    PYTHON_CMD=""
    for cmd in python3 python py; do
        if command -v "$cmd" &> /dev/null; then
            _ver=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1 || true)
            if [ -n "$_ver" ]; then
                _major=$(echo "$_ver" | cut -d. -f1)
                _minor=$(echo "$_ver" | cut -d. -f2)
                if [ "$_major" -ge 3 ] && [ "$_minor" -ge 8 ]; then
                    PYTHON_CMD="$cmd"
                    break
                fi
            fi
        fi
    done
    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python 3.8+ not found. Install: https://www.python.org/downloads/"
        exit 1
    fi
    print_success "Python found: $($PYTHON_CMD --version)"

    # ---- Clone or Copy Repository ----
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

    # ---- Deploy files via update_toolkit.py ----
    print_info "Deploying skills, agents, and platform adapter..."
    "$PYTHON_CMD" "$SOURCE_DIR/scripts/update_toolkit.py" \
        --upstream "$REPO_URL" \
        --target "$SOURCE_DIR" \
        --all-platforms \
        --branch "$BRANCH" 2>&1 | sed 's/^/  /'
    print_success "File deployment complete"

    # ---- Install Python Dependencies (--user, no venv on Windows) ----
    print_info "Installing Python dependencies..."
    if [ -f "$SOURCE_DIR/requirements.txt" ]; then
        $PYTHON_CMD -m pip install --user -r "$SOURCE_DIR/requirements.txt" -q 2>/dev/null && {
            print_success "Python dependencies installed"
        } || {
            print_warning "Some deps failed. Run: $PYTHON_CMD -m pip install --user -r requirements.txt"
            cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/"
        }
    fi

    # ---- Optional: Install Playwright ----
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        read -r -p "Install Playwright for screenshots? (y/n): " REPLY
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installing Playwright Chromium..."
            $PYTHON_CMD -m playwright install chromium 2>/dev/null && {
                print_success "Playwright Chromium installed"
            } || {
                print_warning "Playwright install failed."
            }
        fi
    fi

    # ---- Verify ----
    echo ""
    print_info "Verifying installation..."
    [ -f "$INSTALL_DIR/SKILL.md" ] && print_success "Main skill" || print_error "Main skill missing"
    [ -d "$SKILLS_DIR/geo-audit" ] && print_success "Sub-skills" || print_error "Sub-skills missing"
    [ -d "$INSTALL_DIR/scripts" ]  && print_success "Scripts"    || print_error "Scripts missing"

    # ---- Summary ----
    echo ""
    echo -e "${GREEN}+------------------------------------------+${NC}"
    echo -e "${GREEN}|        Installation Complete!            |${NC}"
    echo -e "${GREEN}+------------------------------------------+${NC}"
    echo ""
    echo "  Skills:   ${INSTALL_DIR}"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    echo "  Claude Code:  /geo audit https://example.com"
    echo "  OpenCode:     /geo-audit https://example.com"
    echo ""
    echo "  See docs/ for full command reference."
    echo ""
}

main "$@"
