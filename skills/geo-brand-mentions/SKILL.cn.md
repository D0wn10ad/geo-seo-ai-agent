---
name: geo-brand-mentions-cn
description: CN-specific brand mention scanning — Baidu Baike, Zhihu, WeChat OA, Xiaohongshu, Bilibili, Douyin
version: 1.0.0
region: cn
parent: geo-brand-mentions
---

# Brand Mention Scanner — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Replace the Western platform importance ranking with CN-specific platforms below.
Scoring methodology (presence, engagement, recency) mirrors the base skill.

Reference: `regions/cn/platforms.md` for platform details and verification methods.

---

## Platform Importance Ranking for AI Citations (China Market)

### 1. Baidu Baike (百度百科) — SIGNAL STRENGTH: CRITICAL

**Why Baidu Baike matters most:**
- Baidu Baike is China's equivalent of Wikipedia — the #1 entity recognition signal for all CN AI engines
- All major CN AI models (Baidu AI, ERNIE, Doubao, Tongyi, Kimi, DeepSeek) reference Baidu Baike for entity grounding
- A verified Baidu Baike entry is the single strongest trust signal in CN AI search
- Unlike Wikipedia, Baidu Baike entries can be created/edited by brands (with verification)

**What to check:**
- **Brand entry**: Does the brand have a dedicated Baidu Baike page?
- **Verification status**: Is the page verified (认证版本)?
- **Content quality**: Is the entry comprehensive (history, products, key personnel)?
- **Update recency**: Has the entry been updated in the last 6 months?
- **References**: Does the entry cite authoritative Chinese sources?
- **Images/logos**: Are official brand images present?

**Scoring (0-30):**
- Verified entry with comprehensive content: 25-30
- Unverified entry with moderate content: 15-24
- Minimal entry (stub): 5-14
- No entry: 0

---

### 2. Zhihu (知乎) — SIGNAL STRENGTH: HIGH

**Why Zhihu matters:**
- Zhihu is China's premier Q&A platform (similar to Quora + Reddit)
- Heavily indexed by all CN AI engines for community-validated content
- AI models treat Zhihu answers as authoritative, especially answers with high upvotes
- Zhihu's expert badge system provides direct authority signals for AI entity recognition

**What to check:**
- **Brand mentions**: Number of Zhihu questions/answers mentioning the brand
- **Official account**: Does the brand have a verified Zhihu organization account?
- **Engagement**: Upvote counts, comment volume, and recency of mentions
- **Sentiment**: Positive/negative/neutral ratio
- **Expert participation**: Are industry experts discussing the brand?

**Scoring (0-20):**
- Verified account + 10+ high-engagement mentions: 16-20
- Active mentions without verified account: 10-15
- Sparse or old mentions: 4-9
- No presence: 0

---

### 3. WeChat Official Account (微信公众号) — SIGNAL STRENGTH: HIGH

**Why WeChat matters:**
- WeChat is China's super-app with 1.3B+ monthly active users
- WeChat Official Accounts (公众号) are primary content distribution channels
- CN AI engines index WeChat articles through搜狗 (Sogou) integration
- WeChat OA verification adds entity trust signals

**What to check:**
- **Official Account**: Does the brand have a verified WeChat Official Account?
- **Content frequency**: How often does the account publish?
- **Engagement**: Average read counts and engagement rates
- **Verification**: Is the account verified (认证) with official brand name?

**Scoring (0-15):**
- Verified OA with regular publishing (weekly+): 12-15
- OA with sporadic publishing: 6-11
- No OA but mentioned in others' WeChat articles: 2-5
- No presence: 0

---

### 4. Xiaohongshu (小红书 / RED) — SIGNAL STRENGTH: MEDIUM-HIGH

**Why Xiaohongshu matters:**
- Xiaohongshu is China's leading lifestyle/content-commerce platform (300M+ users)
- Increasingly indexed by CN AI engines for product/brand discovery
- User-generated content with purchase intent signals
- Particularly important for B2C, lifestyle, beauty, travel, and food brands

**What to check:**
- **Brand mentions**: Number of Xiaohongshu posts mentioning the brand
- **Official account**: Does the brand have a verified brand account?
- **Content quality**: Are posts authentic-looking with real user photos?
- **Engagement**: Likes, saves, comments on brand-related posts

**Scoring (0-10):**
- Strong organic presence: 8-10
- Moderate mentions: 4-7
- Minimal: 1-3
- None: 0

---

### 5. Bilibili (B站) — SIGNAL STRENGTH: MEDIUM

**Why Bilibili matters:**
- Bilibili is China's leading video platform for Gen Z and Millennials
- CN AI engines (especially Doubao) index Bilibili video content
- Strong for tech, education, entertainment, and gaming brands
- Video transcripts provide rich text signals for AI indexing

**What to check:**
- **Brand channel**: Does the brand have a Bilibili channel?
- **Video mentions**: Are creators mentioning the brand in videos?
- **Engagement**: Views, likes, danmaku (弹幕) volume
- **Content type**: Reviews, tutorials, unboxings, comparisons

**Scoring (0-10):**
- Active channel or frequent creator mentions: 8-10
- Occasional mentions: 4-7
- Rare: 1-3
- None: 0

---

### 6. Douyin (抖音) — SIGNAL STRENGTH: MEDIUM

**Why Douyin matters:**
- Douyin is the Chinese version of TikTok (700M+ DAU)
- ByteDance's AI (Doubao) heavily indexes Douyin content
- Short-form video content with strong discovery algorithms
- Brand accounts and influencer collaborations visible to AI

**What to check:**
- **Brand account**: Does the brand have an official Douyin account?
- **Influencer mentions**: Are KOLs (key opinion leaders) mentioning the brand?
- **Engagement**: Views, likes, shares on brand-related content
- **Hashtag presence**: Brand-related hashtag volume

**Scoring (0-10):**
- Active account with regular content: 8-10
- Some influencer mentions: 4-7
- Minimal: 1-3
- None: 0

---

### 7. Industry/Niche CN Sources (36氪, 虎嗅, CSDN, 掘金) — SIGNAL STRENGTH: MEDIUM

**Why these matter:**
- 36Kr (36氪) and Huxiu (虎嗅) are China's top tech/business media — indexed by all CN AI
- CSDN and Juejin (掘金) are China's top developer communities — crucial for tech/SaaS brands
- Mentions in these sources provide strong authority signals for CN AI models

**What to check:**
- Media coverage on 36Kr and Huxiu
- Technical articles on CSDN and Juejin
- Industry report mentions

**Scoring (0-5):**
- Multiple mentions across 2+ sources: 5
- Single source mentions: 2-4
- None: 0

---

## Citation-Probability Weight Adjustment

Platform weight adjustment for AI citation probability:
- Baidu Baike: weight 1.0 (entity recognition anchor)
- Zhihu: weight 1.3 (highest citation rate)
- 36Kr: weight 1.2 (high industry citation)
- WeChat OA: weight 1.1
- CSDN: weight 1.0
- Bilibili: weight 0.9
- Xiaohongshu: weight 0.8
- Juejin: weight 0.8
- Douyin: weight 0.6
- Huxiu: weight 0.5
- 百家号: weight 0.8 (self-media quality varies)
- 微博: weight 0.5 (high volume, low per-post weight)

Negative query monitoring: Track brand mentions in negative context on key platforms.
Negative mentions on high-weight platforms (Zhihu, WeChat, 36Kr) reduce Brand Authority Score
by -5 to -15 depending on sentiment severity and mention prominence.

---

## Total Brand Mention Score (CN)

Max 100 points: Baidu Baike (30) + Zhihu (20) + WeChat OA (15) + Xiaohongshu (10) + Bilibili (10) + Douyin (10) + Industry CN Sources (5)

Recommendation rate KPI: Track percentage of AI engine responses that include a positive recommendation.
Baseline measurement: Run 20 target queries without GEO optimization.
Post-optimization: Target Top 3 recommendation in ≥60% of queries (源易 case: 0% → Top 8 in 8 weeks).

Output file: `GEO-BRAND-MENTIONS-CN.md`
