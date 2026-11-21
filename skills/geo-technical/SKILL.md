---
name: geo-technical
description: Technical SEO audit with GEO-specific checks — crawlability, indexability, security, performance, SSR, and AI crawler access
version: 1.0.0
author: geo-seo-claude
tags: [geo, technical-seo, core-web-vitals, ssr, crawlability, security, performance]
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
---

<!-- GEO-CN-VARIANT:v1 -->

**Conditional CN variant.** Only when `REGION` resolves to `cn`, read the sibling `SKILL.cn.md` alongside this file and apply its overrides; its CN knowledge files are enumerated in the geo skill's `regions/cn-variants.json` (self-locating resolution is documented in `geo/SKILL.md` → "CN variant loading"). For `global` or any non-CN region, do NOT load `SKILL.cn.md` or any `regions/cn/` file.

# GEO Technical SEO Audit

## Purpose

Technical SEO forms the foundation of both traditional search visibility and AI search citation. A technically broken site cannot be crawled, indexed, or cited by any platform. This skill audits 8 categories of technical health with specific attention to GEO requirements — most critically, **server-side rendering** (AI crawlers do not execute JavaScript) and **AI crawler access** (many sites inadvertently block AI crawlers in robots.txt).

## How to Use This Skill

1. Collect the target URL (homepage + 2-3 key inner pages)
2. Fetch each page using curl/WebFetch to get raw HTML and HTTP headers
3. Run through each of the 8 audit categories below
4. Score each category using the rubric
5. Generate GEO-TECHNICAL-AUDIT.md with results

---

## Category 1: Crawlability (15 points)

### 1.1 robots.txt Validity
- Fetch `https://[domain]/robots.txt`
- Check for syntactic validity: proper `User-agent`, `Allow`, `Disallow` directives
- Check for common errors: missing User-agent, wildcards blocking important paths, Disallow: / blocking entire site
- Verify XML sitemap is referenced: `Sitemap: https://[domain]/sitemap.xml`

### 1.2 AI Crawler Access (CRITICAL for GEO)
Check robots.txt for directives targeting these AI crawlers:

| Crawler | User-Agent | Platform |
|---|---|---|
| GPTBot | GPTBot | ChatGPT / OpenAI |
| Google-Extended | Google-Extended | Gemini / Google AI training |
| Googlebot | Googlebot | Google Search + AI Overviews |
| Bingbot | bingbot | Bing Copilot + ChatGPT (via Bing) |
| PerplexityBot | PerplexityBot | Perplexity AI |
| ClaudeBot | ClaudeBot | Anthropic Claude |
| Amazonbot | Amazonbot | Alexa / Amazon AI |
| CCBot | CCBot | Common Crawl (used by many AI models) |
| FacebookBot | FacebookExternalHit | Meta AI |
| Bytespider | Bytespider | TikTok / ByteDance AI |
| Applebot-Extended | Applebot-Extended | Apple Intelligence |

**Scoring for AI crawler access:**
- All major AI crawlers allowed: 5 points
- Some blocked but Googlebot + Bingbot allowed: 3 points
- GPTBot or PerplexityBot blocked: 1 point (significant GEO impact)
- Googlebot blocked: 0 points (fatal)

**Important nuance**: Blocking Google-Extended does NOT block Googlebot. Google-Extended only controls AI training data usage, not search indexing. However, blocking Google-Extended may reduce presence in AI Overviews. Recommend allowing Google-Extended unless there is a specific data licensing concern.

### 1.3 XML Sitemaps
- Fetch sitemap (check robots.txt for location, or try `/sitemap.xml`, `/sitemap_index.xml`)
- Validate XML syntax
- Check for `<lastmod>` dates (should be present and accurate)
- Count URLs — compare to expected number of indexable pages
- Check for sitemap index if large site (50,000+ URLs per sitemap max)
- Verify all sitemap URLs return 200 status codes (sample check)

### 1.4 Crawl Depth
- Homepage = depth 0. Check that all important pages are reachable within **3 clicks** (depth 3)
- Pages at depth 4+ receive significantly less crawl budget and are less likely to be cited by AI
- Check internal linking: are key content pages linked from the homepage or main navigation?

### 1.5 Noindex Management
- Check for `<meta name="robots" content="noindex">` on pages that SHOULD be indexed
- Check for `X-Robots-Tag: noindex` HTTP headers
- Common mistakes: noindex on paginated pages, category pages, or key landing pages

**Category Scoring:**
| Check | Points |
|---|---|
| robots.txt valid and complete | 3 |
| AI crawlers allowed | 5 |
| XML sitemap present and valid | 3 |
| Crawl depth within 3 clicks | 2 |
| No erroneous noindex directives | 2 |

---

## Category 2: Indexability (12 points)

### 2.1 Canonical Tags
- Every indexable page must have a `<link rel="canonical" href="...">` tag
- Canonical must point to itself (self-referencing) for the authoritative version
- Check for conflicting canonicals (canonical in HTML vs. HTTP header)
- Check for canonical chains (A canonicals to B, B canonicals to C — should be A to C)

### 2.2 Duplicate Content
- Check for www vs. non-www (both should resolve, one should redirect)
- Check for HTTP vs. HTTPS (HTTP should redirect to HTTPS)
- Check for trailing slash consistency (pick one pattern and redirect the other)
- Check for parameter-based duplicates (`?sort=price` creating duplicate pages)

### 2.3 Pagination
- If paginated content exists, check for `rel="next"` / `rel="prev"` (note: Google ignores these as of 2019, but Bing still uses them)
- Preferred: use `rel="canonical"` on paginated pages pointing to a view-all page or the first page
- Ensure paginated pages are not noindexed if they contain unique content

### 2.4 Hreflang (international sites)
- Check for `<link rel="alternate" hreflang="xx">` tags
- Validate: reciprocal hreflang (if page A points to page B, B must point back to A)
- Validate: x-default fallback exists
- Check for language/region code validity (ISO 639-1 / ISO 3166-1)

### 2.5 Index Bloat
- Estimate number of indexed pages (check sitemap count, use `site:domain.com` estimate)
- Compare indexed pages to actual valuable content pages
- Flag if indexed pages significantly exceed content pages (index bloat from thin/duplicate/parameter pages)

**Category Scoring:**
| Check | Points |
|---|---|
| Canonical tags correct on all pages | 3 |
| No duplicate content issues | 3 |
| Pagination handled correctly | 2 |
| Hreflang correct (if applicable) | 2 |
| No index bloat | 2 |

---

## Category 3: Security (10 points)

### 3.1 HTTPS Enforcement
- Site must load over HTTPS
- HTTP must redirect to HTTPS (301 redirect)
- No mixed content warnings (HTTP resources on HTTPS pages)
- SSL/TLS certificate must be valid and not expired

### 3.2 Security Headers
Check HTTP response headers for:

| Header | Required Value | Purpose |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Forces HTTPS |
| `Content-Security-Policy` | Appropriate policy | Prevents XSS |
| `X-Content-Type-Options` | `nosniff` | Prevents MIME sniffing |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Prevents clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` or stricter | Controls referrer data |
| `Permissions-Policy` | Appropriate restrictions | Controls browser features |

**Category Scoring:**
| Check | Points |
|---|---|
| HTTPS enforced with valid cert | 4 |
| HSTS header present | 2 |
| X-Content-Type-Options | 1 |
| X-Frame-Options | 1 |
| Referrer-Policy | 1 |
| Content-Security-Policy | 1 |

---

## Category 4: URL Structure (8 points)

### 4.1 Clean URLs
- URLs should be human-readable: `/blog/seo-guide` not `/blog?id=12345`
- No session IDs in URLs
- Lowercase only (no mixed case)
- Hyphens for word separation (not underscores)
- No special characters or encoded spaces

### 4.2 Logical Hierarchy
- URL path should reflect site architecture: `/category/subcategory/page`
- Flat where appropriate — avoid unnecessarily deep nesting
- Consistent pattern across the site

### 4.3 Redirect Chains
- Check for redirect chains (A redirects to B redirects to C)
- Maximum 1 hop recommended (A redirects to C directly)
- Check for redirect loops
- All redirects should be 301 (permanent), not 302 (temporary), unless intentionally temporary

### 4.4 Parameter Handling
- URL parameters should not create duplicate indexable pages
- Use canonical tags or `robots.txt` Disallow for parameter variations
- Configure parameter handling in Google Search Console and Bing Webmaster Tools

**Category Scoring:**
| Check | Points |
|---|---|
| Clean, readable URLs | 2 |
| Logical hierarchy | 2 |
| No redirect chains (max 1 hop) | 2 |
| Parameter handling configured | 2 |

---

## Category 5: Mobile Optimization (10 points)

### Critical Context
As of **July 2024**, Google crawls ALL sites exclusively with mobile Googlebot. There is no desktop crawling. If your site does not work on mobile, it does not work for Google. Period.

### 5.1 Responsive Design
- Check for `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Content must not require horizontal scrolling on mobile
- No fixed-width layouts wider than viewport

### 5.2 Tap Targets
- Interactive elements (buttons, links) must be at least 48x48 CSS pixels
- Minimum 8px spacing between tap targets
- Check that navigation is usable on mobile

### 5.3 Font Sizes
- Base font size should be at least 16px
- No text requiring zoom to read
- Sufficient contrast ratio (WCAG AA: 4.5:1 for normal text, 3:1 for large text)

### 5.4 Mobile Content Parity
- All content visible on desktop must also be visible on mobile
- No hidden content behind "read more" toggles that Googlebot cannot expand (though Google has improved at expanding these as of 2025)
- Images and media must load on mobile

**Category Scoring:**
| Check | Points |
|---|---|
| Viewport meta tag correct | 3 |
| Responsive layout (no horizontal scroll) | 3 |
| Tap targets appropriately sized | 2 |
| Font sizes legible | 2 |

---

## Category 6: Core Web Vitals (15 points)

### 2026 Metrics and Thresholds
Core Web Vitals use the **75th percentile** of real user data (field data) as the benchmark. Lab data is useful for debugging but field data determines the ranking signal.

| Metric | Good | Needs Improvement | Poor | Notes |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s | Measures loading — time until largest visible element renders |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms | Replaced FID in March 2024. Measures ALL interactions, not just first |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 | Measures visual stability — unexpected layout movements |

### How to Assess Without CrUX Data
When real user data is unavailable, estimate from page characteristics:
- **LCP**: Check largest above-fold element. Is it an image (check size/format)? Is it text (check web font loading)? Server response time (TTFB)?
- **INP**: Check for heavy JavaScript on page. Long tasks (>50ms) block interactivity. Check for third-party scripts.
- **CLS**: Check for images without explicit width/height. Check for dynamically inserted content above the fold. Check for web fonts causing layout shift (FOUT/FOIT).

### Common LCP Fixes
1. Optimize hero images: WebP/AVIF format, correct sizing, preload with `<link rel="preload">`
2. Reduce server response time (TTFB < 800ms)
3. Eliminate render-blocking CSS/JS
4. Preconnect to critical third-party origins

### Common INP Fixes
1. Break up long tasks (>50ms) into smaller chunks using `requestIdleCallback` or `scheduler.yield()`
2. Reduce third-party JavaScript
3. Use `content-visibility: auto` for off-screen content
4. Debounce/throttle event handlers

### Common CLS Fixes
1. Always include `width` and `height` attributes on images and videos
2. Reserve space for ads and embeds with CSS `aspect-ratio` or explicit dimensions
3. Use `font-display: swap` with size-adjusted fallback fonts
4. Avoid inserting content above existing content after page load

**Category Scoring:**
| Check | Points |
|---|---|
| LCP < 2.5s | 5 |
| INP < 200ms | 5 |
| CLS < 0.1 | 5 |

---

## Category 7: Server-Side Rendering (15 points) — CRITICAL FOR GEO

### Why SSR Is Mandatory for AI Visibility
AI crawlers (GPTBot, PerplexityBot, ClaudeBot, etc.) do **NOT execute JavaScript**. They fetch the raw HTML and parse it. If your content is rendered client-side by React, Vue, Angular, or any other JavaScript framework, AI crawlers see an empty page.

Even Googlebot, which does execute JavaScript, deprioritizes JS-rendered content due to the additional crawl budget required. Google processes JS rendering in a separate "rendering queue" that can delay indexing by days or weeks.

### Detection Method
1. Fetch the page with curl (no JavaScript execution): `curl -s [URL]`
2. Compare the raw HTML from curl to the rendered DOM that a browser would produce (no browser binary required)
3. If key content (headings, paragraphs, product info, article text) is MISSING from the curl output, the site relies on client-side rendering

### What to Check
- **Main content text**: Is the article body / product description / page content in the raw HTML?
- **Headings**: Are H1, H2, H3 tags present in raw HTML?
- **Navigation**: Is the main navigation server-rendered?
- **Structured data**: Is JSON-LD in the raw HTML or injected by JavaScript?
- **Meta tags**: Are title, description, canonical, OG tags in the raw HTML?
- **Internal links**: Are navigation and content links in the raw HTML? (Critical for crawlability)

### SSR Solutions to Recommend
| Framework | SSR Solution |
|---|---|
| React | Next.js (SSR/SSG), Remix, Gatsby (SSG) |
| Vue | Nuxt.js (SSR/SSG) |
| Angular | Angular Universal |
| Svelte | SvelteKit |
| Generic | Prerender.io (prerendering service), Rendertron |

### Scoring Detail
- All key content server-rendered: 15 points
- Main content server-rendered but some elements JS-only: 10 points
- Critical content requires JS (product info, article text): 5 points
- Entire page is client-rendered (empty body in raw HTML): 0 points

**Category Scoring:**
| Check | Points |
|---|---|
| Main content in raw HTML | 8 |
| Meta tags + structured data in raw HTML | 4 |
| Internal links in raw HTML | 3 |

---

## Category 8: Page Speed & Server Performance (15 points)

### 8.1 Time to First Byte (TTFB)
- Target: **< 800ms** (ideally < 200ms)
- Measure with curl: `curl -o /dev/null -s -w 'TTFB: %{time_starttransfer}s\n' [URL]`
- If TTFB > 800ms: check server location, caching, database queries, CDN usage

### 8.2 Resource Optimization
- Total page weight target: **< 2MB** (critical pages < 1MB)
- Check for uncompressed resources (gzip/brotli compression should be enabled)
- Check for unminified CSS and JavaScript
- Check for unused CSS/JS (can represent 50%+ of downloaded bytes on many sites)

### 8.3 Image Optimization
- Check image formats: WebP or AVIF preferred over JPEG/PNG
- Check for oversized images (images larger than display size)
- Check for lazy loading: images below fold should have `loading="lazy"`
- Check for explicit dimensions (width/height attributes prevent CLS)
- Above-fold images should NOT be lazy loaded (harms LCP)

### 8.4 Code Splitting and Lazy Loading
- JavaScript should be code-split so each page only loads what it needs
- Check for large JavaScript bundles (> 200KB compressed is a warning, > 500KB is critical)
- Third-party scripts should load asynchronously (`async` or `defer`)
- Check for render-blocking resources in `<head>`

### 8.5 Caching
- Check `Cache-Control` headers on static resources (images, CSS, JS)
- Static assets should have long cache times: `max-age=31536000` (1 year) with content-hashed filenames
- HTML pages should have shorter cache or `no-cache` with validation (`ETag` or `Last-Modified`)

### 8.6 CDN Usage
- Check if static resources are served from a CDN (different domain or CDN-specific headers)
- For global audience, CDN is critical for consistent performance
- Check for CDN-specific headers: `CF-Ray` (Cloudflare), `X-Cache` (AWS CloudFront), `X-Served-By` (Fastly)

**Category Scoring:**
| Check | Points |
|---|---|
| TTFB < 800ms | 3 |
| Page weight < 2MB | 2 |
| Images optimized (format, size, lazy) | 3 |
| JS bundles reasonable (< 200KB compressed) | 2 |
| Compression enabled (gzip/brotli) | 2 |
| Cache headers on static resources | 2 |
| CDN in use | 1 |

---

## Category 9: Agent-Readiness Signals (non-scoring)

These checks surface emerging AI agent compatibility signals. None contribute to the numeric score — they produce a pass or a recommendation. The underlying standards are either IETF drafts or early-adoption features; penalizing absence would be unfair.

### 9.1 RFC 8288 Link Headers (Service Discovery)

RFC 8288 (Web Linking) defines the HTTP `Link:` response header. Servers can use it to advertise related resources — API catalog, service docs, MCP server card — in a machine-readable way, without HTML parsing.

**How to check:** Capture all `Link:` response headers from the standard homepage fetch (no extra request).

**What to look for:**
- Parse `<url>; rel="relation-type"` pairs.
- High-value rel types: `api-catalog` (RFC 9609), `describedby`, `service-doc`, `mcp-server-card`.

**When to surface a recommendation:** Only for API-first sites (API docs linked in nav, `/api/` or `/developers/` paths, swagger/OpenAPI in sitemap). Omit this section entirely for standard business sites — absence is expected and not noteworthy.

| State | Treatment |
|---|---|
| `Link:` headers present, known rel types | Informational — document what was found |
| `Link:` headers present, unknown rel types | Informational — note and explain |
| Absent, API-first site | Recommendation — explain and suggest implementation |
| Absent, standard business site | Omit — do not surface |

### 9.2 Markdown Content Negotiation

Checks if the server responds to `Accept: text/markdown` with `Content-Type: text/markdown`. Cloudflare's "Markdown for Agents" feature enables this — AI agents receive clean Markdown instead of HTML, eliminating boilerplate stripping and improving content extraction accuracy.

**How to check:** Send a GET to the homepage with `Accept: text/markdown`. This is one additional HTTP request per audit.

**Evaluation:**
- If response `Content-Type` is `text/markdown` (or `text/markdown; charset=utf-8`): pass — note as a leading-edge capability.
- Otherwise: forward-looking recommendation, not a failure.
- If the request errors or returns non-200: skip and note the error. Do not penalize.

| State | Treatment |
|---|---|
| `text/markdown` returned | Bonus — note as a leading-edge capability |
| Standard HTML returned | Forward-looking recommendation |
| Request errors / non-200 | Skip, note the error, do not penalize |

---

## IndexNow Protocol

### What It Is
IndexNow is an open protocol that allows websites to notify search engines instantly when content is created, updated, or deleted. Supported by Bing, Yandex, Seznam, and Naver. Google does NOT support IndexNow but monitors the protocol.

### Why It Matters for GEO
ChatGPT uses Bing's index. Bing Copilot uses Bing's index. Faster Bing indexing means faster AI visibility on two major platforms.

### Implementation Check
1. Check for IndexNow key file: `https://[domain]/.well-known/indexnow-key.txt` or similar
2. Check if CMS has IndexNow plugin (WordPress: IndexNow plugin; many modern CMS platforms support it natively)
3. If not implemented, recommend adding it with instructions

---

## Overall Scoring

| Category | Max Points | Weight |
|---|---|---|
| Crawlability | 15 | Core foundation |
| Indexability | 12 | Core foundation |
| Security | 10 | Trust signal |
| URL Structure | 8 | Crawl efficiency |
| Mobile Optimization | 10 | Google requirement |
| Core Web Vitals | 15 | Ranking signal |
| Server-Side Rendering | 15 | GEO critical |
| Page Speed & Server | 15 | Performance |
| **Total** | **100** | |

Non-scoring checks (Category 9) appear in the output under "Agent-Readiness Signals" and do not affect this total.

### Score Interpretation
- **90-100**: Excellent — technically sound for both traditional SEO and GEO
- **70-89**: Good — minor issues to address but fundamentally solid
- **50-69**: Needs Work — significant technical debt impacting visibility
- **30-49**: Poor — major issues blocking crawling, indexing, or AI visibility
- **0-29**: Critical — fundamental technical failures requiring immediate attention

---

## Output Format

Generate **GEO-TECHNICAL-AUDIT.md** with:

```markdown
# GEO Technical SEO Audit — [Domain]
Date: [Date]

## Technical Score: XX/100

## Score Breakdown
| Category | Score | Status |
|---|---|---|
| Crawlability | XX/15 | Pass/Warn/Fail |
| Indexability | XX/12 | Pass/Warn/Fail |
| Security | XX/10 | Pass/Warn/Fail |
| URL Structure | XX/8 | Pass/Warn/Fail |
| Mobile Optimization | XX/10 | Pass/Warn/Fail |
| Core Web Vitals | XX/15 | Pass/Warn/Fail |
| Server-Side Rendering | XX/15 | Pass/Warn/Fail |
| Page Speed & Server | XX/15 | Pass/Warn/Fail |

Status: Pass = 80%+ of category points, Warn = 50-79%, Fail = <50%

## AI Crawler Access
| Crawler | User-Agent | Status | Recommendation |
|---|---|---|---|
| GPTBot | GPTBot | Allowed/Blocked | [Action] |
| Googlebot | Googlebot | Allowed/Blocked | [Action] |
[Continue for all AI crawlers]

## Critical Issues (fix immediately)
[List with specific page URLs and what is wrong]

## Warnings (fix this month)
[List with details]

## Recommendations (optimize this quarter)
[List with details]

## Agent-Readiness Signals (non-scoring)

### RFC 8288 Link Headers (Service Discovery)

**Status:** Present / Absent / Not Applicable

<!-- If present: -->
| Relation Type | URL | Meaning |
|---|---|---|
| api-catalog | /.well-known/api-catalog | Machine-readable index of available APIs |
| mcp-server-card | /.well-known/mcp.json | MCP server capability declaration |

AI agents and API clients can discover your services without parsing HTML.

<!-- If absent, API-first site only: -->
**Informational Recommendation:** This site has API/developer-oriented content but no `Link:` headers advertising discoverable services.

Example: `Link: </.well-known/api-catalog>; rel="api-catalog"`

Relevant for: sites with public APIs, OpenAPI docs, or MCP server integrations.
Reference: RFC 8288, RFC 9609.

<!-- If absent, standard business site: omit this section entirely -->

### Markdown Content Negotiation

**Status:** Supported / Not Supported
**Test:** GET [url] with `Accept: text/markdown`
**Response Content-Type:** [value]

<!-- If supported: -->
This site serves clean Markdown to AI agents on request. AI crawlers that support content negotiation receive formatted text without HTML boilerplate.

<!-- If not supported: -->
**Forward-Looking Recommendation:** Cloudflare Workers/Pages sites can enable Markdown content negotiation with a one-line configuration change. When an AI agent sends `Accept: text/markdown`, the server responds with clean Markdown instead of HTML.

- Currently Cloudflare-specific
- Relevant for: sites already on Cloudflare infrastructure
- Other CDNs and frameworks expected to adopt this pattern as AI agent traffic grows

## Detailed Findings
[Per-category breakdown with evidence]
```

---

## Parallel Audit Worker Execution Contract

The following block is the executable phase-2 worker instruction for `geo-technical`, carried over verbatim from the former `agents/geo-technical.md`. It is loaded into one of five concurrent tasks during `/geo audit`; its Region Awareness, Execution Steps, and Output Format sections are authoritative for that worker's report. The methodology rubric above remains the reference scoring rubric and is not replaced by this contract.

# GEO Technical SEO Agent

You are a technical SEO specialist. Your job is to analyze a target URL for technical health factors that affect both traditional search engines and AI crawlers. AI crawlers generally do NOT execute JavaScript, making server-side rendering and HTML content accessibility critical. You produce a structured report section covering all technical dimensions.

## Region Awareness

This agent adjusts its technical checks based on the target region (passed as REGION in task description).

- **Global (default)**: Standard Western-focused technical checks, hreflang validation for multi-region sites
- **China (cn)**: In addition to standard checks:
  - Check for ICP (Internet Content Provider) license in footer — required for China-hosted sites
  - Check Baidu crawlers (BaiduSpider) access in robots.txt alongside Western bots
  - Check for CDN/ hosting within mainland China (required for fast performance in CN)
  - Check for Baidu-specific meta tags (baidu-site-verification)
  - Check if site uses a .cn domain and whether it's blocked outside China (Great Firewall considerations)
  - For hreflang: validate CN-specific language codes (zh-CN, zh-Hans)
  - Master technical checklist: The geo-technical / schema master source article `Mh-fwA8Vmrt-KaujrzkJ8Q` is attributed in `regions/cn/provenance.md` (master checklists section); it was not spot-checked and has no dedicated themed doc, so treat it as `UNVERIFIED`, reported only, do not change scoring

## Execution Steps

### Step 1: Fetch Page HTML and Response Headers

- Use WebFetch to retrieve the target URL.
- Capture and record HTTP response headers, paying attention to:
  - Status code (200, 301, 302, 404, etc.)
  - Content-Type header
  - Cache-Control and ETag headers
  - X-Robots-Tag header (can override meta robots)
  - Server header (technology identification)
  - Content-Encoding (compression: gzip, br)
  - `Link:` headers — capture all values for RFC 8288 service discovery analysis (Step 10)

### Step 2: Robots.txt and XML Sitemap

**Robots.txt:**
- Fetch `/robots.txt` from the domain root.
- Check for:
  - Default User-agent rules (`User-agent: *`)
  - Specific bot rules (Googlebot, Bingbot, and AI crawlers)
  - If REGION is `cn` or TLD is `.cn`: also check BaiduSpider, Sogou, 360Spider rules
  - Disallow patterns that may unintentionally block important content
  - Crawl-delay directives (can slow indexing)
  - Sitemap references
  - Syntax errors or formatting issues

**XML Sitemap:**
- Check for sitemap at locations referenced in robots.txt, or at `/sitemap.xml` and `/sitemap_index.xml`.
- If found, validate:
  - Proper XML formatting
  - Presence of `<lastmod>` dates (and whether they appear accurate/recent)
  - URL count (note if very large or very small relative to likely site size)
  - Does the target URL appear in the sitemap?

### Step 3: Meta Tags Analysis

Extract and evaluate all SEO-relevant meta tags from the page HTML:

| Meta Tag | Check | Issue if Missing/Wrong |
|---|---|---|
| `<title>` | Present, 50-60 characters, includes primary keyword | Missing title = no search snippet control |
| `<meta name="description">` | Present, 150-160 characters, compelling, includes keyword | Missing = Google generates its own |
| `<link rel="canonical">` | Present, self-referencing or pointing to preferred version | Missing = potential duplicate content |
| `<meta name="robots">` | Check for noindex, nofollow, noarchive, nosnippet, max-snippet | noindex = page excluded from search |
| `<meta name="viewport">` | Present with `width=device-width, initial-scale=1` | Missing = mobile usability failure |
| `<html lang="...">` | Present with correct language code | Missing = language detection issues |
| Open Graph tags | og:title, og:description, og:image, og:url, og:type | Missing = poor social/AI preview |
| Twitter Card tags | twitter:card, twitter:title, twitter:description, twitter:image | Missing = poor X/Twitter preview |
| `<link rel="alternate" hreflang="...">` | Present if multilingual site | Missing on multilingual = wrong language served |

### Step 4: Security Headers

Check for the presence and correctness of security headers:

| Header | Expected Value | Risk if Missing |
|---|---|---|
| HTTPS | Site loads over HTTPS | HTTP = browser warnings, ranking penalty |
| Strict-Transport-Security (HSTS) | `max-age=31536000; includeSubDomains` | Missing = vulnerable to downgrade attacks |
| Content-Security-Policy (CSP) | Defined policy restricting sources | Missing = XSS vulnerability risk |
| X-Frame-Options | `DENY` or `SAMEORIGIN` | Missing = clickjacking vulnerability |
| X-Content-Type-Options | `nosniff` | Missing = MIME-type sniffing attacks |
| Referrer-Policy | `strict-origin-when-cross-origin` or stricter | Missing = referrer data leakage |
| Permissions-Policy | Restricts browser feature access | Missing = feature abuse risk |

Score deductions:
- No HTTPS: -30 points (critical)
- No HSTS: -10 points
- No CSP: -10 points
- No X-Frame-Options: -5 points
- No X-Content-Type-Options: -5 points
- No Referrer-Policy: -5 points
- No Permissions-Policy: -3 points

### Step 5: URL Structure

Evaluate the target URL and observable site URL patterns:

**Criteria:**
- Clean, readable URLs (no excessive parameters, session IDs, or hash fragments)
- Descriptive slugs containing relevant keywords
- Logical hierarchy reflecting site structure (e.g., `/category/subcategory/page`)
- Consistent URL format (trailing slashes, www vs. non-www)
- Reasonable URL length (under 100 characters preferred)
- Lowercase only (no mixed case)
- Hyphens for word separation (no underscores)
- No unnecessary nesting depth (more than 4 levels deep is a concern)

**Score (0-100):**
- Clean, descriptive, hierarchical: 80-100
- Minor issues (length, slight inconsistency): 60-79
- Significant issues (parameters, no hierarchy): 40-59
- Problematic (session IDs, excessive depth, unreadable): 0-39

### Step 6: Mobile Optimization

Analyze the HTML source for mobile optimization signals:

- `<meta name="viewport">` tag present and correctly configured
- Responsive design indicators in CSS/HTML:
  - Media queries present in inline/linked stylesheets
  - Flexible layout patterns (flexbox, grid, percentage widths)
  - Responsive images (`srcset`, `sizes` attributes, `<picture>` element)
- Touch-friendly indicators:
  - Button/link sizing (minimum 44x44px touch targets)
  - No reliance on hover-only interactions in visible markup
- No horizontal scroll indicators (fixed-width elements wider than viewport)
- Font size adequacy (base font size >= 16px for mobile readability)

### Step 7: Core Web Vitals Assessment

Assess Core Web Vitals risk from HTML source analysis. Note: This is a static analysis from HTML; actual field data requires CrUX or PageSpeed Insights.

**Largest Contentful Paint (LCP) Risk Indicators:**
- Large hero images without `loading="lazy"` or `fetchpriority="high"`
- Render-blocking CSS/JS in `<head>` (stylesheets without `media` attribute, scripts without `async`/`defer`)
- Web fonts loaded without `font-display: swap` or `font-display: optional`
- No preload hints for critical resources (`<link rel="preload">`)
- Large above-the-fold images without width/height attributes or explicit sizing

**Interaction to Next Paint (INP) Risk Indicators:**
NOTE: INP replaced FID (First Input Delay) as a Core Web Vital in March 2024.
- Heavy JavaScript bundles in `<head>` without `defer` or `async`
- Large number of synchronous script tags
- Complex DOM structure (deep nesting, excessive element count)
- Third-party scripts loaded synchronously (analytics, ads, widgets)
- Event handlers visible in HTML (onclick, etc.) suggesting heavy JS interaction layer

**Cumulative Layout Shift (CLS) Risk Indicators:**
- Images without explicit `width` and `height` attributes
- Embeds/iframes without dimensions
- Dynamically injected content above the fold (ad slots, banners)
- Web fonts that may cause text reflow (no `font-display` property)
- No `aspect-ratio` CSS or dimension attributes on media elements

**Risk Rating per Vital:**
- Low Risk: Few or no indicators found
- Medium Risk: Some indicators present
- High Risk: Multiple indicators found

### Step 8: Server-Side Rendering and JavaScript Dependency (CRITICAL)

This is the most important check for GEO. AI crawlers (GPTBot, ClaudeBot, PerplexityBot) generally do NOT execute JavaScript. Content that requires JS to render is invisible to AI search.

**Check for Client-Side Rendering Indicators:**
- Empty or minimal `<body>` content with a single root div (e.g., `<div id="root"></div>` or `<div id="app"></div>`)
- Presence of client-side framework bundles without SSR signals:
  - React: `bundle.js`, `main.js` with empty body
  - Vue: `app.js` with `<div id="app">`
  - Angular: `main.js` with `<app-root>`
  - Next.js/Nuxt: Check for `__NEXT_DATA__` or `__NUXT__` scripts (these indicate SSR IS in use)
- `<noscript>` tags containing fallback content (suggests JS-dependent primary content)
- Content loaded via API calls (look for fetch/XHR patterns in inline scripts)

**Check for Server-Side Rendering Signals:**
- Full HTML content present in the initial response (paragraphs, headings, text content visible in raw HTML)
- `__NEXT_DATA__` script tag (Next.js SSR/SSG)
- `__NUXT__` or `__NUXT_DATA__` (Nuxt.js SSR/SSG)
- `data-reactroot` or `data-server-rendered` attributes
- Full meta tags rendered in initial HTML (not injected by JS)
- Substantial text content in the HTML `<body>` before any script execution

**Severity Assessment:**
- **CRITICAL**: Page body is essentially empty without JS execution. AI crawlers see nothing.
- **HIGH**: Main content is present but significant sections (navigation, sidebar, related content) require JS.
- **MEDIUM**: Core content is server-rendered but interactive elements and secondary content require JS.
- **LOW**: Fully server-rendered. JS enhances but does not create content.

### Step 9: Additional Technical Checks

- **Duplicate content signals**: Check for missing canonical tags, parameter-based URL variations, www/non-www resolution.
- **Redirect chains**: Note if the target URL required redirects to reach (check response codes).
- **Internationalization**: Check for hreflang tags if the site appears multilingual. If REGION is `cn`, validate zh-CN, zh-Hans, zh-Hant language tags.
- **Structured data errors**: Note any JSON-LD syntax issues visible in the source (malformed JSON, missing required fields).
- **Resource hints**: Check for `<link rel="preconnect">`, `<link rel="dns-prefetch">`, `<link rel="preload">` for performance optimization.
- **ICP License (CN sites)**: If REGION is `cn` or TLD is `.cn`, check footer for ICP filing number (e.g., `京ICP备XXXXXXXX号`). Required for China-hosted sites; absence is a compliance issue.
- **Baidu verification (CN)**: Check for `<meta name="baidu-site-verification" content="...">` tag. If missing, recommend adding for Baidu Webmaster Tools.
- **China CDN**: If targeting CN market, check whether the site uses a China-based CDN or hosting. Sites hosted outside China can have 100-300ms+ latency for mainland users.
- **Domain blocking**: If site is on `.com` targeting CN, check whether the site is accessible from mainland China (note: cannot fully verify, but flag as risk).

### Step 10: Agent-Readiness Signals (non-scoring)

These checks do not affect the Technical Score. They surface emerging AI agent compatibility signals.

**RFC 8288 Link Headers (Service Discovery):**
Using the `Link:` headers captured in Step 1 (no extra request needed):
1. Parse all `<url>; rel="relation-type"` pairs.
2. Identify high-value rel types: `api-catalog` (RFC 9609), `describedby`, `service-doc`, `mcp-server-card`.
3. If headers are present: document what was found.
4. If absent: check whether the site is API-first (API docs in nav, `/api/` or `/developers/` paths, OpenAPI in sitemap). Surface a recommendation only if API-first signals are present. Omit entirely for standard business sites.

**Markdown Content Negotiation:**
Send a GET request to the homepage with the header `Accept: text/markdown` (one additional HTTP request):
1. If the response `Content-Type` is `text/markdown` (or `text/markdown; charset=utf-8`): pass — note as a leading-edge capability.
2. If the response is standard HTML: forward-looking recommendation — note that Cloudflare Workers/Pages sites can enable this with a one-line config change.
3. If the request errors or returns non-200: skip and note the error. Do not penalize.

Surface both findings in the output under "Agent-Readiness Signals." Neither affects any existing score.

### Step 11: Calculate Technical Score

Compute the **Technical Score (0-100)** using these category weights:

| Category | Weight | Max Points |
|---|---|---|
| Server-Side Rendering / JS Dependency | 25% | 25 |
| Meta Tags & Indexability | 15% | 15 |
| Crawlability (robots.txt, sitemap) | 15% | 15 |
| Security Headers | 10% | 10 |
| Core Web Vitals Risk | 10% | 10 |
| Mobile Optimization | 10% | 10 |
| URL Structure | 5% | 5 |
| Response Headers & Status | 5% | 5 |
| Additional Checks | 5% | 5 |

SSR/JS Dependency has the highest weight because it is the single biggest factor determining whether AI crawlers can access content.

## Output Format

```markdown
## Technical Foundations

**Technical Score: [X]/100** [Critical/Poor/Fair/Good/Excellent]

### Score Breakdown

| Category | Score | Weight | Weighted | Status |
|---|---|---|---|---|
| Server-Side Rendering | [X]/100 | 25% | [X] | [Flag] |
| Meta Tags & Indexability | [X]/100 | 15% | [X] | [Flag] |
| Crawlability | [X]/100 | 15% | [X] | [Flag] |
| Security Headers | [X]/100 | 10% | [X] | [Flag] |
| Core Web Vitals Risk | [X]/100 | 10% | [X] | [Flag] |
| Mobile Optimization | [X]/100 | 10% | [X] | [Flag] |
| URL Structure | [X]/100 | 5% | [X] | [Flag] |
| Response & Status | [X]/100 | 5% | [X] | [Flag] |
| Additional Checks | [X]/100 | 5% | [X] | [Flag] |

### Server-Side Rendering Assessment

**Status:** [CRITICAL/HIGH/MEDIUM/LOW risk]
**Rendering Type:** [SSR/SSG/CSR/Hybrid]
**Framework Detected:** [Next.js/Nuxt/React SPA/Vue SPA/WordPress/etc.]

[Detailed findings about what AI crawlers can and cannot see]

### Crawlability & Indexability

**Robots.txt:** [Found/Not Found] — [Key findings]
**XML Sitemap:** [Found/Not Found] — [Key findings]
**Meta Robots:** [Indexable/Noindex/Other]
**Canonical:** [Self-referencing/Cross-domain/Missing]

### Meta Tags Audit

| Tag | Status | Value/Issue |
|---|---|---|
| Title | [Present/Missing] | [Value or issue] |
| Description | [Present/Missing] | [Value or issue] |
| Canonical | [Present/Missing] | [Value or issue] |
| Viewport | [Present/Missing] | [Value or issue] |
| Language | [Present/Missing] | [Value or issue] |
| Open Graph | [Complete/Partial/Missing] | [Details] |
| Twitter Card | [Complete/Partial/Missing] | [Details] |

### Security Headers

| Header | Status | Value |
|---|---|---|
| HTTPS | [Yes/No] | |
| HSTS | [Present/Missing] | [Value] |
| CSP | [Present/Missing] | [Summary] |
| X-Frame-Options | [Present/Missing] | [Value] |
| X-Content-Type-Options | [Present/Missing] | [Value] |
| Referrer-Policy | [Present/Missing] | [Value] |

### Core Web Vitals Risk Assessment

| Vital | Risk Level | Indicators Found |
|---|---|---|
| LCP | [Low/Medium/High] | [Key indicators] |
| INP | [Low/Medium/High] | [Key indicators] |
| CLS | [Low/Medium/High] | [Key indicators] |

Note: This is a static HTML analysis. Validate with PageSpeed Insights or CrUX data for field measurements.

### Mobile Optimization

**Status:** [Optimized/Partially Optimized/Not Optimized]
[Key findings]

### URL Structure

**Target URL:** `[URL]`
**Assessment:** [Clean/Minor Issues/Problematic]
[Key findings]

### Agent-Readiness Signals (non-scoring)

#### RFC 8288 Link Headers (Service Discovery)

**Status:** Present / Absent / Not Applicable

<!-- If present: list parsed relation types, URLs, and meaning -->
<!-- If absent on API-first site: surface recommendation with example -->
<!-- If absent on standard business site: omit this section -->

#### Markdown Content Negotiation

**Status:** Supported / Not Supported
**Test:** GET [url] with `Accept: text/markdown`
**Response Content-Type:** [value]

<!-- If supported: note as leading-edge capability -->
<!-- If not supported: forward-looking recommendation, Cloudflare-specific context -->
<!-- If request errored: note the error, skip recommendation -->

### Priority Actions

1. **[CRITICAL]** [Action item — especially SSR/JS issues]
2. **[HIGH]** [Action item]
3. **[HIGH]** [Action item]
4. **[MEDIUM]** [Action item]
5. **[LOW]** [Action item]
```

## Important Notes

- Server-side rendering analysis is the HIGHEST PRIORITY check. If the page is a client-side SPA with no SSR, this is a critical finding that affects the entire GEO audit.
- Core Web Vitals analysis from HTML source is an estimation of risk, not a measurement. Always note that actual measurements require field data.
- INP (Interaction to Next Paint) replaced FID (First Input Delay) as of March 2024. Never reference FID as a current Core Web Vital.
- Security headers are a trust signal for both users and search engines. Missing HTTPS is a critical finding.
- When analyzing meta tags, note both presence and quality. A title tag that exists but is "Home" or "Untitled" is effectively missing.
- AI crawlers respect robots.txt but may handle it differently than traditional crawlers. Note any discrepancies between Googlebot and AI crawler rules.
