---
name: geo
description: >
  GEO-first SEO analysis tool. Optimizes websites for AI-powered search engines
  (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) while maintaining
  traditional SEO foundations. Performs full GEO audits, citability scoring,
  AI crawler analysis, llms.txt generation, brand mention scanning, platform-specific
  optimization, schema markup, technical SEO, content quality (E-E-A-T), and
  client-ready GEO report generation. Use when user says "geo", "seo", "audit",
  "AI search", "AI visibility", "optimize", "citability", "llms.txt", "schema",
  "brand mentions", "GEO report", or any URL for analysis. The fork extension
  also adds 4 closure-loop skills: "matrix" (intent angle planning),
  "pipeline" (5-stage AI citation pipeline), "distribute" (tiered multi-platform
  distribution), and "compete" (cross-engine competitor gap analysis).
  Supports region-specific audits: `--region cn` for China market analysis,
  or auto-detects region from URL and content.
---

# GEO-SEO Analysis Tool — Multi-AI Agent (February 2026)

> **Philosophy:** GEO-first, SEO-supported. AI search is eating traditional search.
> This tool optimizes for where traffic is going, not where it was.

---

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `/geo audit <url> [--region <code>]` | Full GEO + SEO audit with parallel subagents |
| `/geo page <url> [--region <code>]` | Deep single-page GEO analysis |
| `/geo citability <url> [--region <code>]` | Score content for AI citation readiness |
| `/geo crawlers <url> [--region <code>]` | Check AI crawler access (robots.txt analysis) |
| `/geo llmstxt <url> [--region <code>]` | Analyze or generate llms.txt file |
| `/geo brands <url> [--region <code>]` | Scan brand mentions across AI-cited platforms |
| `/geo platforms <url> [--region <code>]` | Platform-specific optimization (ChatGPT, Perplexity, Google AIO) |
| `/geo schema <url> [--region <code>]` | Detect, validate, and generate structured data |
| `/geo technical <url> [--region <code>]` | Traditional technical SEO audit |
| `/geo content <url> [--region <code>]` | Content quality and E-E-A-T assessment |
| `/geo report <url> [--region <code>]` | Generate client-ready GEO deliverable |
| `/geo report-pdf <url> [--region <code>]` | Generate professional PDF report with charts and scores |
| `/geo quick <url> [--region <code>]` | 60-second GEO visibility snapshot |
| `/geo prospect <cmd>` | CRM-lite: manage prospects through the sales pipeline |
| `/geo proposal <domain>` | Auto-generate client proposal from audit data |
| `/geo compare <domain>` | Monthly delta report: show score improvements to client |
| `/geo update` | Check/update this fork's skills via pinned `npx skills@1.9.0` (Claude Code + OpenCode) |
| `/geo matrix <core-topic> [--region <code>]` | (fork+) Build 4-quadrant intent matrix and 12-week schedule |
| `/geo pipeline <url> [--region <code>]` | (fork+) Run 5-stage AI citation pipeline + 6-engine preferred-answer verify |
| `/geo distribute <topic> [--region <code>]` | (fork+) Generate tiered 14-day multi-platform distribution plan |
| `/geo compete <domain> <c1,c2,...> [--region <code>]` | (fork+) Cross-engine competitor citation gap matrix |

---

## Script Path Resolution (Self-Locating)

<!-- GEO-SCRIPT-RESOLUTION:v1 -->

Helper scripts are located relative to the `SKILL.md` you are reading — never through a deploy-time rewritten absolute path. Set `SKILL_DIR` to the absolute directory containing that file, then probe these candidates **in order** and keep the first that contains `fetch_page.py`:

1. `"$SKILL_DIR/scripts"` — scripts shipped beside this SKILL.md (the `geo` skill itself).
2. `"$SKILL_DIR/../geo/scripts"` — npx-installed sibling `geo` skill, e.g. `.agents/skills/geo-<name>/` → `.agents/skills/geo/`; also covers the `.claude/skills/geo/` symlink view.
3. `"$SKILL_DIR/../../geo/scripts"` — source tree, e.g. `skills/geo-<name>/` → repo-root `geo/`.
4. `"$SKILL_DIR/../../../.claude/skills/geo/scripts"` — canonical Claude Code symlink path reached from an `.agents/skills/...` install.

Use this preamble before any script invocation in an installed skill:

```bash
SKILL_DIR="$(cd "$(dirname "<PATH-TO-THIS-SKILL.md>")" && pwd)"
GEO_SCRIPTS=""
for candidate in \
  "$SKILL_DIR/scripts" \
  "$SKILL_DIR/../geo/scripts" \
  "$SKILL_DIR/../../geo/scripts" \
  "$SKILL_DIR/../../../.claude/skills/geo/scripts"; do
  [ -f "$candidate/fetch_page.py" ] || continue
  GEO_SCRIPTS="$(cd "$candidate" && pwd)"
  break
done
: "${GEO_SCRIPTS:?GEO scripts root not found — verify the ordered fallback list}"
PY="$(command -v python3 || command -v python)"
```

Replace `<PATH-TO-THIS-SKILL.md>` with the path of the SKILL.md you are reading, then invoke scripts as `"$PY" "$GEO_SCRIPTS/<script>.py" ...`.

**Windows / Git Bash:** both installers require Git Bash, which supplies `cd`, `dirname`, `command -v`, forward-slash paths, and `python3`/`python` on PATH; all four candidates and the preamble therefore work unchanged on Windows. Native PowerShell/CMD is explicitly out of scope because Git Bash is the documented Windows installer entry point. The reference implementation of this probe is `resolve_scripts.py` beside this file (in `geo/`); invoke it with the resolved `PY` interpreter and a skill directory to print the root.

---

## Region Support

The tool supports region-specific analysis to account for different AI search
ecosystems, platforms, and user behaviors across markets. Currently implemented:

| Region | Code | AI Engines | Key Platforms | Profiles |
|--------|------|------------|---------------|----------|
| Global | `global` | ChatGPT, Claude, Perplexity, Gemini, Copilot | YouTube, Reddit, Wikipedia, LinkedIn | Default |
| China | `cn` | Baidu AI, Doubao, Yuanbao, Qwen, Kimi, DeepSeek | Baidu Baike, Zhihu, WeChat OA, Xiaohongshu, Bilibili, Douyin | `regions/profiles.yaml` |

<!-- GEO-CN-VARIANT:v1 -->

### CN variant loading (conditional)

The registered `regions/` knowledge base is mirrored under this skill as
`regions/profiles.yaml`, `regions/cn/*.md` and `regions/cn-variants.json` so an
`npx skills@1.9.0` recursive copy ships it (a bare repo-root `regions/` dir has
no `SKILL.md` and is NOT installed). `cn-variants.json` is the manifest: it
enumerates all 17 `SKILL.cn.md` variants and every CN knowledge file.

Resolve these files from the SKILL.md being read — never from a hardcoded path.
Anchor `SKILL_DIR` as in [Script Path Resolution](#script-path-resolution-self-locating), then use `<PY> <GEO_SCRIPTS>/../resolve_regions.py "$SKILL_DIR"` (candidate roots:
`"$SKILL_DIR/regions"`, `"$SKILL_DIR/../geo/regions"`, `"$SKILL_DIR/../../regions"`,
`"$SKILL_DIR/../../../.claude/skills/geo/regions"`; it prints the first existing
root and fails closed otherwise). The same ordered probe is implemented in
`geo/scripts/region_resolver.py`, which is dependency-free and can be executed
from the installed skill:

```bash
<PY> "$GEO_SCRIPTS/region_resolver.py" detect <url>       # cn / global / multi
<PY> "$GEO_SCRIPTS/region_resolver.py" profile cn         # CN profile (BaiduSpider, baidu_baike)
<PY> "$GEO_SCRIPTS/region_resolver.py" guidance cn        # CN-only files to load
<PY> "$GEO_SCRIPTS/region_resolver.py" guidance global    # empty: no CN guidance
```

**Gate:** when `REGION` is `cn`, load the sibling `SKILL.cn.md` for the command
being run plus the `regions/cn/` files and the profile. When `REGION` is
`global` or any non-CN value, do NOT load `SKILL.cn.md` or any `regions/cn/`
file — CN content is never folded inline into a primary `SKILL.md`.

### How region is determined

1. **Explicit**: `--region cn` on any command
2. **TLD-based**: `.cn`, `.com.cn` → China; `.kr` → Korea (if implemented)
3. **Content-based**: HTML `lang` attribute + CJK/Cyrillic script detection → region
4. **Multi-language prompt**: If `.com` site has 3+ languages, **ask user**

### Adding a new region

See `regions/README.md` (mirrored at `regions/README.md` under this skill) for the complete guide. Steps:
1. Add profile to `regions/profiles.yaml` (update both the repo-root copy and this skill's mirror)
2. Create `regions/<code>/` with optional reference data files (mirror them here for npx installs)
3. Create optional `SKILL.<code>.md` overrides for skill files; add each to `regions/cn-variants.json` when it is a CN variant
4. Update all 5 audit-worker SKILL.md files with Region Awareness sections
5. Update fork skills that accept `--region`

---

## Market Context (Why GEO Matters)

| Metric | Value | Source |
|--------|-------|--------|
| GEO services market (2025) | $850M-$886M | Yahoo Finance / Superlines |
| Projected GEO market (2031) | $7.3B (34% CAGR) | Industry analysts |
| AI-referred sessions growth | +527% (Jan-May 2025) | SparkToro |
| AI traffic conversion vs organic | 4.4x higher | Industry data |
| Google AI Overviews reach | 1.5B users/month, 200+ countries | Google |
| ChatGPT weekly active users | 900M+ | OpenAI |
| Perplexity monthly queries | 500M+ | Perplexity |
| Gartner: search traffic drop by 2028 | -50% | Gartner |
| Marketers investing in GEO | Only 23% | Industry surveys |
| Brand mentions vs backlinks for AI | 3x stronger correlation | Ahrefs (Dec 2025) |

---

## Orchestration Logic

### Full Audit (`/geo audit <url> [--region <code>]`)

All audit commands accept an optional `--region` flag (e.g. `--region cn`).
If omitted, the tool auto-detects the region from the URL and page content.
See [Region Support](#region-support) below.

**Phase 0: Region Detection (Sequential)**
1. Check URL for country TLD (`.cn`, `.com.cn`, `.kr`, etc.)
2. Fetch homepage and check `<html lang="...">` attributes
3. Scan content for dominant language scripts (CJK, Cyrillic, Latin)
4. Resolution: if multi-language detected (e.g. `.com` with 3+ languages), **ask user**:
   - "1. Global — treat as global English"
   - "2. Global+CN — run both Global and China assessments"
   - "3. CN only — China market only"
5. Set REGION variable (default: `global`)
6. Load region profile from `regions/profiles.yaml` — provides region-specific scoring weights, AI engines, platforms, schema defaults, and crawler expectations

**Phase 1: Discovery (Sequential)**
1. Fetch homepage HTML (curl or `fetch_url`)
2. Detect business type (SaaS, Local, E-commerce, Publisher, Agency, Other)
3. Extract key pages from sitemap.xml or internal links (up to 50 pages)

**Phase 2: Parallel Analysis (5 skill-backed workers, dispatched in parallel)**

Invoke the 5 migrated audit-worker skills **in parallel** using the host's task/subagent
mechanism. Load each worker's `SKILL.md` into its own task context so the full agent
instruction body (Region Awareness, Execution Steps, Output Format) is available to
that worker. Do NOT run them sequentially in the main conversation: a bare skill
invocation runs in main context, so true 5-way parallelism requires a parallel
task/subagent dispatch. From an npx install the same files resolve under the
host's skills directory; the former agent definition files are not installed by npx.

| Audit worker skill | Load this instruction file | Responsibility |
|--------------------|----------------------------|----------------|
| geo-ai-visibility | `skills/geo-ai-visibility/SKILL.md` | GEO audit, citability, AI crawlers, llms.txt, brand mentions |
| geo-platform-analysis | `skills/geo-platform-analysis/SKILL.md` | Platform-specific optimization (ChatGPT, Perplexity, Google AIO) |
| geo-technical | `skills/geo-technical/SKILL.md` | Technical SEO, Core Web Vitals, crawlability, indexability |
| geo-content | `skills/geo-content/SKILL.md` | Content quality, E-E-A-T, readability, AI content detection |
| geo-schema | `skills/geo-schema/SKILL.md` | Schema markup detection, validation, generation |

**Phase 3: Synthesis (Sequential)**
1. Collect all subagent reports (region-aware: subagents received REGION in task description)
2. Calculate composite GEO Score (0-100) using region-specific weights
3. Generate prioritized action plan with region-specific recommendations
4. Output client-ready report (region-tagged filename, e.g. `GEO-AUDIT-REPORT-CN.md`)

### Scoring Methodology (Region-Aware)

Weights vary by region. Loaded from `regions/profiles.yaml`.

| Category | Global Weight | CN Weight | Measured By |
|----------|--------------|-----------|-------------|
| AI Citability & Visibility | 25% | 20% | Passage scoring, answer block quality, AI crawler access |
| Brand Authority Signals | 20% | **30%** | Brand mentions across region-relevant platforms |
| Content Quality & E-E-A-T | 20% | 15% | Expertise signals, original data, author credentials |
| Technical Foundations | 15% | 10% | SSR, Core Web Vitals, crawlability, mobile, security |
| Structured Data | 10% | **15%** | Schema completeness, JSON-LD validation, Baidu extensions |
| Platform Optimization | 10% | 10% | Region-specific AI platform readiness (ChatGPT/Baidu AI) |

Non-global regions fall back to Global weights if their profile omits a weight.

When running with `--region cn`, all scoring rubrics should reference the
CN-specific AI engines (`regions/cn/ai-engines.md`), platforms (`regions/cn/platforms.md`),
and schema guidance (`regions/cn/schema.md`).

---

## Business Type Detection

Analyze homepage for patterns:

| Type | Signals |
|------|---------|
| **SaaS** | Pricing page, "Sign up", "Free trial", "/app", "/dashboard", API docs |
| **Local Service** | Phone number, address, "Near me", Google Maps embed, service area |
| **E-commerce** | Product pages, cart, "Add to cart", price elements, product schema |
| **Publisher** | Blog, articles, bylines, publication dates, article schema |
| **Agency** | Portfolio, case studies, "Our services", client logos, testimonials |
| **Other** | Default — apply general GEO best practices |

Adjust recommendations based on detected type. Local businesses need LocalBusiness schema and Google Business Profile optimization. SaaS needs SoftwareApplication schema and comparison page strategy. E-commerce needs Product schema and review aggregation.

---

## Sub-Skills (19 Specialized Components)

| # | Skill | Directory | Purpose |
|---|-------|-----------|---------|
| 1 | geo-audit | `skills/geo-audit/` | Full audit orchestration and scoring |
| 2 | geo-citability | `skills/geo-citability/` | Passage-level AI citation readiness |
| 3 | geo-crawlers | `skills/geo-crawlers/` | AI crawler access and robots.txt |
| 4 | geo-llmstxt | `skills/geo-llmstxt/` | llms.txt standard analysis and generation |
| 5 | geo-brand-mentions | `skills/geo-brand-mentions/` | Brand presence on AI-cited platforms |
| 6 | geo-platform-optimizer | `skills/geo-platform-optimizer/` | Platform-specific AI search optimization |
| 7 | geo-schema | `skills/geo-schema/` | Structured data for AI discoverability |
| 8 | geo-technical | `skills/geo-technical/` | Technical SEO foundations |
| 9 | geo-content | `skills/geo-content/` | Content quality and E-E-A-T |
| 10 | geo-report | `skills/geo-report/` | Client-ready deliverable generation |
| 11 | geo-report-pdf | `skills/geo-report-pdf/` | Professional PDF report with charts |
| 12 | geo-prospect | `skills/geo-prospect/` | CRM-lite prospect and client pipeline management |
| 13 | geo-proposal | `skills/geo-proposal/` | Auto-generate client proposals from audit data |
| 14 | geo-compare | `skills/geo-compare/` | Monthly delta tracking and progress reports |
| 15 | geo-update | `skills/geo-update/` | Check/update pinned npx skills from this fork |
| 16 | geo-intent-matrix | `skills/geo-intent-matrix/` | (fork+) 4-quadrant intent angle matrix + 12-week schedule |
| 17 | geo-citation-pipeline | `skills/geo-citation-pipeline/` | (fork+) 5-stage AI citation pipeline + 6-engine preferred-answer verify |
| 18 | geo-distribution-plan | `skills/geo-distribution-plan/` | (fork+) Tier 1/2/3 platform distribution plan with 14-day cadence |
| 19 | geo-competitor-citation | `skills/geo-competitor-citation/` | (fork+) Cross-engine competitor citation gap matrix |

---

## Subagents (5 Parallel Workers)

Each of the 5 audit workers is now a SKILL.md-bearing skill. The phase-2 orchestrator
dispatches all 5 in parallel via the host's task/subagent mechanism and loads each
worker's SKILL.md into its own context. Every worker receives the REGION variable
appended to its task description. Each worker SKILL.md retains its "Region Awareness"
section, which adjusts its scoring rubrics based on the target region (e.g. CN uses
Baidu AI instead of ChatGPT, Baidu Baike instead of Wikipedia, etc.).

| Audit worker skill | Instruction file | Skills Used |
|--------------------|-------------------|-------------|
| geo-ai-visibility | `skills/geo-ai-visibility/SKILL.md` | geo-citability, geo-crawlers, geo-llmstxt, geo-brand-mentions |
| geo-platform-analysis | `skills/geo-platform-analysis/SKILL.md` | geo-platform-optimizer |
| geo-technical | `skills/geo-technical/SKILL.md` | geo-technical |
| geo-content | `skills/geo-content/SKILL.md` | geo-content |
| geo-schema | `skills/geo-schema/SKILL.md` | geo-schema |

---

## Output Files

All commands generate structured output. When a region is specified (or auto-detected
as non-global), a `-<REGION>` suffix is appended to output filenames. For example:
`/geo audit example.com --region cn` produces `GEO-AUDIT-REPORT-CN.md`.

| Command | Global Output File | Region Output File |
|---------|-------------------|-------------------|
| `/geo audit` | `GEO-AUDIT-REPORT.md` | `GEO-AUDIT-REPORT-{REGION}.md` |
| `/geo page` | `GEO-PAGE-ANALYSIS.md` | `GEO-PAGE-ANALYSIS-{REGION}.md` |
| `/geo citability` | `GEO-CITABILITY-SCORE.md` | `GEO-CITABILITY-SCORE-{REGION}.md` |
| `/geo crawlers` | `GEO-CRAWLER-ACCESS.md` | `GEO-CRAWLER-ACCESS-{REGION}.md` |
| `/geo llmstxt` | `llms.txt` | `llms-{REGION}.txt` |
| `/geo brands` | `GEO-BRAND-MENTIONS.md` | `GEO-BRAND-MENTIONS-{REGION}.md` |
| `/geo platforms` | `GEO-PLATFORM-OPTIMIZATION.md` | `GEO-PLATFORM-OPTIMIZATION-{REGION}.md` |
| `/geo schema` | `GEO-SCHEMA-REPORT.md` | `GEO-SCHEMA-REPORT-{REGION}.md` |
| `/geo technical` | `GEO-TECHNICAL-AUDIT.md` | `GEO-TECHNICAL-AUDIT-{REGION}.md` |
| `/geo content` | `GEO-CONTENT-ANALYSIS.md` | `GEO-CONTENT-ANALYSIS-{REGION}.md` |
| `/geo report` | `GEO-CLIENT-REPORT.md` | `GEO-CLIENT-REPORT-{REGION}.md` |
| `/geo report-pdf` | `GEO-REPORT.pdf` | `GEO-REPORT-{REGION}.pdf` |
| `/geo quick` | Inline summary (no file) | Inline (region noted) |
| `/geo prospect` | Updates `~/.geo-prospects/prospects.json` | Same (prospect has region field) |
| `/geo proposal` | `~/.geo-prospects/proposals/<domain>-proposal-<date>.md` | Same (region noted in proposal) |
| `/geo compare` | `~/.geo-prospects/reports/<domain>-monthly-<YYYY-MM>.md` | Same (region noted in report) |
| `/geo matrix` | `~/.geo-prospects/matrices/<domain>-<topic>-<YYYY-MM-DD>.md` | `...-{REGION}.md` |
| `/geo pipeline` | `~/.geo-prospects/pipelines/<domain>-<slug>-<YYYY-MM-DD>.md` | `...-{REGION}.md` |
| `/geo distribute` | `~/.geo-prospects/distribution/<domain>-<topic-slug>-<YYYY-MM-DD>.md` | `...-{REGION}.md` |
| `/geo compete` | `~/.geo-prospects/competitor/<my-domain>-<YYYY-MM-DD>.md` | `...-{REGION}.md` |

---

## PDF Report Generation

The `/geo report-pdf <url>` command generates a professional, branded PDF report:

### How It Works
1. Run the full audit or individual analyses first
2. Collect all scores and findings into a JSON structure
3. Execute the PDF generator: `"$PY" "$GEO_SCRIPTS/generate_pdf_report.py" data.json GEO-REPORT.pdf`

### What the PDF Includes
- **Cover page** with GEO score gauge visualization
- **Score breakdown** with color-coded bar charts
- **AI Platform Readiness** dashboard with horizontal bar chart
- **Crawler Access** status table with color-coded Allow/Block
- **Key Findings** categorized by severity (Critical/High/Medium/Low)
- **Prioritized Action Plan** (Quick Wins, Medium-Term, Strategic)
- **Methodology & Glossary** appendix

### Workflow
1. First run `/geo audit <url>` to collect all data
2. Then run `/geo report-pdf <url>` to generate the PDF
3. The tool will compile audit data into JSON, then generate the PDF
4. Output: `GEO-REPORT.pdf` in the current directory

---

## Quality Gates

- **Crawl limit:** Max 50 pages per audit (focus on quality over quantity)
- **Timeout:** 30 seconds per page fetch
- **Rate limiting:** 1-second delay between requests, max 5 concurrent
- **Robots.txt:** Always respect, always check
- **Duplicate detection:** Skip pages with >80% content similarity

---

## Fork Extension: The GEO 4-Step Closure Loop

The fork adds 4 skills that wire the existing audit/optimization skills into a
closed 4-step GEO workflow. The loop runs:

```
   Step 1: Angles                Step 2: Publish                Step 3: Guide                  Step 4: Measure
   ┌─────────────────────┐  ┌──────────────────────────┐  ┌───────────────────────────┐  ┌──────────────────────────┐
   │ geo-intent-matrix   │→ │ geo-content (existing) + │→ │ geo-citation-pipeline +   │→ │ geo-competitor-citation  │
   │ 4-quadrant intent   │  │ geo-distribution-plan    │  │ geo-platform-optimizer,   │  │ → feeds back into matrix │
   │ + 12-week schedule  │  │ (14-day cadence)         │  │ geo-schema, geo-llmstxt   │  │ for next-quarter angles  │
   └─────────────────────┘  └──────────────────────────┘  └───────────────────────────┘  └──────────────────────────┘
```

**Typical fork-extension run:**

```
# Step 1: Plan the topic
/geo matrix "vector databases"

# Step 2: For each P0 piece from the matrix — produce content (existing skill)
/geo content https://mysite.com/blog/vector-databases-overview

# Step 3: Run the citation pipeline before distribution
/geo pipeline https://mysite.com/blog/vector-databases-overview

# Step 4: Distribute (only if pipeline returns PIPELINE_READY)
/geo distribute "vector databases"

# Step 5: 14 days later — verify preferred-answer pickup
/geo pipeline https://mysite.com/blog/vector-databases-overview --verify

# Step 6: 30 days later — measure against competitors
/geo compete mysite.com pinecone.io,weaviate.io,qdrant.io
```

The 4 fork skills share data via `~/.geo-prospects/` (matrices/, pipelines/,
distribution/, competitor/). See each skill's SKILL.md for full I/O contracts.

---

## Quick Start Examples

```
# Full GEO audit of a website (global)
/geo audit https://example.com

# China market audit (explicit region)
/geo audit https://example.cn --region cn

# Check AI bot access (auto-detects region from URL)
/geo crawlers https://shop.example.cn

# Score citability with China-specific AI engines
/geo citability https://example.com/blog/ai-trends --region cn

# Generate region-tagged output
/geo brands https://example-cn.com --region cn
# → GEO-BRAND-MENTIONS-CN.md

# Get a 60-second visibility snapshot
/geo quick https://example.com

# Generate a client-ready report
/geo report https://example.com
```
