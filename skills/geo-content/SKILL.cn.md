---
name: geo-content-cn
description: CN-specific content quality and E-E-A-T assessment — Chinese authority signals, Baidu Baike cross-reference, CJK readability
version: 1.0.0
region: cn
parent: geo-content
---

# GEO Content Quality & E-E-A-T — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base E-E-A-T scoring rubric.

Reference: `regions/cn/ai-engines.md` for CN engine citation preferences.

---

## Adjustments to Base Scoring

### Experience (25% — CN-adjusted)

**Signals to add:**

| Signal | Points | How to Score |
|---|---|---|
| First-hand Chinese market experience (在中国市场的直接经验) | 5 | 5 if specific CN case studies, 3 if generic CN references, 0 if none |
| Original Chinese-language research or data | 5 | 5 if proprietary CN data, 3 if references CN research, 0 if none |
| CN-specific case studies with local results | 4 | 4 if detailed with local numbers, 2 if general, 0 if none |
| Evidence of on-the-ground CN presence | 3 | 3 if CN office/team photos, 1 if generic stock, 0 if none |

**CN adjustment:** For content targeting the CN market, experience with the Chinese market (not just international experience) carries additional weight. CN AI engines favor content from authors who demonstrate direct familiarity with Chinese business practices, regulations, and market conditions.

### Expertise (25% — CN-adjusted)

**Signals to add:**

| Signal | Points | How to Score |
|---|---|---|
| Credentials from Chinese institutions | 5 | 5 if CN university/org credentials, 3 if international + CN mention, 0 if none |
| CSDN/Juejin community authority | 3 | 3 if high-reputation CSDN/Juejin profile, 1 if basic profile, 0 if absent |
| WeChat Official Account with verified status | 3 | 3 if verified OA with regular content, 1 if basic OA, 0 if absent |
| Citations from Chinese government/academic sources | 4 | 4 if cites 国务院/教育部/中科院, 2 if cites Chinese industry reports, 0 if none |

**CN adjustment:** Authority in the Chinese context is heavily tied to recognition by Chinese institutions. A Western credential (e.g., Google certification) carries less weight with CN AI engines than a Chinese equivalent (e.g., Baidu certification, 百度认证).

### Authoritativeness (25% — CN-adjusted)

**Signals to add:**

| Signal | Points | How to Score |
|---|---|---|
| Baidu Baike entry for the brand/author | 5 | 5 if Baidu Baike entry exists, 3 if proposed, 0 if none |
| Zhihu mentions and citation count | 4 | 4 if cited on Zhihu by high-rep users, 2 if low-rep mentions, 0 if none |
| Xiaohongshu brand presence | 3 | 3 if active with engagement, 1 if basic presence, 0 if absent |
| WeChat ecosystem references | 3 | 3 if mentioned in WeChat articles, 1 if only in Moments, 0 if none |
| Chinese media coverage (36Kr, Huxiu, Jiemian) | 4 | 4 if covered by major CN outlets, 2 if small CN outlets, 0 if none |
| Bilibili content about the brand/topic | 3 | 3 if substantial Bilibili coverage, 1 if minimal, 0 if none |

**CN adjustment:** Baidu Baike is the single strongest authority signal for the Chinese market — equivalent to Wikipedia for the global market. A brand without a Baidu Baike entry is missing the most fundamental CN authority signal.

### Trustworthiness (25% — CN-adjusted)

**Signals to add:**

| Signal | Points | How to Score |
|---|---|---|
| ICP license displayed in footer | 4 | 4 if ICP filing visible, 0 if absent but site targets CN |
| Chinese-language privacy policy | 2 | 2 if Chinese version exists, 0 if English-only |
| Chinese business license information | 3 | 3 if business license info visible, 1 if partial, 0 if none |
| Customer service available in Chinese | 3 | 3 if Chinese-language support, 1 if chatbot only, 0 if none |
| WeChat customer service contact | 2 | 2 if WeChat support contact, 0 if none |
| Chinese social media account verification | 2 | 2 if verified CN social accounts, 0 if none |

**CN adjustment:** Trust signals in the Chinese market differ from global: ICP filing is a regulatory requirement, not optional. Chinese consumers trust brands with active WeChat Official Accounts and verified social media presence.

---

## CN Content Quality Metrics

### Character Count Benchmarks (Chinese text)

Chinese text is significantly denser than English. Use character counts instead of word counts:

| Page Type | Minimum Characters | Ideal Range | Notes |
|---|---|---|---|
| Homepage | 300 | 300-800 | Chinese text: 1 character ≈ 1.5 English words semantically |
| Blog post | 800 | 800-2000 | Thorough but focused |
| Pillar content / Ultimate guide | 1500 | 2000-4000 | Comprehensive topic coverage |
| Product page | 200 | 300-800 | Descriptions, specs, use cases |
| Service page | 300 | 500-1200 | What, how, why, for whom |
| About page | 200 | 300-600 | Company/person story and credentials |
| FAQ page | 500 | 800-2000 | Thorough answers, not one-liners |

### Readability (Chinese-specific)

Chinese text does not have word spaces. Readability is measured by:
- **Average sentence length:** 15-25 characters per sentence is ideal (Chinese sentences are shorter than English)
- **Average paragraph length:** 2-4 sentences — short paragraphs for mobile readability
- **Jargon handling:** Technical terms should include Chinese translations for foreign terms
- **段落 (paragraph) breaks:** Clear visual breaks every 3-5 sentences
- **Punctuation:** Proper use of Chinese punctuation (。！？，；：) — not mixed with English punctuation

### Paragraph Structure for Chinese AI Parsing

- **2-4 sentences** per paragraph
- **One idea per paragraph**
- **Lead with key claim**
- **Chinese quotable patterns:** Starting with "X是指..." (X refers to...), "X的核心是..." (the core of X is...), "关键在于..." (the key is...)
- Baidu AI Search prefers: Concise 50-80 character paragraphs
- Doubao prefers: Slightly longer 100-150 character context-rich paragraphs

---

## CN E-E-A-T Scoring Composition

| Component | Weight (CN) | Max Points |
|---|---|---|
| Experience (CN-adjusted) | 25% | 25 |
| Expertise (CN-adjusted) | 25% | 25 |
| Authoritativeness (CN-adjusted) | 25% | 25 |
| Trustworthiness (CN-adjusted) | 25% | 25 |
| **Subtotal** | | **100** |
| Topical Authority Modifier | | +10 to -5 |
| **Final Score** | | **Capped at 100** |

### CN Score Interpretation

- **85-100**: Exceptional — strong AI citation candidate for CN AI engines
- **70-84**: Good — solid CN foundation, Baidu AI + Doubao citation potential
- **55-69**: Average — multiple E-E-A-T gaps reducing CN AI visibility
- **40-54**: Below Average — significant content quality and trust issues for CN market
- **0-39**: Poor — fundamental content strategy overhaul needed for CN

---

## Chinese Content Quality Assessment

### Signs of Low-Quality Chinese Content

| Signal | Chinese Example |
|---|---|
| Machine translation patterns | Awkward phrasing that follows English grammar structure |
| Literal translations of idioms | 直译 idioms that don't make sense in Chinese context |
| Wrong measure words | 一个 vs 一位 vs 一名 errors |
| Mixed simplified/traditional characters | Inconsistent script usage |
| English-heavy without explanation | "我们需要update这个SEO的KPI" — excessive loanwords |
| 的/地/得 errors | Common grammar mistakes that degrade content quality |

### High-Quality Chinese Content Signals

| Signal | Description |
|---|---|
| Natural Chinese phrasing | Written in native Chinese, not translated from English |
| Chinese data sources | References 国家统计局, 艾瑞咨询,  QuestMobile, 易观 |
| Chinese terminology consistency | Correct use of industry-standard Chinese terms |
| Proper 的/地/得 usage | Grammatically correct Chinese |
| Appropriate formality level | Professional register for B2B, conversational for consumer content |

---

## Output Format (CN)

Generate **GEO-CONTENT-ANALYSIS-CN.md** with the same structure as the base skill, with Chinese-language section headings and CN-specific findings.

Output file: `GEO-CONTENT-ANALYSIS-CN.md`
