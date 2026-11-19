## Why

The `region-aware-geo` change gave the toolkit a China region: detection, a profile in `regions/profiles.yaml`, engine and platform reference docs, skill overrides, and inline agent logic. That foundation works, but the CN knowledge it points to is thin. It has no claim-level provenance, no unified source-authority model, no cross-validation rules, and no record of how each AI engine composes the sources it cites.

Auditors running a CN audit today have no way to answer basic questions from the toolkit itself: which source is more trustworthy, how many independent sources corroborate a claim, or which content sources feed each engine. There is also no guardrail text for manipulation tactics and no supplementary CN-only quality signals. The source material exists in roughly two dozen industry articles and one published research method, but it is scattered, unverified, and in places contradictory.

This change adds that knowledge as reference material and wires it into the existing CN entry points. It leaves the authoritative market-share data in `regions/cn/ai-engines.md` byte-for-byte intact and keeps every new external figure attributed and explicitly unverified.

## What Changes

- **CN provenance appendix**: `regions/cn/provenance.md`, a claim-to-source table covering every external figure used by the new docs, each tagged `UNVERIFIED` with an article ID, plus a source index and a small set of webfetch spot-checks.
- **Seven themed knowledge docs** under `regions/cn/`: canonical source-tiering, multi-source cross-validation, per-agent platform and content behavior, engineering playbooks, compliance and anti-abuse red lines, supplementary KPIs plus the agentic_geo method note, and a navigation index.
- **Four surgical reconciliations** of existing content: per-engine referral-platform lists and scoring rubrics in `regions/cn/ai-engines.md`, the DSS authoritative-source subsection in `skills/geo-content/SKILL.cn.md`, and the `ernie` to `yuanbao` engine-id fix in `regions/profiles.yaml`.
- **Wiring**: references from the relevant `SKILL.cn.md` overrides, the five agents' inline Region Awareness blocks, and `skills/geo-audit/SKILL.md`, so audits actually consult the new material.
- **Supplementary CN KPIs**: reported-only signals surfaced in region-tagged audit output, with no scoring changes.
- **Method track**: a documentation-only note on the agentic_geo research method, with no runtime port.

## Scope

### In scope

- Eight new themed docs under `regions/cn/` (provenance, source-tiering, cross-validation, platform-behavior, engineering-playbooks, compliance-anti-abuse, kpi-and-method, and the README index).
- The four reconciliation sites listed above, each a section-level edit with no whole-file rewrite.
- Supplementary CN KPIs, reported only.
- The method track as documentation and background only.
- Pointer-based wiring into skills, agents, and the audit skill.

### Out of scope

- No change to global or CN scoring weights, the GEO Score formula, or any non-CN region.
- No new `/geo` slash commands.
- No port of the agentic_geo Python or machine-learning system: no models, no training, no feedback runner, no new dependencies, no lockfile.
- No merging article content-composition figures into the authoritative market-share tables, and no laundering unverified marketing numbers into fact.
- No black-hat or manipulation tactic presented as a recommendation. Those terms appear only as prohibitions in the compliance doc.
- No edits to `AGENTS.md` and no commits of gitignored client artifacts.

## Capabilities

- `cn-provenance`: every external figure carries an article ID and an `UNVERIFIED` tag, with a representative subset spot-checked.
- `canonical-source-tiering`: one CN tier model, `CN-T1` through `CN-T4`, plus two cross-cutting gates, reconciling five competing external schemes.
- `cross-validation`: five corroboration rules for auditors, reported only and never used as scoring parameters.
- `per-agent-content-composition`: a separate, labeled layer describing which content sources each engine draws from, kept apart from market-adoption data.
- `engineering-playbooks`: governance and engineering frameworks, including 三区分治, with compliance red lines deferred by reference.
- `compliance-red-lines`: prohibition-only guidance, with manipulation tactics explicitly rejected.
- `supplementary-cn-kpis`: region-tagged, reported-only signals with no weight changes.
- `method-track`: documentation of the agentic_geo method with an explicit no-ML-port boundary.

## Impact

- Eight new files under `regions/cn/`, plus section-level edits to `regions/cn/ai-engines.md`, `regions/profiles.yaml`, `skills/geo-content/SKILL.cn.md`, `skills/geo-audit/SKILL.md`, six existing `SKILL.cn.md` overrides, one new `SKILL.cn.md` override, and five agent files.
- No breaking changes. Global behavior and non-CN regions are unchanged.
- No new Python dependencies and no new commands.
- The authoritative market-share table and both scoring-weight blocks stay byte-identical.
- All new external figures are attributed and unverified, so no unverified number becomes a stated fact.
