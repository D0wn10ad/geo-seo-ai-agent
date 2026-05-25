---
name: geo-audit-cn
description: CN-specific GEO audit orchestration — Baidu AI engines, CN brand platforms, Chinese-language exec summary
version: 1.0.0
region: cn
parent: geo-audit
---

# GEO Audit Orchestration — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base audit workflow.

---

## Phase 0: Region Detection (CN-specific)

When `--region cn` is explicitly passed or auto-detected:
- Skip the multi-language dialog — treat as CN-only
- Load `regions/cn/ai-engines.md` for CN AI engine rubrics
- Load `regions/cn/platforms.md` for CN brand mention targets
- Load `regions/cn/schema.md` for CN schema guidance
- CN score weights apply (see Phase 3)

---

## Phase 1: Discovery Additions (CN)

### CN Business Type Detection

| Business Type | CN Detection Signals |
|---|---|
| **CN E-commerce (电商)** | Taobao/Tmall/JD links, 天猫/淘宝 schema, Chinese product names |
| **WeChat OA Publisher** | WeChat Official Account QR code, WeChat Pay, WeChat article embed |
| **CN SaaS (中国SaaS)** | Chinese pricing (¥), Alipay/WeChat Pay integration, 小程序 references |
| **CN Local Business** | 大众点评 (Dianping) links, Baidu Maps embed, Chinese address format |
| **CN Media (媒体)** | 今日头条 integration, 微信公众号 embeds, Chinese social share buttons |

### CN Crawl Adjustments

- BaiduSpider must NOT be disallowed in robots.txt for any crawled path
- Check for Baidu Webmaster Tools verification (百度站长平台验证)
- Verify sitemap is readable by BaiduSpider specifically
- When crawling `.cn` domains, handle GB2312/GBK encoding gracefully

---

## Phase 2: Parallel Subagent Delegation (CN-adjusted)

### Subagent 1: AI Visibility (CN)

- Use `regions/cn/ai-engines.md` for citation scoring targets
- Check brand presence on CN platforms: Baidu Baike (百度百科), Zhihu (知乎), WeChat OA (微信公众号), Xiaohongshu (小红书), Bilibili (哔哩哔哩), Douyin (抖音)
- Reference `regions/cn/platforms.md` for full CN platform list

### Subagent 2: Platform Optimization (CN)

- Assess Baidu AI Search, Doubao (豆包), ERNIE Bot (文心一言), Qwen (通义千问), Kimi (月之暗面), DeepSeek (深度求索)
- Reference `regions/cn/ai-engines.md` for CN engine-specific rubrics

### Subagent 4: Content E-E-A-T (CN)

- Add CN-specific E-E-A-T signals (see `SKILL.cn.md` in geo-content)
- Evaluate Chinese content quality, not English benchmarks
- Check for Baidu Baike cross-reference and Chinese author credentials

### Subagent 5: Schema (CN)

- Add Baidu-specific schema extensions (see `regions/cn/schema.md`)
- Check for Baidu's DataCenter and BreadcrumbList requirements

---

## Phase 3: Score Aggregation (CN)

### CN Score Composition

| Category | CN Weight | What It Measures |
|---|---|---|
| **AI Citability** | 20% | Citability within CN AI engines (Baidu AI, Doubao, etc.) |
| **Brand Authority** | **30%** | Third-party mentions on CN platforms |
| **Content E-E-A-T** | 15% | Chinese E-E-A-T signals |
| **Technical GEO** | 10% | Baidu crawler access, CN technical infrastructure |
| **Schema & Structured Data** | **15%** | Schema + Baidu extensions |
| **Platform Optimization** | 10% | CN AI platform readiness |

### CN Issue Severity Classification

**Critical (Fix Immediately):**
- BaiduSpider blocked in robots.txt
- ICP license missing for CN-hosted sites
- Baidu Baike entry non-existent
- CN AI crawlers all blocked
- Site inaccessible from mainland China

**High (Fix Within 1 Week):**
- Baidu Baike entry outdated or inaccurate
- No Baidu Webmaster Tools verification
- Missing WeChat Official Account
- Zhihu no brand presence
- Chinese content is machine-translated (not native)

**Medium (Fix Within 1 Month):**
- Xiaohongshu brand page missing
- No Bilibili presence for media/consumer brands
- CN social media inactive
- Chinese-language pages have poor readability
- No CN CDN for performance

**Low (Optimize When Possible):**
- Douyin brand account inactive
- Baidu Baike entry could be more detailed
- 36Kr/Huxiu media coverage gaps
- CSDN/Juejin developer community presence absent for tech brands

---

## CN Quick Wins (Template)

1. Verify BaiduSpider is NOT blocked in robots.txt
2. Submit site to Baidu Webmaster Tools (百度站长平台)
3. Create/update Baidu Baike entry for the brand
4. Set up WeChat Official Account with verification
5. Ensure ICP license is displayed (if CN-hosted)
6. Add Baidu-specific meta tags (`applicable-device`, `Cache-Control: no-transform`)
7. Create Chinese-language versions of all key pages
8. Register on Zhihu and post 1-2 relevant answers

---

## Output

Output file: `GEO-AUDIT-REPORT-CN.md`

Use the same template as the base skill, but with:
- Chinese-language section headings where appropriate
- CN-specific critical/high/medium/low issues
- CN weight table in the score breakdown
- CN platform names in Brand Authority section
- Quick wins targeting CN ecosystem
