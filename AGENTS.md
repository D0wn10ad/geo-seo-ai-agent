# AGENTS.md — geo-seo-ai-agent

> **Important**: Load `platform/SKILL.md` FIRST for platform detection and tool mapping if running outside Claude Code native context.

## What this is

A **multi-platform AI agent toolkit** for Generative Engine Optimization (GEO) audits. The code IS the Markdown — `geo/SKILL.md` is the entrypoint, `skills/geo-*/SKILL.md` are sub-commands, `agents/*.md` are parallel subagent definitions. Python scripts under `scripts/` are utility helpers invoked by skills.

## Essential commands

```
pip install -r requirements.txt              # install Python deps
pytest tests/                                 # run tests (single test file)
python scripts/fetch_page.py page <url>       # test page fetching
```

No lint, typecheck, build, CI, or lockfile exists. No Makefile, no task runner.

## Key architecture

- **Orchestrator:** `geo/SKILL.md` — defines all 22 `/geo <command>` slash commands
- **Full audit flow** (`/geo audit <url>`): phase 1 (discovery/crawl) → phase 2 (5 parallel subagents) → phase 3 (weighted scoring + action plan)
- **Scoring formula:** `GEO_Score = Citability(25%) + Brand(20%) + EEAT(20%) + Technical(15%) + Schema(10%) + Platform(10%)`
- **Fork adds 4 closure-loop skills:** `matrix`, `distribute`, `pipeline`, `compete`

## Data storage

```
~/.geo-prospects/     # CRM + all audit/proposal/report output
```

## Python scripts

- `scripts/fetch_page.py` — most-used utility. CLI modes: `page`, `robots`, `llms`, `sitemap`, `blocks`, `full`
- `scripts/generate_pdf_report.py` — 931 lines, heaviest script. Uses ReportLab directly with custom drawing primitives
- `scripts/crm_dashboard.py` — CLI CRM (see quirk 4 below)
- `scripts/webapp/app.py` — Flask + HTMX CRM web UI

## Quirks

### 1. `sed` venv patching in `install.sh`

The installer creates a venv at `~/.claude/skills/geo/.venv/`, then rewrites `python3` in skill/agent `.md` files via `sed` to pin the venv interpreter:
- `python3 ~/...scripts/` → `~/.claude/...scripts/` (scripts run via shebang after chmod)
- `python3 -c <code>` → `~/.claude/skills/geo/.venv/bin/python3 -c <code>`
- `python3 -m <mod>` → `~/.claude/skills/geo/.venv/bin/python3 -m <mod>`

The tilde is intentionally kept literal — Claude Code's Bash expands it at runtime. The Windows installer (`install-win.sh`) does **none of this** — it has no venv at all and uses `pip install --user`.

### 2. Missing skill files

Of 22 documented `/geo` commands, 20 have `skills/geo-*/SKILL.md` files. Two don't:
- `/geo quick` — implemented directly in the orchestrator `geo/SKILL.md` (no dedicated file)
- `/geo page` — listed in the command table as producing `GEO-PAGE-ANALYSIS.md`, but **no implementation exists**. No skill file, no inline code. Likely unfinished/legacy.

### 3. Unused `validators` dependency

`requirements.txt` pins `validators>=0.22.0,<1.0.0`, but **no Python file in the repo imports it**. Installed for nothing. The repo does its own URL validation (e.g., `fetch_page.py:33`).

### 4. Mixed Italian/English CRM

Two UIs, both incomplete:
- **CLI** (`crm_dashboard.py`): docstring is Italian (`"Visualizza il CRM dei prospect con rich."`), all labels/code are English
- **Web UI** templates: `<html lang="it">` with heavily Italian UI. `dashboard.html` has ~10 Italian strings (`Clienti Attivi`, `GEO Score Medio`, `Azienda`, `Scarica PDF`) mixed with English. `prospect.html` is ~15 Italian strings. The Flask backend (`app.py`) is entirely English. Someone started building in Italian, partially switched mid-development.

### 5. Upstream remote missing (fork-specific)

`/geo update` will **fail** on a fresh clone — requires `git remote add upstream https://github.com/zubair-trabzada/geo-seo-claude`. `FORK_CHANGELOG.md:53` incorrectly claims it "continues to work" without that step.

### 6. No lockfile

`requirements.txt` uses loose ranges. No `poetry.lock`, `requirements-lock.txt`, or constraints. Two installs at different times may get different dep versions, causing subtle inconsistencies.

### 7. Unmerged Content Signals PR

`pr-draft-content-signals.md` describes an unmerged Content Signals feature. References `specs/` and `aeo-scan` directories that don't exist in the current tree — artifacts from upstream that were never included.
