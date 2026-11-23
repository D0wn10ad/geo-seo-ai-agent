# Architecture & Design

The repository is structured to provide GEO+SEO support across both **Claude Code**
and **OpenCode**. Skills are distributed by the pinned `npx skills@1.9.0`
CLI; the committed tree is the source of truth and nothing is generated or
rewritten at install time. npx distributes skills only — it does not install
command files.

```
geo-seo-ai-agent/
├── skills/                       # single skills root: 21 geo-* skills + vendored uv
│   ├── geo/                      # orchestrator + nested utilities and region KB
│   │   ├── SKILL.md              # /geo command table and routing
│   │   ├── scripts/              # Python utilities (travel nested with the skill)
│   │   │   ├── fetch_page.py     # Page fetching & parsing
│   │   │   ├── citability_scorer.py  # AI citability scoring engine
│   │   │   ├── brand_scanner.py  # Brand mention detection
│   │   │   ├── llmstxt_generator.py  # llms.txt validation & generation
│   │   │   ├── generate_pdf_report.py # PDF report generator (ReportLab)
│   │   │   ├── region_resolver.py
│   │   │   ├── crm_dashboard.py
│   │   │   ├── bootstrap_env.sh  # idempotent, checksum-keyed dep bootstrap
│   │   │   ├── install_uv.sh     # pinned uv 0.13.9 installer helper
│   │   │   └── requirements.txt  # Python dependencies
│   │   ├── assets/schema/        # 6 JSON-LD templates
│   │   └── references/regions/   # region profiles + CN knowledge base (cn/)
│   │       ├── profiles.yaml
│   │       ├── cn-variants.json
│   │       └── cn/
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
│   ├── geo-ai-visibility/        # Phase-2 AI visibility worker
│   ├── geo-platform-analysis/    # Phase-2 platform worker
│   ├── geo-intent-matrix/        # (fork+) 4-quadrant intent planning
│   ├── geo-citation-pipeline/    # (fork+) AI citation pipeline + verification
│   ├── geo-distribution-plan/    # (fork+) Multi-platform distribution
│   ├── geo-competitor-citation/  # (fork+) Cross-engine gap analysis
│   ├── geo-update/               # Pinned npx check/update policy
│   └── uv/                       # Vendored pinned uv installer skill
├── docs/                         # Full documentation
├── uninstall.sh                  # cleanup fallback for pre-npx installs
└── README.md                     # Main project view
```

### What npx installs

`npx skills@1.9.0 add -a claude-code -a opencode -y
https://github.com/D0wn10ad/geo-seo-ai-agent.git` discovers every directory that
contains a `SKILL.md` and copies that hierarchy verbatim into the target agents'
config dirs. The install root also receives `skills-lock.json`, which records the
pinned source and version used by `npx skills@1.9.0 check` and
`npx skills@1.9.0 update`.

The source of truth is entirely in the committed tree:

| Committed source | Role after install |
|---|---|
| `skills/geo/SKILL.md` | Orchestrator and `/geo` command table |
| `skills/geo-*/SKILL.md` (21 files) + vendored `skills/uv/SKILL.md` | Skill tree copied verbatim by npx; two `geo-*` files are internal phase-2 workers |
| `skills/geo/scripts/`, `skills/geo/assets/schema/`, `skills/geo/references/regions/` | Nested utilities, JSON-LD templates and region profiles; CN knowledge base in `skills/geo/references/regions/cn/` |
| `skills/<geo-x>/references/cn.md` (17 files) | CN companions for the region-aware skills |

There is no deploy-time rewriting, no generated `.opencode/` source, and no
copy-tree updater script. The `.opencode/` directory seen on some machines is a
local deploy artifact produced by the agent tooling, not committed source. npx
distributes skills only; it does not install command files. To change a skill,
edit its committed `skills/geo-*/SKILL.md` file.

**Other derived relationships:**

| Relationship | How linked |
|---|---|
| `skills/<geo-x>/references/cn.md` (region overrides) ↔ `skills/geo/references/regions/profiles.yaml` | CN companions are loaded when targeting that region; the orchestrator appends `--region <code>` |
| `docs/*.md` ↔ `skills/*/SKILL.md` | Docs describe usage patterns that must match orchestrator behavior; verify by diffing docs against the orchestrator's `/geo <command>` table |
| `skills/geo/references/regions/cn/ai-engines.md` → `skills/geo-platform-analysis/SKILL.md` | CN engine rubrics are referenced by the region-awareness logic in the worker skill |
| `skills/geo/references/regions/cn/schema.md` → `skills/geo-schema/SKILL.md` | CN-specific schema defaults and Baidu extensions are applied via conditional logic |
| `skills/geo/references/regions/cn/platforms.md` → `skills/geo-ai-visibility/SKILL.md` | CN brand platforms feed the region-aware brand scoring section |

### Python environment bootstrap

npx installs skills only. Python dependencies are bootstrapped separately with
`skills/geo/scripts/install_uv.sh` (pinned uv 0.13.9) and `skills/geo/scripts/bootstrap_env.sh`.
The bootstrap creates `${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent/venv`, installs
`requirements.txt` with `uv pip`, and writes a checksum sentinel so repeated runs
are no-ops until the requirements file changes. Python 3.10+ is required because the pinned `lxml` release requires 3.10+.

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

### Data Storage

The CRM and reporting skills (`/geo prospect`, `/geo proposal`, `/geo compare`)
store runtime data outside the installed skill directories:

```
~/.geo-prospects/
├── prospects.json              # Client/prospect pipeline data
├── proposals/                  # Generated proposal documents
│   └── <domain>-proposal-<date>.md
└── reports/                    # Monthly delta reports
    └── <domain>-monthly-<YYYY-MM>.md
```

This directory is never removed by an update or by `uninstall.sh` —
delete it manually if you no longer need your prospect data.
