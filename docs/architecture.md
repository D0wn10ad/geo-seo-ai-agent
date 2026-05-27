# Architecture & Design

The repository is structured to seamlessly provide GEO+SEO support across both **Claude Code** and **OpenCode** platforms. Abstract tool names (`` `fetch_url` ``, `` `run_command` ``) are used in instruction text, resolved at runtime by the platform adapter layer (`platform/SKILL.md`).

```
geo-seo-claude/
├── geo/                          # Main skill orchestrator
│   └── SKILL.md                  # Primary skill file with commands & routing
├── platform/                     # Platform adapter layer
│   ├── SKILL.md                  # Platform detection + abstract tool mapping
│   └── TOOL-MAP.md               # Abstract-to-real tool name reference table
├── regions/                      # Region profiles (feature branch)
│   ├── profiles.yaml             # Scoring weights, engines, platforms per region
│   ├── README.md                 # Guide for adding new regions
│   └── cn/                       # China market reference data
├── skills/                       # 20 specialized sub-skills
│   ├── geo-audit/                # Full audit orchestration & scoring
│   ├── geo-citability/           # AI citation readiness scoring
│   ├── geo-crawlers/             # AI crawler access analysis
│   ├── geo-llmstxt/              # llms.txt standard analysis & generation
│   ├── geo-brand-mentions/       # Brand presence on AI-cited platforms
│   ├── geo-platform-optimizer/   # Platform-specific AI search optimization
│   ├── geo-schema/               # Structured data for AI discoverability
│   ├── geo-technical/            # Technical SEO foundations
│   ├── geo-content/              # Content quality & E-E-A-T
│   ├── geo-report/               # Client-ready markdown report generation
│   ├── geo-report-pdf/           # Professional PDF report with charts
│   ├── geo-prospect/             # CRM-lite prospect pipeline management
│   ├── geo-proposal/             # Auto-generate client proposals
│   ├── geo-compare/              # Monthly delta tracking & progress reports
│   ├── geo-intent-matrix/        # (fork+) 4-quadrant intent planning
│   ├── geo-citation-pipeline/    # (fork+) AI citation pipeline + verification
│   ├── geo-distribution-plan/    # (fork+) Multi-platform distribution
│   └── geo-competitor-citation/  # (fork+) Cross-engine gap analysis
├── agents/                       # 5 parallel subagents (Claude Code)
│   ├── geo-ai-visibility.md
│   ├── geo-platform-analysis.md
│   ├── geo-technical.md
│   ├── geo-content.md
│   └── geo-schema.md
├── .opencode/                    # OpenCode-specific config
│   ├── agents/                   # 5 subagents (OpenCode permission format)
│   └── commands/                 # 21 command wrappers
├── scripts/                      # Python utilities
│   ├── fetch_page.py             # Page fetching & parsing
│   ├── citability_scorer.py      # AI citability scoring engine
│   ├── brand_scanner.py          # Brand mention detection
│   ├── llmstxt_generator.py      # llms.txt validation & generation
│   ├── generate_pdf_report.py    # PDF report generator (ReportLab)
│   └── update_toolkit.py         # Cross-platform installer/updater
├── schema/                       # JSON-LD templates
│   ├── organization.json         # Organization schema (with sameAs)
│   ├── local-business.json       # LocalBusiness schema
│   ├── article-author.json       # Article + Person schema (E-E-A-T)
│   ├── software-saas.json        # SoftwareApplication schema
│   ├── product-ecommerce.json    # Product schema with offers
│   └── website-searchaction.json # WebSite + SearchAction schema
├── install.sh                    # Legacy installer (Claude Code)
├── uninstall.sh                  # Legacy uninstaller
├── requirements.txt              # Python dependencies
└── README.md                     # Main project view
```

### Full Audit Flow

When you run `/geo audit https://example.com`:

1. **Discovery** — Fetches homepage, detects business type, crawls sitemap
2. **Parallel Analysis** — Launches 5 subagents simultaneously:
   - AI Visibility (citability, crawlers, llms.txt, brand mentions)
   - Platform Analysis (ChatGPT, Perplexity, Google AIO readiness)
   - Technical SEO (Core Web Vitals, SSR, security, mobile)
   - Content Quality (E-E-A-T, readability, freshness)
   - Schema Markup (detection, validation, generation)
3. **Synthesis** — Aggregates scores, generates composite GEO Score (0-100)
4. **Report** — Outputs prioritized action plan with quick wins

### Platform Adapter Layer

The `platform/` directory provides runtime platform detection and abstract tool name resolution. When a skill or agent uses `` `fetch_url` `` or `` `run_command` `` in its instruction text, the platform adapter maps these to the real tool names for the current platform:

| Abstract Name | Claude Code | OpenCode |
|---------------|-------------|----------|
| `` `fetch_url` `` | `WebFetch` | `webfetch` |
| `` `run_command` `` | `Bash` | `bash` |
| `` `read_file` `` | `Read` | `read` |
| `` `write_file` `` | `Write` | `write` |
| `` `search_files` `` | `Glob` | `glob` |
| `` `search_content` `` | `Grep` | `grep` |

The adapter is loaded first (via `AGENTS.md`), ensuring the tool mapping is available from session start.

### Generate, Don't Duplicate

Some platform-specific files in `.opencode/` are **generated at install time** by `scripts/update_toolkit.py`, never hand-edited:

| Derived File | Source of Truth | Generator |
|---|---|---|
| `.opencode/agents/geo-*.md` (5 files) | `agents/geo-*.md` — Claude Code agents are the single source | `generate_opencode_agents()` in `update_toolkit.py` |
| `.opencode/commands/geo-*.md` (21 files) | `_GEO_COMMANDS` dict in `update_toolkit.py` | `generate_opencode_commands()` in `update_toolkit.py` |
| `~/.claude/skills/geo/regions/` | `regions/` in repo | `copy_tree()` in `update_toolkit.py` |

**Why:** Prevents divergence. Previously, `.opencode/agents/*` and `agents/*` were manually maintained copies that drifted apart — the OpenCode copies lacked Region Awareness sections introduced in the `feature/region-aware-geo` branch. By generating at install time, OpenCode agents always reflect the same body content as Claude Code agents, with only the frontmatter differing.

**Rule:** If you need to change an OpenCode agent body, edit `agents/geo-<name>.md`. If you need to change an OpenCode command wrapper, edit the `_GEO_COMMANDS` dict in `scripts/update_toolkit.py`. Never edit `.opencode/` files directly.

**Other derived relationships:**

| Relationship | How Linked |
|---|---|
| `SKILL.cn.md` (skill overrides) ↔ `regions/profiles.yaml` | Files named `SKILL.<code>.md` alongside a `SKILL.md` are loaded when targeting that region; their `_GEO_COMMANDS`-generated command wrappers append `--region <code>` |
| `docs/*.md` ↔ `skills/*/SKILL.md` | Documentation files describe usage patterns that must match orchestrator behavior; verify by diffing docs against the orchestrator's `/geo <command>` table |
| `regions/cn/ai-engines.md` → `agents/geo-platform-analysis.md` | The CN engine rubrics are referenced by the region-awareness logic in the agent file; update both when adding a new engine |
| `regions/cn/schema.md` → `agents/geo-schema.md` | CN-specific schema defaults and Baidu extensions documented in region data, applied via conditional logic in the agent |
| `regions/cn/platforms.md` → `agents/geo-ai-visibility.md` | CN brand platforms listed in region data, referenced by the agent's region-awareness brand scoring section |

**Footnote:** `(†)` — These directories exist in the git repo only as build-time source snapshots for backward compatibility. `update_toolkit.py` generates the actual deployed files from the canonical sources listed above. The stale committed copies have been removed from git tracking.

### Data Storage

The CRM and reporting skills (`/geo prospect`, `/geo proposal`, `/geo compare`) store runtime data outside the Claude Code directory:

```
~/.geo-prospects/
├── prospects.json              # Client/prospect pipeline data
├── proposals/                  # Generated proposal documents
│   └── <domain>-proposal-<date>.md
└── reports/                    # Monthly delta reports
    └── <domain>-monthly-<YYYY-MM>.md
```

This directory is **not removed** by the uninstaller — delete it manually if you no longer need your prospect data.
