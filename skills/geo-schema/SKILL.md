---
name: geo-schema
description: Schema.org structured data audit and generation optimized for AI discoverability — detect, validate, and generate JSON-LD markup
version: 1.0.0
author: geo-seo-claude
tags: [geo, schema, structured-data, json-ld, entity-recognition, ai-discoverability]
---

<!-- GEO-CN-VARIANT:v1 -->

**Conditional CN variant.** Only when `REGION` resolves to `cn`, read `references/cn.md` and apply its overrides; its CN knowledge files are enumerated in the geo skill's `regions/cn-variants.json` (self-locating resolution is documented in `geo/SKILL.md` → "CN variant loading"). For `global` or any non-CN region, do NOT load `references/cn.md` or any `regions/cn/` file.

# GEO Schema & Structured Data

<!-- GEO-SCRIPT-RESOLUTION:v1 -->

**Script resolution.** Set `SKILL_DIR` to this SKILL.md's directory. Resolve `GEO_SCRIPTS` as the first existing of `"$SKILL_DIR/scripts"`, `"$SKILL_DIR/../geo/scripts"`, `"$SKILL_DIR/../../geo/scripts"`, `"$SKILL_DIR/../../../.claude/skills/geo/scripts"` (full preamble in `geo/SKILL.md` → "Script Path Resolution"). Set `PY="$(command -v python3 || command -v python)"`, then invoke scripts as `"$PY" "$GEO_SCRIPTS/<script>.py" ...`. Windows runs through Git Bash, which supplies these commands and forward-slash paths; native PowerShell/CMD is out of scope.

## Purpose

Structured data is the primary machine-readable signal that tells AI systems what an entity IS, what it does, and how it connects to other entities. While schema markup has traditionally been about earning Google rich results, its role in GEO is fundamentally different: **structured data is how AI models understand and trust your entity**. A complete entity graph in structured data dramatically increases citation probability across all AI search platforms.

## How to Use This Skill

1. Fetch the target page HTML using `fetch_page.py` (see note below)
2. Detect all existing structured data (JSON-LD, Microdata, RDFa)
3. Validate detected schemas against Schema.org specifications
4. Identify missing recommended schemas based on business type
5. Generate ready-to-use JSON-LD code blocks
6. Output GEO-SCHEMA-REPORT.md

---

## Step 1: Detection

**IMPORTANT:** `` `fetch_url` `` converts HTML to markdown and strips `<head>` content, which removes JSON-LD blocks. Use `fetch_page.py` instead:
```bash
"$PY" "$GEO_SCRIPTS/fetch_page.py" <url> page
```
The output includes a `structured_data` array with all parsed JSON-LD blocks from the page.

### Scan for JSON-LD
Look for `<script type="application/ld+json">` blocks in the HTML. Parse each block as JSON. A page may contain multiple JSON-LD blocks — collect all of them.

### Scan for Microdata
Look for elements with `itemscope`, `itemtype`, and `itemprop` attributes. Map the hierarchy of nested items. Note: Microdata is harder for AI crawlers to parse than JSON-LD. Flag a recommendation to migrate to JSON-LD if Microdata is the only format found.

### Scan for RDFa
Look for elements with `typeof`, `property`, and `vocab` attributes. Similar to Microdata — recommend migration to JSON-LD.

### Priority Order
JSON-LD is the **strongly recommended format** for GEO. Google, Bing, and AI platforms all process JSON-LD most reliably. If the site uses Microdata or RDFa exclusively, flag this as a high-priority migration.

---

## Step 2: Validation

For each detected schema block, validate:

1. **Valid JSON**: Is the JSON-LD syntactically valid? Check for trailing commas, unquoted keys, malformed strings.
2. **Valid @type**: Does the `@type` match a recognized Schema.org type? Check against https://schema.org/docs/full.html.
3. **Required Properties**: Does the schema include all required properties for its type? (See per-type requirements below.)
4. **Recommended Properties**: Does the schema include recommended properties that increase AI discoverability?
5. **sameAs Links**: Does the schema include `sameAs` properties linking to other platform presences?
6. **URL Validity**: Do all URLs in the schema resolve (not 404)?
7. **Nesting**: Is the schema properly nested (e.g., author inside Article, address inside Organization)?
8. **Rendering Method**: Is the JSON-LD in the server-rendered HTML or injected via JavaScript? Per Google's December 2025 guidance, **JavaScript-injected structured data may face delayed processing**. Flag any schema that requires JS execution.

---

## Step 3: Schema Types for GEO

### Organization (CRITICAL — every business site)
Essential for entity recognition across all AI platforms. This is how AI models identify WHAT the business is.

**Required properties:**
- `@type`: "Organization" (or subtype: Corporation, LocalBusiness, etc.)
- `name`: Official business name
- `url`: Official website URL
- `logo`: URL to logo image (ImageObject preferred)

**Recommended properties for GEO:**
- `sameAs`: Array of ALL platform URLs (see sameAs strategy below)
- `description`: 1-2 sentence description of the organization
- `foundingDate`: ISO 8601 date
- `founder`: Person schema
- `address`: PostalAddress schema
- `contactPoint`: ContactPoint with telephone, email, contactType
- `areaServed`: Geographic area
- `numberOfEmployees`: QuantitativeValue
- `industry`: Text or DefinedTerm
- `award`: Array of awards received
- `knowsAbout`: Array of topics the organization is expert in (strong GEO signal)

### LocalBusiness (for businesses with physical locations)
Extends Organization. Critical for local AI search results and Google Gemini.

**Additional required properties:**
- `address`: Full PostalAddress
- `telephone`: Phone number
- `openingHoursSpecification`: Operating hours

**Recommended for GEO:**
- `geo`: GeoCoordinates (latitude, longitude)
- `priceRange`: Price indicator
- `aggregateRating`: AggregateRating schema
- `review`: Array of Review schemas
- `hasMap`: URL to Google Maps

### Article + Author (CRITICAL for publishers)
The Author schema is one of the strongest E-E-A-T signals for AI platforms.

**Article required:**
- `@type`: "Article" (or NewsArticle, BlogPosting, TechArticle)
- `headline`: Article title
- `datePublished`: ISO 8601
- `dateModified`: ISO 8601 (critical for freshness signals)
- `author`: Person or Organization schema
- `publisher`: Organization schema with logo
- `image`: Representative image

**Author (Person) required for GEO:**
- `name`: Full name
- `url`: Author page URL on the site
- `sameAs`: LinkedIn, Twitter, personal site, Google Scholar, ORCID
- `jobTitle`: Professional title
- `worksFor`: Organization schema
- `knowsAbout`: Array of expertise areas
- `alumniOf`: Educational institutions
- `award`: Professional awards

### Product (for e-commerce)
**Required:**
- `name`, `description`, `image`
- `offers`: Offer with price, priceCurrency, availability
- `brand`: Brand schema
- `sku` or `gtin`/`mpn`

**Recommended for GEO:**
- `aggregateRating`: AggregateRating
- `review`: Array of individual reviews
- `category`: Product category
- `material`, `weight`, `width`, `height` (where applicable)

### FAQPage
**Status as of 2024**: Google restricts FAQ rich results to government and health sites. However, the FAQPage schema still serves GEO purposes — AI platforms parse FAQ structured data for question-answer extraction. Implement it for AI readability even though rich results may not appear.

**Structure:**
- `@type`: "FAQPage"
- `mainEntity`: Array of Question schemas, each with `acceptedAnswer` containing an Answer schema

### SoftwareApplication (for SaaS)
**Required:**
- `name`, `description`
- `applicationCategory`: e.g., "BusinessApplication"
- `operatingSystem`: Supported platforms
- `offers`: Pricing

**Recommended for GEO:**
- `aggregateRating`: User ratings
- `featureList`: Array of features (strong citation signal)
- `screenshot`: Screenshots
- `softwareVersion`: Current version
- `releaseNotes`: Link to changelog

### WebSite + SearchAction (for sitelinks search box)
**Structure:**
```json
{
  "@type": "WebSite",
  "name": "Site Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### Person (standalone — for personal brands, authors, thought leaders)
Use as a standalone schema on About/Bio pages. This builds the entity graph for individual expertise.

**Required:** `name`, `url`
**Recommended for GEO:** `sameAs`, `jobTitle`, `worksFor`, `knowsAbout`, `alumniOf`, `award`, `description`, `image`

### speakable Property (for voice/AI assistants)
The `speakable` property marks specific sections of content as particularly suitable for voice and AI assistant consumption. Add to Article or WebPage schemas.

```json
{
  "@type": "Article",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".key-takeaway"]
  }
}
```
This signals to AI assistants which passages are the best candidates for citation or reading aloud.

---

## Step 4: Deprecated/Changed Schemas to Flag

| Schema | Status | Note |
|---|---|---|
| HowTo | Rich results deprecated Aug 2023 | Still useful for AI parsing, but do not promise rich results |
| FAQPage | Restricted to govt/health Aug 2023 | Still useful for AI parsing (see above) |
| SpecialAnnouncement | Deprecated 2023 | Was for COVID; remove if still present |
| CourseInfo | Replaced by Course updates 2024 | Use updated Course schema properties |
| VideoObject `contentUrl` | Changed behavior 2024 | Must point to actual video file, not page URL |
| Review snippet | Stricter enforcement 2024 | Self-serving reviews on product pages may not display |

Flag any deprecated schemas found and recommend replacements.

---

## Step 5: sameAs Strategy (CRITICAL for Entity Recognition)

The `sameAs` property is the single most important structured data property for GEO. It tells AI systems: "This entity on my website is the SAME entity as these profiles elsewhere." This creates the entity graph that AI platforms use to verify, trust, and cite sources.

### Recommended sameAs Links (in priority order)

1. **Wikipedia article** — highest authority entity link
2. **Wikidata item** — machine-readable entity identifier (e.g., `https://www.wikidata.org/wiki/Q12345`)
3. **LinkedIn** — company page or personal profile
4. **YouTube** — channel URL
5. **Twitter/X** — profile URL
6. **Facebook** — page URL
7. **Crunchbase** — company profile (for startups/tech)
8. **GitHub** — organization or personal profile (for tech)
9. **Google Scholar** — author profile (for researchers/academics)
10. **ORCID** — researcher identifier (for academics)
11. **Instagram** — profile URL
12. **Apple App Store / Google Play** — app listings (for software)
13. **BBB** — Better Business Bureau listing (for US businesses)
14. **Industry directories** — relevant vertical directories

### sameAs Audit Process
1. Collect all known web presences for the entity
2. Check that each URL resolves (not 404 or redirected)
3. Verify the Organization/Person schema includes ALL of them
4. Check that the information on each platform is consistent (name, description, founding date, etc.)
5. Flag any platforms where the entity should have a presence but does not

---

## Step 6: JSON-LD Generation

Based on the detected business type, generate ready-to-paste JSON-LD blocks. Always generate:

1. **Organization or Person** (depending on entity type) — always
2. **WebSite with SearchAction** — always for the homepage
3. **Business-type-specific** — Article for publishers, Product for e-commerce, LocalBusiness for local, SoftwareApplication for SaaS
4. **BreadcrumbList** — for any page deeper than homepage

### Generation Rules
- Use the `@graph` pattern to include multiple schemas in one JSON-LD block
- All URLs must be absolute (not relative)
- Include `@id` properties for cross-referencing between schemas
- Use ISO 8601 for all dates
- Include `speakable` on Article schemas with CSS selectors pointing to key content sections
- Place JSON-LD in `<head>` section — NOT injected via JavaScript

### Template: Organization with Full GEO Signals
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 600,
    "height": 60
  },
  "description": "Concise description of what the company does.",
  "foundingDate": "2020-01-15",
  "founder": {
    "@type": "Person",
    "name": "Founder Name",
    "sameAs": "https://www.linkedin.com/in/founder"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service",
    "email": "support@example.com"
  },
  "sameAs": [
    "https://en.wikipedia.org/wiki/Company_Name",
    "https://www.wikidata.org/wiki/Q12345",
    "https://www.linkedin.com/company/company-name",
    "https://www.youtube.com/@companyname",
    "https://twitter.com/companyname",
    "https://github.com/companyname",
    "https://www.crunchbase.com/organization/company-name"
  ],
  "knowsAbout": [
    "Topic 1",
    "Topic 2",
    "Topic 3"
  ]
}
```

---

## Scoring Rubric (0-100)

| Criterion | Points | How to Score |
|---|---|---|
| Organization/Person schema present and complete | 15 | 15 if full, 10 if basic, 0 if none |
| sameAs links (5+ platforms) | 15 | 3 per valid sameAs link, max 15 |
| Article schema with author details | 10 | 10 if full author schema, 5 if name only, 0 if none |
| Business-type-specific schema present | 10 | 10 if complete, 5 if partial, 0 if missing |
| WebSite + SearchAction | 5 | 5 if present, 0 if not |
| BreadcrumbList on inner pages | 5 | 5 if present, 0 if not |
| JSON-LD format (not Microdata/RDFa) | 5 | 5 if JSON-LD, 3 if mixed, 0 if only Microdata/RDFa |
| Server-rendered (not JS-injected) | 10 | 10 if in HTML source, 5 if JS but in head, 0 if dynamic JS |
| speakable property on articles | 5 | 5 if present, 0 if not |
| Valid JSON + valid Schema.org types | 10 | 10 if no errors, 5 if minor issues, 0 if major errors |
| knowsAbout property on Organization/Person | 5 | 5 if present with 3+ topics, 0 if missing |
| No deprecated schemas present | 5 | 5 if clean, 0 if deprecated schemas found |

---

## Output Format

Generate **GEO-SCHEMA-REPORT.md** with:

```markdown
# GEO Schema & Structured Data Report — [Domain]
Date: [Date]

## Schema Score: XX/100

## Detected Schemas
| Page | Schema Type | Format | Status | Issues |
|---|---|---|---|---|
| / | Organization | JSON-LD | Valid | Missing sameAs |
| /blog/post-1 | Article | JSON-LD | Valid | No author schema |

## Validation Results
[List each schema with pass/fail per property]

## Missing Recommended Schemas
[List schemas that should be present based on business type but are not]

## sameAs Audit
| Platform | URL | Status |
|---|---|---|
| Wikipedia | [URL or "Not found"] | Present/Missing |
| LinkedIn | [URL or "Not found"] | Present/Missing |
[Continue for all recommended platforms]

## Generated JSON-LD Code
[Ready-to-paste JSON-LD blocks for each missing or incomplete schema]

## Implementation Notes
- Where to place each JSON-LD block
- Server-rendering requirements
- Testing with Google Rich Results Test and Schema.org Validator
```

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
