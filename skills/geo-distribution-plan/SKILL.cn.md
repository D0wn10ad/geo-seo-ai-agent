---
name: geo-distribution-plan-cn
description: CN-only multi-platform content distribution plan — Baidu Baike, Zhihu, WeChat OA, Xiaohongshu, Bilibili, Douyin, 36Kr, Huxiu, CSDN, Juejin
version: 1.0.0
region: cn
parent: geo-distribution-plan
---

# GEO Distribution Plan — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Use this CN-only platform inventory and rewrite constraints instead of the global defaults.

Reference: `regions/cn/platforms.md` for full CN platform profiles.

---

## CN Platform Tiering Matrix

### Pre-scored CN platform reference

| Platform | A | Default F | C | Default tier | Citation affinity | Audience fit notes |
|---|---|---|---|---|---|---|---|---|
| Baidu Baike (百度百科) | 5 | 4 | KNOWN | T1 | Avg 0.0% (entity recognition anchor) | Encyclopedic content only; not for promotional posts |
| Zhihu (知乎) | 5 | 4 | KNOWN | T1 | Avg ~15.8% | Strongest CN AI-search citation source; long-form Q&A |
| WeChat OA (微信公众号) | 4 | 4 | UNKNOWN | T2 | Avg ~10.5% | Closed garden — valuable for owned-audience retention |
| Xiaohongshu (小红书) | 3 | 3 | UNKNOWN | T3 | Avg ~7.5% | Consumer / lifestyle / visual; rarely cited by CN AI engines |
| Bilibili (哔哩哔哩) | 3 | 4 | PARTIAL | T2 | Avg ~8.9% | Video + text; CN Gen Z audience; growing AI-corpus coverage |
| Douyin (抖音) | 2 | 3 | UNKNOWN | T3 | Avg ~5.5% | Reach-only; short-form video; limited AI citation potential |
| 36Kr (36氪) | 4 | 4 | PARTIAL | T1 | Avg ~12.1% | Premium B2B / tech / startup — best for business content |
| Huxiu (虎嗅) | 4 | 4 | PARTIAL | T3 | Avg ~5.0% | B2B / business / industry analysis |
| CSDN (中国软件开发网) | 3 | 4 | PARTIAL | T2 | Avg ~8.2% | Developer / technical content |
| Juejin (掘金) | 3 | 4 | PARTIAL | T2 | Avg ~6.8% | Developer / front-end / engineering |

B2B content: prioritize CSDN/Juejin/36Kr. B2C content: prioritize Xiaohongshu/Zhihu/Bilibili. Refer to `regions/cn/platforms.md` for full per-engine breakdowns.

Quality Gate note: Base skill requires ≥50% platforms at KNOWN coverage. In CN context, this gate is waived because CN platforms have lower AI-training-corpus coverage (only 2 of 10 are KNOWN) but higher overall citation diversity. Instead, use the Day 30 reclaim checkpoint (below) to verify citation outcomes. See `regions/cn/platforms.md` for per-platform coverage details.

### CN-specific distribution notes

When `region: cn`:
- All platform references, rewrite constraints, and syndication targets use Chinese platforms
- Tier 1: Baidu Baike (if encyclopedic), Zhihu column, 36Kr (if B2B/tech)
- Tier 2: WeChat OA, Bilibili, CSDN/Juejin
- Tier 3: Xiaohongshu, Douyin, Huxiu
- Rewrite briefs must be in Chinese, matching platform-specific content styles
- Social cuts target Chinese social platforms (WeChat Moments, Weibo)
- Authority reclaim checklist includes Baidu Baike update, Zhihu answer monitoring, and Baidu Zhanzhang URL submission

---

## CN 14-Day Cadence Template

| Day | Move | Platforms | Rewrite intensity | Canonical handling |
|---|---|---|---|---|
| **D0** | Publish canonical | Main domain | None | Self-canonical; submit to Baidu Zhanzhang |
| **D+1** | Tier 1 syndication | 1-2 T1 (Zhihu + 36Kr) | Distinct Chinese opening + native formatting | Attribution line at end; canonical tag where supported |
| **D+3** | Tier 2 wave A | 2 T2 (WeChat OA + CSDN/Juejin) | Distinct opening + conclusion; platform-native structure | Attribution line; cross-link to T1 posts |
| **D+5** | Tier 2 wave B | 1 T2 (Bilibili — video adaptation) | Video script + Chinese description | Description links to canonical |
| **D+7** | Tier 3 + social cuts | Xiaohongshu cut, Douyin clip, Weibo post | Excerpt or snippet; Chinese social-native format | Teaser link to canonical; bio link |
| **D+10** | Authority follow-up | Baidu Baike update if applicable | Propose Baidu Baike entry or update | External canonical as source |
| **D+14** | Reclaim checkpoint #1 | All published surfaces | Run checklist | |

### CN multi-platform citation network

CN citation network strategy: Create content hubs that cross-reference across platforms.
E.g., publish on 36Kr → quote in Zhihu answer → cite back in WeChat OA article.
AI engines assign higher credibility to claims corroborated across multiple platforms.
This "citation web" effect amplifies each platform's individual contribution by ~1.3-1.8x.

### CN conflict-avoidance rules

- Never publish two near-verbatim Chinese copies on the same day on KNOWN/PARTIAL platforms
- WeChat OA and Zhihu should cover different angles of the same topic — not identical content
- Baidu Baike content must be strictly objective/encyclopedic — no promotional language
- Zhihu posts must be in first-person Q&A format, not direct article syndication
- Xiaohongshu requires visual-first approach — text-only posts perform poorly

---

## Per-Platform Rewrite Constraints (CN)

### Baidu Baike

- **Format:** Third-person, encyclopedic, objective tone — NO promotional language
- **Length:** 800-2000 Chinese characters per entry
- **Structure:** Definition → history → features → references
- **Citations:** Must cite published sources (authoritative media, government, academic)
- **Review:** Baidu Baike entries go through community review — may take 1-4 weeks to publish
- **CTA:** No CTA allowed — the entry is informational. Edit carefully or platform may reject.

### Zhihu

- **Opening pattern:** Sharp question hook → personal stake → detailed answer
- **Length:** 1500-4000 Chinese characters for Tier 1 treatment
- **Format:** First-person conversational; bolded inline takeaways; use native image/code blocks
- **CTA:** External link only after first 30% of answer; "推荐阅读" at end

### WeChat Official Account

- **Opening pattern:** Cover image + 1-sentence hook + 3-bullet TL;DR (本文重点)
- **Length:** 800-2500 Chinese characters; mobile skim format
- **Format:** Short paragraphs (2-3 sentences); subheadings every 200-300 characters; 1-2 images
- **CTA:** Soft CTA at end (关注/收藏); external links via reply-keyword pattern only

### Xiaohongshu

- **Opening pattern:** Visual-first — cover image carries the hook text
- **Length:** 300-800 characters; high emoji density accepted
- **Format:** Numbered listicle or before/after; topic tags (#) at end
- **CTA:** Profile-link follow; external links heavily deprioritized

### Bilibili

- **Opening pattern:** Video title + thumbnail hook + 1-paragraph Chinese description
- **Length:** 5-15 min video; description 200-500 characters
- **Format:** Video content with Chinese subtitles; description with topic tags
- **CTA:** Follow/subscribe at end; links in description in Chinese format

### Douyin

- **Opening pattern:** 3-second hook in video + text overlay
- **Length:** 15-60 seconds; 50-100 character caption
- **Format:** Short vertical video; trending music/effects; text captions
- **CTA:** Profile bio link; no inline links

### 36Kr

- **Opening pattern:** News/analysis hook → industry context → detailed breakdown
- **Length:** 800-2000 Chinese characters
- **Format:** Professional business journalism tone; data charts welcome
- **CTA:** Byline bio link; source attribution at end
- **Access:** Must pitch to 36Kr editors or have media partnership

### Huxiu

- **Opening pattern:** Industry insight hook → trend analysis → expert opinion
- **Length:** 800-2000 Chinese characters
- **Format:** Professional analysis; opinion-backed with data; editorial tone
- **CTA:** Byline bio link; "首次发表于..." at end

### CSDN

- **Opening pattern:** Problem statement → environment/version → solution
- **Length:** 1500-5000 characters; code blocks expected
- **Format:** Working code; version-pinned deps; reproducible commands
- **CTA:** Source repo link at bottom; canonical link in author bio

### Juejin

- **Opening pattern:** Problem → approach → code solution
- **Length:** 1000-4000 characters; code blocks
- **Format:** Modern developer writing; clean code snippets
- **CTA:** Like/follow prompt; GitHub link in bio

---

## CN Authority-Signal Reclaim Checklist

### Day 7

- [ ] Check Baidu Zhanzhang for indexing status of syndicated URLs
- [ ] Verify Zhihu answer is visible in search for target keywords
- [ ] Confirm WeChat OA article has been indexed (search-in-WeChat test)
- [ ] Count Zhihu upvotes, comments, and saves
- [ ] Check Bilibili video views and engagement metrics

### Day 14

- [ ] Run Stage 6 verification on CN AI engines: has any CN engine started citing?
- [ ] Identify which CN platform's version gets cited (Zhihu often wins over Baidu Baike)
- [ ] Check Baidu Search for the canonical URL — any ranking changes?
- [ ] Confirm no canonical-confusion penalty (check Baidu Webmaster Tools)

### Day 30

- [ ] Run `/geo compete <domain> <competitors> --region cn` — CN gap matrix
- [ ] Catalog earned CN media coverage (36Kr, Huxiu pickups)
- [ ] Decide on second-wave: more Baidu Baike updates, additional Zhihu answers
- [ ] Archive distribution plan to `~/.geo-prospects/distribution/_archive/`

---

## CN Output Format

Generate `~/.geo-prospects/distribution/<domain>-<topic-slug>-<YYYY-MM-DD>-CN.md`
