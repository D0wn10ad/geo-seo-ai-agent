# Regional Profiles for GEO-SEO AI Agent

This directory defines region-specific profiles for the GEO audit pipeline. Each region profile contains scoring weights, AI engine lists, brand platforms, crawler configurations, and technical check presets.

## How region detection works

The `scripts/region_resolver.py` script handles region resolution:

1. If `--region <code>` is passed explicitly, use that region
2. Otherwise, auto-detect from the URL and page content:
   - Domain TLD (`.cn`, `.com.cn` → CN)
   - Content language detection (Chinese content → CN)
   - Multi-language sites → prompt user for choice
3. If detection is ambiguous, the user is asked before any crawling begins

## Adding a new region

To add a new region (e.g., `kr` for South Korea):

### 1. Add region profile to `profiles.yaml`

Add a new section under `regions:`:

```yaml
  kr:
    label: "South Korea"
    code: kr
    description: >
      South Korean market. Uses Naver, Kakao, and local AI platforms.
    tlds: [.kr, .co.kr]
    languages: [ko]
    scoring_weights:
      citability: 25
      brand: 20
      eeat: 20
      technical: 15
      schema: 10
      platform: 10
    ai_engines:
      - naver_search
      - kakao_brain
      - clova_x
    brand_platforms:
      - id: namuwiki
        name: Namu Wiki (나무위키)
        weight: 25
      - id: naver_cafe
        name: Naver Cafe
        weight: 20
      - id: kakao_talk
        name: KakaoTalk
        weight: 15
    crawlers:
      - Yeti
      - DaumBot
    schema_defaults:
      address_country: KR
      same_as_platforms: [namuwiki, naver]
    technical_checks:
      - mobile_optimization
      - sitemap_robots
```

### 2. (Optional) Add reference data

Create a `regions/<code>/` directory with reference documents:

```
regions/kr/
├── ai-engines.md     # KR AI engine evaluation criteria
├── platforms.md      # KR brand platform scoring data
└── schema.md         # KR schema guidance
```

### 3. (Optional) Create SKILL overrides

If individual commands need region-specific behavior, create `SKILL.<code>.md` files in the relevant skill directories:

```
skills/geo-platform-optimizer/
  SKILL.md            # base (already exists)
  SKILL.kr.md         # KR-specific AI engine rubrics (create this)
skills/geo-brand-mentions/
  SKILL.md            # base
  SKILL.kr.md         # KR-specific platform scoring (create this)
```

### 4. Update agents

Each of the 5 agent files under `agents/` needs a "Region Awareness" section with conditional logic for the new region. Add an `IF region == '<code>' THEN use ... ELSE ...` block following the existing pattern (see `agents/geo-ai-visibility.md` or `agents/geo-platform-analysis.md` for the pattern).

### 5. Fork skills

The 4 fork skills (`geo-distribution-plan`, `geo-competitor-citation`, `geo-intent-matrix`, `geo-citation-pipeline`) read engine/platform lists from `profiles.yaml`. If your new region needs custom behavior in these skills, update their `--region` validation and platform lists.

## Available regions

| Code | Label | Status |
|------|-------|--------|
| `global` | Global (Western Default) | Built-in |
| `cn` | China | Implemented |
