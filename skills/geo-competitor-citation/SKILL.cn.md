---
name: geo-competitor-citation-cn
description: >
  Cross-engine competitor GEO gap analysis for China market. Runs a representative
  Chinese-language question set against 6 CN AI engines (Baidu AI Search, Doubao,
  Yuanbao (腾讯元宝), Qwen, Kimi, DeepSeek) for the brand and N competitors, normalizes
  citations, and builds a 3-D gap matrix (brand × engine × intent type) showing
  citation count, average position, and contextual sentiment. Uses CN brand alias
  patterns and CN platform references for alias merging and gap narrative. Emits
  LEADING / PARITY / LAGGING / CRITICAL_GAP verdict per quadrant plus a top-3
  remediation plan mapped back to geo-content, geo-distribution-plan, and
  geo-citation-pipeline.
version: 1.0.0
region: cn
parent: geo-competitor-citation
---

# GEO Competitor Citation Gap — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base skill.

Reference: `regions/cn/ai-engines.md`, `regions/cn/platforms.md`.

---

## Engine Selection (CN)

Replace the 6 Western AI engines with the following 6 CN AI engines.
Engine characteristics and sourcing preferences are detailed in `regions/cn/ai-engines.md`.

| # | CN Engine | Replaces (Western) | Surface | Programmatic? | Probe handling |
|---|---|---|---|---|---|
| 1 | **Baidu AI Search** (百度AI搜索) | Google AI Overviews | ai.baidu.com | No stable public-URL query API | Manual capture via user pasting response |
| 2 | **Doubao** (字节豆包) | ChatGPT | doubao.com | No stable public-URL query API | Manual capture |
| 3 | **Yuanbao** (腾讯元宝) | Claude | yuanbao.tencent.com | No stable public-URL query API | Manual capture |
| 4 | **Qwen** (通义千问) | Perplexity | tongyi.aliyun.com | No stable public-URL query API | Manual capture |
| 5 | **Kimi** (月之暗面) | Gemini | kimi.moonshot.cn | No stable public-URL query API | Manual capture |
| 6 | **DeepSeek** (深度求索) | Copilot | chat.deepseek.com | No stable public-URL query API | Manual capture |

All 6 CN engines currently lack stable public-URL query endpoints. This means **all 360 probes require manual capture**. Budget 90–120 minutes of human time for a full run, or reduce to a 2-runs-per-probe (240 probe) sweep.

---

## Question Set Construction — CN Adaptation

The 20-question probe set follows the same 4-intent structure (Definitional / Comparative / Procedural / Causal, 5 per quadrant) but all questions must be in **Chinese (Simplified)**.

### CN probe question examples

| Intent | Probe ID | Example question (Chinese) | English gloss |
|---|---|---|---|
| Definitional | D1 | 什么是[主题]？它的核心原理是什么？ | What is [topic]? What are its core principles? |
| Definitional | D2 | [主题]和[相关概念]有什么区别？ | What is the difference between [topic] and [related concept]? |
| Definitional | D3 | [主题]的发展历程是怎样的？ | What is the development history of [topic]? |
| Definitional | D4 | [主题]的主要应用场景有哪些？ | What are the main application scenarios of [topic]? |
| Definitional | D5 | [主题]的市场规模有多大？ | How big is the market size for [topic]? |
| Comparative | C1 | [品牌A]和[品牌B]哪个更好？优缺点对比 | Which is better, [Brand A] or [Brand B]? Compare pros and cons |
| Comparative | C2 | [主题]领域的前三名企业是哪些？ | Who are the top 3 companies in [topic]? |
| Comparative | C3 | 国内最好的[产品类别]推荐 | Best [product category] recommendations in China |
| Comparative | C4 | [方案A]和[方案B]的区别及选择建议 | Differences between [Solution A] and [Solution B] and selection advice |
| Comparative | C5 | [品牌]在[行业]中的排名如何？ | How does [Brand] rank in [industry]? |
| Procedural | P1 | 如何开始使用[主题/产品]？ | How to get started with [topic/product]? |
| Procedural | P2 | [主题]的实施步骤是什么？ | What are the implementation steps for [topic]? |
| Procedural | P3 | 如何优化[流程/系统]？ | How to optimize [process/system]? |
| Procedural | P4 | [产品]的使用技巧和最佳实践 | Usage tips and best practices for [product] |
| Procedural | P5 | 如何避免[主题]中的常见错误？ | How to avoid common mistakes in [topic]? |
| Causal | Ca1 | 为什么[现象]会发生？ | Why does [phenomenon] happen? |
| Causal | Ca2 | [趋势]背后的驱动因素是什么？ | What are the driving factors behind [trend]? |
| Causal | Ca3 | [技术/政策]对[行业]有什么影响？ | What impact does [tech/policy] have on [industry]? |
| Causal | Ca4 | 为什么[品牌]在[市场]取得成功？ | Why did [Brand] succeed in [market]? |
| Causal | Ca5 | [问题]的根本原因是什么？ | What is the root cause of [problem]? |

### Question quality gates (CN-specific additions)

Each question must additionally:
- Use natural Chinese phrasing with common search terms (not English syntax translated to Chinese)
- Avoid English mixed with Chinese unless industry standard (e.g., "AI" is acceptable)
- Be answerable by Chinese-language content on either the brand's CN site or CN platforms
- Not require Western-specific context (replace Western examples with CN equivalents)

---

## CN Brand Alias Patterns

Chinese brand citation tracking requires careful alias handling because brands often have multiple Chinese names, transliterations, and abbreviations.

### Common CN alias patterns

```yaml
brand: <brand-name>
canonical_domain: <brand-domain.cn>
cn_domains:
  - <brand-domain.com.cn>
  - <brand-domain.cn>
  - <brand.tmall.com>      # Tmall flagship store
  - <brand.jd.com>         # JD store
aliases:
  - <official Chinese name>      # e.g., "苹果" for Apple
  - <Chinese transliteration>    # e.g., "特斯拉" for Tesla
  - <abbreviation>               # e.g., "BAT" for Baidu/Alibaba/Tencent
  - <nickname/short name>        # e.g., "狗东" for JD.com
  - <pinyin name>                # e.g., "tengxun" for Tencent
  - <English name>               # e.g., the original English brand name
  - <mixed CN+EN form>           # e.g., "iPhone 15" vs "苹果15"
cn_platform_accounts:
  - <brand on Baidu Baike>
  - <brand on Zhihu>
  - <brand on WeChat OA>
  - <brand on Xiaohongshu>
  - <brand on Bilibili>
  - <brand on Douyin>
```

### CN alias merging rules

A cited source counts as the brand if any of the following match:

1. **Domain match**: `canonical_domain`, any `cn_domains`, or any `cn_platform_accounts` URL pattern.
2. **Chinese name match**: The `context_excerpt` or `anchor_text` contains the Chinese brand name, transliteration, or abbreviation.
3. **Platform mention match**: The citation originates from a CN platform URL (e.g., `zhihu.com`, `xiaohongshu.com`) and the excerpt contains the brand.
4. **Mixed-format match**: Both the Chinese and English name appear together ("苹果 iPhone 15" counts as Apple).

**Important**: Many CN AI engines cite brand names differently from Western engines — Baidu AI Search may cite a Baidu Baike entry using the Chinese name, while DeepSeek may cite the same brand using its English name. Both must match to the same brand entity.

---

## CN Platform References for Gap Narratives

When the gap narrative template (Step 7 of the base skill) refers to competitor cited surfaces, use CN platform equivalents:

| Base skill reference | CN equivalent |
|---|---|
| "their Reddit AMA" | "他们的知乎问答" (their Zhihu Q&A thread) |
| "their Wikipedia article" | "他们的百度百科词条" (their Baidu Baike entry) |
| "a third-party comparison post on G2" | "一篇第三方对比文章在36氪上" (a third-party comparison on 36Kr) |
| "a YouTube review" | "一个B站评测视频" (a Bilibili review video) |
| "a Twitter/X thread" | "一个微博话题" (a Weibo topic thread) |
| "their GitHub repo" | "他们的CSDN技术文章" (their CSDN technical article) |
| "a Reddit thread" | "一条小红书笔记" (a Xiaohongshu note) |
| "a LinkedIn article" | "一篇微信公众号文章" (a WeChat Official Account article) |

For the gap narrative template sentence 3, the sample text becomes:

> The dominant cited source for `<competitor>` was `<cn-platform-domain>` — appearing in `<N>` of the `<their-count>` cited answers.

For sentence 4:

> The gap is concentrated on probes `<probe-ids>`, where the engine cited `<competitor>` via `<surface-pattern>` (e.g., "their Baidu Baike entry from 2024" or "a Zhihu answer with 10K+ upvotes" or "a third-party comparison article on Huxiu").

---

## Adjusted Verdict Rubric (CN Context)

The base verdict rubric applies identically, with one adjustment for CN-specific data sparsity:

| Verdict | Criteria (CN) |
|---|---|
| **LEADING** | My citation count ≥ best competitor's count AND my average position ≤ best competitor's position AND my sentiment is AUTHORITATIVE in ≥ 50% of cited probes |
| **PARITY** | My citation count within ±1 of best competitor's AND my average position within ±1.0 of best competitor's (widened from ±0.5 due to higher manual capture variance) |
| **LAGGING** | My citation count is 2–3 below best competitor's, OR my average position is 1.5–2.5 worse (widened from 1.0–2.0) |
| **CRITICAL_GAP** | My citation count is ≥ 3 below best competitor's (lowered from ≥ 4 — CN engine citation sets tend to be smaller), OR I am NOT CITED while ≥ 1 competitor is cited (lowered from ≥ 2) |

**Rationale for widened ranges:** All 6 CN engines require manual capture (vs. 2 of 6 programmatic in the Western flow). Manual captures have higher variance — a user may capture 2 of 3 runs for one engine and 3 of 3 for another, introducing small positional noise. The widened PARITY and LAGGING thresholds absorb this noise without producing false gap signals.

### Mention rate differential KPI

Compare brand's mention rate vs each competitor per engine.

- **Primary metric:** `(brand_mention_rate - competitor_mention_rate)` per engine per query.
- **Target:** ≥20% advantage over nearest competitor within 12 weeks.
- **Tracking:** `~/.geo-prospects/<domain>/mention-rate-diff-*.md` updated monthly.

---

## Remediation Mapping — CN Platform Adjustments

When mapping gaps to upstream skills, adapt the remediation actions to CN ecosystem:

| Gap pattern | CN-adjusted remediation |
|---|---|
| Competitor cited via Baidu Baike entry | `geo-distribution-plan`: Target Baidu Baike entry creation/update |
| Competitor cited via Zhihu answer | `geo-distribution-plan`: Run Zhihu Q&A seeding campaign |
| Competitor cited via WeChat OA article | `geo-content` + `geo-distribution-plan`: Publish WeChat OA article with CN GEO elements |
| Competitor cited via Xiaohongshu note | `geo-distribution-plan`: Create Xiaohongshu brand content |
| Competitor cited via Bilibili video | `geo-distribution-plan`: Produce Bilibili video with transcript optimization |
| Competitor cited via 36Kr/Huxiu coverage | `geo-brand-mentions`: Pitch CN tech media for coverage; `geo-distribution-plan` for syndication |
| Citation gap on Baidu AI Search specifically | `geo-citation-pipeline`: Run CN pipeline with Baidu Zhanzhang submission |
| You have the right content but BaiduSpider missed it | `geo-crawlers`: Check CN crawler access; `geo-citation-pipeline`: Baidu Zhanzhang push |

### Phased displacement strategy (源易 methodology)

- **Phase 1 (Month 1-2):** Claim platforms with lowest bar — 百家号, 什么值得买, 头条号
- **Phase 2 (Month 3-4):** Dominate 2nd-tier citation platforms — 知乎, 搜狐号, CSDN
- **Phase 3 (Month 5-6):** Challenge established authorities on Baidu Baike, 36Kr
- **Scoring:** Weighted by platform authority → competitor displacement difficulty → engine-specific citation probability

---

## Scoring for CN Context

### Per-engine score components (CN)

When the base skill computes per-engine scores, use these CN rubrics:

| Engine | Top scoring signal | Second signal | Third signal |
|---|---|---|---|
| Baidu AI Search | Baidu Baike presence | .gov.cn / .edu.cn authority | Chinese citation quality |
| Doubao | Content freshness (< 90 days) | ByteDance ecosystem presence | Multi-format content |
| Yuanbao (腾讯元宝) | Structured data completeness | Factual density | Author credentials |
| Qwen | E-commerce/technical content | Logical structure | Alibaba ecosystem tie-in |
| Kimi | Content depth (long-form) | Heading hierarchy | Academic quality |
| DeepSeek | Technical accuracy | Code/format quality | Developer ecosystem |

Engine weighting: Engines are weighted by MAU tier (see regions/cn/ai-engines.md).
Composite gap score uses weighted averages across all 6 engines.

---

## Output Format

Generate `~/.geo-prospects/competitor/<my-domain>-<YYYY-MM-DD>-CN.md`.

The output structure mirrors the base format with these CN-specific changes:

### Header section

```markdown
# GEO Competitor Citation Gap Report — China Market

**My domain:** <my-domain>
**Competitors:** <c1>, <c2>, <c3>, <c4>
**Run date:** <YYYY-MM-DD>
**Region:** China (CN)
**Topic scope:** <from matrix `<topic>` / "matrix-less probe set">
**Probes executed:** 20 questions × 6 CN engines × 3 runs = 360 probes
**Engines captured programmatically:** None (all manual)
**Engines captured manually:** Baidu AI Search, Doubao, Yuanbao (腾讯元宝), Qwen, Kimi, DeepSeek
```

### Gap Matrix tables

Replace Western engine column headers with CN engine names:

```
| Intent \ Engine | Baidu AI Search | Doubao | Yuanbao (腾讯元宝) | Qwen | Kimi | DeepSeek |
|---|---|---|---|---|---|---|
| Definitional | <n>/5 | <n>/5 | <n>/5 | <n>/5 | <n>/5 | <n>/5 |
...
```

### Competitor Comparison tables

Same structure, 6 CN engine columns.

---

## Quality Gates — CN-Specific

In addition to the base quality gates:

- **Capture variance gate:** Because all CN probes are manual, a quadrant verdict requires ≥ 3 of the 5 probes in that intent to have valid captures across ≥ 5 of the 6 engines (lowered from 4/5 probes × 6 engines due to manual capture overhead). Quadrants below this threshold are marked `INSUFFICIENT_DATA`.
- **Alias confirmation:** On first run for a CN-market brand, require user confirmation of the Chinese alias list (brand names in CN are less standardized than Western equivalents).
- **Transliteration check:** Flag any citation where the engine used a non-standard transliteration of the brand name — add it to the alias list for the next run.
- **Freshness:** Captures older than 21 days must not be reused for CN (engines update indexes faster in the CN AI market than Western equivalents).

---

## Upstream and Downstream Skill Hooks — CN

### Upstream (CN)

| Upstream skill | CN-specific consumption |
|---|---|
| `geo-intent-matrix` (CN) | Probe questions sourced from CN-language matrix |
| `geo-brand-mentions` (CN) | CN brand alias inventory from CN platform scan |
| `geo-citation-pipeline` (CN) | CN pipeline state — Baidu Zhanzhang, ByteSpider access |

### Downstream (CN)

| Downstream skill | CN-specific feed |
|---|---|
| `geo-content` (CN) | New Chinese-language content briefs from CRITICAL_GAP narratives |
| `geo-distribution-plan` (CN) | CN platform distribution targets (Baidu Baike, Zhihu, WeChat OA, Xiaohongshu) |
| `geo-citation-pipeline` (CN) | URL list for Baidu Zhanzhang submission |
| `geo-intent-matrix` (CN) | Re-balance toward quadrants with CN citation gaps |

---

## Important Notes (CN)

- **All-manual capture:** Unlike the Western flow (where Perplexity and Google AI Overviews are programmatic), all 6 CN engines require manual interaction. Budget time accordingly and be transparent with the user.
- **Baidu Baike is the kingmaker:** A competitor with a verified, comprehensive Baidu Baike entry will almost always outperform on Baidu AI Search and Yuanbao (腾讯元宝). Prioritize Baidu Baike entry creation/improvement if this pattern appears in the gap matrix.
- **Platform polarization:** CN AI engines strongly favor their own ecosystem content (Baidu engines favor Baidu Baike, ByteDance's Doubao favors Douyin/Toutiao). A citation gap on one engine may not correlate with gaps on others — assess per-engine, not averaged.
- **Dual-name brands:** Foreign brands in China often have multiple aliases (official Chinese name + transliteration + colloquial name + English name). User confirmation of the alias list is critical — a missed alias produces a false CRITICAL_GAP.
- **Output filename:** Use the `-CN.md` suffix so reports are distinguished from Western-market reports in `~/.geo-prospects/competitor/`.
