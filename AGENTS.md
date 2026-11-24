# AGENTS.md — geo-seo-ai-agent

> **Important**: Load `skills/geo/SKILL.md` FIRST for the orchestrator and command table; it self-locates its scripts and region files.

## What this is

A **multi-platform AI agent toolkit** for Generative Engine Optimization (GEO) audits. The code IS the Markdown — `skills/geo/SKILL.md` is the orchestrator, the 21 `skills/geo-*/SKILL.md` files are the sub-skills (including two internal phase-2 workers), and the CN companions live at `skills/<geo-x>/references/cn.md`. Python scripts under `skills/geo/scripts/` are utility helpers invoked by skills. Distribution is pinned npx (`npx skills@1.9.0 add ...`): the install copies committed files verbatim and rewrites nothing. npx distributes skills only — it does not install command files.

## Essential commands

```
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git   # install / re-install (pinned)
npx skills@1.9.0 check                                  # verify installed skills against the pin
bash skills/geo/scripts/install_uv.sh                   # one-time: pinned uv 0.13.9, only if absent
bash skills/geo/scripts/bootstrap_env.sh                # one-time: checksum-keyed cache venv for deps
pytest tests/                                           # run all tests (or `pytest tests/<file>.py`)
<venv>/bin/python skills/geo/scripts/fetch_page.py page <url>  # test page fetching
```

Requires Python 3.10+ for the utility scripts (the pinned `lxml` needs 3.10+). `npx` installs skills only — it does not install Python dependencies; use the two bootstrap helpers above, which leave the system Python untouched and write to `${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent/venv`. The old git-clone install scripts were removed; `uninstall.sh` remains a cleanup fallback for pre-npx installs. npx is the only install path.

No lint, typecheck, build, CI, or Python dependency lockfile exists. No Makefile, no task runner.

## Key architecture

- **Orchestrator:** `skills/geo/SKILL.md` — defines all 22 `/geo <command>` slash commands; the 21 `skills/geo-*/SKILL.md` files are the sub-skills.
- **Distribution:** pinned `npx skills@1.9.0 add` copies the committed `skills/` hierarchy verbatim into each target agent's config dir. `skills-lock.json` in the install root records the pinned source/version (gitignored). npx distributes skills only — it does not install command files.
- **Python deps:** one-time `skills/geo/scripts/install_uv.sh` + `skills/geo/scripts/bootstrap_env.sh` create a shared, checksum-keyed cache venv; re-run only when `requirements.txt` changes.
- **Full audit flow** (`/geo audit <url>`): phase 1 (discovery/crawl) → phase 2 (5 parallel subagents) → phase 3 (weighted scoring + action plan)
- **Scoring formula:** `GEO_Score = Citability(25%) + Brand(20%) + EEAT(20%) + Technical(15%) + Schema(10%) + Platform(10%)`
- **Non-scoring:** `geo-technical` Category 9 Agent-Readiness signals are explicitly NON-scoring and do NOT feed `GEO_Score` (skills/geo-technical/SKILL.md:368+, :439).
- **Fork adds 4 closure-loop skills:** `matrix`, `distribute`, `pipeline`, `compete`
- **Region-aware:** every command accepts `--region <code>` (e.g. `--region cn`); region auto-detects from URL/content when omitted, and China markets also use `skills/<geo-x>/references/cn.md`. The CN knowledge base (11 files, incl. `ai-engines.md`, `platforms.md`, `schema.md`) lives in `skills/geo/references/regions/cn/`, with profiles at `skills/geo/references/regions/profiles.yaml` and the variant manifest at `skills/geo/references/regions/cn-variants.json`. `openspec/changes/` holds region-aware change records.

## Data storage

```
~/.geo-prospects/     # CRM + all audit/proposal/report output
```

Client-facing artifacts written to the repo root are gitignored on purpose: `/GEO-*.md`, `/GEO-*.pdf`, `*.pdf`, `/llms.txt`, `/llms-full.txt`, `/audit-data*.json` — do not commit them.

## Python scripts

- `skills/geo/scripts/fetch_page.py` — most-used utility. CLI modes: `page`, `robots`, `llms`, `sitemap`, `blocks`, `full`; `robots` mode returns `cloudflare_managed:true` when Cloudflare-managed robots is detected.
- `skills/geo/scripts/generate_pdf_report.py` — 943 lines, heaviest script. Uses ReportLab directly with custom drawing primitives
- `skills/geo/scripts/crm_dashboard.py` — CLI CRM (see quirk 4 below)
- `skills/geo/scripts/webapp/app.py` — Flask + HTMX CRM web UI; its `region_label()` falls back from `region` to `country`
- `skills/geo/scripts/install_uv.sh` — pinned uv 0.13.9 installer helper for the dependency bootstrap
- `skills/geo/scripts/bootstrap_env.sh` — idempotent, checksum-keyed cache-venv bootstrap

## Tests (`tests/`)

19 pytest modules. Largest by size: `test_surviving_behavior_characterization.py`, `test_fetch_page_ssr.py`, `test_env_bootstrap.py`, `test_uv_bootstrap.py`. Coverage groups: npx/docs (`test_npx_docs.py` scans README.md + docs/*.md; `test_agents_md_current.py` guards this root file), CN region preservation (`test_cn_region_preservation.py`), deleted legacy updater (`test_legacy_updater_removed.py`), retired installers (`test_legacy_installers_retired.py`), pruned deps (`test_pruned_deps.py`), script relocation (`test_scripts_relocation.py`), self-locating markdown (`test_self_locating_markdown.py`), uninstall safety/execution (`test_uninstall_safety.py`, `test_uninstall_execution.py`), upgrade path (`test_upgrade_path.py`), webapp region (`test_webapp_region.py`), robots/Cloudflare (`test_fetch_robots_cloudflare.py`, 3 tests: managed block detected, plain not flagged, missing not flagged), agent/skill folding (`test_agent_skill_fold.py`). `agent-readiness-test-results.md` is a manual-record doc, not a pytest suite.

## Quirks

### 1. Distribution rewrites nothing

Skills are distributed by pinned `npx skills@1.9.0 add`, which copies the committed `skills/` hierarchy verbatim into each target agent's config dir — no deploy-time path rewriting and no generated source wrappers. npx distributes skills only; it does not install command files. The old deploy-time markdown-rewriting flow was deleted in the npx migration. `skills-lock.json` in the install root records the pinned source and version and is gitignored; bump the pin only as a deliberate repo-wide change across the update skill, README, and docs together.

### 2. Missing skill files

There are 21 `skills/geo-*/SKILL.md` files: 19 back public `/geo` commands, and two (`geo-ai-visibility`, `geo-platform-analysis`) are internal phase-2 workers with no public command. Three documented commands have no dedicated skill file:
- `/geo quick` — inline summary in the `geo` skill command/output tables; no dedicated skill file.
- `/geo page` — defined by the `geo` skill, which sets `GEO-PAGE-ANALYSIS.md` as the output file; no dedicated `skills/geo-page/SKILL.md`.
- `/geo help` — built-in command listing, no skill file.

### 3. `.opencode/` is a local deploy artifact, not committed source

`.opencode/`, when present, is a local npx deploy artifact — never source to edit or commit here. `.gitignore` blocks `.opencode/*` except `!.opencode/agents/` and `!.opencode/commands/`. Don't edit or expect those files as source in this repo. npx distributes skills only; it does not install command files.

### 4. Mixed Italian/English CRM

Two UIs, both incomplete:
- **CLI** (`crm_dashboard.py`): docstring is Italian (`"Visualizza il CRM dei prospect con rich."`), all labels/code are English
- **Web UI** templates: `<html lang="it">` with heavily Italian UI. `dashboard.html` has ~10 Italian strings (`Clienti Attivi`, `GEO Score Medio`, `Azienda`, `Scarica PDF`) mixed with English. `prospect.html` is ~15 Italian strings. The Flask backend (`app.py`) is entirely English. Someone started building in Italian, partially switched mid-development.

### 5. `/geo update` targets this fork via pinned npx

`npx skills@1.9.0 check` / `npx skills@1.9.0 update` operate against the pinned source recorded in `skills-lock.json` (`https://github.com/D0wn10ad/geo-seo-ai-agent.git`), so updates self-target this fork. The `zubair-trabzada/geo-seo-claude` references in `FORK_CHANGELOG.md:5 and :93` are stale upstream history, not the active update source.

### 6. No Python dependency lockfile

`requirements.txt` uses loose ranges. There is no `poetry.lock`, `requirements-lock.txt`, or constraints file for Python deps (the `skills-lock.json` pin applies only to npx skill sources). Two installs at different times may get different dep versions, causing subtle inconsistencies.

### 7. Unmerged Content Signals PR

`pr-draft-content-signals.md` describes an unmerged Content Signals feature. References `specs/` and `aeo-scan` directories that don't exist in the current tree — artifacts from upstream that were never included.

### 8. Dependency set is intentionally minimal

`requirements.txt` pins exactly seven runtime deps. The npx migration pruned the previously listed `validators` (along with `playwright` and `Pillow`) as unused; `reportlab` remains for PDF generation. There is no browser-automation step in the distributed skills.
