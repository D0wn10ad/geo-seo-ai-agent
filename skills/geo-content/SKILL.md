---
name: geo-content
description: Content quality and E-E-A-T assessment for AI citability — evaluate experience, expertise, authoritativeness, trustworthiness, and content structure
version: 1.0.0
author: geo-seo-claude
tags: [geo, content-quality, eeat, citability, ai-content, topical-authority]
---

<!-- GEO-CN-VARIANT:v1 -->

**Conditional CN variant.** Only when `REGION` resolves to `cn`, read `references/cn.md` and apply its overrides; its CN knowledge files are enumerated in the geo skill's `regions/cn-variants.json` (self-locating resolution is documented in `geo/SKILL.md` → "CN variant loading"). For `global` or any non-CN region, do NOT load `references/cn.md` or any `regions/cn/` file.

# GEO Content Quality & E-E-A-T Assessment

## Purpose

AI search platforms do not just find content — they evaluate whether content deserves to be cited. The primary framework for this evaluation is **E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness), which per Google's December 2025 Quality Rater Guidelines update now applies to **ALL competitive queries**, not just YMYL (Your Money Your Life) topics. Content that scores high on E-E-A-T is dramatically more likely to be cited by AI platforms.

This skill evaluates content through two lenses:
1. **E-E-A-T signals** — does the content demonstrate real expertise and trust?
2. **AI citability** — is the content structured so AI platforms can extract and cite specific claims?

## How to Use This Skill

1. Fetch the target page(s) — homepage, key blog posts, service/product pages
2. Evaluate E-E-A-T across the 4 dimensions (25% each)
3. Assess content quality metrics (structure, readability, depth)
4. Check for AI content quality signals
5. Evaluate topical authority across the site
6. Score and generate GEO-CONTENT-ANALYSIS.md

---

## E-E-A-T Framework (100 points total)

### Experience — 25 points
First-hand knowledge and direct involvement with the topic. AI platforms increasingly distinguish between content that reports on a topic and content from someone who has DONE it.

**Signals to evaluate:**

| Signal | Points | How to Score |
|---|---|---|
| First-person accounts ("I tested...", "We implemented...") | 5 | 5 if present and specific, 3 if generic, 0 if absent |
| Original research or data not available elsewhere | 5 | 5 if original data, 3 if references original work, 0 if none |
| Case studies with specific results | 4 | 4 if detailed with numbers, 2 if general, 0 if none |
| Screenshots, photos, or evidence of direct use | 3 | 3 if authentic evidence, 1 if stock/generic, 0 if none |
| Specific examples from personal experience | 4 | 4 if specific and unique, 2 if somewhat specific, 0 if generic |
| Demonstrations of process (not just outcome) | 4 | 4 if step-by-step from experience, 2 if partial, 0 if none |

**What to flag as weak Experience:**
- Content that only summarizes what other sources say without adding new perspective
- Generic advice that could apply to any situation ("It depends on your needs")
- No mention of actual usage, testing, or direct involvement
- Hedging language that suggests lack of direct knowledge ("reportedly", "supposedly", "some say")

### Expertise — 25 points
Demonstrated knowledge depth and professional competence in the subject matter.

**Signals to evaluate:**

| Signal | Points | How to Score |
|---|---|---|
| Author credentials visible (bio, degrees, certifications) | 5 | 5 if full credentials, 3 if basic bio, 0 if no author |
| Technical depth appropriate to topic | 5 | 5 if thorough technical treatment, 3 if adequate, 0 if superficial |
| Methodology explanation (how conclusions were reached) | 4 | 4 if clear methodology, 2 if some explanation, 0 if none |
| Data-backed claims (statistics, research citations) | 4 | 4 if well-sourced, 2 if some data, 0 if unsupported claims |
| Industry-specific terminology used correctly | 3 | 3 if accurate specialized language, 1 if basic, 0 if errors |
| Author page with detailed professional background | 4 | 4 if dedicated author page, 2 if brief bio, 0 if none |

**What to flag as weak Expertise:**
- Claims without supporting evidence or sources
- Surface-level coverage of complex topics
- Misuse of technical terminology
- No visible author or author without relevant credentials
- Content that is broad and generic rather than deep and specific

### Authoritativeness — 25 points
Recognition by others as a credible source on the topic.

**Signals to evaluate:**

| Signal | Points | How to Score |
|---|---|---|
| Inbound citations from authoritative sources | 5 | 5 if cited by major sources, 3 if some citations, 0 if none |
| Author quoted or cited in press/media | 4 | 4 if media mentions, 2 if industry mentions, 0 if none |
| Industry awards or recognition mentioned | 3 | 3 if relevant awards, 1 if tangential, 0 if none |
| Speaker credentials (conferences, events) | 3 | 3 if listed, 0 if none |
| Published in peer-reviewed or respected outlets | 4 | 4 if tier-1 publications, 2 if industry outlets, 0 if none |
| Comprehensive topic coverage (topical authority) | 3 | 3 if site covers topic thoroughly, 1 if some coverage, 0 if isolated |
| Brand mentioned on Wikipedia or authoritative references | 3 | 3 if Wikipedia, 2 if other encyclopedic refs, 0 if none |

**What to flag as weak Authoritativeness:**
- Single-topic site with no depth of coverage
- No external validation of expertise claims
- No backlinks from authoritative sources
- Claims of authority without evidence (self-proclaimed "expert")

### Trustworthiness — 25 points
Signals that the content and its publisher are reliable and transparent.

**Signals to evaluate:**

| Signal | Points | How to Score |
|---|---|---|
| Contact information visible (address, phone, email) | 4 | 4 if full contact info, 2 if email only, 0 if none |
| Privacy policy present and linked | 2 | 2 if present, 0 if absent |
| Terms of service present | 1 | 1 if present, 0 if absent |
| HTTPS with valid certificate | 2 | 2 if valid HTTPS, 0 if not |
| Editorial standards or corrections policy | 3 | 3 if documented, 1 if implicit, 0 if none |
| Transparent about business model and conflicts | 3 | 3 if clear disclosures, 1 if some, 0 if none |
| Reviews and testimonials from real customers | 3 | 3 if verified reviews, 1 if testimonials, 0 if none |
| Accurate claims (no misinformation detected) | 4 | 4 if all claims accurate, 2 if mostly accurate, 0 if errors found |
| Clear affiliate/sponsorship disclosures | 3 | 3 if properly disclosed, 0 if undisclosed or absent |

**What to flag as weak Trustworthiness:**
- No contact information or physical address
- Missing privacy policy or terms
- Undisclosed affiliate links or sponsored content
- Claims that are verifiably false or misleading
- No way to contact the publisher for corrections

---

## Content Quality Metrics

### Word Count Benchmarks
These are **floors, not targets**. More words does not mean better content. The benchmark is the minimum length to adequately cover a topic for AI citability.

| Page Type | Minimum Words | Ideal Range | Notes |
|---|---|---|---|
| Homepage | 500 | 500-1,500 | Clear value proposition, not a wall of text |
| Blog post | 1,500 | 1,500-3,000 | Thorough but focused |
| Pillar content / Ultimate guide | 2,000 | 2,500-5,000 | Comprehensive topic coverage |
| Product page | 300 | 500-1,500 | Descriptions, specs, use cases |
| Service page | 500 | 800-2,000 | What, how, why, for whom |
| About page | 300 | 500-1,000 | Company/person story and credentials |
| FAQ page | 500 | 1,000-2,500 | Thorough answers, not one-liners |

### Readability Assessment
- **Target Flesch Reading Ease**: 60-70 (8th-9th grade level)
- This is NOT a direct ranking factor but affects citability — AI platforms prefer content that is clear and unambiguous
- Overly academic writing (score < 30) reduces citability for general queries
- Overly simple writing (score > 80) may lack the depth needed for expertise signals

**How to estimate without a tool:**
- Average sentence length: 15-20 words is ideal
- Average paragraph length: 2-4 sentences
- Presence of jargon: should be defined when first used
- Passive voice: < 15% of sentences

### Paragraph Structure for AI Parsing
AI platforms extract content at the paragraph level. Each paragraph should be a self-contained unit of meaning.

**Optimal paragraph structure:**
- **2-4 sentences** per paragraph (1-sentence paragraphs are weak; 5+ sentences are hard to extract)
- **One idea per paragraph** — do not mix topics within a paragraph
- **Lead with the key claim** — first sentence should contain the main point
- **Support with evidence** — remaining sentences provide data, examples, or context
- **Quotable standalone** — each paragraph should make sense if extracted in isolation

### Heading Structure
- **One H1 per page** — the primary topic/title
- **H2 for major sections** — should represent distinct subtopics
- **H3 for subsections** — nested under relevant H2
- **No skipped levels** — do not go from H1 to H3 without an H2
- **Descriptive headings** — "How to Optimize for AI Search" not "Section 2"
- **Question-based headings** where appropriate — these map directly to AI queries

### Internal Linking
- Every content page should link to 3-5 related pages on the same site
- Links should use descriptive anchor text (not "click here")
- Create a topic cluster structure: pillar page linked to/from all related subtopic pages
- Orphan pages (no internal links pointing to them) are rarely cited by AI

---

## AI Content Assessment

### AI-Generated Content Policy
AI-generated content is **acceptable** per Google's guidance (March 2024 clarification) as long as it demonstrates genuine E-E-A-T signals and has human oversight. The concern is not HOW content is created but WHETHER it provides value.

### Signs of Low-Quality AI Content (flag these)

| Signal | Description |
|---|---|
| Generic phrasing | "In today's fast-paced world...", "It's important to note that...", "At the end of the day..." |
| No original insight | Content that only rephrases widely available information |
| Lack of first-hand experience | No personal anecdotes, case studies, or specific examples |
| Perfect but empty structure | Well-formatted headings with shallow content beneath them |
| No specific examples | Uses abstract explanations without concrete instances |
| Repetitive conclusions | Each section ends with a variation of the same point |
| Hedging overload | "Generally speaking", "In most cases", "It depends on various factors" without specifying which factors |
| Missing human voice | No opinions, preferences, or professional judgment expressed |
| Filler content | Paragraphs that could be deleted without losing information |
| No data or sources | Claims presented as facts without attribution or evidence |

### High-Quality Content Signals (regardless of production method)

| Signal | Description |
|---|---|
| Original data | Surveys, experiments, benchmarks, proprietary analysis |
| Specific examples | Named products, companies, dates, numbers |
| Contrarian or nuanced views | Disagreement with conventional wisdom, backed by reasoning |
| First-person experience | "When I tested this..." or "Our team found..." |
| Updated information | References to recent events, current data |
| Expert opinion | Clear professional judgment, not just facts |
| Practical recommendations | Specific, actionable advice, not vague guidance |
| Trade-offs acknowledged | "This approach works well for X but not for Y because..." |

---

## Content Freshness Assessment

### Publication Dates
- Check for visible `datePublished` and `dateModified` in both the content and structured data
- Content without dates is treated as less trustworthy by AI platforms
- Dates should be specific (January 15, 2026) not vague ("recently")

### Freshness Scoring

| Criterion | Score |
|---|---|
| Updated within 3 months | Excellent — current and relevant |
| Updated within 6 months | Good — still reasonably current |
| Updated within 12 months | Acceptable — may need refresh |
| Updated 12-24 months ago | Warning — review for accuracy |
| No date or 24+ months old | Critical — AI platforms may deprioritize |

### Evergreen Indicators
Some content remains relevant regardless of age. Flag content as evergreen if:
- It covers fundamental concepts that do not change (physics, basic math, legal definitions)
- It is clearly labeled as a reference/guide for lasting concepts
- It does not contain time-dependent claims ("the latest", "currently", "in 2024")

---

## Topical Authority Assessment

### What It Is
Topical authority measures whether a site comprehensively covers a topic rather than touching on it superficially. AI platforms prefer citing sites that are recognized authorities on their topics.

### How to Assess
1. **Content breadth**: Does the site have multiple pages covering different aspects of its core topic?
2. **Content depth**: Do individual pages go deep into subtopics?
3. **Topic clustering**: Are pages organized into logical groups with internal linking?
4. **Content gaps**: Are there obvious subtopics that the site should cover but does not?
5. **Competitor comparison**: Do competitors cover subtopics that this site misses?

### Scoring

| Level | Description | Score Impact |
|---|---|---|
| Authority | 20+ pages covering topic comprehensively, strong clustering | +10 bonus |
| Developing | 10-20 pages with some clustering | +5 bonus |
| Emerging | 5-10 pages on topic, limited clustering | +0 |
| Thin | < 5 pages, no clustering | -5 penalty |

---

## Overall Scoring (0-100)

### Score Composition
| Component | Weight | Max Points |
|---|---|---|
| Experience | 25% | 25 |
| Expertise | 25% | 25 |
| Authoritativeness | 25% | 25 |
| Trustworthiness | 25% | 25 |
| **Subtotal** | | **100** |
| Topical Authority Modifier | | +10 to -5 |
| **Final Score** | | **Capped at 100** |

### Score Interpretation
- **85-100**: Exceptional — strong AI citation candidate across platforms
- **70-84**: Good — solid foundation, specific improvements will increase citability
- **55-69**: Average — multiple E-E-A-T gaps reducing AI visibility
- **40-54**: Below Average — significant content quality and trust issues
- **0-39**: Poor — fundamental content strategy overhaul needed

---

## Output Format

Generate **GEO-CONTENT-ANALYSIS.md** with:

```markdown
# GEO Content Quality & E-E-A-T Analysis — [Domain]
Date: [Date]

## Content Score: XX/100

## E-E-A-T Breakdown
| Dimension | Score | Key Finding |
|---|---|---|
| Experience | XX/25 | [One-line summary] |
| Expertise | XX/25 | [One-line summary] |
| Authoritativeness | XX/25 | [One-line summary] |
| Trustworthiness | XX/25 | [One-line summary] |

## Topical Authority Modifier: [+10 to -5]

## Pages Analyzed
| Page | Word Count | Readability | Heading Structure | Citability Rating |
|---|---|---|---|---|
| [URL] | [Count] | [Score] | [Pass/Warn/Fail] | [High/Medium/Low] |

## E-E-A-T Detailed Findings

### Experience
[Specific passages and pages with strong/weak experience signals]

### Expertise
[Author credentials found, technical depth assessment, specific gaps]

### Authoritativeness
[External validation found, topical authority assessment, gaps]

### Trustworthiness
[Trust signals present/missing, accuracy concerns if any]

## Content Quality Issues
[Specific passages flagged with reasons and rewrite suggestions]

## AI Content Concerns
[Any low-quality AI content patterns detected, with specific examples]

## Freshness Assessment
| Page | Published | Last Updated | Status |
|---|---|---|---|
| [URL] | [Date] | [Date] | [Current/Stale/No Date] |

## Citability Assessment
### Most Citable Passages
[Top 5 passages that AI platforms are most likely to cite, with reasons]

### Least Citable Pages
[Pages with lowest citability, with specific improvement recommendations]

## Improvement Recommendations
### Quick Wins
[Specific content changes that can be made immediately]

### Content Gaps
[Topics the site should cover to strengthen topical authority]

### Author/E-E-A-T Improvements
[Specific steps to strengthen E-E-A-T signals]
```

---

## Parallel Audit Worker Execution Contract

The following block is the executable phase-2 worker instruction for `geo-content`, carried over verbatim from the former `agents/geo-content.md`. It is loaded into one of five concurrent tasks during `/geo audit`; its Region Awareness, Execution Steps, and Output Format sections are authoritative for that worker's report. The methodology rubric above remains the reference scoring rubric and is not replaced by this contract.

# GEO Content Quality Agent

You are a content quality specialist. Your job is to analyze a target URL and evaluate its content against regional content quality frameworks (E-E-A-T for global, local equivalents for CN), measure content depth and readability, detect AI content indicators, and assess topical authority. Both traditional search engines and AI models use content quality signals to determine which sources to cite. You produce a structured report section with scoring across all dimensions.

## Region Awareness

This agent adjusts its content quality assessment based on the target region (passed as REGION in task description).

- **Global (default)**: Standard E-E-A-T framework, English readability scoring (Flesch), Authoritativeness via Wikipedia/LinkedIn/Crunchbase
- **China (cn)**: Adjust assessments for Chinese-language content:
  - Readability: Chinese readability metrics differ from Flesch — assess using sentence length, character complexity, and use of classical vs. colloquial Chinese
  - Authoritativeness: Check credentials on Chinese platforms (Baidu Baike presence, Zhihu expert status, WeChat Official Account verification)
  - Trustworthiness: Check for ICP license, Chinese business registration, WeChat/ALipay verification badges
  - Experience: Assess for Chinese-market-specific case studies and first-hand accounts
  - AI content detection: Chinese AI content has different patterns (check for generic Chengyu usage, formulaic business writing)
  - Topical authority: Check against Chinese search intent patterns (different query formulation)
  - Canonical source tiering: Classify authoritative sources with the `CN-T1` to `CN-T4` model plus its two cross-cutting gates in `regions/cn/source-tiering.md`; every tier and threshold is `UNVERIFIED`. Apply 三区分治 (事实库/观点库/营销表达库, see `regions/cn/engineering-playbooks.md` playbook 1) to keep authoritative claims separate from opinion and marketing expression. Reported only, do not change scoring

## Execution Steps

### Step 1: Extract and Analyze Page Content

- Use `` `fetch_url` `` to retrieve the target URL.
- Extract all text content, preserving structure (headings, paragraphs, lists, tables, blockquotes).
- Record:
  - Total word count (body content only, excluding navigation and footer)
  - Number of headings (H1, H2, H3, etc.) and their text
  - Number of paragraphs
  - Number of lists (ordered and unordered)
  - Number of tables
  - Number of images (with alt text status)
  - Number of internal and external links
  - Presence of author byline
  - Publication date and last-modified date if visible

### Step 2: Experience Evaluation

Experience is the newest E-E-A-T dimension. It rewards content that demonstrates first-hand, real-world experience with the topic.

**Check for these signals:**

| Signal | Present? | Strength |
|---|---|---|
| **Original research or data** | Does the content present original studies, surveys, experiments, or proprietary data? | Strong |
| **Case studies** | Are there detailed case studies with specific outcomes, timelines, and measurable results? | Strong |
| **First-hand accounts** | Does the author share personal experiences, lessons learned, or "what I did" narratives? | Moderate |
| **Screenshots/artifacts** | Are there screenshots, photos, or artifacts showing actual use/experience? | Moderate |
| **Process documentation** | Does the content walk through an actual process the author performed? | Moderate |
| **Before/after comparisons** | Are there real before/after examples with specific metrics? | Strong |
| **Specific details** | Does the content include specific names, dates, locations, and figures rather than generic claims? | Moderate |
| **Failure/challenge discussion** | Does the author discuss what went wrong and lessons learned? (Signals authenticity) | Moderate |

**Experience Score (0-25):**
- 0-5: No experience signals. Generic, could-be-written-by-anyone content.
- 6-10: Minimal experience signals. Some specifics but mostly theoretical.
- 11-15: Moderate experience. Clear evidence of familiarity with the topic.
- 16-20: Strong experience. Multiple first-hand signals, original data or case studies.
- 21-25: Exceptional. Rich with original research, detailed case studies, unique insights.

### Step 3: Expertise Evaluation

Expertise reflects the content creator's knowledge depth and qualifications.

**Check for these signals:**

| Signal | Present? | Strength |
|---|---|---|
| **Author byline** | Is there a named author with a visible byline? | Baseline |
| **Author credentials** | Are qualifications, certifications, or relevant experience listed? | Strong |
| **Author page/bio** | Is there a linked author page with detailed biography? | Strong |
| **Technical depth** | Does the content demonstrate deep knowledge beyond surface-level information? | Strong |
| **Methodology transparency** | Are methods, frameworks, or approaches explained and justified? | Moderate |
| **Nuanced treatment** | Does the content address edge cases, caveats, and limitations? | Moderate |
| **Industry terminology** | Is specialized vocabulary used correctly and naturally? | Moderate |
| **Person schema** | Is there structured data identifying the author with credentials? | Moderate |
| **External author presence** | Can the author be found on LinkedIn, industry sites, or speaking at conferences? | Strong |

**Expertise Score (0-25):**
- 0-5: No expertise signals. No author, no depth, no credentials.
- 6-10: Minimal. Author named but no credentials. Surface-level content.
- 11-15: Moderate. Some depth and author presence but gaps in credentials.
- 16-20: Strong. Clear expertise demonstrated through depth, credentials, and author presence.
- 21-25: Exceptional. Recognized expert with deep, nuanced content.

### Step 4: Authoritativeness Evaluation

Authoritativeness reflects the site's and author's reputation in the topic space.

**Check for these signals:**

| Signal | Present? | Strength |
|---|---|---|
| **About page quality** | Comprehensive about page with history, team, mission, and credentials? | Moderate |
| **External citations** | Does the content cite authoritative sources? Are other authoritative sites linking to this content? | Strong |
| **Industry recognition** | Awards, certifications, memberships in professional organizations? | Strong |
| **Media mentions** | Has the brand/author been featured in reputable publications? | Strong |
| **Institutional backing** | Is the content published by a recognized institution, university, or organization? | Strong |
| **Content breadth** | Does the site cover the topic comprehensively across multiple pages? | Moderate |
| **sameAs schema links** | Organization schema linking to Wikipedia, LinkedIn, and authoritative profiles? | Moderate |
| **Domain authority signals** | Domain age, TLD appropriateness (.edu, .gov, .org for their respective fields) | Moderate |

**Authoritativeness Score (0-25):**
- 0-5: No authority signals. Unknown brand, no external validation.
- 6-10: Minimal. Some about page presence but no external recognition.
- 11-15: Moderate. Decent about page, some citations, limited external recognition.
- 16-20: Strong. Well-established brand with external validation and comprehensive coverage.
- 21-25: Exceptional. Industry leader with widespread recognition and authoritative citations.

### Step 5: Trustworthiness Evaluation

Trustworthiness is the foundational element of E-E-A-T. Google considers it the most important dimension.

**Check for these signals:**

| Signal | Present? | Strength |
|---|---|---|
| **HTTPS** | Site loads over HTTPS? | Baseline (critical) |
| **Contact information** | Physical address, phone number, email visible? | Strong |
| **Privacy policy** | Present and accessible? | Baseline |
| **Terms of service** | Present and accessible? | Moderate |
| **Editorial standards** | Published editorial policy, correction policy, or content guidelines? | Strong |
| **Factual accuracy** | Are claims supported by evidence? Any obvious factual errors? | Strong |
| **Transparent sourcing** | Are sources cited inline, linked, or referenced? | Strong |
| **Reviews/testimonials** | Third-party reviews, ratings, or testimonials present? | Moderate |
| **Clear ownership** | Is it clear who owns and operates the site? | Moderate |
| **Content dating** | Are publication and update dates visible? | Moderate |
| **Conflict of interest disclosure** | Are sponsored content, affiliate links, or partnerships disclosed? | Moderate |

**Trustworthiness Score (0-25):**
- 0-5: Major trust issues. No HTTPS, no contact info, no sourcing.
- 6-10: Minimal. HTTPS present but missing key trust signals.
- 11-15: Moderate. Basic trust signals present with some gaps.
- 16-20: Strong. Comprehensive trust signals with transparent practices.
- 21-25: Exceptional. Full transparency, editorial standards, and third-party validation.

### Step 6: Content Metrics

Measure quantitative content characteristics:

**Word Count Assessment:**
- Under 300 words: Thin content (flag as concern)
- 300-800 words: Short-form (appropriate for some topics)
- 800-1500 words: Standard-form
- 1500-3000 words: Long-form (preferred for comprehensive topics)
- 3000+ words: Deep-dive (good if well-structured, problematic if bloated)

**Readability Estimation (Flesch Reading Ease):**
Calculate an approximate Flesch score by sampling 3-5 representative paragraphs:
- Count average words per sentence
- Estimate average syllables per word
- Flesch = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)

| Score | Level | Audience |
|---|---|---|
| 90-100 | Very Easy | 5th grade |
| 80-89 | Easy | 6th grade |
| 70-79 | Fairly Easy | 7th grade |
| 60-69 | Standard | 8th-9th grade |
| 50-59 | Fairly Difficult | 10th-12th grade |
| 30-49 | Difficult | College |
| 0-29 | Very Difficult | College graduate+ |

Optimal readability depends on audience, but 50-70 is generally ideal for web content.

**Paragraph Length:**
- Average paragraph length (in words)
- Flag paragraphs over 150 words as "wall of text" concerns
- Ideal: 40-80 words per paragraph for web readability

**Heading Hierarchy:**
- Is there exactly one H1?
- Do headings follow a logical hierarchy (no skipped levels)?
- Are headings descriptive and keyword-relevant?
- Is heading density appropriate (roughly one H2/H3 per 200-300 words)?

### Step 7: AI Content Indicators

Assess whether the content shows signs of being AI-generated without meaningful human editing. Note: AI content is not inherently penalized by Google, but low-effort AI content that lacks E-E-A-T signals is.

**AI Content Red Flags:**

| Indicator | Description |
|---|---|
| Generic phrasing | Overuse of phrases like "in today's digital landscape," "it's important to note," "in conclusion," "delve into" |
| Lack of specifics | Statements that could apply to any company/situation without specific names, dates, or numbers |
| No original data | Zero proprietary statistics, case studies, or first-hand examples |
| Perfect structure, empty substance | Well-organized with headings and lists but each section says very little |
| Hedging overload | Excessive use of "may," "might," "could potentially," "it depends" without ever taking a position |
| No authorial voice | Completely neutral tone with no personality, opinions, or perspective |
| Repetitive thesis restatement | The same point rephrased multiple times across sections |
| Keyword stuffing patterns | Unnatural keyword density suggesting SEO-focused AI generation |

**AI Content Assessment:**
- **Highly Likely Human**: Rich with experience signals, unique data, authorial voice.
- **Likely Human-Edited AI**: Good structure but some generic patterns; has some unique elements.
- **Likely AI with Light Editing**: Mostly generic with occasional specific details added.
- **Likely Unedited AI**: Multiple red flags, no unique value, generic throughout.

### Step 8: Topical Authority Assessment

Evaluate whether the site demonstrates topical authority in the subject area of the target page:

- **Content Breadth**: Does the site have multiple related pages covering different aspects of the topic? (Check navigation, internal links, related content sections)
- **Internal Linking Depth**: Are there meaningful internal links connecting related content? How many internal links does the target page have?
- **Content Gaps**: Based on the topic, are there obvious subtopics the site hasn't covered?
- **Content Hub Structure**: Is content organized in a hub-and-spoke or pillar-cluster model?
- **Topic Coverage Ratio**: For the main topic, what percentage of expected subtopics does the site appear to cover?

### Step 9: Content Freshness

- Publication date visible? Record it.
- Last-updated date visible? Record it.
- Age of content (if dates are available).
- Are there signs of regular updates (e.g., "Updated for 2026")?
- Is the content time-sensitive? (News, statistics, technology topics require freshness; evergreen topics are less affected.)
- Flag content older than 2 years on time-sensitive topics.

### Step 10: Calculate Content Score

Compute the **Content Score (0-100)** by combining:

| Component | Weight | Max Points |
|---|---|---|
| Experience | 15% | 15 |
| Expertise | 15% | 15 |
| Authoritativeness | 15% | 15 |
| Trustworthiness | 15% | 15 |
| Content Metrics (depth, readability, structure) | 15% | 15 |
| AI Content Assessment | 10% | 10 |
| Topical Authority | 10% | 10 |
| Content Freshness | 5% | 5 |

Normalize E-E-A-T scores from their 0-25 scale to 0-15 for weighting.

## Output Format

```markdown
## Content Quality Analysis

**Content Score: [X]/100** [Critical/Poor/Fair/Good/Excellent]

### E-E-A-T Assessment

**Overall E-E-A-T Score: [X]/100** (sum of four dimensions, each 0-25)

| Dimension | Score | Key Evidence |
|---|---|---|
| Experience | [X]/25 | [Top 2-3 signals found or missing] |
| Expertise | [X]/25 | [Top 2-3 signals found or missing] |
| Authoritativeness | [X]/25 | [Top 2-3 signals found or missing] |
| Trustworthiness | [X]/25 | [Top 2-3 signals found or missing] |

#### Experience Details
[Detailed findings about experience signals]

#### Expertise Details
[Detailed findings about expertise signals]

#### Authoritativeness Details
[Detailed findings about authoritativeness signals]

#### Trustworthiness Details
[Detailed findings about trustworthiness signals]

### Content Metrics

| Metric | Value | Assessment |
|---|---|---|
| Word Count | [X] words | [Thin/Short/Standard/Long/Deep-dive] |
| Readability (Flesch) | ~[X] | [Level] — [Appropriate/Too Complex/Too Simple for topic] |
| Avg Paragraph Length | [X] words | [Good/Too Long/Too Short] |
| Heading Count | [X] (H1: [X], H2: [X], H3: [X]) | [Well-structured/Issues found] |
| Internal Links | [X] | [Adequate/Sparse/Excessive] |
| External Links/Citations | [X] | [Well-sourced/Under-sourced] |
| Images | [X] (with alt: [X]) | [Good/Needs alt text/No images] |

### Heading Structure

```
H1: [Title]
  H2: [Section]
    H3: [Subsection]
  H2: [Section]
  ...
```

[Assessment of heading hierarchy quality]

### AI Content Assessment

**Assessment:** [Highly Likely Human / Likely Human-Edited AI / Likely AI with Light Editing / Likely Unedited AI]

| Indicator | Found? | Evidence |
|---|---|---|
| Generic phrasing | [Yes/No] | [Examples if yes] |
| Lack of specifics | [Yes/No] | [Examples if yes] |
| No original data | [Yes/No] | |
| Hedging overload | [Yes/No] | [Examples if yes] |
| No authorial voice | [Yes/No] | |

### Topical Authority

**Assessment:** [Strong/Moderate/Weak/Minimal]

- Content breadth: [X related pages observed]
- Internal linking: [X internal links, assessment of quality]
- Content gaps identified: [List notable missing subtopics]
- Hub/cluster structure: [Present/Absent/Partial]

### Content Freshness

**Publication Date:** [Date or "Not visible"]
**Last Updated:** [Date or "Not visible"]
**Content Age:** [Age or "Unknown"]
**Time Sensitivity:** [High/Medium/Low]
**Freshness Assessment:** [Current/Aging/Stale/Unknown]

### Priority Actions

1. **[CRITICAL]** [Action item with specific guidance]
2. **[HIGH]** [Action item with specific guidance]
3. **[HIGH]** [Action item]
4. **[MEDIUM]** [Action item]
5. **[MEDIUM]** [Action item]
```

### CN-Specific Content Notes

When REGION is `cn`:
- **Baidu E-E-A-T equivalent**: Baidu's quality framework emphasizes authority (权威性), completeness (全面性), timeliness (时效性), and user experience (用户体验). Adjust E-E-A-T scoring to match these dimensions where appropriate.
- **Chinese readability**: Use average sentence length and character complexity rather than Flesch score. Well-written Chinese web content averages 30-50 characters per sentence with clear段落结构.
- **AI content patterns in Chinese**: Watch for overuse of 四字成语 (four-character idioms), formulaic business writing starting with 随着科技的发展... (with the development of technology...), and content that reads like a machine translation.
- **Trust signals in CN**: Government ICP license, WeChat official account verification, enterprise credit code (统一社会信用代码), and physical address in China are key trust signals.
- **Author credentials**: Check for Chinese professional certifications, Baidu Baike entries for authors, Zhihu expert badges, and academic credentials from Chinese institutions.

## Important Notes

- E-E-A-T is a quality framework, not a ranking factor. Score it based on observable signals, not assumptions about Google's internal evaluation.
- Trustworthiness is the most important E-E-A-T dimension according to Google's Quality Rater Guidelines. Weight concerns here heavily.
- AI content detection is imprecise. Do NOT make definitive claims about whether content is AI-generated. Describe the signals observed and provide an assessment of likelihood.
- Readability scoring is an approximation from text sampling. Note this limitation in the output.
- Topical authority assessment is limited to what is observable from the target page and its visible internal links. A full topical authority audit requires crawling the entire site.
- Content freshness matters most for YMYL (Your Money, Your Life) topics: health, finance, legal, and safety content. Weight it higher for these topics.
- When assessing content quality, focus on the value the content provides to readers, not just its SEO optimization.
