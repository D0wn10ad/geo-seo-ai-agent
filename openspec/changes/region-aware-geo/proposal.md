## Why

The GEO toolkit is Western-only — all 20 skills and 5 agents hardcode Western AI engines (ChatGPT, Claude, Perplexity, Gemini, Copilot), Western brand platforms (YouTube, Reddit, Wikipedia, LinkedIn), schema.org/US defaults, and English-only scoring. This makes it unusable for Chinese market audits and provides no path to add other regions.

The fork already serves users targeting Chinese search visibility. Without region-aware profiles, each CN audit requires manual mental translation: "replace YouTube with Baidu Baike, replace ChatGPT with Doubao, adjust scoring weights..." This is error-prone and doesn't scale.

## What Changes

- **Region profile system**: `regions/profiles.yaml` as the data layer (machine-readable region metadata, scoring weights, platform/engine lists) with a `regions/README.md` explaining how to add new regions
- **Region detection**: `scripts/region_resolver.py` for URL-based + content-based region detection with user prompt when ambiguous
- **CN reference data**: `regions/cn/` directory with CN-specific AI engine evaluation criteria, brand platform data, and schema guidance
- **Skill-level .cn.md overrides**: 5 `SKILL.cn.md` files for individual commands (`/geo citability --region cn`, etc.)
- **Agent inline region-awareness**: 5 agent `.md` files with conditional region logic (agents are self-contained and don't load skill files)
- **Orchestrator update**: `geo/SKILL.md` gains `--region` parameter, Phase 0 region detection, region-weighted scoring, region-tagged output files
- **Fork skill alignment**: 4 fork skills read shared platform/engine data from `profiles.yaml` instead of hardcoded lists
- **Region-tagged scoring**: Per-region scoring weights in profiles.yaml, per-region output files, per-region score fields in CRM

## Capabilities

- `region-detection`: FQDN analysis (.cn → CN, Chinese content → CN, multi-lang → ask user), runs before any crawl
- `region-profiles`: profiles.yaml data layer with scoring weights, engine lists, platform lists, crawler lists, schema defaults, and technical checks per region
- `skill-overrides`: SKILL.cn.md instruction layer for individual `/geo <cmd>` invocations when `--region` is passed
- `agent-region-awareness`: 5 agents with inline IF/ELSE logic for CN-specific scoring rubrics and platform lists during full audits
- `region-scoring`: Per-region scoring weights applied at synthesis. Global score only used as fallback for unimplemented regions. No composite global score.
- `fork-alignment`: 4 fork skills (matrix, distribute, pipeline, compete) read engine/platform data from profiles.yaml. Existing `--region` params remain backward compatible.

## Impact

- ~15 new files + ~12 edited files
- No breaking changes for existing users (no `--region` = old Global behavior)
- No new Python dependencies
- Backward compatible: existing CRM data, output files, and scoring unchanged
- Queues behind `multi-ai-agent-architecture` (both touch agents, skills, and docs)
