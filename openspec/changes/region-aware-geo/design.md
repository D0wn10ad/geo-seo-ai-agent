## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REGION-AWARE GEO PIPELINE                        │
└─────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │  User: /geo audit │
                              │  example.com      │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │  Phase 0: Region  │
                              │  Detection        │
                              │  (region_resolver)│
                              └────────┬─────────┘
                                       │ "cn" / "global"
                                       │
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
     ┌────────▼────────┐    ┌─────────▼──────────┐   ┌─────────▼─────────┐
     │ Phase 1:        │    │ Phase 2: 5 Agents  │   │ Phase 3:          │
     │ Discovery       │    │                    │   │ Synthesis         │
     │ (seq)           │    │ each receives      │   │ (seq)             │
     └────────┬────────┘    │ REGION parameter   │   │ • Per-region      │
              │             └───┬────┬────┬──────┘   │   scoring          │
              │                 │    │    │          │ • Region-tagged   │
              │                 │    │    │          │   output files    │
              │                 │    │    │          │ • No composite    │
              │                 │    │    │          │   global score    │
              │                 │    │    │          └───────────────────┘
              │                 │    │    │
              │      ┌──────────┘    │    └──────────┐
              │      │               │               │
        ┌─────▼──────▼──┐   ┌───────▼────────┐  ┌───▼──────────┐
        │ Agent reads    │   │ If region !=   │  │ Agent applies │
        │ its inline     │   │ global: read   │  │ region-aware  │
        │ REGION logic   │   │ SKILL.cn.md    │  │ rubric from   │
        │ from .md file  │   │ for overrides  │  │ profiles.yaml │
        └────────────────┘   └────────────────┘  └──────────────┘
```

## Design Decisions

### 1. Agents are self-contained (no skill loading during audits)

Each agent `.md` file contains ALL logic inline — platform lists, scoring rubrics, dimension criteria. The SKILL.md + SKILL.cn.md pattern **only works for individual commands** (`/geo citability --region cn`). During a full audit, agents don't load skill files at all.

**Chosen approach:** Each agent gets an inline "Region Awareness" section with conditional logic. The agent reads `REGION` from its task prompt and applies the correct rubric.

### 2. Parameter passing: orchestrator → agents

When the orchestrator delegates to subagents via the Task/delegate tool, it appends `REGION=<value>` directly to the task description prompt.

**Rejected alternatives:**
- Temp `.region` file: race conditions with parallel agents, cleanup complexity
- Environment variables: not reliably propagated to agent sandboxes

### 3. Data layer vs instruction layer

| Layer | File | Content | Update cadence |
|---|---|---|---|
| **Data** | `regions/profiles.yaml` | Machine-readable: scoring weights, engine lists, platform lists, crawler lists, TLD patterns, language codes, schema defaults | Rarely (new region) |
| **Instructions** | `skills/*/SKILL.cn.md` | AI-readable: per-platform scoring criteria, per-engine evaluation rubrics, platform-specific check steps | Frequently (rubric refinements) |

profiles.yaml is the single source of truth for WHAT exists per region. SKILL.cn.md is the HOW for each component.

### 4. Region detection logic

```
Input URL → region_resolver.detect(url, content)
             ↓
  .cn / .com.cn TLD     → CN (confident)
  .com, only Chinese     → CN (confident)
    content
  .com, multiple langs   → ASK user:
    (/en/, /cn/)             "1. Global  2. Global + CN  3. CN only"
  none of the above      → Global (default, backward compatible)
```

Detection runs as Phase 0, before any page crawling. No silent default when ambiguous.

### 5. Scoring model: per-region primary, global only as fallback

| Scenario | Scoring |
|---|---|
| No `--region`, auto-detect → Global | 25/20/20/15/10/10 weights, Western platforms (unchanged) |
| `--region cn` | 20/30/15/10/15/10 weights, CN platforms |
| Auto-detect → multi-lang → "Global + CN" | Two independent scores, reported separately |
| unimplemented region (`--region kr`) | Fallback to Global with warning |

No composite global score. Per-region scores are always primary. The old "global" score is relabeled "Western Default" in documentation — it's not a true global, just the US+EU-centric starting point.

### 6. Output file naming

| Run type | Files |
|---|---|
| Global only (default) | `GEO-AUDIT-REPORT.md` (unchanged) |
| CN only | `GEO-AUDIT-REPORT-CN.md` |
| Global + CN | `GEO-AUDIT-REPORT-GLOBAL.md` + `GEO-AUDIT-REPORT-CN.md` |

-suffix only added when needed to disambiguate. Single-region runs keep original filenames.

### 7. profiles.yaml data model

```yaml
regions:
  cn:
    label: "China"
    code: cn
    tlds: [.cn, .com.cn]
    languages: [zh, zh-CN, zh-Hans, zh-Hant]
    scoring_weights:
      citability: 20
      brand: 30
      eeat: 15
      technical: 10
      schema: 15
      platform: 10
    ai_engines:
      - id: baidu_ai
      - id: doubao
      - id: ernie
      - id: qwen
      - id: kimi
      - id: deepseek
    brand_platforms:
      - id: baidu_baike  (weight: 25)
      - id: zhihu        (weight: 20)
      - id: wechat_oa    (weight: 20)
      - id: xiaohongshu  (weight: 15)
      - id: bilibili     (weight: 10)
      - id: douyin       (weight: 10)
    crawlers:
      - BaiduSpider
      - SogouSpider
      - 360Spider
      - Bytespider
    schema_defaults:
      address_country: CN
      same_as_platforms: [baidu_baike, wechat, weibo]
    technical_checks:
      - icp_filing
      - china_cdn
      - baidu_webmaster_tools
      - mobile_first
```

### 8. Agent integration pattern

Each agent gets a "Region Awareness" section after the header, before execution steps:

```markdown
## Region Awareness

REGION parameter provided: [global / cn]

- If `global` or absent: use default platforms and scoring (below).
- If `cn`: apply CN overrides documented in this section instead.
```

The agent body IS the single source of truth for both global and CN. No external file loading needed during agent execution. The AI reads its own instruction text and applies the correct conditional branch.

## Edge Cases

| Edge case | Handling |
|---|---|
| `--region xy` (nonexistent) | Error: "Region 'xy' not found in profiles.yaml. Available: global, cn" |
| Multi-lang site, user picks "Global + CN" | Two sequential audit pipelines. Phase 1 (crawl) shared; Phases 2+3 per region |
| Site has both .cn and .com | `--region cn` on .com: treat as CN. Content detection + ask if ambiguous |
| No --region + undetectable | Default to Global. No silent CN assignment |
| Existing CRM data, no region field | `region: global` assumed for legacy entries |
| `/geo compare` across regions | Only compares within same region. Cross-region returns error |
| `/geo quick` | No region awareness. Always Global (complexity doesn't justify for quick snapshots) |
| Site in China behind GFW (blocks foreign IPs) | WebFetch fails. Agent notes failure, scores technical as "unverifiable" |
| BaiduSpider ignores robots.txt | Known behavior — note but don't penalize. Check is advisory for CN |
| Fork skills with existing --region param | Keep own param (backward compatible) but read engine lists from profiles.yaml |

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Agents misinterpret inline conditional logic | Medium | Clear IF/ELSE formatting. Consistent pattern across all 5 agents |
| profiles.yaml drifts from SKILL.cn.md | Low | profiles.yaml has lists, SKILL.cn.md has rubrics. Rubric drift is acceptable |
| Baidu platform APIs change | Medium | WebFetch-based checks, not API-dependent |
| GFW blocks agent requests from outside China | High | Document limitations. Graceful score degradation when fetches fail |
| Fork owners modify platform lists independently | Medium | Fork skills read from profiles.yaml for shared data. Can still add fork-specific entries |
| `--region cn` passed to `/geo update` | None | Silently ignored (doesn't use region) |
