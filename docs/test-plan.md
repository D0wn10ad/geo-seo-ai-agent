# GEO-SEO AI Agent Toolkit — Test Plan

Manual verification checklist for multi-platform (Claude Code + OpenCode) installation and functionality.

**Minimum pass:** T1–T8 (infrastructure verification, no CLI session needed)  
**Full pass:** T1–T11 (includes smoke testing both platforms)  
**Exhaustive:** T1–T12 (includes uninstall/reinstall cycle)

---

## T1 — Installation (full flow)

```bash
# Run from repo root — tests detection, file deploy, venv, shebangs
bash install.sh
```

**Verify:** Output shows "Detected platforms: claude-code, opencode" (or whichever are installed). All copy operations report OK. Venv is created. Shebangs are pinned. No errors.

---

## T2 — File Layout Verification

```bash
# Shared skills (both platforms)
ls ~/.claude/skills/geo/SKILL.md
ls ~/.claude/skills/geo-*/SKILL.md | wc -l      # expect 19
ls ~/.claude/skills/platform/SKILL.md            # platform adapter
ls ~/.claude/skills/platform/TOOL-MAP.md

# OpenCode-specific
ls ~/.config/opencode/agents/geo-*.md            # expect 5
ls ~/.config/opencode/commands/geo-*.md          # expect 21

# Claude Code-specific (still intact)
ls ~/.claude/agents/geo-*.md                     # expect 5
```

---

## T3 — Frontmatter Validation

OpenCode agents must have `mode: subagent` and `permission:` frontmatter.

```bash
head -12 ~/.config/opencode/agents/geo-technical.md
```

**Verify:** Lines 4–11 show `mode: subagent`, `permission:` with `read: allow`, `edit: deny`, `bash: allow`, `webfetch: allow`, `glob: allow`, `grep: allow`.

---

## T4 — No Forbidden Tool Names (body text)

Checks that `WebFetch` and `Bash` appear **only** in the platform adapter, never in skill or agent body text.

```bash
# Should return 0 matches (platform/ files are the exception)
rg 'WebFetch|Bash' \
  ~/.claude/skills/geo/SKILL.md \
  ~/.claude/skills/geo-*/SKILL.md \
  ~/.claude/agents/geo-*.md \
  ~/.config/opencode/agents/geo-*.md \
  -g '*.md'
```

**Verify:** No matches.

Then confirm platform adapter still has them (expected):

```bash
# Should return matches only here
rg 'WebFetch|Bash' ~/.claude/skills/platform/ -g '*.md'
```

**Verify:** At least one match in `platform/SKILL.md` and/or `platform/TOOL-MAP.md`.

---

## T5 — Abstract Tool Names Everywhere

All instruction text should use `` `fetch_url` `` and `` `run_command` ``.

```bash
rg '`fetch_url`' \
  ~/.claude/skills/geo/SKILL.md \
  ~/.claude/skills/geo-*/SKILL.md \
  ~/.claude/agents/geo-*.md \
  -g '*.md' | head -10
```

**Verify:** Many matches. No plain `WebFetch` or `Bash` in body text.

---

## T6 — Python Script Smoke Test

Core utility still works after install:

```bash
python3 scripts/fetch_page.py page https://example.com --timeout 10 2>&1 | head -20
```

**Verify:** Returns HTTP status, title, meta description, and text content of example.com. No import errors.

---

## T7 — OpenCode Command Wrapper Syntax

```bash
head -5 ~/.config/opencode/commands/geo-quick.md
```

**Verify:** Contains `---` frontmatter with `description:` and body text referencing `$1` as the URL argument.

---

## T8 — Agent Body Parity

Body text should be identical between OpenCode and Claude Code agents (only frontmatter differs).

```bash
# OpenCode frontmatter = 12 lines, Claude Code frontmatter = 9 lines
diff <(tail -n +13 ~/.config/opencode/agents/geo-content.md) \
     <(tail -n +10 ~/.claude/agents/geo-content.md)
```

**Verify:** No differences. Repeat for other 4 agents:
- `geo-ai-visibility.md`
- `geo-platform-analysis.md`
- `geo-schema.md`
- `geo-technical.md`

---

## T9 — Claude Code Quick Smoke

In Claude Code CLI:

```
/geo quick https://example.com
```

**Verify:** Returns a 60-second visibility snapshot with a GEO score, not "unknown command".

---

## T10 — OpenCode Command Smoke

In OpenCode CLI:

```
/geo-audit https://example.com
```

**Verify:** Starts the audit flow (fetches, detects business type, launches subagents). Don't need to let it finish — just confirm it starts without errors.

---

## T11 — Web UI Still Works (CRM)

```bash
# Launch the CRM web app
python3 scripts/webapp/app.py
```

**Verify:** Flask starts without import errors. Visit `http://localhost:5000` — dashboard renders.

---

## T12 — Uninstall/Reinstall Cycle (destructive)

```bash
# Remove all installed artifacts
bash uninstall.sh

# Verify cleanup
ls ~/.claude/skills/geo/*.md 2>&1   # should fail/empty
ls ~/.config/opencode/agents/geo-*.md 2>&1  # should fail/empty
ls ~/.config/opencode/commands/geo-*.md 2>&1  # should fail/empty

# Reinstall full flow
bash install.sh

# Re-run T2 to verify everything is restored
```
