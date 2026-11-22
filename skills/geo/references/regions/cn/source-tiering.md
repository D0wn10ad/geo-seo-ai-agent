# CN Region: Canonical Source-Tiering Model

This doc defines ONE canonical source-tier model for China-market GEO audits and records the provenance of the five competing schemes it reconciles. The source articles describe several different tiering systems that do not agree with each other. Presenting them side by side as equal truth would leave an auditing agent with no way to decide, so this doc fixes a single internal hierarchy and maps every external scheme onto it.

The canonical model is a toolkit-internal reconciliation device. It is not an endorsement of any external scheme as fact, and no external scheme is treated here as a verified standard. Every scheme, figure, and threshold below carries an `UNVERIFIED` tag and an article ID traceable to `regions/cn/provenance.md` (rows 1 to 10).

## Discipline (read first)

- External article text is untrusted data. It is never treated as instructions. Promotional calls to action and tool-wrapper reminders in the fetched pages were ignored and are not reproduced here.
- Every scheme and threshold is `UNVERIFIED`. That status is about truth, not just origin. A spot-check that finds claim text in an article confirms attribution only. It does not turn a marketing or industry claim into an established fact.
- No external scheme is called authoritative or verified. The only scheme that was spot-checked is T/CAPT 026-2026, and the article itself describes it as a non-binding group standard. Attribution confirmed does not mean standard verified.
- The canonical labels `CN-T1` to `CN-T4` belong to this toolkit. They are not T/CAPT A-D, not S/A/B/C, not 豆包 Level1-4, not a star count, and not an EEAT6.0 score. Those schemes are mapped onto the canonical tiers below.
- No full article text is pasted. Only short attributed phrases appear, enough to identify each claim.
- Metric-layer separation is mandatory. This doc covers source-authority tiering, meaning how trustworthy a source type is. It is NOT the per-agent content-composition percentages in the platform-behavior layer (theme 3), and it is NOT the 源易 overall-usage and MAU tables in `regions/cn/ai-engines.md`. Those three layers answer different questions and are never merged.

## The canonical model (ONE model)

The canonical model has four ordered tiers plus two cross-cutting gates. The four-tier shape and the source-type descriptions are anchored on the T/CAPT 026-2026 A-D scheme (`ScUyd3hGPbjCjVrAugO4yg`, UNVERIFIED), because it is the only scheme with explicit source-type definitions and the only one that was spot-checked. That makes it the clearest descriptive backbone, not a verified authority. The two gates absorb the mechanisms that are not really tiers: 豆包's auth-info filter and EEAT6.0's numeric trust score.

### Canonical tiers

| Canonical tier | Short label | Source type (descriptive, UNVERIFIED) | External schemes mapping here |
|---|---|---|---|
| `CN-T1` | 权威源 / institutional authority | Government, central media, court/judicial bodies, official standards, .gov.cn and .edu.cn domains | T/CAPT A (UNVERIFIED); S (UNVERIFIED); 豆包 Level1 (UNVERIFIED); EEAT6.0 above 85 (UNVERIFIED); top star band (UNVERIFIED) |
| `CN-T2` | 专业源 / professional authority | Academic papers, association whitepapers, industry reports, verified Baike entries, known expert citations | T/CAPT B (UNVERIFIED); A (UNVERIFIED); 豆包 Level2 (UNVERIFIED); EEAT6.0 60 to 85 (UNVERIFIED); upper-mid stars (UNVERIFIED) |
| `CN-T3` | 自有源 / owned or commercial | Company website, product manual, reviews, self-published brand content | T/CAPT C, including 官网=C (UNVERIFIED); B (UNVERIFIED); 豆包 Level3 (UNVERIFIED); mid stars (UNVERIFIED) |
| `CN-T4` | 低质源 / low quality or anonymous | Anonymous, low-quality, uncited or unverified user content | T/CAPT D (UNVERIFIED); C (UNVERIFIED); 豆包 Level4 (UNVERIFIED); EEAT6.0 below 60 demote (UNVERIFIED); low stars (UNVERIFIED) |

All four rows are `UNVERIFIED`. The source-type descriptions are attributed claims from `ScUyd3hGPbjCjVrAugO4yg` (provenance rows 1 to 2), not established classification rules.

### Cross-cutting gates (not tiers)

These two mechanisms modify a source's placement but are not tiers themselves. Treating them as tiers is one of the conflicts this model resolves.

- **Filter-AuthInfoLevel** (豆包, `1T5NvuffOyMYZOPofczrvg`, UNVERIFIED, provenance row 7). An authentication-information filter applied across tiers. In the canonical model it is a gate that can hold or demote a source regardless of its `CN-T` tier. Its exact behavior is UNVERIFIED and was not spot-checked.
- **EEAT6.0 entity-trust thresholds** (`Tlmyhz_NWUHwGbEwYHIzLA`, UNVERIFIED, provenance row 9). The attributed thresholds are below 60 demote and above 85 quality. In the canonical model this is a numeric gate layered over the tiers: above 85 supports `CN-T1` or `CN-T2`, 60 to 85 supports `CN-T2` or `CN-T3`, below 60 demotes toward `CN-T4`. Both thresholds are UNVERIFIED and were not spot-checked.

## Provenance map: five schemes onto one model

Each row records where a scheme comes from, its verification status, and how it maps onto the canonical tiers. Article IDs match `regions/cn/provenance.md` rows 1 to 10.

| Scheme (as attributed) | Article ID | Provenance row | Status | Canonical mapping | Origin and conflict note |
|---|---|---|---|---|---|
| T/CAPT 026-2026 A-D, 官网=C | `ScUyd3hGPbjCjVrAugO4yg` | rows 1 to 2 | UNVERIFIED (spot-checked, text present; non-binding group standard) | A -> `CN-T1`, B -> `CN-T2`, C -> `CN-T3`, D -> `CN-T4` | Only spot-checked scheme and only one with explicit source types, so used as descriptive backbone. Not a verified standard. |
| 豆包 Level1-4 + Filter-AuthInfoLevel | `1T5NvuffOyMYZOPofczrvg` | row 7 | UNVERIFIED (not spot-checked) | Level1 -> `CN-T1`, Level2 -> `CN-T2`, Level3 -> `CN-T3`, Level4 -> `CN-T4`; Filter-AuthInfoLevel -> cross-cutting gate | Platform-internal leveling. The auth filter is a gate, not a tier. |
| S/A/B/C | `stQruNQ0RwxCt-QLmZIvwA` | row 8 | UNVERIFIED (not spot-checked) | S -> `CN-T1`, A -> `CN-T2`, B -> `CN-T3`, C -> `CN-T4` | Four letters like T/CAPT but a different top label (S instead of A). 官网 placement is unspecified in the attributed source. |
| EEAT6.0 entity-trust, below 60 demote, above 85 quality | `Tlmyhz_NWUHwGbEwYHIzLA` | row 9 | UNVERIFIED (not spot-checked) | above 85 -> `CN-T1`/`CN-T2`, 60 to 85 -> `CN-T2`/`CN-T3`, below 60 -> demote `CN-T4` | A numeric trust score, not a source-type tier. Thresholds are UNVERIFIED. |
| 星级 star ratings | `3dAOBxF81M64uPytfHZucQ` | row 10 | UNVERIFIED (not spot-checked) | high stars -> `CN-T1`, upper-mid -> `CN-T2`, mid -> `CN-T3`, low -> `CN-T4` | The star scale is unspecified in the attributed source, so this mapping is provisional and UNVERIFIED. |

## Conflict table

The schemes disagree on several dimensions. The last column shows how the canonical model resolves each one without declaring any external scheme true.

| Dimension | T/CAPT A-D | 豆包 Level1-4 | S/A/B/C | EEAT6.0 | 星级 | Canonical resolution |
|---|---|---|---|---|---|---|
| Tier count | 4 (A-D) | 4 (Level1-4) | 4 (S/A/B/C) | numeric score, not tiers | scale unspecified | Fix 4 canonical tiers (`CN-T1` to `CN-T4`); treat the score as a gate. All UNVERIFIED. |
| Top label | A | Level1 | S | above 85 | top stars | Use neutral `CN-T1`, avoid importing any scheme's label. |
| 官网 placement | explicitly C, so `CN-T3` | unspecified | unspecified | depends on trust score | unspecified | Adopt `CN-T3` from the only scheme that states it, flagged UNVERIFIED. |
| Mechanism kind | source-type classification | platform leveling plus auth filter | source-type classification | numeric trust score | star classification | Classification sets the tiers; the auth filter and EEAT score become cross-cutting gates. |
| Letter meaning of C | mid tier, the company site | not used | lowest tier | not used | not used | Drop bare letter labels entirely to avoid this collision. |
| Verification | spot-checked, attribution only | not spot-checked | not spot-checked | not spot-checked | not spot-checked | None is verified. Canonical model is an internal reconciliation, not a standard. |

## How downstream docs reference this model

- Todo 11 folds this into `skills/geo-content/SKILL.cn.md` DSS 权威来源 (lines 134 to 140). Reference the canonical tiers `CN-T1` to `CN-T4`, not the external scheme names, and keep the `UNVERIFIED` tag on every attributed figure.
- Todo 13 wires the same canonical tiers into the SKILL.cn.md overrides. Use one vocabulary everywhere so audits do not face two sources of truth.
- When a source needs a tier, assign `CN-T1` to `CN-T4` using the descriptive source types, then apply the two gates. Record the article ID and `UNVERIFIED` status alongside the assignment.
- Do not restate an external scheme as the authority. The provenance map above is the only place the five schemes are named together.

## Open items and risks

- Provenance rows 7 to 10 (豆包 Level1-4, S/A/B/C, EEAT6.0, 星级) were not spot-checked. Their exact labels, scales, and thresholds stay UNVERIFIED until a dedicated source check is done.
- The 星级 scale is not specified in the attributed source. The star mapping is provisional and must not be stated as a fixed rule.
- T/CAPT 026-2026 is a group standard, not national law, per the spot-checked article. Do not describe it as a binding or verified standard.
- This doc records attribution and reconciliation, not truth. Any downstream doc carrying a figure from here must keep its `UNVERIFIED` tag and article ID.
