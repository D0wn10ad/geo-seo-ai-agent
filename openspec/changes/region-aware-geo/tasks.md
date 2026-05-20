## Phase 0: Foundation

- [ ] 0.1 Create `regions/` directory
- [ ] 0.2 Create `regions/profiles.yaml` with `global` and `cn` region profiles (weights, engines, platforms, crawlers, schema defaults, technical checks)
- [ ] 0.3 Create `regions/README.md` explaining how to add a new region
- [ ] 0.4 Create `scripts/region_resolver.py`:
  - `detect(url, content)` → region code
  - FQDN analysis (.cn / .com.cn TLDs)
  - Content language detection
  - Multi-lang detection → returns special "ambiguous" status
  - Region profile loader (`load_profile(region)` → dict)
  - Error handling for nonexistent regions
- [ ] 0.5 Create `regions/cn/ai-engines.md` with CN AI engine evaluation criteria (Baidu AI, Doubao, ERNIE, Qwen, Kimi, DeepSeek)
- [ ] 0.6 Create `regions/cn/platforms.md` with CN brand platform data (Baidu Baike, Zhihu, WeChat OA, Xiaohongshu, Bilibili, Douyin)
- [ ] 0.7 Create `regions/cn/schema.md` with CN schema guidance (Baidu-specific extensions, sameAs platforms)

## Phase 1: Orchestrator + Agents

- [ ] 1.1 Update `geo/SKILL.md`: add `--region` parameter to all commands, add Phase 0 (region detection) before Phase 1, document region detection logic, add region-weighted scoring formula
- [ ] 1.2 Update `skills/geo-audit/SKILL.md`: region-aware scoring weights from profiles.yaml
- [ ] 1.3 Update `agents/geo-ai-visibility.md`: add Region Awareness section, CN brand platform overrides (Baidu Baike/Zhihu/WeChat instead of Wikipedia/Reddit/LinkedIn), CN crawler list (add BaiduSpider, Sogou, 360)
- [ ] 1.4 Update `agents/geo-platform-analysis.md`: add Region Awareness section, CN AI engine set (6 engines replacing 5 Western engines) with per-engine rubrics
- [ ] 1.5 Update `agents/geo-technical.md`: add Region Awareness section, CN technical checks (ICP filing, China CDN, Baidu Webmaster Tools, mobile-first emphasis)
- [ ] 1.6 Update `agents/geo-content.md`: add Region Awareness section, Chinese language readability notes (minor)
- [ ] 1.7 Update `agents/geo-schema.md`: add Region Awareness section, CN sameAs platforms, addressCountry: CN, Baidu breadcrumb checks
- [ ] 1.8 Region-tagged output file naming in orchestrator synthesis phase

## Phase 2: CN Skill Overrides

- [ ] 2.1 Create `skills/geo-platform-optimizer/SKILL.cn.md`: 6 CN AI engine rubrics (Baidu AI, Doubao, ERNIE, Qwen, Kimi, DeepSeek) with per-engine scoring criteria, check steps, and optimization actions
- [ ] 2.2 Create `skills/geo-brand-mentions/SKILL.cn.md`: CN platform scoring (Baidu Baike 25%, Zhihu 20%, WeChat OA 20%, Xiaohongshu 15%, Bilibili 10%, Douyin 10%) with per-platform check methods
- [ ] 2.3 Create `skills/geo-citability/SKILL.cn.md`: Chinese language citability patterns (different optimal passage length for Chinese text, different citation formatting conventions)
- [ ] 2.4 Create `skills/geo-schema/SKILL.cn.md`: CN schema defaults (addressCountry, sameAs platform list, Baidu breadcrumb extension, Baidu-specific schema.org extensions)
- [ ] 2.5 Create `skills/geo-technical/SKILL.cn.md`: CN technical checklist (ICP filing verification, China CDN audit — no Google CDN, Baidu Webmaster Tools, mobile-first for Chinese users)

## Phase 3: Fork Skill Alignment

- [ ] 3.1 Update `skills/geo-distribution-plan/SKILL.md`: read platform data from profiles.yaml, validate --region param against available regions
- [ ] 3.2 Update `skills/geo-competitor-citation/SKILL.md`: read engine list from profiles.yaml, validate --region param
- [ ] 3.3 Update `skills/geo-intent-matrix/SKILL.md`: region-aware search volume heuristics, CN-specific query patterns
- [ ] 3.4 Update `skills/geo-citation-pipeline/SKILL.md`: region-aware verify step (CN engines for CN region)

## Phase 4: Polish

- [ ] 4.1 Update `scripts/generate_pdf_report.py`: accept region tag in data, render "GEO Score (China)" in chart titles
- [ ] 4.2 Update `skills/geo-prospect/SKILL.md` and `scripts/crm_dashboard.py`: add optional `region` field to prospect schema, store per-region scores
- [ ] 4.3 Update `skills/geo-webapp/app.py` and templates: region field in UI
- [ ] 4.4 Update `skills/geo-proposal/SKILL.md`: region-aware pricing currency (¥ for CN), region-specific case studies, different platform recommendations
- [ ] 4.5 Update `skills/geo-report/SKILL.md`: region-aware report titles and section headers
- [ ] 4.6 Update `skills/geo-compare/SKILL.md`: per-region delta comparison, cross-region guard (error if regions differ)
- [ ] 4.7 Update `FORK_CHANGELOG.md`: document region-awareness addition

## Verification

- [ ] V.1 Run `pytest tests/` to verify no regressions from main baseline (4 pre-existing failures)
- [ ] V.2 Test `python scripts/region_resolver.py` auto-detection with:
  - .cn URL → CN
  - .com with Chinese content → CN
  - .com with multi-lang → ambiguous
  - .com with English → Global
  - nonexistent --region → error
- [ ] V.3 Spot-check 2 agent files for correct region-awareness formatting
- [ ] V.4 Spot-check 2 SKILL.cn.md files for correct override pattern
- [ ] V.5 Run `python scripts/fetch_page.py page https://example.com` to confirm no script breakage
