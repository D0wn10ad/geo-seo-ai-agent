#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO AI Agent Toolkit Installer
# Installs the GEO-first SEO analysis tool for both
# Claude Code and OpenCode with an isolated Python venv.
# Delegates file copying to scripts/update_toolkit.py.
# ============================================================

REPO_URL="https://github.com/D0wn10ad/geo-seo-ai-agent.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
INSTALL_DIR="${SKILLS_DIR}/geo"
VENV_DIR="${INSTALL_DIR}/.venv"
VENV_PY="${VENV_DIR}/bin/python3"
TEMP_DIR=$(mktemp -d)

# Detect if running via curl pipe (no interactive input available)
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

    PYTHON_CMD=""
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PY_VERSION=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if [ -n "$PY_VERSION" ]; then
            MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
            MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
            if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
                PYTHON_CMD="python"
            fi
        fi
    fi
    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python 3.8+ is required but not found."
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

    # ---- Deploy files via update_toolkit.py ----
    print_info "Deploying skills, agents, and platform adapter..."
    "$PYTHON_CMD" "$SOURCE_DIR/scripts/update_toolkit.py" \
        --upstream "$REPO_URL" \
        --target "$SOURCE_DIR" \
        --all-platforms \
        --branch "$BRANCH" 2>&1 | sed 's/^/  /'
    print_success "File deployment complete"

    # ---- Create Virtual Environment ----
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
            # Bootstrap pip into the venv (ensurepip is available at python3 system level)
            if "$VENV_PY" -m ensurepip --upgrade 2>/dev/null || \
               "$PYTHON_CMD" -m ensurepip --upgrade --root "$VENV_DIR" 2>/dev/null; then
                VENV_OK=true
            else
                # Last resort: download get-pip.py
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

    if [ "$VENV_OK" = false ]; then
        print_warning "Could not create virtual environment."
        print_warning "Installing dependencies system-wide with --user flag."
        print_warning "  Fix: sudo apt install python3-venv && $0"
        USER_INSTALL=true
    else
        print_success "Virtual environment created"
        USER_INSTALL=false
    fi

    # ---- Install Python Dependencies ----
    if [ -f "$SOURCE_DIR/requirements.txt" ]; then
        if [ "$USER_INSTALL" = true ]; then
            print_info "Installing Python dependencies (system --user)..."
            $PYTHON_CMD -m pip install --user -r "$SOURCE_DIR/requirements.txt" --quiet || {
                print_warning "Dependency install had issues — continuing anyway."
            }
            print_success "Dependencies installed (system --user)"
        elif [ "$USE_UV" = true ]; then
            print_info "Installing Python dependencies into venv via uv..."
            uv pip install --python "$VENV_PY" -r "$SOURCE_DIR/requirements.txt" --quiet || {
                print_warning "uv pip install failed — falling back to pip."
                "$VENV_PY" -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet || {
                    print_warning "Dependency install had issues — continuing anyway."
                }
            }
            print_success "Dependencies installed (isolated venv)"
        else
            print_info "Installing Python dependencies into venv..."
            "$VENV_PY" -m pip install --upgrade pip --quiet 2>/dev/null || true
            "$VENV_PY" -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet || {
                print_warning "Dependency install had issues — continuing anyway."
            }
            print_success "Dependencies installed (isolated venv)"
        fi
    else
        print_warning "requirements.txt missing — skipping dependency install."
    fi
    cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/" 2>/dev/null || true

    # ---- Rewrite script shebangs ----
    if [ "$USER_INSTALL" = false ]; then
        print_info "Pinning script shebangs to venv interpreter..."
        SHEBANG_COUNT=0
        for f in "$INSTALL_DIR/scripts/"*.py; do
            [ -f "$f" ] || continue
            sed_inplace "1s|^#!.*|#!${VENV_PY}|" "$f"
            chmod +x "$f"
            SHEBANG_COUNT=$((SHEBANG_COUNT + 1))
        done
        print_success "${SHEBANG_COUNT} script(s) pinned to venv"
    else
        print_info "Skipping shebang pinning (no venv — scripts use system python3)"
    fi

    # ---- Optional: Install Playwright ----
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        read -p "Install Playwright browsers for screenshots? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installing Playwright Chromium into venv..."
            if "$VENV_PY" -m playwright install chromium 2>/dev/null; then
                print_success "Playwright Chromium installed"
            else
                print_warning "Playwright install failed"
            fi
        fi
    fi

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
}

main "$@"
