#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO AI Agent Toolkit Uninstaller
# Removes from both Claude Code and OpenCode paths.
# ============================================================

CLAUDE_SKILLS="${HOME}/.claude/skills"
CLAUDE_AGENTS="${HOME}/.claude/agents"
XDG_CONFIG="${XDG_CONFIG_HOME:-${HOME}/.config}"
OPENCODE_AGENTS="${XDG_CONFIG}/opencode/agents"
OPENCODE_COMMANDS="${XDG_CONFIG}/opencode/commands"

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

echo ""
echo -e "${YELLOW}GEO-SEO AI Agent Toolkit Uninstaller${NC}"
echo ""
echo "This will remove the following:"
echo ""

# List what will be removed
[ -d "${CLAUDE_SKILLS}/geo" ] && echo "  → ${CLAUDE_SKILLS}/geo/"
for skill_dir in "${CLAUDE_SKILLS}"/geo-*/; do
    [ -d "$skill_dir" ] && echo "  → ${skill_dir}"
done
for agent_file in "${CLAUDE_AGENTS}"/geo-*.md; do
    [ -f "$agent_file" ] && echo "  → ${agent_file}"
done
for agent_file in "${OPENCODE_AGENTS}"/geo-*.md; do
    [ -f "$agent_file" ] && echo "  → ${agent_file}"
done
for cmd_file in "${OPENCODE_COMMANDS}"/geo-*.md; do
    [ -f "$cmd_file" ] && echo "  → ${cmd_file}"
done

echo ""
if [ "$INTERACTIVE" = true ]; then
    read -p "Are you sure you want to uninstall? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Uninstall cancelled."
        exit 0
    fi
else
    echo -e "${YELLOW}Non-interactive mode — proceeding...${NC}"
fi

echo ""

# Remove shared skills (Claude Code path — also used by OpenCode)
for skill_dir in "${CLAUDE_SKILLS}/geo" "${CLAUDE_SKILLS}"/geo-*/; do
    if [ -d "$skill_dir" ]; then
        name=$(basename "$skill_dir")
        rm -rf "$skill_dir"
        echo -e "${GREEN}✓ Removed skill: ${name}${NC}"
    fi
done

# Remove Claude Code agents
for agent_file in "${CLAUDE_AGENTS}"/geo-*.md; do
    if [ -f "$agent_file" ]; then
        rm -f "$agent_file"
        echo -e "${GREEN}✓ Removed Claude agent: $(basename "$agent_file")${NC}"
    fi
done

# Remove OpenCode agents
for agent_file in "${OPENCODE_AGENTS}"/geo-*.md; do
    if [ -f "$agent_file" ]; then
        rm -f "$agent_file"
        echo -e "${GREEN}✓ Removed OpenCode agent: $(basename "$agent_file")${NC}"
    fi
done

# Remove OpenCode commands
for cmd_file in "${OPENCODE_COMMANDS}"/geo-*.md; do
    if [ -f "$cmd_file" ]; then
        rm -f "$cmd_file"
        echo -e "${GREEN}✓ Removed OpenCode command: $(basename "$cmd_file")${NC}"
    fi
done

echo ""
echo -e "${GREEN}GEO-SEO has been uninstalled from all platforms.${NC}"
echo ""
echo "Note: Python dependencies were in an isolated venv inside the skill"
echo "directory and have been removed."
echo ""
echo "Prospect data at ~/.geo-prospects/ was not removed."
echo "To remove manually: rm -rf ~/.geo-prospects"
echo ""
