---
name: geo-intent-matrix-cn
description: CN-specific intent-angle matrix — Chinese question generation, Baidu Index/WeChat Index SV sources, CN platform hooks
version: 1.0.0
region: cn
parent: geo-intent-matrix
---

# GEO Intent-Angle Matrix — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base intent matrix workflow.

Reference: `regions/cn/ai-engines.md`, `regions/cn/platforms.md`.

---

## CN Intent Distribution Assumptions

Base Profound study distribution (Definitional 31%, Comparative 27%, Procedural 24%, Causal 18%) shifts for CN AI engines:
- CN engines cite **Comparative** content more heavily (estimated 30%) — Baidu AI Search and Doubao favor side-by-side comparisons
- **Definitional** is slightly lower (29%) — CN engines prefer concise definitions in Chinese
- **Procedural** content performs similarly (23%)
- **Causal** is lower (18%) — CN AI engines tend to cite fewer long-form analytical pieces

These are heuristic estimates. Actual distribution depends on the topic and CN engine.

---

## Chinese Question Generation

### Definitional Expansion (CN)

For core topic `T`:

1. 什么是`T`？(What is T?)
2. `T`有什么用途？(What is T used for?)
3. `T`和`R`有什么区别？(What is the difference between T and R?)
4. `T`在<行业>中的应用是什么？(What is T's application in <industry>?)
5. `T`的发展历史是什么？(What is the history of T?)
6. 如何简单理解`T`？(How to understand T simply?)

### Comparative Expansion (CN)

1. `T`和`Alt1`哪个好？(Which is better, T or Alt1?)
2. <年>年最值得推荐的`T`解决方案 (Best T solutions in <year>)
3. `T`和`Alt2`的对比分析 (Comparative analysis of T and Alt2)
4. 选择`T`还是`Alt3`？关键因素分析 (Choose T or Alt3? Key factors)
5. `T`的优缺点分析 (Pros and cons of T)
6. `T`替代方案推荐 (T alternative recommendations)

### Procedural Expansion (CN)

1. 如何开始使用`T`？(How to start using T?)
2. `T`的安装和配置步骤 (T installation and configuration steps)
3. 从`前代`迁移到`T`的方法 (How to migrate from <predecessor> to T)
4. 如何将`T`集成到`系统`中？(How to integrate T into <system>?)
5. `T`常见问题排查 (Common T troubleshooting)
6. 如何优化`T`的性能？(How to optimize T's performance?)

### Causal Expansion (CN)

1. 为什么`T`很重要？(Why is T important?)
2. `T`为什么会有这样的特性？(Why does T have these characteristics?)
3. `T`的工作原理是什么？(How does T work?)
4. 什么原因导致`T`失败/性能不佳？(What causes T to fail/underperform?)
5. 为什么<行业>从`前代`转向了`T`？(Why did <industry> shift from <predecessor> to T?)
6. `T`的核心机制详解 (Detailed explanation of T's core mechanism)

### Prompt expansion strategy

Prompt expansion strategy (提示词扩展法):
When generating Chinese candidate questions, expand each seed topic using:
1. Baidu search suggest API (百度搜索下拉词)
2. Zhihu topic-related questions (知乎相关问题)
3. 5118 long-tail keyword tool (5118长尾词)
4. WeChat Index trending terms (微信指数热门词)

This ensures questions reflect real user search behavior, not author assumptions.

---

## CN Search Volume Sources

Replace global SV sources with CN equivalents:

| CN Data Source | Type | Accessibility | Reliability |
|---|---|---|---|
| 百度指数 (Baidu Index) | Keyword search volume trend | Free access at index.baidu.com | Most reliable CN source |
| 微信指数 (WeChat Index) | WeChat ecosystem search volume | WeChat mini-program | Useful for WeChat-targeted content |
| 知乎热搜 (Zhihu Hot List) | Trending Q&A topics | Public API | Good for CN audience interest signals |
| 微博热搜 (Weibo Hot Search) | Trending topics | Public API | Useful for Causal content ideas |
| 360趋势 (360 Trends) | Search volume trends | Free access | Supplementary to Baidu Index |
| 5118 / 站长工具 | CN SEO tool data | Paid tools | Most granular keyword data |

SV scoring uses the same 1-5 bucket system as the base skill, applied to CN search volume estimates.

---

## CN AI Citation Propensity (AICP)

| Intent | Base AICP | CN Adjustments |
|---|---|---|
| Definitional | 4 | +1 if topic is trending on Baidu Index; –1 if topic has a Baidu Baike entry that dominates |
| Comparative | 5 | +0; CN AI engines strongly favor comparison tables |
| Procedural | 4 | +1 if topic is developer-oriented (CSDN/Juejin audience) |
| Causal | 3 | +1 if topic is covered by 36Kr/Huxiu (CN AI engines cite business analysis) |

---

## CN Content-Form Binding

| Intent | Required Form | CN Specific Notes |
|---|---|---|
| Definitional | Standalone definition block | Opening "X是指..." or "X是..." in Chinese; numeric fact within first 6 sentences |
| Comparative | HTML table ≥ 3 rows | Table with Chinese column headers; price in RMB; audience in Chinese demographics |
| Procedural | Ordered list 5-15 steps | Each step starts with Chinese imperative (打开/安装/配置/运行) |
| Causal | Cause → effect chain + cited studies | Named CN sources (CN academic papers, 36Kr reports, B2B case studies) |

---

## CN Coverage Score Interpretation

Use the same coverage score formula, but reference CN competition landscape:
- **CN Locked:** Baidu Baike + Zhihu + 3+ CN media outlets dominate every engine
- **CN Crowded:** Multiple high-authority CN answers
- **CN Contested:** Some CN incumbents but no consensus

---

## CN 12-Week Schedule Hooks

Downstream actions map to CN skill equivalents:

- `→ geo-citation-pipeline-cn` (CN pipeline after publication)
- `→ geo-distribution-plan-cn` (CN distribution cadence)
- `→ geo-competitor-citation --region cn` (CN competitor analysis 14 days post-publication)

### Citation affinity per intent

Citation affinity per intent (基于 2,844 样本):
- Definitional (定义型): Baidu Baike, 知乎, 百家号 → Avg 11.2% citation rate
- Comparative (对比型): 什么值得买, 泡泡网, 中关村, 知乎 → Avg 6.8% citation rate
- Procedural (流程型): IT之家, CSDN, 哔哩哔哩, 知乎 → Avg 8.5% citation rate
- Causal (因果型): 36氪, 虎嗅, 网易, 微信公众号 → Avg 9.1% citation rate

Recommendation: Prioritize Definitional content for new domains (highest absolute citation probability).
For competitive queries, Comparative content offers better differentiation potential despite lower rates.

---

## Output Format

Generate `~/.geo-prospects/matrices/<domain>-<topic>-<YYYY-MM-DD>-CN.md`

Use the same template as the base skill, with Chinese question text, CN SV sources, and CN platform hooks throughout.
