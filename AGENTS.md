# AGENTS.md — geo-seo-ai-agent

> **Important**: Load `platform/SKILL.md` FIRST for platform detection and tool mapping if running outside Claude Code native context.

## What this is

A **multi-platform AI agent toolkit** for Generative Engine Optimization (GEO) audits. The code IS the Markdown — `geo/SKILL.md` is the entrypoint, `skills/geo-*/SKILL.md` are sub-commands, `agents/*.md` are parallel subagent definitions. Python scripts under `scripts/` are utility helpers invoked by skills.

## Essential commands

```
pip install -r requirements.txt              # install Python deps (loose-range deps)
pytest tests/                                 # run all tests (or `pytest tests/<file>.py`)
python scripts/fetch_page.py page <url>       # test page fetching
```

Requires Python 3.10+ (install.sh / install-win.sh probe python3.15..3.10; Pillow/lxml drop 3.9) — trust the installers over README.md.

No lint, typecheck, build, CI, or lockfile exists. No Makefile, no task runner.

## Key architecture

- **Orchestrator:** `geo/SKILL.md` — defines all 22 `/geo <command>` slash commands
- **Full audit flow** (`/geo audit <url>`): phase 1 (discovery/crawl) → phase 2 (5 parallel subagents) → phase 3 (weighted scoring + action plan)
- **Scoring formula:** `GEO_Score = Citability(25%) + Brand(20%) + EEAT(20%) + Technical(15%) + Schema(10%) + Platform(10%)`
- **Non-scoring:** `geo-technical` Category 9 Agent-Readiness signals are explicitly NON-scoring and do NOT feed `GEO_Score` (skills/geo-technical/SKILL.md:368+, :439).
- **Fork adds 4 closure-loop skills:** `matrix`, `distribute`, `pipeline`, `compete`
- **Region-aware:** every command accepts `--region <code>` (e.g. `--region cn`); region auto-detects from URL/content when omitted, and China markets also use `skills/geo-*/SKILL.cn.md`. `regions/` root holds only `cn/`, `README.md`, `profiles.yaml`; the CN knowledge base (11 files, incl. `ai-engines.md`, `platforms.md`, `schema.md`) lives in `regions/cn/`. `openspec/changes/` holds region-aware change records.

## Data storage

```
~/.geo-prospects/     # CRM + all audit/proposal/report output
```

Client-facing artifacts written to the repo root are gitignored on purpose: `/GEO-*.md`, `/GEO-*.pdf`, `*.pdf`, `/llms.txt`, `/llms-full.txt`, `/audit-data*.json` — do not commit them.

## Python scripts

- `scripts/fetch_page.py` — most-used utility. CLI modes: `page`, `robots`, `llms`, `sitemap`, `blocks`, `full`; `robots` mode returns `cloudflare_managed:true` when Cloudflare-managed robots is detected.
- `scripts/generate_pdf_report.py` — 941 lines, heaviest script. Uses ReportLab directly with custom drawing primitives
- `scripts/crm_dashboard.py` — CLI CRM (see quirk 4 below)
- `scripts/webapp/app.py` — Flask + HTMX CRM web UI; its `region_label()` falls back from `region` to `country`

## Tests (`tests/`)

`test_update_toolkit.py` (deploy-path rewriting — largest), `test_fetch_page_ssr.py`, `test_webapp_region.py` (webapp region label + render), `test_fetch_robots_cloudflare.py` (3 tests: managed block detected, plain not flagged, missing not flagged). `agent-readiness-test-results.md` is a manual-record doc, not a pytest suite.

## Quirks

### 1. Runtime path rewriting in deployed markdown

The deploy flow rewrites `python3` references in installed skill/agent `.md` files at deployment time (in `scripts/update_toolkit.py`, not `install.sh`) so runtime commands resolve to installed paths:
- `python3 scripts/<name>.py` → `~/.claude/skills/geo/scripts/<name>.py` (self-executing shebang)
- `python3 -c <code>` → `<venv>/bin/python3 -c <code>`
- `python3 -m <mod>` → `<venv>/bin/python3 -m <mod>`

The tilde is intentionally kept literal — Claude Code's Bash expands it at runtime. The `--runtime-python` and `--runtime-scripts-root` flags on `update_toolkit.py` control the replacement paths. The Windows installer (`install-win.sh`) does **none of this** — it has no venv at all and uses `pip install --user`. Source markdown files in the repo are never modified.

### 2. Missing skill files

Of 22 documented `/geo` commands, 20 have `skills/geo-*/SKILL.md` files. Two don't:
- `/geo quick` — implemented directly in the orchestrator `geo/SKILL.md` (no dedicated file)
- `/geo page` — listed in the command table as producing `GEO-PAGE-ANALYSIS.md`, but **no implementation exists**. No skill file, no inline code. Likely unfinished/legacy.

### 3. `.opencode/` is deploy-generated, not committed

README's architecture shows `.opencode/` (agents + 21 command wrappers), but the directory **does not exist** in the working tree — it's generated at deploy time by `update_toolkit.py`. `.gitignore` blocks all of `.opencode/*` except `!.opencode/agents/` and `!.opencode/commands/`. Don't edit or expect those files here.

### 4. Mixed Italian/English CRM

Two UIs, both incomplete:
- **CLI** (`crm_dashboard.py`): docstring is Italian (`"Visualizza il CRM dei prospect con rich."`), all labels/code are English
- **Web UI** templates: `<html lang="it">` with heavily Italian UI. `dashboard.html` has ~10 Italian strings (`Clienti Attivi`, `GEO Score Medio`, `Azienda`, `Scarica PDF`) mixed with English. `prospect.html` is ~15 Italian strings. The Flask backend (`app.py`) is entirely English. Someone started building in Italian, partially switched mid-development.

### 5. `/geo update` pulls from this fork, not upstream

`update_toolkit.py` defaults `--upstream` to `https://github.com/D0wn10ad/geo-seo-ai-agent` (`REPO_URL`), so `/geo update` self-updates this fork. It no longer needs the `zubair-trabzada/geo-seo-claude` remote that older docs (`FORK_CHANGELOG.md:53`, the `geo-update` skill) still reference — those claims are stale.

### 6. No lockfile

`requirements.txt` uses loose ranges. No `poetry.lock`, `requirements-lock.txt`, or constraints. Two installs at different times may get different dep versions, causing subtle inconsistencies.

### 7. Unmerged Content Signals PR

`pr-draft-content-signals.md` describes an unmerged Content Signals feature. References `specs/` and `aeo-scan` directories that don't exist in the current tree — artifacts from upstream that were never included.

### 8. Unused `validators` dependency

requirements.txt lists `validators>=0.22.0,<1.0.0` but no .py file imports it (upstream added it while removing reportlab; this fork keeps reportlab AND adds validators). Harmless at runtime.
