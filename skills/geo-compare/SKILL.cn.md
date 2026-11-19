---
name: geo-compare-cn
description: CN region override for GEO monthly delta report — CN scores, CN platforms, supplementary CN KPIs
version: 1.0.0
region: cn
parent: geo-compare
---

# GEO Monthly Delta Report — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Use CN-specific scoring labels, platforms, and region-tagged KPIs below. Do not change the base delta-calculation logic or any scoring weight.

Reference: `regions/cn/ai-engines.md` and `regions/cn/platforms.md` for CN engine and platform details.

---

## 中国区补充观测 (CN Supplementary KPIs)

When REGION is cn, add a "中国区补充观测 (CN supplementary KPIs)" block to the monthly report using `regions/cn/kpi-and-method.md` Part A. These six KPIs are region-tagged and reported only: they do not enter the GEO Score, do not change any weight, and are not merged into global reports. Show baseline → current deltas for each KPI where observed, with article IDs and `UNVERIFIED` tags for external figures.

---

## Output Format (CN)

Generate `~/.geo-prospects/reports/<domain>-monthly-CN-<YYYY-MM>.md` (same `-CN` region tag convention as other CN outputs).
