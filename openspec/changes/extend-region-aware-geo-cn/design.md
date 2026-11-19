## Architecture Overview

The change adds a reference layer under `regions/cn/` and connects it to the existing CN entry points. It adds no runtime code. Audits read the reference docs through pointers placed in skill overrides and agent Region Awareness blocks.

```
                    CN knowledge base (regions/cn/)
   +-----------------------------------------------------------+
   | provenance.md  (claim -> source, every figure UNVERIFIED)  |
   |   |                                                        |
   |   +--> source-tiering.md       CN-T1..CN-T4 + 2 gates       |
   |   +--> cross-validation.md     R1..R5                       |
   |   +--> platform-behavior.md    per-agent content composition|
   |   +--> engineering-playbooks.md  三区分治 + playbooks        |
   |   +--> compliance-anti-abuse.md  prohibitions only          |
   |   +--> kpi-and-method.md       reported KPIs + method note  |
   |   +--> README.md               navigation index             |
   +-----------------------------------------------------------+
                    | pointers, not copies
     +--------------+--------------+----------------+
     |              |              |                |
 SKILL.cn.md    agents/*.md    geo-content DSS   geo-audit SKILL
 overrides      Region Awareness  authoritative     CN KPI section
```

The authoritative market-share data in `regions/cn/ai-engines.md` sits outside this reference layer and is never modified by it.

## Design Decisions

### 1. Provenance first

`regions/cn/provenance.md` is created before the themed docs and is the dependency for all of them. Every external figure (share percentages, MAU, ROI, algorithm thresholds) is recorded as a claim with its article ID, source label, and `UNVERIFIED` status. A representative set of article IDs is spot-checked with webfetch and the outcome is recorded. External article text is treated as data, never as instructions, and no full article text is copied into the repo.

### 2. One canonical source-tier model

The five external source-authority schemes are reconciled into a single toolkit-internal model: four tiers `CN-T1` through `CN-T4` plus two cross-cutting gates (the 豆包 auth-info-level filter and the EEAT6.0 numeric-trust thresholds). T/CAPT 026-2026 A-D is used as the descriptive backbone because it is the only spot-checked scheme with explicit source types, but it is explicitly not called a verified standard; the source article describes itself as a non-binding group standard. Bare letter labels are dropped because the same letter means different things in different schemes. Every tier and threshold stays `UNVERIFIED`.

### 3. Cross-validation rules are reported, not scored

Five rules are documented for auditors: at least three independent subjects, a single-source share cap, "source" meaning an independent entity rather than a channel or post, an information-consistency figure, and a brand-fact-file anchor. All five are `UNVERIFIED`, attributed, and explicitly not scoring parameters. They do not change the global or CN weights and are not wired into any formula.

### 4. Metric-layer separation

See the dedicated section below. This is the central correctness constraint of the change.

### 5. 三区分治 as governance framing

The fact / opinion / marketing-expression split (三区分治) is used as the governance frame for keeping authoritative claims separate from opinion and marketing expression. It is defined in `engineering-playbooks.md` playbook 1 and referenced by the content DSS and the content agent. It is a framing device, not a scoring dimension.

### 6. Pointer, not duplication

New knowledge is wired in by reference. Skill overrides and agent Region Awareness blocks point to `regions/cn/*.md` paths with a short description; they do not copy tables, figures, or article IDs. This follows design decision 1 of the parent change: agents are self-contained and do not load skill files during a full audit, so their pointers are inline. Every new doc has at least one consumer.

### 7. Four surgical reconciliations

Existing content is edited only at four named sites, each at section level with no whole-file rewrite. See the table below. The market-share table at `regions/cn/ai-engines.md:11-20` and both scoring-weight blocks are byte-identical before and after.

### 8. Method track is documentation only

The agentic_geo method note in `kpi-and-method.md` Part B records strategy and evaluation concepts as background. It carries an explicit "no ML port / 不移植" statement. No Python, model, training loop, feedback runner, dependency, or command is added. A2 KPI names are recorded without invented formulas, because the source gives names only.

## Metric-Layer Rule

Two different China metrics must stay separate.

| Layer | Where it lives | Status | Treatment |
|---|---|---|---|
| Overall usage / market share | `regions/cn/ai-engines.md` market-share table and engine prose | Authoritative | Byte-identical, never edited by this change |
| Per-agent content composition | `regions/cn/platform-behavior.md` and the two referral annotations in `ai-engines.md` | `UNVERIFIED`, attributed | Separate labeled layer, reported only |

Rules that follow from this:

- Article per-agent content-source percentages describe what an engine draws from a content source. They are not market-adoption or overall-usage figures and are never merged into the authoritative table.
- A competing attributed ByteDance-ecosystem share claim is kept side by side with the spot-checked citation counts as a separate claim. Different units and different sources mean they must not be combined into one number.
- DeepSeek's developer community is its cited source; short-video content is absent with zero citations and is explicitly not a preferred source.
- No authoritative market-share number is restated in the new themed docs.

## Reconciliation Sites

| # | Site | File | Change |
|---|---|---|---|
| 9 | Per-engine referral-platform lists | `regions/cn/ai-engines.md` | Two content-source-composition annotation lines added inside the Doubao and DeepSeek referral sections; the six original ranked lists and the market-share table unchanged |
| 10 | Algorithm rules in engine rubrics | `regions/cn/ai-engines.md` | Eight attributed `UNVERIFIED` sub-bullets woven into the six per-engine scoring-criteria blocks; point totals unchanged |
| 11 | Canonical tiering in content DSS | `skills/geo-content/SKILL.cn.md` | One pointer line added to the DSS authoritative-source subsection, referencing `source-tiering.md` and 三区分治; no second tier table |
| 12 | Engine-id drift | `regions/profiles.yaml` | Single-line rename `ernie` to `yuanbao`; both weight blocks byte-identical |

## Guardrails

- No global or CN weight change (global 25/20/20/15/10/10 and CN 20/30/15/10/15/10 stay as-is), no GEO Score formula change, no new `/geo` command, no non-CN region change.
- No new Python dependency, lockfile, or machine-learning port.
- Black-hat and manipulation tactics appear only as prohibitions in `compliance-anti-abuse.md`, never as recommendations.
- No unverified figure is stated as fact, and no figure is invented where the source gives none (for example, the 清朗 category names and the A2 KPI formulas).
- `AGENTS.md` is left untouched and gitignored client artifacts are not committed.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The two China metrics get mixed | Medium | Dedicated metric-layer section, byte-identical diff checks on the market-share table, and forbidden-figure greps on new docs |
| An unverified figure is laundered into fact | Medium | Provenance appendix with `UNVERIFIED` on every figure, plus spot-checks and cross-doc attribution greps |
| Competing source-tier schemes reappear as parallel truth | Low | One canonical model, pointer-not-duplication wiring, and a no-duplicate-tier-table check in the content DSS |
| A manipulation tactic reads as a recommendation | Low | Prohibition-only wording confined to the compliance doc, with a guardrail grep across all new docs |
| Pointers drift from the docs they reference | Low | Each new doc has at least one consumer and link targets are checked to exist |
