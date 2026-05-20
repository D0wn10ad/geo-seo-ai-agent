---
name: geo-citability-cn
description: CN-specific citability scoring adjustments — Chinese language, CN AI engine preferences
version: 1.0.0
region: cn
parent: geo-citability
---

# AI Citability Scoring — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base citability scoring rubric.

Reference: `regions/cn/ai-engines.md` for CN engine-specific citation preferences.

---

## Adjustments to Base Scoring Rubric

### Category 1: Answer Block Quality (30% → CN-adjusted)

The base criteria apply, with these CN-specific considerations:

- **Definition patterns in Chinese**: "X是..." (X is...), "X指的是..." (X refers to...), "X是指..." (X means...)
- **Answer-first structure**: Same principle — answer in first 1-2 sentences
- **Quantified answers**: Chinese numeric formats (约X%, 达到X, 超过X)
- **Baidu AI prefers**: Concise 50-100 character paragraphs. Doubao prefers: slightly longer 100-200 character context-rich answers

**CN adjustment**: Answer blocks written in clear modern Chinese (现代汉语) score higher than those using classical Chinese patterns (文言文). Avoid excessive 专业术语 (jargon) without explanation.

### Category 2: Self-Containment (20% → CN-adjusted)

- Chinese content often assumes cultural context. Flag passages that assume CN-specific knowledge without explanation
- For CN-audience content (e.g., `.cn` domain targeting CN users), CN cultural context is acceptable
- For global audience content being analyzed for CN citability, ensure passages define China-specific terms

### Category 3: Structural Readability (20% → CN-adjusted)

- Chinese text does not have spaces, making readability different from English:
  - Short sentences (15-25 characters ideal for web)
  - Clear段落 (paragraph) breaks every 3-5 sentences
  - Use of 粗体 (bold) for key terms
  - Numbered lists for processes, with Chinese numbering (一、二、三 or 1. 2. 3.)
- Baidu AI favors: Well-structured content with clear hierarchical headings
- Doubao favors: Mixed text + bullet point formatting

### Category 4: Statistical Density (20% → CN-adjusted)

- CN AI engines favor statistics from Chinese government sources, Chinese industry reports, and CN-accredited research
- Sources from 国家统计局 (NBS), 艾瑞咨询 (iResearch), 易观 (Analysys),  QuestMobile carry weight
- Dates should be in Chinese format (YYYY年MM月DD日) or ISO format
- Currency values should be in RMB (人民币/¥) format for CN context

### Category 5: Uniqueness (15% → No change)

Same criteria apply. CN AI engines also value original data and proprietary insights.

---

## Additional CN Citability Checks

### Chinese Language Quality
- Proper use of 的/地/得 (common grammar errors degrade citability)
- Natural Chinese phrasing (not machine translation patterns)
- Appropriate formality level for the topic (professional vs casual)
- Avoid excessive English loanwords without Chinese explanation

### Baidu Baike Cross-Reference
- Does content reference or align with Baidu Baike definitions for key terms?
- Consistency with Baidu Baike terminology improves AI citation likelihood

### Mobile-First Formatting
- Most CN users access content via mobile
- Short paragraphs (2-4 sentences) for mobile readability
- Bullet points and numbered lists for mobile scanning

### Multilingual Content
- If the page offers both Chinese and English versions, CN AI engines will cite the Chinese version
- Ensure Chinese content is original, not a direct translation (CN AI prefers native Chinese writing)

Output file: `GEO-CITABILITY-SCORE-CN.md`
