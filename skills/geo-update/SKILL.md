---
name: geo-update
description: Pull the latest GEO-SEO skill updates from the upstream repository using update_toolkit.py. Supports both Claude Code and OpenCode platforms.
---

# GEO-SEO Update Skill

<!-- GEO-SCRIPT-RESOLUTION:v1 -->

**Script resolution.** Set `SKILL_DIR` to this SKILL.md's directory. Resolve `GEO_SCRIPTS` as the first existing of `"$SKILL_DIR/scripts"`, `"$SKILL_DIR/../geo/scripts"`, `"$SKILL_DIR/../../geo/scripts"`, `"$SKILL_DIR/../../../.claude/skills/geo/scripts"` (full preamble in `geo/SKILL.md` → "Script Path Resolution"). Set `PY="$(command -v python3 || command -v python)"`, then invoke scripts as `"$PY" "$GEO_SCRIPTS/<script>.py" ...`. Windows runs through Git Bash, which supplies these commands and forward-slash paths; native PowerShell/CMD is out of scope.

## Purpose

Updates the locally installed GEO-SEO skills, agents, scripts, and documentation to the latest version from the upstream repository. Delegates to `$GEO_SCRIPTS/update_toolkit.py` for cross-platform installation.

---

## Update Workflow

### Step 1: Verify Repository

Resolve `GEO_SCRIPTS` with the ordered fallback list above, then check that
`$GEO_SCRIPTS/update_toolkit.py` exists.

### Step 2: Run Update

Run the update toolkit script:

```
run_command "$PY" "$GEO_SCRIPTS/update_toolkit.py" --upstream https://github.com/zubair-trabzada/geo-seo-claude
```

If a custom upstream URL was configured, ask the user and pass `--upstream <url>`.

### Step 3: Report Results

When the script completes, report to the user:
- Which platforms were updated
- Installation paths used
- Reminder that changes take effect in new sessions
