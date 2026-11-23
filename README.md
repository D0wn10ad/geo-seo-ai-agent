<p align="center">
  <img src="assets/banner.svg" alt="GEO-SEO AI Agent Toolkit" width="900"/>
</p>

<p align="center">
  <strong>GEO-first, SEO-supported.</strong> Optimize websites for AI-powered search engines<br/>
  (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) while maintaining traditional SEO foundations.
</p>

<p align="center">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-ready-brightgreen"/> <img alt="OpenCode" src="https://img.shields.io/badge/OpenCode-ready-blue"/>
</p>

<p align="center">
  AI search is eating traditional search. This toolkit optimizes for where traffic is going, not where it was.
</p>

---

## Overview

This is a fork of [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) extended with a **cross-platform architecture** (Claude Code + OpenCode with superpowers) and **4 closure-loop skills** that complete the GEO workflow:

| Fork-added Skill | Command | Purpose |
|---|---|---|
| `geo-intent-matrix` | `/geo matrix <core-topic>` | 4-quadrant intent matrix + 12-week editorial schedule |
| `geo-citation-pipeline` | `/geo pipeline <url>` | 5-stage AI citation pipeline + 6-engine preferred-answer verification |
| `geo-distribution-plan` | `/geo distribute <topic>` | Authority-tiered 14-day multi-platform distribution plan |
| `geo-competitor-citation` | `/geo compete <domain> <c1,c2,...>` | Cross-engine competitor citation gap matrix with verdict per quadrant |

Upstream skills, agents, scripts, and schemas remain unchanged. See [FORK_CHANGELOG.md](FORK_CHANGELOG.md) for the full diff.

---

## Quick Start

### Install (macOS / Linux) — pinned npx, both agents

Install the skills for Claude Code and OpenCode from this fork with the pinned
`skills` CLI. This is the default and only supported distribution path:

```bash
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git
```

To target a single agent, keep only the corresponding `-a` flag. The `1.9.0` pin
is deliberate: `skills-lock.json` in the install root records the pinned source
and version, and both the lock format and CLI surface change between releases.
Do **not** substitute an unpinned `npx skills`.

### Windows

The same pinned command works on Windows when run from **Git Bash** (bundled with
[Git for Windows](https://git-scm.com/downloads)). PowerShell and Command Prompt
are not supported.

```bash
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git
```

### Python dependencies — one-time bootstrap

`npx` installs skills only; it does **not** install Python dependencies. The
utility scripts require Python 3.10+ (the pinned `lxml` release requires 3.10+). From a clone of
this repo, bootstrap the shared cache venv:

```bash
bash skills/geo/scripts/install_uv.sh     # installs pinned uv 0.13.9 only if absent
bash skills/geo/scripts/bootstrap_env.sh  # creates ${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent/venv
```

`bootstrap_env.sh` resolves `skills/geo/scripts/requirements.txt` beside the
script by default. Pass a different `requirements.txt` path as the first argument
if you are running it outside the repo. The bootstrap is checksum-keyed and
idempotent: re-running it is a no-op until `requirements.txt` changes. Your system
Python is untouched, and `~/.geo-prospects/` is never removed.

### Check and update

From the install root (the directory holding `skills-lock.json` / `.agents/skills/`):

```bash
npx skills@1.9.0 check
npx skills@1.9.0 update
```

`check` exits non-zero when an installed skill is behind its pinned source — that
is the expected signal to run `update`, not an error to ignore. Re-run `check`
afterwards to confirm a clean state. If the install must be rebuilt for both
agents, re-run the pinned `add` command above. Changes take effect in new
sessions, so restart your AI client.

See [skills/geo-update/SKILL.md](skills/geo-update/SKILL.md) for the full update
workflow. Bump the pin only as a deliberate repo-wide change: update that skill,
this Quick Start, and the docs together, then re-run the full suite and a fresh
`npx skills@1.9.0 add` verification.

### Requirements

| Dependency | Notes |
|------------|-------|
| Python 3.10+ | Required for utility scripts (pinned `lxml` needs 3.10+) |
| Node.js + npx | Runs the pinned `skills@1.9.0` CLI |
| Claude Code CLI and/or OpenCode | Target agents; at least one must be installed |
| `uv` | Installed by `skills/geo/scripts/install_uv.sh` (pinned 0.13.9) for the dep bootstrap |
| Internet access | Required: audits fetch live URLs and AI-cited platforms |

### Upgrading a pre-npx install

The old git-clone install scripts were removed. If you used one, clean up with
`bash uninstall.sh` (it preserves `~/.geo-prospects/`) and then run the pinned
`npx skills@1.9.0 add` command above. See [Uninstall](#uninstall) and
[Upgrading an older install](#upgrading-an-older-install).

---

## Commands

All 22 commands work identically in Claude Code (`/geo <cmd>`) and OpenCode (`/geo-<cmd>`):

| Command | Purpose |
|---------|---------|
| `/geo audit <url>` | Full GEO + SEO audit with 5 parallel subagents |
| `/geo citability <url>` | AI citation readiness score |
| `/geo crawlers <url>` | AI crawler access check (robots.txt) |
| `/geo llmstxt <url>` | Analyze or generate llms.txt |
| `/geo brands <url>` | Brand mention scan across AI-cited platforms |
| `/geo platforms <url>` | Platform-specific optimization (ChatGPT, Perplexity, Google AIO) |
| `/geo schema <url>` | Structured data detection, validation, generation |
| `/geo technical <url>` | Technical SEO audit |
| `/geo content <url>` | Content quality & E-E-A-T assessment |
| `/geo page <url>` | Deep single-page GEO analysis |
| `/geo quick <url>` | 60-second GEO visibility snapshot |
| `/geo report <url>` | Client-ready GEO report (Markdown) |
| `/geo report-pdf <url>` | Professional PDF report with charts |
| `/geo prospect <cmd>` | CRM-lite: manage prospects pipeline |
| `/geo proposal <domain>` | Auto-generate client proposal |
| `/geo compare <domain>` | Monthly delta / progress report |
| `/geo update` | Check/update pinned npx skills for this fork |
| `/geo matrix <topic>` | Intent matrix + editorial schedule |
| `/geo pipeline <url>` | 5-stage AI citation pipeline |
| `/geo distribute <topic>` | Multi-platform distribution plan |
| `/geo compete <d> <c1,c2,...>` | Competitor citation gap analysis |
| `/geo help` | Show all commands with descriptions |

> Commands after `/geo update` are fork-added. Run `/geo help` inside your AI client for the full list.

---

## Architecture

```
geo-seo-ai-agent/
├── skills/                     # single skills root: 21 geo-* skills + vendored uv
│   ├── geo/                    # orchestrator + nested utilities and region KB
│   │   ├── SKILL.md            # orchestrator and /geo command table
│   │   ├── scripts/            # Python utilities (travel nested with the geo skill)
│   │   │   ├── fetch_page.py
│   │   │   ├── citability_scorer.py
│   │   │   ├── brand_scanner.py
│   │   │   ├── llmstxt_generator.py
│   │   │   ├── generate_pdf_report.py
│   │   │   ├── region_resolver.py
│   │   │   ├── crm_dashboard.py
│   │   │   ├── bootstrap_env.sh    # idempotent, checksum-keyed dep bootstrap
│   │   │   ├── install_uv.sh       # pinned uv 0.13.9 installer helper
│   │   │   ├── webapp/
│   │   │   └── requirements.txt    # Python dependencies
│   │   ├── assets/schema/      # JSON-LD templates (6 files)
│   │   └── references/regions/ # region profiles + CN knowledge base (cn/)
│   │       ├── profiles.yaml
│   │       ├── cn-variants.json
│   │       └── cn/
│   ├── geo-audit/              # 17 of these carry references/cn.md
│   ├── geo-citability/
│   ├── geo-crawlers/
│   ├── geo-llmstxt/
│   ├── geo-brand-mentions/
│   ├── geo-platform-optimizer/
│   ├── geo-schema/
│   ├── geo-technical/
│   ├── geo-content/
│   ├── geo-report/
│   ├── geo-report-pdf/
│   ├── geo-prospect/
│   ├── geo-proposal/
│   ├── geo-compare/
│   ├── geo-ai-visibility/      ═ phase-2 worker skill
│   ├── geo-platform-analysis/  ═ phase-2 worker skill
│   ├── geo-intent-matrix/      ═ fork-added
│   ├── geo-citation-pipeline/  ═ fork-added
│   ├── geo-distribution-plan/  ═ fork-added
│   ├── geo-competitor-citation/═ fork-added
│   ├── geo-update/
│   └── uv/                     ═ vendored pinned installer helper
├── docs/                       # full documentation
└── uninstall.sh                # cleanup fallback for pre-npx installs
```

`npx skills@1.9.0 add` discovers directories containing a `SKILL.md` and copies
their hierarchy verbatim. `skills/geo/SKILL.md`, the vendored `skills/uv/` skill,
and the nested `skills/geo/scripts/`, `skills/geo/assets/schema/` and
`skills/geo/references/regions/` files are the source of truth — nothing is
generated or rewritten at install time. npx distributes skills only; it does
not install command files. `.opencode/` is a local deploy artifact, not
committed source. Runtime `--region <code>` data (including `--region cn`) lives
in `skills/geo/references/regions/cn/`, with 17 CN companions at
`skills/<geo-x>/references/cn.md`.

---

## Data Storage

CRM and reporting skills store data outside the skill directory:

```
~/.geo-prospects/
├── prospects.json
├── proposals/
└── reports/
```

This directory is **not removed** by `uninstall.sh` — delete manually if needed.

---

## How It Works

### Full Audit Flow (`/geo audit <url>`)

1. **Discovery** — Fetches homepage, detects business type, crawls sitemap (up to 50 pages)
2. **Parallel Analysis** — 5 subagents run simultaneously:
   - AI Visibility (citability, crawlers, llms.txt, brand mentions)
   - Platform Analysis (ChatGPT, Perplexity, Google AIO readiness)
   - Technical SEO (Core Web Vitals, SSR, security, mobile)
   - Content Quality (E-E-A-T, readability, freshness)
   - Schema Markup (detection, validation, generation)
3. **Synthesis** — Aggregates scores into composite GEO Score (0–100)
4. **Report** — Prioritized action plan with quick wins

### Scoring

| Category | Weight |
|----------|--------|
| AI Citability & Visibility | 25% |
| Brand Authority Signals | 20% |
| Content Quality & E-E-A-T | 20% |
| Technical Foundations | 15% |
| Structured Data | 10% |
| Platform Optimization | 10% |

---

## Uninstall

For an **npx-managed** install, remove via npx (this leaves the lock/manifest and cache intact):

```bash
npx skills@1.9.0 remove    # select the geo / geo-* skills
```

`bash uninstall.sh` is retained as a **cleanup fallback** for installs made by the old git-clone installer. It detects the npx layout and, when found, only prints the pinned command above — it never deletes npx-owned links, the cache, or symlink targets. On a pre-npx install it removes only `~/.claude/skills/geo*`, `~/.claude/agents/geo-*.md`, and the OpenCode agents/commands under `${XDG_CONFIG_HOME:-~/.config}` (old per-skill venv included), with symlink-safe handling.

`~/.geo-prospects/` is always preserved. The bootstrap venv at `${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent` is a shared cache and is not removed. On Windows, run the npx command above from Git Bash. See [Getting Started](docs/getting-started.md) for the full install, update, and uninstall walkthrough and [Upgrading an older install](#upgrading-an-older-install) if you are migrating from a pre-npx setup.

---

## Upgrading an older install

If you have a pre-npx (git-clone) install, you can move to the pinned npx distribution. `uninstall.sh`-first is the **documented recommended default** for a clean state, but uninstall is optional — a direct in-place `npx skills@1.9.0 add` is also supported. `npx skills@1.9.0 add` overwrites same-named skill directories wholesale (it does not merge), but it does **not** remove artifacts it does not own. `~/.geo-prospects/` is preserved in **both** paths.

### Path A (recommended): uninstall first, then clean npx add

```bash
# 1) Remove pre-npx artifacts (preserves ~/.geo-prospects/ and the shared cache venv)
bash uninstall.sh

# 2) Install with the pinned npx CLI (this fork, both agents)
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git

# 3) One-time bootstrap (Python 3.10+; installs pinned uv only if absent)
bash ~/.claude/skills/geo/scripts/install_uv.sh
bash ~/.claude/skills/geo/scripts/bootstrap_env.sh

# 4) Verify
npx skills@1.9.0 check
ls ~/.claude/skills/geo/SKILL.md
```

Run the bootstrap from the installed skill path shown above (adjust if your agent uses a different install root). Re-run bootstrap only when `requirements.txt` changes. Restart your AI client so new sessions pick up the installed skills.

### Path B (in-place): direct add + manual legacy cleanup

`npx skills@1.9.0 add` refreshes/replaces managed skill directories even over an older install, but it will **not** auto-clean legacy-only artifacts. Use this path when you want to avoid running `uninstall.sh`, then complete the cleanup checklist yourself.

```bash
# 1) In-place pinned add (overwrites same-named skill directories)
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git

# 2) Manual cleanup of legacy-only artifacts npx does not own (only if present)
rm -rf ~/.claude/skills/geo/.venv                  # legacy `.venv` (old per-skill venv; bootstrap now uses XDG cache venv)
rm -f  ~/.claude/agents/geo-*.md                   # old agent files from pre-npx installs
rm -f  "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/agents/geo-*.md"
rm -f  "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/commands/geo-*.md"  # stale generated .opencode/commands wrappers
# remove any stale symlinks pointing at removed legacy targets:
find ~/.claude/skills ~/.claude/agents "${XDG_CONFIG_HOME:-$HOME/.config}/opencode" \
  -maxdepth 2 -xtype l -name 'geo*' -delete 2>/dev/null || true

# 3) One-time bootstrap (if not already bootstrapped)
bash ~/.claude/skills/geo/scripts/install_uv.sh
bash ~/.claude/skills/geo/scripts/bootstrap_env.sh

# 4) Verify
npx skills@1.9.0 check
ls ~/.claude/skills/geo/SKILL.md
```

**Do not remove:** `~/.geo-prospects/` (preserved runtime data), the npx download cache, `skills-lock.json`, or any npx-managed cache/symlink targets. The bootstrap venv at `${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent` is a shared cache and is kept in both paths. If you need a fully clean npx-managed removal instead of an upgrade, use `npx skills@1.9.0 remove` (not `uninstall.sh`).

---

## Documentation

Detailed docs are in the `docs/` directory:

| Doc | What's in it |
|-----|-------------|
| [Getting Started](docs/getting-started.md) | Prerequisites, install, first audit, troubleshooting |
| [Commands Reference](docs/commands-reference.md) | Every `/geo` command with usage and examples |
| [Architecture](docs/architecture.md) | Repo layout, audit flow, subagent dispatch |
| [Skills & Agents](docs/skills-and-agents.md) | Sub-skills, subagents, scripts, schemas |
| [Scoring Methodology](docs/scoring-methodology.md) | GEO Score computation, signals, caveats |
| [FAQ](docs/faq.md) | Common questions for users and contributors |
| [Test Plan](docs/test-plan.md) | Manual verification checklist for multi-platform install |

---

## Use Cases

- **GEO Agencies** — Run client audits and generate deliverables
- **Marketing Teams** — Monitor and improve AI search visibility
- **Content Creators** — Optimize content for AI citations
- **Local Businesses** — Get found by AI assistants
- **SaaS Companies** — Improve entity recognition across AI platforms
- **E-commerce** — Optimize product pages for AI shopping recommendations

---

## License

MIT — see [LICENSE](LICENSE). Original work © 2026 Zubair Trabzada.
