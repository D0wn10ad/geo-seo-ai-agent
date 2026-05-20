---
name: geo-audit
description: Full website GEO+SEO audit with parallel subagent delegation. Orchestrates a comprehensive Generative Engine Optimization audit across AI citability, platform analysis, technical infrastructure, content quality, and schema markup. Produces a composite GEO Score (0-100) with prioritized action plan. Supports region-specific scoring (--region cn for China markets).
---

# GEO Audit Orchestration Skill

## Purpose

This skill performs a comprehensive Generative Engine Optimization (GEO) audit of any website. GEO is the practice of optimizing web content so that AI systems (ChatGPT, Claude, Perplexity, Gemini, etc.) can discover, understand, cite, and recommend it. This audit measures how well a site performs across all GEO dimensions and produces an actionable improvement plan.

## Key Insight

Traditional SEO optimizes for search engine rankings. GEO optimizes for AI citation and recommendation. Sites that score high on GEO metrics see 30-115% more visibility in AI-generated responses (Georgia Tech / Princeton / IIT Delhi 2024 study). The two disciplines overlap but have distinct requirements.

---

## Audit Workflow

### Phase 0: Region Detection

**Before any site analysis, determine the target region:**

1. Check for an explicit `--region <code>` argument (e.g. `--region cn`)
2. If not provided, auto-detect from URL TLD (`.cn` → China), HTML `lang` attribute, and dominant content script (CJK, Cyrillic, Latin)
3. If multi-language signals detected, **ask the user**:
   - "1. Global — treat as global English"
   - "2. Global+CN — run both Global and China assessments"
   - "3. CN only — China market only"
4. Set REGION variable (default: `global`)
5. Load region profile from `regions/profiles.yaml` for region-specific scoring weights, AI engines, platforms, and crawler expectations

**When REGION is `cn`:**
- Reference `regions/cn/ai-engines.md` instead of default Western AI engines
- Reference `regions/cn/platforms.md` for brand mention targets
- Reference `regions/cn/schema.md` for schema guidance
- Score weights shift: Brand 30%, Citability 20%, EEAT 15%, Technical 10%, Schema 15%, Platform 10%

---

### Phase 1: Discovery and Reconnaissance

**Step 1: Fetch Homepage and Detect Business Type**

1. Use `fetch_url` to retrieve the homepage at the provided URL.
2. Extract the following signals:
   - Page title, meta description, H1 heading
   - Navigation menu items (reveals site structure)
   - Footer content (reveals business info, location, legal pages)
   - Schema.org markup on homepage (Organization, LocalBusiness, etc.)
   - Pricing page link (SaaS indicator)
   - Product listing patterns (E-commerce indicator)
   - Blog/resource section (Publisher indicator)
   - Service pages (Agency indicator)
   - Address/phone/Google Maps embed (Local business indicator)

3. Classify the business type using these patterns:

| Business Type | Detection Signals |
|---|---|
| **SaaS** | Pricing page, "Sign up" / "Free trial" CTAs, app.domain.com subdomain, feature comparison tables, integration pages |
| **Local Business** | Physical address on homepage, Google Maps embed, "Near me" content, LocalBusiness schema, service area pages |
| **E-commerce** | Product listings, shopping cart, product schema, category pages, price displays, "Add to cart" buttons |
| **Publisher** | Blog-heavy navigation, article schema, author pages, date-based archives, RSS feeds, high content volume |
| **Agency/Services** | Case studies, portfolio, "Our Work" section, team page, client logos, service descriptions |
| **Hybrid** | Combination of above signals -- classify by dominant pattern |

**Step 2: Crawl Sitemap and Internal Links**

1. Attempt to fetch `/sitemap.xml` and `/sitemap_index.xml`.
2. If sitemap exists, extract up to 50 unique page URLs prioritized by:
   - Homepage (always include)
   - Top-level navigation pages
   - High-value pages (pricing, about, contact, key service/product pages)
   - Blog posts (sample 5-10 most recent)
   - Category/landing pages
3. If no sitemap exists, crawl internal links from the homepage:
   - Extract all `<a href>` links pointing to the same domain
   - Follow up to 2 levels deep
   - Prioritize pages linked from main navigation
4. Respect `robots.txt` directives -- do not fetch disallowed paths.
5. Enforce a maximum of 50 pages and a 30-second timeout per fetch.

**Step 3: Collect Page-Level Data**

For each page in the crawl set, record:
- URL, title, meta description, canonical URL
- H1-H6 heading structure
- Word count of main content
- Schema.org types present
- Internal/external link counts
- Images with/without alt text
- Open Graph and Twitter Card meta tags
- Response status code
- Whether the page has structured data

---

### Phase 2: Parallel Subagent Delegation

Delegate analysis to 5 specialized subagents. Each subagent operates on the collected page data and produces a category score (0-100) plus findings.

**Subagent 1: AI Visibility Analysis (geo-ai-visibility)**
- Analyze content blocks for quotability by AI systems (citability scoring)
- Check AI crawler access via robots.txt and llms.txt presence
- Scan brand presence across region-relevant platforms (global: YouTube, Reddit, Wikipedia, LinkedIn; CN: Baidu Baike, Zhihu, WeChat OA, Xiaohongshu, Bilibili, Douyin)
- Score brand authority signals that AI models use for entity recognition
- If REGION is `cn`, use `regions/cn/platforms.md` for platform list

**Subagent 2: Platform Optimization (geo-platform-analysis)**
- Assess readiness for region-specific AI engines (global: ChatGPT, Perplexity, Gemini, Copilot; CN: Baidu AI, Doubao, ERNIE, Qwen, Kimi, DeepSeek)
- Check platform-specific ranking factors and optimization opportunities
- If REGION is `cn`, use `regions/cn/ai-engines.md` for engine rubrics

**Subagent 3: Technical GEO Infrastructure (geo-technical)**
- Analyze robots.txt for AI crawler access
- Verify meta tags, headers, and technical accessibility for AI systems
- Check page speed, server-side rendering, and Core Web Vitals
- Assess security headers and mobile optimization

**Subagent 4: Content E-E-A-T Quality (geo-content)**
- Evaluate Experience, Expertise, Authoritativeness, Trustworthiness signals
- Check author bios, credentials, source citations
- Assess content freshness, depth, and originality
- Verify "About" page quality and team credentials

**Subagent 5: Schema & Structured Data (geo-schema)**
- Validate all schema.org markup
- Check for GEO-critical schema types (FAQ, HowTo, Organization, Product, Article)
- Assess schema completeness and accuracy
- Identify missing schema opportunities

---

### Phase 3: Score Aggregation and Report Generation

#### Composite GEO Score Calculation (Region-Aware)

The overall GEO Score (0-100) is a weighted average of six category scores.
Weights vary by region, loaded from `regions/profiles.yaml`.

| Category | Global Weight | CN Weight | What It Measures |
|---|---|---|---|
| **AI Citability** | 25% | 20% | How quotable/extractable content is for AI systems |
| **Brand Authority** | 20% | **30%** | Third-party mentions on region-relevant platforms |
| **Content E-E-A-T** | 20% | 15% | Experience, Expertise, Authoritativeness, Trustworthiness |
| **Technical GEO** | 15% | 10% | AI crawler access, llms.txt, rendering, speed |
| **Schema & Structured Data** | 10% | **15%** | Schema.org markup + region-specific (e.g. Baidu extensions) |
| **Platform Optimization** | 10% | 10% | Region-specific AI platform readiness |

**Formula (Global):**
```
GEO_Score = (Citability * 0.25) + (Brand * 0.20) + (EEAT * 0.20) + (Technical * 0.15) + (Schema * 0.10) + (Platform * 0.10)
```

**Formula (China):**
```
GEO_Score_CN = (Citability * 0.20) + (Brand * 0.30) + (EEAT * 0.15) + (Technical * 0.10) + (Schema * 0.15) + (Platform * 0.10)
```

When REGION is `global`, use Global weights. When REGION is `cn`, use China weights.
For unimplemented regions, fall back to Global weights.

#### Score Interpretation

| Score Range | Rating | Interpretation |
|---|---|---|
| 90-100 | Excellent | Top-tier GEO optimization; site is highly likely to be cited by AI |
| 75-89 | Good | Strong GEO foundation with room for improvement |
| 60-74 | Fair | Moderate GEO presence; significant optimization opportunities exist |
| 40-59 | Poor | Weak GEO signals; AI systems may struggle to cite or recommend |
| 0-39 | Critical | Minimal GEO optimization; site is largely invisible to AI systems |

---

## Issue Severity Classification

Every issue found during the audit is classified by severity:

### Critical (Fix Immediately)
- All AI crawlers blocked in robots.txt
- No indexable content (JavaScript-rendered only with no SSR)
- Domain-level noindex directive
- Site returns 5xx errors on key pages
- Complete absence of any structured data
- Brand not recognized as an entity by any AI system

### High (Fix Within 1 Week)
- Key AI crawlers (GPTBot, ClaudeBot, PerplexityBot) blocked
- No llms.txt file present
- Zero question-answering content blocks on key pages
- Missing Organization or LocalBusiness schema
- No author attribution on content pages
- All content behind login/paywall with no preview

### Medium (Fix Within 1 Month)
- Partial AI crawler blocking (some allowed, some blocked)
- llms.txt exists but is incomplete or malformed
- Content blocks average under 50 citability score
- Missing FAQ schema on pages with FAQ content
- Thin author bios without credentials
- No Wikipedia or Reddit brand presence

### Low (Optimize When Possible)
- Minor schema validation errors
- Some images missing alt text
- Content freshness issues on non-critical pages
- Missing Open Graph tags
- Suboptimal heading hierarchy on some pages
- LinkedIn company page exists but is incomplete

---

## Output Format

Generate a file called `GEO-AUDIT-REPORT.md` (or `GEO-AUDIT-REPORT-CN.md` when
 `--region cn` is specified) with the following structure:

```markdown
# GEO Audit Report: [Site Name] [If CN: — China Market]

**Audit Date:** [Date]
**URL:** [URL]
**Region:** [global | cn]
**Business Type:** [Detected Type]
**Pages Analyzed:** [Count]

---

## Executive Summary

**Overall GEO Score: [X]/100 ([Rating])**

[2-3 sentence summary of the site's GEO health, biggest strengths, and most critical gaps.]

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|---|
| AI Citability | [X]/100 | 25% (global) / 20% (CN) | [X] |
| Brand Authority | [X]/100 | 20% (global) / 30% (CN) | [X] |
| Content E-E-A-T | [X]/100 | 20% (global) / 15% (CN) | [X] |
| Technical GEO | [X]/100 | 15% (global) / 10% (CN) | [X] |
| Schema & Structured Data | [X]/100 | 10% (global) / 15% (CN) | [X] |
| Platform Optimization | [X]/100 | 10% (both) | [X] |
| **Overall GEO Score** | | | **[X]/100** |

---

## Critical Issues (Fix Immediately)

[List each critical issue with specific page URLs and recommended fix]

## High Priority Issues

[List each high-priority issue with details]

## Medium Priority Issues

[List each medium-priority issue]

## Low Priority Issues

[List each low-priority issue]

---

## Category Deep Dives

### AI Citability ([X]/100)
[Detailed findings, examples of good/bad passages, rewrite suggestions]

### Brand Authority ([X]/100)
[Platform presence map, mention volume, sentiment]

### Content E-E-A-T ([X]/100)
[Author quality, source citations, freshness, depth]

### Technical GEO ([X]/100)
[Crawler access, llms.txt, rendering, headers]

### Schema & Structured Data ([X]/100)
[Schema types found, validation results, missing opportunities]

### Platform Optimization ([X]/100)
[Presence on region-relevant platforms: YouTube/Reddit/Wikipedia for global, Baidu Baike/Zhihu/WeChat for CN]

---

## Quick Wins (Implement This Week)

1. [Specific, actionable quick win with expected impact]
2. [Another quick win]
3. [Another quick win]
4. [Another quick win]
5. [Another quick win]

## 30-Day Action Plan

### Week 1: [Theme]
- [ ] Action item 1
- [ ] Action item 2

### Week 2: [Theme]
- [ ] Action item 1
- [ ] Action item 2

### Week 3: [Theme]
- [ ] Action item 1
- [ ] Action item 2

### Week 4: [Theme]
- [ ] Action item 1
- [ ] Action item 2

---

## Appendix: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| [url] | [title] | [issue count] |
```

---

## Quality Gates

- **Page Limit:** Never crawl more than 50 pages per audit. Prioritize high-value pages.
- **Timeout:** 30-second maximum per page fetch. Skip pages that exceed this.
- **Robots.txt:** Always check and respect robots.txt before crawling. Note any AI-specific directives.
- **Rate Limiting:** Wait at least 1 second between page fetches to avoid overloading the server.
- **Error Handling:** Log failed fetches but continue the audit. Report fetch failures in the appendix.
- **Content Type:** Only analyze HTML pages. Skip PDFs, images, and other binary content.
- **Deduplication:** Canonicalize URLs before crawling. Skip duplicate content (e.g., HTTP vs HTTPS, www vs non-www, trailing slashes).

---

## Business-Type-Specific Audit Adjustments

### SaaS Sites
- Extra weight on: Feature comparison tables (high citability), integration pages, documentation quality
- Check for: API documentation structure, changelog pages, knowledge base organization
- Key schema: SoftwareApplication, FAQPage, HowTo

### Local Businesses
- Extra weight on: NAP consistency, Google Business Profile signals, local schema
- Check for: Service area pages, location-specific content, review markup
- Key schema: LocalBusiness, GeoCoordinates, OpeningHoursSpecification

### E-commerce Sites
- Extra weight on: Product descriptions (citability), comparison content, buying guides
- Check for: Product schema completeness, review aggregation, FAQ sections on product pages
- Key schema: Product, AggregateRating, Offer, BreadcrumbList

### Publishers
- Extra weight on: Article quality, author credentials, source citation practices
- Check for: Article schema, author pages, publication date freshness, original research
- Key schema: Article, NewsArticle, Person (author), ClaimReview

### Agency/Services
- Extra weight on: Case studies (citability), expertise demonstration, thought leadership
- Check for: Portfolio schema, team credentials, industry-specific expertise signals
- Key schema: Organization, Service, Person (team), Review
