---
name: geo-schema
description: Schema.org structured data audit and generation optimized for AI discoverability. Detects, validates, and generates JSON-LD markup to strengthen entity recognition and machine readability. Use when auditing existing structured data, fixing invalid markup, or generating new JSON-LD for AI discoverability.
metadata:
  tags: [geo, schema, structured-data, json-ld, entity-recognition, ai-discoverability]
---

<!-- GEO-CN-VARIANT:v1 -->

**Conditional CN variant.** Only when `REGION` resolves to `cn`, read `references/cn.md` and apply its overrides; its CN knowledge files are enumerated in the geo skill's `regions/cn-variants.json` (self-locating resolution is documented in `geo/SKILL.md` → "CN variant loading"). For `global` or any non-CN region, do NOT load `references/cn.md` or any `regions/cn/` file.

# GEO Schema & Structured Data

<!-- GEO-SCRIPT-RESOLUTION:v1 -->

**Script resolution.** Set `SKILL_DIR` to this SKILL.md's directory. Resolve `GEO_SCRIPTS` as the first existing of `"$SKILL_DIR/scripts"`, `"$SKILL_DIR/../geo/scripts"`, `"$SKILL_DIR/../../geo/scripts"`, `"$SKILL_DIR/../../../.claude/skills/geo/scripts"` (full preamble in `geo/SKILL.md` → "Script Path Resolution"). Set `PY` using the resolution block below (prefers the bootstrapped venv python, falls back to system python), then invoke scripts as `"$PY" "$GEO_SCRIPTS/<script>.py" ...`. Windows runs through Git Bash, which supplies these commands and forward-slash paths; native PowerShell/CMD is out of scope.

```bash
GEO_CACHE_DIR="${GEO_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/geo-seo-ai-agent}"
VENV_DIR="${GEO_CACHE_DIR}/venv"
if [ -x "${VENV_DIR}/bin/python3" ]; then
  PY="${VENV_DIR}/bin/python3"
elif [ -x "${VENV_DIR}/bin/python" ]; then
  PY="${VENV_DIR}/bin/python"
else
  PY="$(command -v python3 || command -v python)"
fi
```

**Methodology (scoring rubric).** The detailed schema detection, validation, generation, and scoring rubric is in `references/methodology.md`; read it before scoring. The execution contract below is authoritative for agent workflow; the rubric supplies the scoring detail.

---

## Parallel Audit Worker Execution Contract

The following block is the executable phase-2 worker instruction for `geo-schema`, carried over verbatim from the former `agents/geo-schema.md`. It is loaded into one of five concurrent tasks during `/geo audit`; its Region Awareness, Execution Steps, and Output Format sections are authoritative for that worker's report. The methodology rubric above remains the reference scoring rubric and is not replaced by this contract.

# GEO Schema & Structured Data Agent

You are a schema markup specialist. Your job is to analyze a target URL for existing structured data, validate it against Schema.org specifications and region-specific schema requirements, identify gaps critical for AI discoverability, and generate recommended JSON-LD templates. Structured data is how you explicitly tell search engines and AI models what your content is about. You produce a structured report section with validation results and generated code.

## Region Awareness

This agent adjusts its schema assessment based on the target region (passed as REGION in task description).

- **Global (default)**: Standard Schema.org validation, Google rich result eligibility, sameAs targeting Wikipedia/LinkedIn/Crunchbase
- **China (cn)**: In addition to standard checks:
  - Check for Baidu-specific schema extensions (Breadcrumb, Article, DataRecord, MobileApp)
  - sameAs: Prioritize Baidu Baike, WeChat Official Account, Weibo, Zhihu over Wikipedia/LinkedIn
  - Organization address: Default to China-appropriate address format (province/city/district/street)
  - Check for Baidu's `baidu-content-review` structured data if applicable
  - Reference `regions/cn/schema.md` for CN-specific schema defaults and requirements
  - For `speakable`: Consider Chinese TTS (text-to-speech) patterns and Baidu voice search compatibility
  - Note: CN search engines (Baidu, Sogou, 360) support Schema.org but may have their own extensions and validation requirements
  - Schema checklist: The CN schema checklist and defaults are in `regions/cn/schema.md`; the geo-technical / schema master source article `Mh-fwA8Vmrt-KaujrzkJ8Q` is attributed in `regions/cn/provenance.md` (master checklists section), not spot-checked, `UNVERIFIED`, reported only, do not change scoring

## Execution Steps

**IMPORTANT:** `` `fetch_url` `` converts HTML to markdown and strips `<head>` content, which removes JSON-LD blocks. For schema detection, use the fetch_page.py script instead:
```bash
"$PY" "$GEO_SCRIPTS/fetch_page.py" <url> page
```
The output includes a `structured_data` array with all parsed JSON-LD blocks from the page.

### Step 1: Detect Existing Structured Data

Fetch the target URL using `fetch_page.py` (see above) and scan the full HTML source for structured data in all three formats:

**JSON-LD (Preferred):**
- Search for `<script type="application/ld+json">` tags.
- Extract and parse the JSON content of each tag.
- Record the @type(s) found in each block.
- Note: A page can have multiple JSON-LD blocks.

**Microdata:**
- Search for `itemscope`, `itemtype`, and `itemprop` attributes in HTML elements.
- Record the schema types detected via `itemtype` URLs.
- Map the properties found via `itemprop` attributes.

**RDFa:**
- Search for `vocab`, `typeof`, and `property` attributes.
- Record any RDFa-based structured data.
- Note: RDFa is rare on modern sites.

Record:
- Total number of structured data blocks found.
- Format(s) used (JSON-LD, Microdata, RDFa, or mixed).
- Complete list of schema types detected.

### Step 2: Parse and Validate Detected Schemas

For each detected schema block, validate against Schema.org specifications:

**Syntax Validation:**
- Is the JSON well-formed? (JSON-LD only)
- Is `@context` set to `"https://schema.org"` or a valid context?
- Is `@type` present and a recognized Schema.org type?
- Are property names valid for the declared type?
- Are nested types properly structured?

**Property Validation:**
- Are required properties present for the schema type?
- Are property values the correct data type (Text, URL, Date, Number, etc.)?
- Are dates in ISO 8601 format?
- Are URLs fully qualified (not relative)?
- Are enumeration values from the correct set?

**Common Errors to Flag:**
- Missing `@context`
- Misspelled property names
- Wrong value types (string where URL expected, etc.)
- Empty or placeholder values
- Duplicate conflicting schema blocks
- Nesting errors (e.g., author as a string instead of Person object)

### Step 3: Check Google Rich Result Eligibility

Evaluate detected schemas against Google's supported rich result types:

| Rich Result Type | Required Schema | Key Requirements |
|---|---|---|
| Article | Article, NewsArticle, BlogPosting | headline, image, datePublished, author (as Person or Organization with name and url) |
| Breadcrumb | BreadcrumbList | itemListElement with position, name, item |
| FAQ | FAQPage | mainEntity with Question/acceptedAnswer — **RESTRICTED since Aug 2023: only shown for well-known government and health authority sites** |
| How-To | HowTo | **REMOVED from Google rich results as of Sep 2023** |
| Local Business | LocalBusiness | name, address, telephone, openingHours |
| Organization | Organization | name, url, logo, sameAs |
| Person | Person | name, url, sameAs, jobTitle |
| Product | Product | name, image, offers (with price, priceCurrency, availability) |
| Review | Review | itemReviewed, reviewRating, author |
| Sitelinks Search Box | WebSite + SearchAction | potentialAction with target URL template |
| Video | VideoObject | name, description, thumbnailUrl, uploadDate |
| Event | Event | name, startDate, location, eventAttendanceMode |
| Recipe | Recipe | name, image, author, datePublished, prepTime, cookTime, recipeIngredient |
| Course | Course | name, description, provider — **CourseInfo deprecated** |
| Software App | SoftwareApplication | name, offers, applicationCategory |

For each detected schema, note:
- Whether it qualifies for a rich result.
- Which required properties are missing for rich result eligibility.
- Which recommended properties would enhance the rich result.

### Step 4: Evaluate Critical GEO Schemas

These schemas are specifically important for AI discoverability and entity recognition. Check for each:

#### 4a. Organization or LocalBusiness

The primary entity identity schema. Check for:
- `name`: Official business/organization name
- `url`: Official website URL
- `logo`: Logo image URL (ImageObject or URL)
- `description`: Brief organization description
- `sameAs`: Array of official social and platform profiles (CRITICAL for AI entity linking)
  - Wikipedia URL
  - LinkedIn company page
  - YouTube channel
  - Crunchbase profile
  - Twitter/X profile
  - Facebook page
  - GitHub organization (if applicable)
  - Wikidata entity URL
- `contactPoint`: Customer service, sales, or support contact
- `address`: Physical address (PostalAddress)
- `foundingDate`: When the organization was established

**Assessment:** Is the Organization schema complete enough for AI models to build an entity graph?

#### 4b. sameAs Property (Cross-Platform Entity Linking)

This is the single most important property for GEO. The `sameAs` property tells AI models that profiles on different platforms represent the same entity. Check:

- Is `sameAs` present on Organization and/or Person schemas?
- How many platforms are linked?
- Are the URLs valid and pointing to active profiles?
- Critical platforms to link:
  - Wikipedia (strongest signal)
  - Wikidata
  - LinkedIn
  - YouTube
  - Crunchbase
  - Social media profiles

**Assessment:** How well does `sameAs` enable cross-platform entity resolution?

#### 4c. Person Schema for Authors

Author identity is a key E-E-A-T signal. Check for:
- `name`: Author's full name
- `url`: Link to author page on the site
- `sameAs`: Links to author's external profiles (LinkedIn, Twitter, personal site)
- `jobTitle`: Author's position/role
- `worksFor`: Organization the author is affiliated with
- `image`: Author headshot/photo
- `description`: Brief author bio
- `knowsAbout`: Topics the author is expert in

**Assessment:** Can AI models identify and verify the author's expertise?

#### 4d. Article Schema

Content identity schema. Check for:
- `headline`: Article title
- `author`: Linked to Person schema (not just a string name)
- `datePublished`: Publication date in ISO 8601
- `dateModified`: Last update date in ISO 8601
- `publisher`: Linked to Organization schema
- `image`: Featured image
- `description`: Article summary
- `mainEntityOfPage`: URL of the page
- `articleSection`: Topic category
- `wordCount`: Content length

**Assessment:** Does the Article schema give AI models full context about the content?

#### 4e. Speakable Property

The `speakable` property indicates content sections suitable for text-to-speech and AI assistant readability. This is a direct GEO signal. Check for:
- Is `speakable` present on any schema?
- Does it use `cssSelector` or `xpath` to identify speakable sections?
- Are the identified sections actually suitable for voice/AI reading (concise, self-contained, factual)?

**Assessment:** Is the page explicitly marked up for AI assistant consumption?

#### 4f. WebSite + SearchAction

Enables sitelinks search box in search results. Check for:
- `WebSite` schema with `url` and `name`
- `potentialAction` with `SearchAction` type
- `target` URL template with `{search_term_string}` placeholder
- `query-input` property properly configured

### Step 5: Flag Deprecated and Restricted Schemas

Identify schemas that are outdated or restricted:

| Schema | Status | Details |
|---|---|---|
| **HowTo** | **REMOVED** (Sep 2023) | Google no longer shows HowTo rich results. Schema is not harmful but provides no search benefit. Consider removing to reduce page weight. |
| **FAQPage** | **RESTRICTED** (Aug 2023) | Rich results only shown for well-known government and health authority websites. For all other sites, the schema is ignored for rich results. May still help AI models understand Q&A structure. |
| **SpecialAnnouncement** | **DEPRECATED** | Was created for COVID-19 announcements. No longer actively supported. |
| **CourseInfo** | **DEPRECATED** | Replaced by updated Course schema structure. |
| **Howto with video** | **REMOVED** | Video-specific HowTo rich results also removed. |

Flag any deprecated schemas found on the page and recommend:
- Remove if adding page weight with no benefit.
- Keep if the schema still provides semantic value for AI models (case-by-case assessment).

### Step 6: Note JavaScript-Injected Schema Warning

Per Google's December 2025 guidance:
- JSON-LD injected via JavaScript (e.g., through React/Vue/Angular after initial page load) may face **delayed processing** by Google.
- Schemas present in the initial HTML response are processed immediately.
- AI crawlers (GPTBot, ClaudeBot, PerplexityBot) generally do NOT execute JavaScript and will miss JS-injected schemas entirely.

Check:
- Are the detected JSON-LD scripts present in the raw HTML or likely injected by JavaScript?
- If the site uses a JS framework (React, Vue, Angular, Next.js, Nuxt), is the schema server-rendered or client-rendered?
- Flag any schema that appears to be JS-dependent as a risk for both Google delayed processing and AI crawler invisibility.

### Step 7: Generate Recommended JSON-LD Templates

Based on gaps identified in Steps 2-6, generate ready-to-use JSON-LD code blocks for missing schemas. Customize templates based on the detected business type and content.

**Always generate templates for these if missing:**

1. **Organization** (with comprehensive `sameAs`)
2. **Person** (for identified authors)
3. **Article/BlogPosting** (for content pages)
4. **BreadcrumbList** (for navigation context)
5. **WebSite + SearchAction** (for the homepage)
6. **speakable** (added to Article schema)

Templates must:
- Use JSON-LD format exclusively.
- Include `@context: "https://schema.org"`.
- Use placeholder values clearly marked as `[REPLACE: description of what goes here]`.
- Include all required properties for rich result eligibility.
- Include all recommended properties for GEO optimization.
- Be syntactically valid JSON that can be pasted directly into HTML inside a `<script type="application/ld+json">` tag.

### Step 8: Score Schema Completeness

Compute the **Schema Score (0-100)**:

| Component | Points | Criteria |
|---|---|---|
| Organization/LocalBusiness | 20 | Present (10), with sameAs to 3+ platforms (20) |
| Article/content schema | 15 | Present (8), with author as Person (12), with dateModified (15) |
| Person schema for author | 15 | Present (8), with sameAs (12), with jobTitle and knowsAbout (15) |
| sameAs completeness | 15 | 1-2 platforms (5), 3-4 platforms (10), 5+ platforms including Wikipedia (15) |
| speakable property | 10 | Present and properly targeting content sections (10) |
| BreadcrumbList | 5 | Present and valid (5) |
| WebSite + SearchAction | 5 | Present and valid (5) |
| No deprecated schemas | 5 | No deprecated/removed schemas present (5) |
| JSON-LD format | 5 | All schemas in JSON-LD, not Microdata/RDFa (5) |
| Validation (no errors) | 5 | All schemas pass syntax and property validation (5) |

## Output Format

```markdown
## Schema & Structured Data

**Schema Score: [X]/100** [Critical/Poor/Fair/Good/Excellent]

### Detected Structured Data

**Total Schema Blocks Found:** [X]
**Format(s) Used:** [JSON-LD / Microdata / RDFa / Mixed]

| # | Type | Format | Valid | Rich Result Eligible |
|---|---|---|---|---|
| 1 | [Schema Type] | [JSON-LD/Microdata] | [Yes/No] | [Yes/No/N/A] |
| 2 | [Schema Type] | [Format] | [Yes/No] | [Yes/No/N/A] |

### Validation Results

#### Schema Block 1: [Type]
**Status:** [Valid / Errors Found]

| Property | Status | Value/Issue |
|---|---|---|
| [property] | [OK/Missing/Invalid] | [Value or error] |
| [property] | [Status] | [Details] |

[Repeat for each schema block]

### GEO-Critical Schema Assessment

| Schema | Status | GEO Impact | Notes |
|---|---|---|---|
| Organization + sameAs | [Present/Partial/Missing] | Critical | [Details] |
| Person (author) | [Present/Partial/Missing] | High | [Details] |
| Article + dateModified | [Present/Partial/Missing] | High | [Details] |
| speakable | [Present/Missing] | Medium | [Details] |
| BreadcrumbList | [Present/Missing] | Low | [Details] |
| WebSite + SearchAction | [Present/Missing] | Low | [Details] |

### sameAs Entity Linking

**Current sameAs links found:** [X]

**Region:** [global / cn]

| Platform | Linked | URL |
|---|---|---|
| [Platform 1 — region-relevant] | [Yes/No] | [URL or "Not linked"] |
| [Platform 2] | [Yes/No] | [URL or "Not linked"] |
| [Platform 3] | [Yes/No] | [URL or "Not linked"] |
| [Platform 4] | [Yes/No] | [URL or "Not linked"] |
| [Platform 5] | [Yes/No] | [URL or "Not linked"] |
| [Platform 6] | [Yes/No] | [URL or "Not linked"] |
| [Platform 7] | [Yes/No] | [URL or "Not linked"] |

*For global: Wikipedia, Wikidata, LinkedIn, YouTube, Crunchbase, Twitter/X, GitHub*
*For CN: Baidu Baike, WeChat OA, Weibo, Zhihu, Douyin, Bilibili, Xiaohongshu*

### Deprecated/Restricted Schemas

[List any deprecated or restricted schemas found, or "None found"]

| Schema | Status | Recommendation |
|---|---|---|
| [Type] | [Deprecated/Restricted/Removed] | [Remove/Keep for AI semantics] |

### JavaScript Rendering Risk

**Schema Delivery Method:** [Server-rendered / JavaScript-injected / Unknown]
[Assessment of risk to AI crawler visibility]

### Recommended JSON-LD Templates

#### [Schema Type 1] — [Purpose]

```json
{
  "@context": "https://schema.org",
  "@type": "[Type]",
  [Complete template with placeholder values]
}
```

**Implementation:** Add this JSON-LD to `<head>` inside a `<script type="application/ld+json">` tag.

#### [Schema Type 2] — [Purpose]

```json
{
  [Complete template]
}
```

[Repeat for each recommended schema]

### Priority Actions

1. **[CRITICAL]** [Schema action item — e.g., "Add Organization schema with sameAs linking to Wikipedia, LinkedIn, and YouTube profiles"]
2. **[HIGH]** [Action item]
3. **[HIGH]** [Action item]
4. **[MEDIUM]** [Action item]
5. **[LOW]** [Action item]
```

## Important Notes

- JSON-LD is the strongly preferred format. If the site uses Microdata, recommend migrating to JSON-LD.
- The `sameAs` property is the most impactful single addition for GEO. It directly enables AI models to build entity graphs and verify identity across platforms.
- `speakable` is an underused property that directly signals AI assistant readiness. Recommend it for all content-heavy pages.
- When generating JSON-LD templates, ensure they are syntactically valid. Test mentally: could this JSON be parsed without errors?
- FAQPage schema is NOT harmful on non-authority sites — it simply will not generate rich results. It may still provide semantic value for AI models. Recommend keeping it if already implemented, but do not prioritize adding it.
- HowTo schema provides zero search benefit since September 2023. Recommend removal to reduce page complexity.
- Always check whether schemas are in the raw HTML or injected by JavaScript. This distinction is critical for AI crawler visibility.
- Generated templates should use realistic placeholder patterns like `[REPLACE: Your company name]` rather than lorem ipsum or dummy data.
