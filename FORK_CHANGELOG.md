# Fork Changelog — geo-seo-claude-plus

> **HISTORICAL RECORD.** Entries below describe the tree at the time each change landed. Paths such as `SKILL.cn.md`, `agents/`, `geo/commands/`, and the old installers reflect that history; the current layout is the single `skills/` root documented in the root README and `AGENTS.md`. Do not use this changelog as an install or layout reference.

Downstream changes to [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude).

The upstream LICENSE and all existing skill / agent / script files are **unmodified**. This changelog records only fork-specific additions.

---

## 2026-11-19 — CN knowledge expansion (region-aware GEO CN)

**Scope:** Documentation-only expansion of the China-market knowledge base. No upstream rebase or merge; no scoring weights, commands, Python dependencies, or ML code added.

### Added — themed CN knowledge docs

Eight new reference docs under `regions/cn/`. Every external figure is attributed to a source article ID and marked `UNVERIFIED`; none is promoted to a toolkit scoring parameter.

| Doc | Role |
| --- | --- |
| `regions/cn/provenance.md` | Claim-to-source ledger (45 rows, all `UNVERIFIED`) plus a 28-source index across six themes |
| `regions/cn/source-tiering.md` | One canonical source-authority model: four tiers `CN-T1` through `CN-T4` plus two cross-cutting gates |
| `regions/cn/cross-validation.md` | Five multi-source corroboration rules R1 through R5, attributed and `UNVERIFIED` |
| `regions/cn/platform-behavior.md` | Per-engine sourcing plus a separate content-composition % layer |
| `regions/cn/engineering-playbooks.md` | 三区分治 governance, a 6-step question-knowledge-base, and query-frame mapping |
| `regions/cn/compliance-anti-abuse.md` | Black-hat red lines, recorded as prohibitions only |
| `regions/cn/kpi-and-method.md` | Part A reported-only supplementary CN KPIs; Part B a documentation-only method note (no ML port) |
| `regions/cn/README.md` | Navigation index for the CN knowledge docs |

### Modified — reconciliation, wiring, and outputs

- `regions/cn/ai-engines.md`: per-engine referral-platform lists reconciled with attributed `UNVERIFIED` alternatives for Doubao and DeepSeek, and CN algorithm rules woven into the engine rubrics (single-source cap, at least three independent subjects, official-press penalty, stale-content multiplier), all `UNVERIFIED`.
- `skills/geo-content/SKILL.cn.md`: canonical source tiering folded into the DSS "Authoritative Source" check by pointer, not by duplication.
- `regions/profiles.yaml`: factual engine-id fix, `ernie` renamed to `yuanbao` in the CN `ai_engines` list.
- Seven CN skill overrides (plus a new `skills/geo-compare/SKILL.cn.md`) and the Region Awareness CN blocks in five agents were wired to the new docs by reference.
- `skills/geo-audit/SKILL.md`: a CN-gated pointer surfaces supplementary CN KPIs in audit and report output; global audits are unchanged.
- `openspec/changes/extend-region-aware-geo-cn/`: new change entry with proposal, design, and tasks.

### Reason

The 2026-05-28 CN support added region profiles and three base reference docs but left the CN knowledge layer thin. This change gives auditors a provenance-first, attributed body of CN material covering source trust, cross-validation, per-engine behavior, engineering playbooks, compliance, and supplementary KPIs, and reconciles the earlier engine and tiering material against it.

### Metric-layer rule and guardrails

The 源易 overall-usage tables stay authoritative and byte-identical. Per-agent content-composition percentages are a separate, `UNVERIFIED` layer; competing attributed claims are never merged, and DeepSeek's 抖音 source is recorded as absent (0 citations). All new figures are attributed and `UNVERIFIED`. No global or CN scoring weights changed, and no new scoring dimension or weight key was added. Black-hat terms appear only as prohibitions in `compliance-anti-abuse.md`. The method track is documentation only, with no ML port.

---

## 2026-05-16 — Fork inception

**Forked from upstream commit:** `5d8c0afe3b44bf9123f6849e97541f85eefabaca` ("Feature/isolated python venv linux/mac" — PR #48)
**Fork repo:** `stanleydansu/geo-seo-claude-plus`
**Fork maintainer:** Dan Su

### Added — 4 closure-loop skills

The fork adds four new skills that wire the existing audit/optimization skills into a closed 4-step GEO workflow (angles → publish → guide → measure):

| Skill | Path | Command | Closure-loop role |
| --- | --- | --- | --- |
| `geo-intent-matrix` | `skills/geo-intent-matrix/SKILL.md` | `/geo matrix <core-topic>` | Step 1 — Angles. 4-quadrant intent taxonomy + 12-week rolling schedule. Emits the intent-trigger vocabulary and form-binding contract consumed by the other three new skills. |
| `geo-citation-pipeline` | `skills/geo-citation-pipeline/SKILL.md` | `/geo pipeline <url>` | Step 3 — Guide. 5-stage pipeline (crawlers / internal-link wiring / AI-training authority backlinks / on-page compliance / rapid indexing) + Stage 6 cross-engine preferred-answer snapshot. Inherits from `geo-crawlers`, `geo-citability`, `geo-schema`, `geo-llmstxt`. |
| `geo-distribution-plan` | `skills/geo-distribution-plan/SKILL.md` | `/geo distribute <topic>` | Step 2 — Publish. Tier 1/2/3 platform scoring matrix, AI-training-corpus coverage tags, 14-day cadence, per-platform rewrite briefs (Zhihu / WeChat / Xiaohongshu / CSDN / Juejin / LinkedIn / Medium / Substack / Reddit / Hacker News / X / vertical media), 7/14/30-day reclaim checklist. Gated by `geo-citation-pipeline` returning PIPELINE_READY. |
| `geo-competitor-citation` | `skills/geo-competitor-citation/SKILL.md` | `/geo compete <my-domain> <c1,c2,...>` | Step 4 — Measure. 20 probes × 6 engines × 3 runs = 360-probe sweep. Produces 3-D gap matrix (brand × engine × intent) with verdict per quadrant and top-3 remediation plan. Reuses the intent taxonomy from `geo-intent-matrix`. |

### Modified — orchestrator routing

- `geo/SKILL.md`
  - Frontmatter `description` extended to mention the 4 new commands.
  - **Quick Reference table** — appended 4 new rows for `/geo matrix`, `/geo pipeline`, `/geo distribute`, `/geo compete`.
  - **Sub-Skills table** — renumbered title from "14 Specialized Components" to "19 Specialized Components"; added row 11 (`geo-report-pdf`, previously missing from the table) plus rows 16–19 for the 4 new skills.
  - **Output Files table** — appended 4 new rows mapping each new command to its output path under `~/.geo-prospects/`.
  - **Added section: Fork Extension: The GEO 4-Step Closure Loop** — ASCII diagram of the loop + a typical 6-step end-to-end example invocation.

### Added — attribution files

- `README.md`
  - Added top-section `## About This Fork` block (immediately after the banner, before the upstream content) describing the 4 new skills and linking to LICENSE / NOTICE / FORK_CHANGELOG.md.
  - Upstream `Quick Start`, `Commands`, `Architecture`, `Scoring Methodology`, and all other sections are unchanged.
- `NOTICE` — new file recording upstream copyright and license.
- `FORK_CHANGELOG.md` — this file.

### Unchanged (deliberately preserved)

- `LICENSE` — verbatim MIT, copyright Zubair Trabzada 2026.
- `install.sh` / `install-win.sh` / `uninstall.sh` — core install flow untouched. The fork does not add any new Python dependencies (all 4 new skills use the existing `requests`/`bs4`/WebFetch toolset).
- `requirements.txt` — unchanged.
- All existing `skills/geo-*/SKILL.md` files — unchanged.
- All `agents/geo-*.md` files — unchanged.
- All `scripts/*.py` files — unchanged.
- All `schema/*.json` files — unchanged.
- All `docs/`, `examples/`, `tests/` files — unchanged.
- `geo-update` skill — rewritten for the npx-first flow. Updates come from this fork (`D0wn10ad/geo-seo-ai-agent`) via pinned `npx skills@1.9.0 check` / `npx skills@1.9.0 update`; there is no `git pull upstream` step and no legacy updater script. The former upstream name is retained only as provenance in `README.md` and `NOTICE`.

### Runtime data layout (new directories under `~/.geo-prospects/`)

The new skills follow the upstream convention of writing runtime artifacts under `~/.geo-prospects/` (alongside `audits/`, `proposals/`, `reports/`):

```
~/.geo-prospects/
├── matrices/          # geo-intent-matrix output
├── pipelines/         # geo-citation-pipeline output
├── distribution/      # geo-distribution-plan output
├── competitor/        # geo-competitor-citation output
│   └── _runs/         # raw per-probe captures for reanalysis
└── (upstream dirs: audits/, proposals/, reports/, prospects.json)
```

These directories are created on first use by their respective skills. They are not removed by `uninstall.sh` (matching the upstream behavior for `~/.geo-prospects/`).

---

## 2026-05-28 — Region-aware GEO audits (CN support)

**Merged from fork branch:** `cb3f9c0` (PR #4), including base feature commit `d99a0f0` and CN canon alignment `e661ad8`

### Added — region profile system and CN reference data

- `regions/profiles.yaml` plus `regions/README.md` establish a data-driven region layer for weights, engines, platforms, crawlers, schema defaults, and technical checks.
- `regions/cn/ai-engines.md`, `regions/cn/platforms.md`, and `regions/cn/schema.md` add China-market reference material for engine evaluation, brand presence, and structured data guidance.
- `scripts/region_resolver.py` adds TLD/content-based region detection and profile loading.
- `skills/geo-*/SKILL.cn.md` overrides were added for region-specific command behavior in CN audits.

### Modified — orchestrator, agents, outputs, and CRM

- `geo/SKILL.md` now accepts `--region <code>`, runs a Phase 0 region-detection step, and applies region-specific scoring weights.
- `agents/geo-{ai-visibility,platform-analysis,technical,content,schema}.md` now include Region Awareness sections for CN-specific engines, platforms, technical checks, and schema guidance.
- Fork workflow skills (`geo-intent-matrix`, `geo-distribution-plan`, `geo-citation-pipeline`, `geo-competitor-citation`) gained region-aware behavior so CN audits use the right engines, platforms, and output naming.
- Output and client tooling were updated for region-tagged artifacts, including `scripts/generate_pdf_report.py`, `scripts/crm_dashboard.py`, the CRM web UI, `skills/geo-report/SKILL.md`, `skills/geo-proposal/SKILL.md`, and `skills/geo-compare/SKILL.md`.

### Reason

The upstream toolkit was effectively global/Western-only. This fork change makes the GEO workflow usable for China-market audits by replacing hardcoded global assumptions with explicit region profiles, CN-specific references, and region-aware scoring/output behavior.

## Future changes

Append new entries here in reverse-chronological order. Each entry should include:

- Date
- Upstream commit hash if a rebase / merge from upstream occurred
- Files added / modified / removed
- Reason
