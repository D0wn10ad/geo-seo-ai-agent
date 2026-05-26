---
name: geo-crawlers-cn
description: CN-specific AI crawler access analysis — BaiduSpider, Bytespider, Sogou, 360Spider, YisouSpider classification and scoring
version: 1.0.0
region: cn
parent: geo-crawlers
---

# AI Crawler Access Analysis — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Replace the default Western crawler reference with the CN crawler classification below.

Reference: `regions/profiles.yaml` for CN crawler profile.

---

## Complete CN AI Crawler Reference

### Tier 1: Critical for CN AI Search Visibility (RECOMMEND: ALLOW)

#### BaiduSpider

- **Operator:** Baidu
- **User-Agent:** `BaiduSpider`
- **Full User-Agent String:** `Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)`
- **Purpose:** Primary crawler for Baidu Search, Baidu AI Search, and Baidu's Yuanbao (腾讯元宝) model grounding. Powers all Baidu AI products.
- **Impact of Blocking:** Content will NOT appear in Baidu Search results or Baidu AI Search. This is the highest-impact CN AI crawler — blocking it removes content from China's dominant search and AI ecosystem.
- **Recommendation:** **ALLOW** — Baidu maintains ~65%+ search market share in China. Critical for CN visibility.

#### ByteSpider (Tier 1 in CN context)

- **Operator:** ByteDance
- **User-Agent:** `Bytespider`
- **Full User-Agent String:** `Mozilla/5.0 (compatible; Bytespider; https://zhanzhang.toutiao.com/)`
- **Purpose:** Powers Doubao (豆包, ByteDance's ChatGPT competitor), Douyin/TikTok search, and Toutiao content indexing. Key crawler for ByteDance's AI ecosystem.
- **Impact of Blocking:** Content will not appear in Doubao AI responses or Douyin/TikTok search results.
- **Recommendation:** **ALLOW** — Doubao has 100M+ users in China. Unlike the global context where this is Tier 3, in China it is a critical AI search crawler.

> **Note:** Yuanbao (Tencent/腾讯元宝) may also leverage Bytespider for crawling — treat any Yuanbao access under the Bytespider umbrella.

#### Sogou Spider

- **Operator:** Sogou (搜狗, now part of Tencent)
- **User-Agent:** `Sogou web spider` / `Sogou Push Spider`
- **Full User-Agent String:** `Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)`
- **Purpose:** Powers Sogou Search and Sogou AI Search features. Sogou has ~15% Chinese search market share and powers WeChat Search (搜一搜).
- **Impact of Blocking:** Content will not appear in Sogou search or WeChat Search results.
- **Recommendation:** **ALLOW** — WeChat Search integration makes this critical for brands relying on WeChat ecosystem visibility.

---

### Tier 2: Important for CN AI Ecosystem (RECOMMEND: ALLOW)

#### 360Spider

- **Operator:** 360 (Qihoo 360)
- **User-Agent:** `360Spider`
- **Full User-Agent String:** `Mozilla/5.0 (compatible; 360Spider/1.0; +http://www.360.cn/)`
- **Purpose:** Powers 360 Search (好搜) and 360's AI products. ~8-10% CN search market share.
- **Impact of Blocking:** Content will not appear in 360 Search results.
- **Recommendation:** **ALLOW** — 360 remains a meaningful CN search channel. Lower priority than Baidu but no downside to allowing.

#### YisouSpider

- **Operator:** Alibaba
- **User-Agent:** `YisouSpider`
- **Full User-Agent String:** `Mozilla/5.0 (compatible; YisouSpider; +http://www.yisou.com/)`
- **Purpose:** Powers Alibaba's Yisou Search (一搜) and Quark browser search. Alibaba's AI products (Qwen, Tongyi Qianwen) also use this data.
- **Impact of Blocking:** Content may not appear in Quark browser search or Alibaba AI responses.
- **Recommendation:** **ALLOW** — Quark has significant mobile browser market share in China. Relevant for Qwen AI ecosystem presence.

---

### Tier 3: Training / Specialized Crawlers (CONTEXT-DEPENDENT)

#### Bingbot (in CN context)

- **Operator:** Microsoft
- **User-Agent:** `Bingbot`
- **Purpose:** Powers Bing Search and Copilot in China. Bing is accessible in China and has ~3-5% market share.
- **Recommendation:** **CONTEXT-DEPENDENT** — Allow if targeting CN users who use Copilot/Bing. Bing is legally accessible in China.

#### Googlebot (in CN context)

- **Operator:** Google
- **User-Agent:** `Googlebot`
- **Purpose:** Google Search (limited CN availability). Google-Extended controls Gemini training access.
- **Recommendation:** **CONTEXT-DEPENDENT** — Allow if targeting global audience from a `.cn` domain. Googlebot has limited direct impact on CN users but matters for global+CN hybrid sites.

---

## Recommendation Matrix Summary (CN)

| Crawler | Tier | Recommendation | Reason |
|---|---|---|---|
| BaiduSpider | 1 | **ALLOW** | Powers Baidu Search + Baidu AI (65% CN market) |
| Bytespider | 1 | **ALLOW** | Powers Doubao AI + Douyin search (100M+ users) |
| Sogou Spider | 1 | **ALLOW** | Powers WeChat Search + Sogou AI |
| 360Spider | 2 | **ALLOW** | 360 Search (~8-10% CN share) |
| YisouSpider | 2 | **ALLOW** | Alibaba's Quark browser + Qwen AI |
| Bingbot | 3 | Context | Bing/Copilot accessible in CN |
| Googlebot | 3 | Context | Limited CN reach |

### Maximum CN AI Visibility Configuration (robots.txt)

```
# CN AI Crawlers — ALLOWED for CN AI search visibility
User-agent: BaiduSpider
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Sogou web spider
Allow: /

User-agent: 360Spider
Allow: /

User-agent: YisouSpider
Allow: /

# Global crawlers for hybrid sites
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

# All other crawlers blocked
User-agent: *
Disallow: /
```

---

## CN-Specific Analysis Procedure Adjustments

### Step 1 Addition: Baidu-Specific robots.txt Directives

Check for Baidu-specific directives in robots.txt:
- `Baiduspider` specific Allow/Disallow rules
- Crawl-delay for BaiduSpider (recommended: 1-5 seconds)
- Baidu understands `Sitemap:` directive — ensure sitemap is declared

### Step 2 Addition: Baidu Meta Tags

Check for Baidu-specific meta tags:
- `<meta name="applicable-device" content="pc,mobile">` — device adaptation
- `<meta http-equiv="Cache-Control" content="no-transform">` — prevent proxy transformation
- `<meta name="baidu-site-verification" content="code-xxx">` — Baidu Webmaster verification

### Step 5 Addition: CN JavaScript Rendering

CN AI crawlers have distinct JS rendering capabilities:
- BaiduSpider: Basic JavaScript rendering, improving with their new Spider 2.0
- Bytespider: Limited JS rendering — prefers static HTML
- Sogou Spider: Moderate JS rendering
- 360Spider: Limited JS rendering

SSR/SSG is strongly recommended for CN AI crawler compatibility.

---

## CN Scoring Adjustment

| Component | Weight (CN) | Scoring |
|---|---|---|
| Tier 1 CN Crawlers Allowed | 50% | 33 points per Tier 1 crawler allowed (3 crawlers = 100 points max, scaled to 50) |
| Tier 2 CN Crawlers Allowed | 25% | 50 points per Tier 2 crawler allowed (2 crawlers = 100 points max, scaled to 25) |
| No Blanket AI Blocks | 15% | Full points if CN crawlers are explicitly allowed |
| CN-Specific Files Present | 10% | 5 points for Baidu verification, 5 points for applicable-device meta tag |

Output file: `GEO-CRAWLER-ACCESS-CN.md`
