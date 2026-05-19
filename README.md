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

### macOS / Linux

```bash
# Default branch (main)
curl -fsSL https://raw.githubusercontent.com/D0wn10ad/geo-seo-ai-agent/main/install.sh | bash

# Specific branch (for testing)
curl -fsSL https://raw.githubusercontent.com/D0wn10ad/geo-seo-ai-agent/<branch>/install.sh | bash /dev/stdin -b <branch>
```

### Windows (Git Bash)

```bash
curl -fsSL https://raw.githubusercontent.com/D0wn10ad/geo-seo-ai-agent/main/install-win.sh | bash
```

> Run from Git Bash, not PowerShell or CMD. Requires [Git for Windows](https://git-scm.com/downloads).

### Manual

```bash
git clone https://github.com/D0wn10ad/geo-seo-ai-agent.git
cd geo-seo-ai-agent
bash install.sh
```

### Requirements

| Dependency | Notes |
|------------|-------|
| Python 3.8+ | Debian/Ubuntu also needs `python3-venv` |
| Claude Code CLI | or OpenCode with [oh-my-opencode](https://opencode.ai) plugin |
| Git | Required for installer |
| `uv` (optional) | Faster pip — auto-detected by installer |
| Playwright (optional) | For PDF screenshot generation |

### Isolated install

Python deps go into `~/.claude/skills/geo/.venv/` — your system Python is untouched. Uninstalling removes the venv too.

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
| `/geo update` | Pull latest updates from upstream |
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
├── geo/                        # Main orchestrator (SKILL.md)
├── skills/                     # 19 specialized sub-skills
│   ├── geo-audit/
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
│   ├── geo-intent-matrix/      ═ fork-added
│   ├── geo-citation-pipeline/  ═ fork-added
│   ├── geo-distribution-plan/  ═ fork-added
│   ├── geo-competitor-citation/═ fork-added
│   └── geo-update/
├── platform/                   # Cross-platform tool mapping adapter
│   ├── SKILL.md
│   └── TOOL-MAP.md
├── agents/                     # 5 parallel subagents (Claude Code)
├── .opencode/                  # OpenCode-specific files
│   ├── agents/                 # 5 subagents (OpenCode format)
│   └── commands/               # 21 /geo-* command wrappers
├── scripts/                    # Python utilities
│   ├── fetch_page.py
│   ├── citability_scorer.py
│   ├── brand_scanner.py
│   ├── llmstxt_generator.py
│   ├── generate_pdf_report.py
│   ├── update_toolkit.py       ═ cross-platform installer
│   ├── crm_dashboard.py
│   └── webapp/
├── schema/                     # JSON-LD templates (6 files)
├── docs/                       # Full documentation
│   ├── getting-started.md
│   ├── commands-reference.md
│   ├── architecture.md
│   ├── skills-and-agents.md
│   ├── scoring-methodology.md
│   ├── faq.md
│   └── test-plan.md
├── install.sh                  # Cross-platform installer
├── uninstall.sh                # Cross-platform uninstaller
└── requirements.txt
```

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

```bash
bash uninstall.sh
```

Removes from both `~/.claude/` (skills, agents, venv) and `~/.config/opencode/` (agents, commands).

Manual cleanup:
```bash
rm -rf ~/.claude/skills/geo ~/.claude/skills/geo-* ~/.claude/agents/geo-*.md
rm -rf ~/.config/opencode/agents/geo-*.md ~/.config/opencode/commands/geo-*.md
```

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
