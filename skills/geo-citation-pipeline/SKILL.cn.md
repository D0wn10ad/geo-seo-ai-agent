---
name: geo-citation-pipeline-cn
description: CN-specific AI citation pipeline — BaiduSpider/ByteSpider discovery, CN authority domains, Baidu Zhanzhang submission
version: 1.0.0
region: cn
parent: geo-citation-pipeline
---

# AI Citation Pipeline — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base 6-stage pipeline.

Reference: `regions/cn/ai-engines.md`, `regions/cn/platforms.md`.

---

## Stage 1: AI Crawler Discovery Audit (CN)

Replace the base crawler audit with the CN crawler set:

| Tier | Crawler | User-Agent | Purpose |
|---|---|---|---|
| 1 | BaiduSpider | BaiduSpider | Baidu Search + Baidu AI |
| 1 | Bytespider | Bytespider | Doubao AI + Douyin |
| 1 | Sogou Spider | Sogou web spider | Sogou Search + WeChat Search |
| 2 | 360Spider | 360Spider | 360 Search |
| 2 | YisouSpider | YisouSpider | Quark Browser + Qwen AI |

**CN robots.txt checks:**
- BaiduSpider must NOT appear under a `Disallow:` rule for any page path
- Baidu's `Sitemap:` directive should be explicitly declared for BaiduSpider
- Check for Baidu-specific Crawl-delay (recommended: 5s)
- Verify Bytespider is also allowed (often blocked by default)

**Baidu-specific meta tag check:**
- `<meta name="applicable-device" content="pc,mobile">`
- `<meta http-equiv="Cache-Control" content="no-transform">`
- `<meta name="baidu-site-verification" content="code-xxx">`

### CN 6-Step Citation Pipeline (源易科技 methodology — maps to existing stages)
1. 定位 (Position) → Define target queries + preferred answer format [Stage 0 precursor]
2. 占位 (Claim) → Create/optimize content on target platforms [Stage 2 + 3]
3. 数据 (Data) → Inject structured data points + verifiable sources [Stage 4 + DSS]
4. 放大 (Amplify) → Distribute across platform tiers to trigger cross-citation [Stage 2 + distribution]
5. 验证 (Validate) → Check AI engine answers for target queries [Stage 6]
6. 迭代 (Iterate) → Feed gaps back into content refinement cycle [Stage 0 loop]

Quality gate: Each stage must achieve ≥0.65 confidence before next stage proceeds. If verification at Stage 5 shows <50% preferred-answer rate, loop back to Stage 1 for content reprioritization.

---

## Stage 2: AI-Friendly Internal-Link Wiring (CN)

**CN internal link priorities:**
- Link to Baidu Baike entries for key concepts where possible
- Cross-link between Chinese-language pages (not English content)
- Ensure Chinese anchor text is descriptive and keyword-rich
- For e-commerce: link to product pages with Chinese category names

**CN link structure signals:**
- Baidu's algorithm favors sites with clear China-hosted content clusters
- Internal links should use Simplified Chinese throughout
- Avoid mixing zh-CN and zh-TW links on the same page

---

## Stage 3: AI-Training Authority Backlink Check (CN)

**Tier A domains** (sorted by avg citation rate across 6 CN engines):
- zhihu.com (~15.8%)
- 36kr.com (~12.1%)
- ithome.com (~6.2%)
- baike.baidu.com (entity recognition, not direct citation)
- huxiu.com (~5.0%)
- gov.cn, edu.cn (authority verification)

**Backlink analysis:** Does the site have links from any of these Tier A CN domains? For CN citation potential:
- A backlink from Baidu Baike is the single strongest CN citation signal
- Zhihu backlinks (in answers or article references) provide strong CN authority
- Gov.cn/edu.cn links carry disproportionate weight with CN AI engines

---

## Stage 4: On-Page GEO Element Compliance (CN)

**In addition to base Stage 4 checks:**

| Element | CN Requirement |
|---|---|
| Chinese schema markup | Use `@language: zh-CN` in JSON-LD |
| Article schema date | Dates in Chinese format (YYYY年MM月DD日) |
| Zh-cn language tag | `<html lang="zh-CN">` required |
| Chinese alt text | Every image should have Chinese alt text |
| Mobile optimization | Higher priority for CN (mobile-first CN audience) |
| Page speed | Baidu considers page speed — aim for < 3s FCP from CN |

**Pass-fail per page:**
- PASS: All CN elements present and correct
- WARN: Some elements present, some missing
- FAIL: No CN GEO elements, or Chinese content appears machine-translated

---

## Stage 5: Rapid Indexing — CN Channels

### Baidu Zhanzhang URL Submission (百度站长平台)

The primary CN rapid-indexing channel. Two methods:

**Method A: Baidu Zhanzhang API (Recommended)**
1. Register site at https://ziyuan.baidu.com/
2. Verify site ownership (file upload, DNS record, or HTML tag)
3. Submit URLs via Baidu's API:
   - API endpoint: `http://data.zz.baidu.com/urls?site=<site>&token=<token>`
   - Max 10 submissions/day for most sites
   - Rate limit: 1 submission per URL per 5 minutes

**Method B: Baidu Active Push (主动推送)**
- Install Baidu's JS push snippet on every page
- Baidu automatically discovers new/changed pages when users visit
- Passive but always active

### Sogou URL Submission (搜狗站长平台)
- Register at Sogou站长平台
- Submit via Sogou's URL submission tool
- Slower than Baidu but still useful for Sogou/WeChat Search

### 360 URL Submission (360站长平台)
- Register at 360站长平台
- Submit via 360's URL submission interface

### IndexNow in CN
- IndexNow works in CN but may have latency
- Baidu does NOT support IndexNow — use Baidu Zhanzhang instead
- For hybrid sites: use IndexNow for Bing and Baidu Zhanzhang for Baidu

---

## Stage 6: Preferred-Answer Verification — CN Engines

After the pipeline completes, verify citation status across 6 CN AI engines:

| Engine | Verification Method | Success Signal |
|---|---|---|
| Baidu AI Search (百度AI搜索) | Ask a representative question on https://ai.baidu.com/ | Brand appears in top 3 cited sources |
| Doubao (豆包) | Ask the same question on https://www.doubao.com/ | Brand cited in the response |
| Yuanbao (腾讯元宝) | Test on https://yuanbao.tencent.com/ | Brand appears in generated answer |
| Qwen (通义千问) | Test on https://tongyi.aliyun.com/ | Brand cited |
| Kimi (月之暗面) | Test on https://kimi.moonshot.cn/ | Brand appears in search result |
| DeepSeek (深度求索) | Test on https://chat.deepseek.com/ | Brand cited |

**Score interpretation for CN:**
- **PIPELINE_VERIFIED_STRONG** — cited by 5+ CN AI engines
- **PIPELINE_VERIFIED** — cited by 3-4 CN AI engines
- **PIPELINE_WEAK** — cited by 1-2 CN AI engines
- **PIPELINE_FAIL** — not cited by any CN AI engine

Output file: `~/.geo-prospects/pipelines/<domain>-<slug>-<YYYY-MM-DD>-CN.md`

---

## Monitoring: Continuous CN Engine Tracking

### Engine drift detection (引擎漂移监测)
- Track which platforms each engine cites over time
- Alert if an engine shifts preferred citation sources (e.g., Doubao moving from Xiaohongshu to Bilibili)
- Monthly comparison of `~/.geo-prospects/<domain>/engine-citation-map-*.md`
- When drift detected: reprioritize content distribution toward new preferred platforms
