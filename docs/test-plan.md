# GEO-SEO AI Agent Toolkit — Test Plan

Manual verification checklist for multi-platform (Claude Code + OpenCode) installation and functionality.

**Minimum pass:** T1–T8 (infrastructure verification, no CLI session needed)  
**Full pass:** T1–T11 (includes smoke testing both platforms)  
**Exhaustive:** T1–T12 (includes uninstall/reinstall cycle)

---

## T1 — Installation (npx-first flow)

```bash
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git
npx skills@1.9.0 check
bash skills/geo/scripts/install_uv.sh
bash skills/geo/scripts/bootstrap_env.sh
```

**Verify:** `check` exits 0; `skills-lock.json` in the install root records the
pinned source; both target agents report the installed `geo-*` skills; the
bootstrap prints the venv path with no import errors.

### Pre-npx cleanup check (not the default path)

`bash uninstall.sh` is retained only as a cleanup fallback for older installs.
It no longer distributes or updates skills. If exercised, follow it with the
pinned npx `add` and bootstrap commands above.

---

## T2 — File Layout Verification

```bash
# Shared skills (both platforms)
ls ~/.claude/skills/geo/SKILL.md
ls -d ~/.claude/skills/geo-* | wc -l             # expect 21 geo-* skills (+ vendored uv)
ls ~/.claude/skills/geo/references/regions/cn/   # CN knowledge base
ls ~/.claude/skills/geo/scripts/fetch_page.py    # nested utilities

# OpenCode-specific
ls ~/.config/opencode/skills/ | grep geo
```

---

## T3 — Skill Frontmatter Validation

Each installed skill must have a `SKILL.md` with `name` and `description` frontmatter.

```bash
head -12 ~/.config/opencode/skills/geo-technical/SKILL.md
```

**Verify:** The frontmatter block declares the skill name and description.

---

## T4 — Self-Locating Script Paths

Skills resolve their scripts from the installed skill directory, not a hardcoded repo path.

```bash
rg 'SKILL_DIR|GEO_SCRIPTS' \
  ~/.claude/skills/geo/SKILL.md \
  ~/.claude/skills/geo-*/SKILL.md \
  -g '*.md' | head -10
```

**Verify:** Matches resolve scripts under the installed `geo` skill; no references to deleted `geo/scripts/` or `resolve_regions.py` paths.

---

## T5 — CN Companion Presence

The 17 region-aware skills carry a `references/cn.md` companion.

```bash
find ~/.claude/skills -path '*/references/cn.md' | wc -l   # expect 17
```

**Verify:** 17 CN companions are installed alongside the skills.

---

## T6 — Python Script Smoke Test

Core utility still works after install:

```bash
python3 skills/geo/scripts/fetch_page.py page https://example.com --timeout 10 2>&1 | head -20
```

**Verify:** Returns HTTP status, title, meta description, and text content of example.com. No import errors.

---

## T7 — Skill Install Parity

The same skills are installed for both agents (npx distributes skills only).

```bash
diff <(ls ~/.config/opencode/skills/ | grep geo | sort) \
     <(ls ~/.claude/skills/ | grep geo | sort)
```

**Verify:** No differences — both agents have the same `geo-*` skills.

---

## T8 — Worker Skill Presence

The five phase-2 worker skills are installed alongside the public skills.

```bash
for s in geo-ai-visibility geo-platform-analysis geo-technical geo-content geo-schema; do
  ls ~/.claude/skills/$s/SKILL.md
done
```

**Verify:** All five worker skills are present.

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
python3 skills/geo/scripts/webapp/app.py
```

**Verify:** Flask starts without import errors. Visit `http://localhost:5000` — dashboard renders.

---

## T12 — Uninstall/Reinstall Cycle (destructive)

```bash
# Remove npx-managed skills (select the geo / geo-* skills)
npx skills@1.9.0 remove

# Cleanup fallback only: bash uninstall.sh cleans old git-clone artifacts
# (it detects npx layout and deletes nothing when found)

# Reinstall with the pinned add form, then re-bootstrap deps if needed
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git
bash skills/geo/scripts/bootstrap_env.sh

# Re-run T2 to verify everything is restored, and confirm the pin
npx skills@1.9.0 check
```

**Verify:** `~/.geo-prospects/` is intact before and after; the bootstrap venv
under `${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent` is not deleted.
