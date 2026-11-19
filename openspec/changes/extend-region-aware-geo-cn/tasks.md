## Wave 1: Knowledge foundation

All eight foundation docs were created. Each external figure is attributed and tagged `UNVERIFIED` in the provenance appendix.

- [x] 1. Build provenance + attribution appendix `regions/cn/provenance.md`. Claim-to-source table with `UNVERIFIED` on every figure row, a source index, and three webfetch spot-checks. Outcome: created, 45 claim rows, 28-source index, three spot-checks confirmed.
- [x] 2. Create canonical source-tiering doc `regions/cn/source-tiering.md`. One `CN-T1`..`CN-T4` model plus two gates, with a provenance map of all five schemes and their conflicts. Outcome: created, bare letter labels dropped, all schemes `UNVERIFIED`.
- [x] 3. Create cross-validation doc `regions/cn/cross-validation.md`. Rules R1 through R5, each attributed and `UNVERIFIED`, reported only. Outcome: created, thresholds explicitly not scoring parameters.
- [x] 4. Create platform/content-behavior doc `regions/cn/platform-behavior.md`. Per-agent content-composition layer, opened with a content-composition-not-market-adoption note. Outcome: created, competing claims kept separate, no authoritative market-share number restated.
- [x] 5. Create engineering playbooks doc `regions/cn/engineering-playbooks.md`. Seven frameworks including 三区分治 and the called-compliance KPI. Outcome: created, black-hat terms absent, compliance deferred by reference.
- [x] 6. Create compliance and anti-abuse doc `regions/cn/compliance-anti-abuse.md`. Prohibition-only red lines, manipulation tactics explicitly rejected. Outcome: created, no tactic framed as a recommendation.
- [x] 7. Create agentic-commerce + KPI/method doc `regions/cn/kpi-and-method.md`. Part A reported-only KPIs, Part B method note with an explicit no-ML-port statement. Outcome: created, no invented formulas, no scoring changes.
- [x] 8. Create `regions/cn/README.md` index linking all themed docs plus the three existing base docs. Outcome: created, all ten link targets resolve, metric-layer and unchanged-weight notes restated.

## Wave 2: Reconciliation and wiring

The four reconciliation sites were completed and the new knowledge was wired into skills, agents, and the audit skill.

- [x] 9. Reconcile per-engine referral-platform lists in `regions/cn/ai-engines.md`. Two content-source-composition annotation lines added in the Doubao and DeepSeek referral sections. Outcome: market-share table at lines 11-20 byte-identical, no second ranked table.
- [x] 10. Weave algorithm rules into per-engine scoring rubrics in `regions/cn/ai-engines.md`. Eight attributed `UNVERIFIED` sub-bullets inside the six rubric blocks. Outcome: point totals unchanged, rules applied in place rather than in an appendix.
- [x] 11. Fold canonical tiering into the DSS authoritative-source subsection of `skills/geo-content/SKILL.cn.md`. Outcome: one pointer line to `source-tiering.md` and 三区分治, DSS structure byte-intact, no second tier table.
- [x] 12. One-line factual fix `ernie` to `yuanbao` in `regions/profiles.yaml`. Outcome: single-line diff, both scoring-weight blocks byte-identical.
- [x] 13. Wire new knowledge into `skills/geo-*/SKILL.cn.md` overrides. Outcome: six overrides edited and the missing `geo-compare` CN override created, each new doc has at least one consumer, frontmatter and `-CN` naming preserved.
- [x] 14. Wire new knowledge into the five agents' Region Awareness blocks. Outcome: six inline pointer lines added inside the CN branches, global branches byte-identical, no skill-file loading introduced.
- [x] 15. Add the supplementary CN KPI reference to `skills/geo-audit/SKILL.md`. Outcome: one CN-gated pointer line, no scoring formula or weight change, global audits unchanged.

## Verification

- [x] V.1 All eight new `regions/cn/*.md` docs exist and every new doc has at least one consumer in a skill override or agent.
- [x] V.2 The four reconciliation sites (todos 9 through 12) are complete, with section-level diffs only and no whole-file rewrite.
- [x] V.3 Metric-layer rule holds: the authoritative market-share table at `regions/cn/ai-engines.md:11-20` and both scoring-weight blocks in `regions/profiles.yaml` are byte-identical to the baseline. Article content-composition figures appear only in the labeled, `UNVERIFIED` platform-behavior layer and the two referral annotations, never in the authoritative table.
- [x] V.4 No global or CN weight change, no new `/geo` command, no new dependency or lockfile, and no machine-learning port.
- [x] V.5 Guardrail greps pass: black-hat terms appear only as prohibitions in the compliance doc, no forbidden figure is stated as fact, and no weight-key token appears in the new docs.
- [x] V.6 `git diff AGENTS.md` matches the pre-work baseline; gitignored client artifacts are not committed.
