---
name: geo-update
description: Pull the latest GEO-SEO skill updates from the upstream repository using update_toolkit.py. Supports both Claude Code and OpenCode platforms.
---

# GEO-SEO Update Skill

## Purpose

Updates the locally installed GEO-SEO skills, agents, scripts, and documentation to the latest version from the upstream repository. Delegates to `scripts/update_toolkit.py` for cross-platform installation.

---

## Update Workflow

### Step 1: Verify Repository

Check that `scripts/update_toolkit.py` exists in the current working directory. If not,
determine installation path from `~/.claude/skills/geo/`.

### Step 2: Run Update

Run the update toolkit script:

```
run_command python3 scripts/update_toolkit.py --upstream https://github.com/zubair-trabzada/geo-seo-claude
```

If a custom upstream URL was configured, ask the user and pass `--upstream <url>`.

### Step 3: Report Results

When the script completes, report to the user:
- Which platforms were updated
- Installation paths used
- Reminder that changes take effect in new sessions
