#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO AI Agent Toolkit Uninstaller (LEGACY-CLEANUP FALLBACK)
#
# Skills are now distributed by pinned `npx skills@1.9.0 add`. For an
# npx-managed install this script deletes NOTHING: it guides you to the pinned
# `npx skills@1.9.0 remove` command, which is the only tool that should touch
# npx-owned links, the skills-lock.json manifest, or the npx download cache.
# Shell removal here is restricted to LEGACY artifacts from the old
# git-clone installer.
#
# Deliberate scope decisions:
#   * npx cache (~/.npm/_npx) and skills-lock.json: never touched — npx owns
#     them; "remove" itself decides what to prune.
#   * symlink targets (npx default mode: .claude/skills/<name> ->
#     ../../.agents/skills/<name>): never resolved or deleted. Only a symlink
#     LINK is ever unlinked, and only in legacy mode; targets are never resolved.
#   * bootstrap venv at ${XDG_CACHE_HOME:-$HOME/.cache}/geo-seo-ai-agent:
#     deliberately PRESERVED. It is a shared, checksum-keyed cache outside the
#     skill dirs and may back npx installs too; it is not a skill-dir artifact.
#     Remove it manually only if no GEO install still needs it.
#   * legacy venv ~/.claude/skills/geo/.venv: removed together with the
#     legacy ~/.claude/skills/geo directory in legacy mode.
#   * Windows: explicitly SCOPED OUT. Run the pinned npx commands from Git Bash
#     (native PowerShell/CMD is not supported); this POSIX script performs no
#     Windows-specific cleanup.
# ============================================================

CLAUDE_SKILLS="${HOME}/.claude/skills"
CLAUDE_AGENTS="${HOME}/.claude/agents"
XDG_CONFIG="${XDG_CONFIG_HOME:-${HOME}/.config}"
OPENCODE_AGENTS="${XDG_CONFIG}/opencode/agents"
OPENCODE_COMMANDS="${XDG_CONFIG}/opencode/commands"

# npx-managed install signals, relative to the current working directory.
NPX_AGENTS_SKILLS=".agents/skills"
NPX_LOCK="skills-lock.json"
PINNED_NPX="npx skills@1.9.0"

INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

shopt -s nullglob

# Return 0 when the current install looks npx-managed.
is_npx_managed() {
    [ -f "$NPX_LOCK" ] && return 0
    [ -d "$NPX_AGENTS_SKILLS" ] && return 0
    for link in "${CLAUDE_SKILLS}"/geo*; do
        if [ -L "$link" ]; then
            case "$(readlink "$link")" in
                *".agents/skills"*) return 0 ;;
            esac
        fi
    done
    return 1
}

# Remove one path safely: a symlink LINK is unlinked (never followed), a real
# directory is removed recursively, a real file is unlinked. Targets are never
# resolved, so a symlink into .agents/skills or any arbitrary path is safe.
remove_path() {
    local p="$1"
    if [ -L "$p" ]; then
        rm -f -- "$p"
        echo -e "${GREEN}✓ Unlinked symlink: ${p}${NC}"
    elif [ -d "$p" ]; then
        rm -rf -- "$p"
        echo -e "${GREEN}✓ Removed directory: ${p}${NC}"
    elif [ -e "$p" ]; then
        rm -f -- "$p"
        echo -e "${GREEN}✓ Removed file: ${p}${NC}"
    fi
}

echo ""
echo -e "${YELLOW}GEO-SEO AI Agent Toolkit Uninstaller (legacy-cleanup fallback)${NC}"
echo ""

NPX_MANAGED=false
if is_npx_managed; then
    NPX_MANAGED=true
fi

if [ "$NPX_MANAGED" = true ]; then
    echo -e "${BLUE}Detected an npx-managed install.${NC}"
    echo "Removal is owned by npx; this script deletes nothing."
    echo ""
    echo "Run the pinned command below and select the geo / geo-* skills:"
    echo ""
    echo -e "  ${GREEN}${PINNED_NPX} remove${NC}"
    echo ""
    echo "The npx cache, skills-lock.json manifest and symlink targets are left"
    echo "untouched. Legacy artifacts are not removed in npx mode."
else
    echo "No npx-managed install detected. Legacy artifacts to remove:"
    echo ""
    for skill_dir in "${CLAUDE_SKILLS}/geo" "${CLAUDE_SKILLS}"/geo-*; do
        if [ -e "$skill_dir" ] || [ -L "$skill_dir" ]; then
            echo "  → ${skill_dir}"
        fi
    done
    for agent_file in "${CLAUDE_AGENTS}"/geo-*.md; do
        if [ -e "$agent_file" ] || [ -L "$agent_file" ]; then
            echo "  → ${agent_file}"
        fi
    done
    for agent_file in "${OPENCODE_AGENTS}"/geo-*.md; do
        if [ -e "$agent_file" ] || [ -L "$agent_file" ]; then
            echo "  → ${agent_file}"
        fi
    done
    for cmd_file in "${OPENCODE_COMMANDS}"/geo-*.md; do
        if [ -e "$cmd_file" ] || [ -L "$cmd_file" ]; then
            echo "  → ${cmd_file}"
        fi
    done
fi

echo ""
if [ "$INTERACTIVE" = true ]; then
    read -p "Are you sure you want to continue? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Uninstall cancelled."
        exit 0
    fi
else
    echo -e "${YELLOW}Non-interactive mode — proceeding...${NC}"
fi

echo ""

if [ "$NPX_MANAGED" = true ]; then
    echo -e "${YELLOW}No shell removal performed (npx-managed install).${NC}"
    echo -e "Complete removal with: ${GREEN}${PINNED_NPX} remove${NC}"
else
    # Legacy skills (this also removes the legacy ~/.claude/skills/geo/.venv).
    for skill_dir in "${CLAUDE_SKILLS}/geo" "${CLAUDE_SKILLS}"/geo-*; do
        if [ -e "$skill_dir" ] || [ -L "$skill_dir" ]; then
            remove_path "$skill_dir"
        fi
    done

    # Legacy Claude Code agents.
    for agent_file in "${CLAUDE_AGENTS}"/geo-*.md; do
        if [ -e "$agent_file" ] || [ -L "$agent_file" ]; then
            remove_path "$agent_file"
        fi
    done

    # Legacy OpenCode agents.
    for agent_file in "${OPENCODE_AGENTS}"/geo-*.md; do
        if [ -e "$agent_file" ] || [ -L "$agent_file" ]; then
            remove_path "$agent_file"
        fi
    done

    # Legacy OpenCode command files.
    for cmd_file in "${OPENCODE_COMMANDS}"/geo-*.md; do
        if [ -e "$cmd_file" ] || [ -L "$cmd_file" ]; then
            remove_path "$cmd_file"
        fi
    done
fi

echo ""
if [ "$NPX_MANAGED" = true ]; then
    echo -e "${GREEN}npx-managed install: use ${PINNED_NPX} remove to complete removal.${NC}"
    echo "Legacy artifacts were NOT removed in npx mode."
else
    echo -e "${GREEN}Legacy artifacts removed.${NC}"
fi
echo ""
echo "The bootstrap venv at ${XDG_CACHE_HOME:-${HOME}/.cache}/geo-seo-ai-agent was preserved."
echo "Prospect data at ~/.geo-prospects/ was not removed."
echo ""
