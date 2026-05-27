# CN Canon Sweep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean up residual stale engine naming (ERNIE Bot → Yuanbao) and style drift (emoji markers) across 8 CN skill/agent/region files on `feature/region-aware-geo`.

**Architecture:** Single sweep — find-and-replace with canonical terminology. All files read first, edited with exact old→new strings, verified with grep post-fix.

**Tech Stack:** markdown, grep

**Canonical engine naming (from `regions/cn/ai-engines.md`):**

| Region in repo | Replace with canonical |
|---|---|
| ERNIE Bot / 文心一言 | Yuanbao (腾讯元宝) |
| 文心一言 (ERNIE Bot) | Yuanbao (腾讯元宝) |
| "Baidu AI Search and ERNIE" | "Baidu AI Search and Yuanbao" |
| "百度 AI 搜索和文心一言" | "百度 AI 搜索和腾讯元宝" |
| "Baidu ERNIE, Doubao" | "Yuanbao, Doubao" |

---

### Task 1: geo-report SKILL.cn.md — 6 stale ERNIE refs + emoji

**Files:**
- Modify: `skills/geo-report/SKILL.cn.md:135,233,254,257,317,344`
- Modify: `skills/geo-report/SKILL.cn.md:93-97` (emoji)

High priority replacements:
1. Line 135: `百度 AI 搜索和文心一言` → `百度 AI 搜索和腾讯元宝`
2. Line 233: `百度 AI 搜索、文心一言` → `百度 AI 搜索、腾讯元宝`
3. Line 254: `百度 AI、文心一言、DeepSeek` → `百度 AI、腾讯元宝、DeepSeek`
4. Line 257: `百度 AI、文心一言、Kimi` → `百度 AI、腾讯元宝、Kimi`
5. Line 317: `文心一言就绪度` → `腾讯元宝就绪度` and URL `XX/100`
6. Line 344: `文心一言 (ERNIE Bot)` → `Yuanbao (腾讯元宝)`

Medium priority:
- Lines 93-97: Replace `🟢 🟡 🔴` with `Good / At Risk / Critical` in KPI table

### Task 2: geo-citation-pipeline + geo-audit — 2 engine naming fixes

**Files:**
- Modify: `skills/geo-citation-pipeline/SKILL.cn.md:148`
- Modify: `skills/geo-audit/SKILL.cn.md:58`

Replacements:
1. `geo-citation-pipeline.cn.md`: `ERNIE Bot (文心一言)` → `Yuanbao (腾讯元宝)` in Stage 6 table
2. `geo-audit.cn.md`: `ERNIE Bot (文心一言)` → `Yuanbao (腾讯元宝)` in Subagent 2 list

### Task 3: geo-proposal SKILL.cn.md — 4 ERNIE refs

**Files:**
- Modify: `skills/geo-proposal/SKILL.cn.md:47,94,192,226`

Replacements:
1. Line 47: `文心一言` → `腾讯元宝`
2. Line 94: `文心一言` → `腾讯元宝` 
3. Line 192: `文心一言` → `腾讯元宝`
4. Line 226: `文心一言` → `腾讯元宝`

### Task 4: geo-platform-optimizer + geo-brand-mentions — 4 fixes

**Files:**
- Modify: `skills/geo-platform-optimizer/SKILL.cn.md:26,184,169`
- Modify: `skills/geo-brand-mentions/SKILL.cn.md:13,25`

Replacements:
1. `platform-optimizer:26`: `Baidu's ERNIE-powered AI search` → `Baidu's AI search (Yuanbao-powered)`
2. `platform-optimizer:184`: `both Baidu AI Search and ERNIE` → `Baidu AI Search and Yuanbao`
3. `platform-optimizer:169`: `📋 Scene Knowledge Base Strategy` → `Scene Knowledge Base Strategy`
4. `brand-mentions:13`: `mirrors the base skill` → `uses CN-specific weighted scoring` (or similar accurate statement)
5. `brand-mentions:25`: `Baidu AI, ERNIE, Doubao, Tongyi, Kimi, DeepSeek` → `Baidu AI, Yuanbao, Doubao, Qwen, Kimi, DeepSeek`

### Task 5: regions/cn/platforms.md + agents/geo-platform-analysis.md — 2 fixes

**Files:**
- Modify: `regions/cn/platforms.md:10`
- Modify: `agents/geo-platform-analysis.md:18-23,31-36,217`

Replacements:
1. `platforms.md:10`: `Baidu ERNIE, Doubao` → `Yuanbao, Doubao`
2. `agents/geo-platform-analysis.md:19`: `ERNIE Bot (Baidu)` → `Yuanbao (Tencent)`
3. `agents/geo-platform-analysis.md:22`: `ERNIE, Qwen` → `Yuanbao, Qwen`
4. `agents/geo-platform-analysis.md:33-34`: `ERNIE Bot (replaces Gemini)` → `Yuanbao (replaces Gemini)`
5. `agents/geo-platform-analysis.md:217`: `ERNIE Bot` → `Yuanbao`

### Task 6: Verify

- Run: `grep -rn 'ERNIE\|文心一言' skills/ regions/cn/ agents/ --include='*.md'` — expect 0 matches after fixes
- Run: `grep -rn '🟢\|🟡\|🔴\|📋' skills/ regions/cn/ agents/ --include='*.md'` — document remaining emoji usage
- Run: `pytest tests/` — 55 tests must still pass
