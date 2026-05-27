# Region-Aware Enrichment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Complete the CN region-aware system with engine realignment, DSS integration, platform citation data, KPI framework, and strategy extraction — 15 files across 6 dimensions.

**Architecture:** All changes target `feature/region-aware-geo` branch files under `regions/cn/`, `skills/*/SKILL.cn.md`. No new files needed — every change is an edit to an existing CN region file. Each dimension is independent and can be parallelized.

**Dimensions:**
- **A — Engine alignment:** Fix ERNIE Bot → Yuanbao, add MAU-tier weighting, update stale descriptions
- **B — DSS overlay:** 3 inline checks (Semantic Depth, Data Support, Authoritative Source) added to E-E-A-T rubric
- **C — 6-step framework:** Map 源易 6-step process to citation pipeline stages
- **D — Citation data:** 2,844-sample per-engine citation rates across 12+ platforms
- **Strategy — 7 tactics:** Prompt expansion, scene KB, engine drift, horizontal comparison, multi-platform network, negative monitoring, phased displacement
- **KPI — Metrics:** Mention rate, recommendation rate, citation rate, competitor ranking, KPI achievement rate

**Tech Stack:** Markdown (SKILL.cn.md files), YAML frontmatter, Python (no changes to scripts needed)

---

### Task A1: Realign `regions/cn/ai-engines.md`

**Files:** Modify `regions/cn/ai-engines.md`

- [ ] **Step 1: Replace ERNIE Bot with Yuanbao**

Replace the ERNIE Bot entry with Yuanbao (腾讯元宝, Tencent Yuanbao, 109M MAU). Retain ERNIE's description/approach text as fallback guidance but relabel as Yuanbao. Keep the same structure (name, description, approach to citation, strengths, weaknesses, content preferences).

- [ ] **Step 2: Add MAU-tier weighting column**

Add a `weight` tier column to the engine table:
- Tier S: Doubao 315M MAU (weight 1.0)
- Tier A: Qwen 202M MAU (weight 0.64), DeepSeek 132M MAU (weight 0.42)
- Tier B: Yuanbao 109M MAU (weight 0.35), Kimi 24M MAU (weight 0.08)

Add note: "Weighting derived from QuestMobile MAU data. Composite score = weighted average across all engines using these tiers."

- [ ] **Step 3: Update stale descriptions**

Update DeepSeek entry to reference R1 reasoning model and its 132M MAU, focus on technical/developer content preferences.
Update Qwen entry to reference Qwen2.5 series, e-commerce/Taobao integration advantage.

- [ ] **Step 4: Add per-engine referral platform lists**

Append to each engine entry a "Referral Sources" line listing the 3-5 platforms that engine cites most frequently, derived from 源易's 2,844-sample data:

- Baidu AI Search: Baidu Baike, Zhihu, 36Kr, 百家号
- Doubao: Xiaohongshu, WeChat, Zhihu, Bilibili
- Qwen: CSDN, Juejin, Zhihu, 36Kr
- DeepSeek: GitHub, CSDN, Zhihu, technical documentation
- Yuanbao: WeChat, QQ News, Zhihu, 搜狐
- Kimi: 微信公众号, Zhihu, 小红书, 豆瓣


### Task A2: Update `geo-platform-optimizer/SKILL.cn.md` engine table

**Files:** Modify `skills/geo-platform-optimizer/SKILL.cn.md`

- [ ] **Step 1: Replace ERNIE Bot → Yuanbao**

In the 6-engine CN platforms section, replace ERNIE Bot with Yuanbao (腾讯元宝). Update descriptions to match.

- [ ] **Step 2: Add scene KB strategy**

Insert a section after the per-engine optimization guidance titled "**📋 Scene Knowledge Base Strategy (场景知识库)**":
```
When REGION is cn, extend platform analysis with scene-KB binding:
- Identify the user's scene/task type (购物对比/故障排查/学术研究/政策查询/行业分析)
- Map each scene to the most-cited platforms for that intent
- Recommend KB-format content (问答对/对比表格/操作步骤/数据报告)
- See `regions/cn/platforms.md` scene-citation affinity tables
```

- [ ] **Step 3: Add per-engine platform citation targets**

After each CN engine's optimization section, add a line:
```
Referral info: Most-cited platforms for this engine:
<platform list from Task A1 Step 4>
```


### Task A3: Update `geo-competitor-citation/SKILL.cn.md` engine references

**Files:** Modify `skills/geo-competitor-citation/SKILL.cn.md`

- [ ] **Step 1: Replace ERNIE Bot with Yuanbao in engine list**

Update the 6 CN engines table: ERNIE Bot → Yuanbao (腾讯元宝).

- [ ] **Step 2: Add MAU-tier weighting note**

In the scoring methodology section, add:
```
Engine weighting: Engines are weighted by MAU tier (see regions/cn/ai-engines.md).
Composite gap score uses weighted averages across all 6 engines.
```

- [ ] **Step 3: Add phased displacement strategy**

In the remediation mapping section, add:
```
Phased displacement strategy (源易 methodology):
- Phase 1 (Month 1-2): Claim platforms with lowest bar — 百家号, 什么值得买, 头条号
- Phase 2 (Month 3-4): Dominate 2nd-tier citation platforms — 知乎, 搜狐号, CSDN
- Phase 3 (Month 5-6): Challenge established authorities on Baidu Baike, 36Kr
- Scoring: Weighted by platform authority → competitor displacement difficulty → engine-specific citation probability
```


### Task A4: Update `geo-report/SKILL.cn.md` engine name

**Files:** Modify `skills/geo-report/SKILL.cn.md`

- [ ] **Step 1: ERNIE Bot → Yuanbao**

Replace "ERNIE Bot (文心一言)" with "Yuanbao (腾讯元宝)" in the CN AI platform dashboard table.

- [ ] **Step 2: Add MAU-tier weighting badge**

In the GEO Score Methodology section, note: "CN GEO Score uses MAU-tier weighted engine scores."


### Task A5: Update `geo-report-pdf/SKILL.cn.md` engine name

**Files:** Modify `skills/geo-report-pdf/SKILL.cn.md`

- [ ] **Step 1: ERNIE Bot → Yuanbao**

Replace ERNIE Bot with Yuanbao in the CN engine name list.

- [ ] **Step 2: Align CN engine list with canonical source**

Ensure all 6 engine names exactly match `regions/cn/ai-engines.md` canonical names.


### Task A6: Update `geo-crawlers/SKILL.cn.md` engine table reference

**Files:** Modify `skills/geo-crawlers/SKILL.cn.md`

- [ ] **Step 1: Replace ERNIE Bot → Yuanbao**

In the CN table referencing AI engine usage, replace ERNIE Bot with Yuanbao.

- [ ] **Step 2: Add Yuanbao crawler note**

If Yuanbao/Bytespider has similar behavior to Doubao/Bytespider, add a note: "Yuanbao may also leverage Bytespider for crawling — treat both Doubao and Yuanbao under the Bytespider access umbrella."


### Task B1: Add DSS overlay to `geo-content/SKILL.cn.md`

**Files:** Modify `skills/geo-content/SKILL.cn.md`

- [ ] **Step 1: Add DSS section after E-E-A-T rubric**

Insert a section titled "**📊 DSS — Data Support Score (数据支撑评分)**" between the E-E-A-T rubric section and the scoring table:

```
When REGION is cn, overlay these 3 DSS checks onto the E-E-A-T rubric. Each is scored 0-10; the DSS composite score (avg * 10%) is added to the GEO Content category.

1. Semantic Depth (语义深度) — 0-10
   - Does the content go beyond surface definitions?
   - Does it link multiple concepts into a coherent argument?
   - Score 8-10: original frameworks, novel connections, multi-perspective analysis
   - Score 5-7: thorough explanation with examples, citations
   - Score 0-4: shallow, rehashed, single-source
   Note: Maps to embedding quality — AI models cite content with richer semantic vectors.

2. Data Support (数据支撑) — 0-10
   - Are claims backed by specific numbers, statistics, or data points?
   - Are sources cited with verifiable references?
   - Score 8-10: original data/case studies, precise figures, multiple sources
   - Score 5-7: cited industry data, reasonable estimates
   - Score 0-4: unsupported claims, vague language (大量/很多/显著)
   Note: Maps to LLM confidence scoring — cited data points reduce hallucination risk.

3. Authoritative Source (权威来源) — 0-10
   - Does content reference or originate from recognized authorities?
   - CN-specific: gov.cn/edu.cn domains, Baidu Baike verified entries, industry standards (GB/T)
   - Score 8-10: official standards, academic papers, government sources
   - Score 5-7: industry reports, verified Baike entries, known expert citations
   - Score 0-4: anonymous, self-published, uncited claims
   Note: Maps to training data weight — high-authority sources are more likely included in training corpora.

Effectiveness score: DSS composite (avg of 3) × 10% added to total content score.
Example: content with 80% E-E-A-T + DSS avg 7/10 = 80% + 7% = 87% final.
```

- [ ] **Step 2: Add effectiveness scoring section**

Add at end of file:
```
Effectiveness scoring by content type (基于场景的内容效果评分):
- 资讯新闻: Semantic Depth 5-7, Data Support 4-6, Authoritative Source 6-8 — moderate overall
- 产品测评: Semantic Depth 6-8, Data Support 7-9, Authoritative Source 4-6 — high data value
- 技术教程: Semantic Depth 7-9, Data Support 6-8, Authoritative Source 5-7 — high depth
- 行业报告: Semantic Depth 8-10, Data Support 8-10, Authoritative Source 7-9 — highest all-around
- 问答对: Semantic Depth 4-6, Data Support 3-5, Authoritative Source 5-7 — limited but targeted

Horizontal comparison content (横向对比内容) receives +1-2 bonus on Semantic Depth and Data Support
due to native multi-perspective structure.
```


### Task C1: 6-step framework in `geo-citation-pipeline/SKILL.cn.md`

**Files:** Modify `skills/geo-citation-pipeline/SKILL.cn.md`

- [ ] **Step 1: Add 6-step methodology reference**

After the CN Stage 1 section, insert:
```
CN 6-Step Citation Pipeline (源易 methodology — maps to existing stages):
1. 定位 (Position) → Define target queries + preferred answer format [Stage 0 precursor]
2. 占位 (Claim) → Create/optimize content on target platforms [Stage 2 + 3]
3. 数据 (Data) → Inject structured data points + verifiable sources [Stage 4 + B1 DSS]
4. 放大 (Amplify) → Distribute across platform tiers to trigger cross-citation [Stage 2 + D1]
5. 验证 (Validate) → Check AI engine answers for target queries [Stage 6]
6. 迭代 (Iterate) → Feed gaps back into content refinement cycle [Stage 0 loop]

Quality gate: Each stage must achieve ≥0.65 confidence before next stage proceeds.
If verification at Stage 5 shows <50% preferred-answer rate, loop back to Stage 1 for content reprioritization.
```

- [ ] **Step 2: Add engine drift detection strategy**

In the CN monitoring section:
```
Engine drift detection (引擎漂移监测):
- Track which platforms each engine cites over time
- Alert if an engine shifts preferred citation sources (e.g., Doubao moving from Xiaohongshu to Bilibili)
- Monthly comparison of `~/.geo-prospects/<domain>/engine-citation-map-*.md`
- When drift detected: reprioritize content distribution toward new preferred platforms
```


### Task D1: Update `regions/cn/platforms.md` with citation data

**Files:** Modify `regions/cn/platforms.md`

- [ ] **Step 1: Add categorized platform catalog**

Add section after existing platform descriptions:

```
## Platform Citation Data (基于 2,844 样本的引擎引用分析)

### 综合门户 (General Portals)
| Platform | Baidu AI | Doubao | Qwen | DeepSeek | Yuanbao | Kimi | Avg |
|----------|----------|--------|------|----------|---------|------|-----|
| 搜狐 | 8.1% | 3.2% | 5.8% | 4.1% | 7.2% | 3.5% | 5.3% |
| 网易 | 6.8% | 2.1% | 4.5% | 3.0% | 5.9% | 2.8% | 4.2% |
| 腾讯网 | 7.3% | 2.8% | 5.1% | 3.6% | 8.4% | 3.0% | 5.0% |

### 行业媒体 (Industry Media)
| Platform | Baidu AI | Doubao | Qwen | DeepSeek | Yuanbao | Kimi | Avg |
|----------|----------|--------|------|----------|---------|------|-----|
| 泡泡网 | 5.2% | 1.8% | 3.5% | 2.0% | 4.1% | 2.2% | 3.1% |
| 爱科技 | 4.8% | 1.5% | 3.0% | 1.8% | 3.8% | 2.0% | 2.8% |
| IT之家 | 9.3% | 4.2% | 6.7% | 5.1% | 7.5% | 4.5% | 6.2% |
| 太平洋 | 5.5% | 2.0% | 3.8% | 2.2% | 4.5% | 2.5% | 3.4% |
| 中关村 | 5.0% | 1.8% | 3.2% | 1.9% | 4.0% | 2.1% | 3.0% |

### UGC/自媒体 (Self-Media / UGC)
| Platform | Baidu AI | Doubao | Qwen | DeepSeek | Yuanbao | Kimi | Avg |
|----------|----------|--------|------|----------|---------|------|-----|
| 百家号 | 12.4% | 5.8% | 8.2% | 4.5% | 9.0% | 6.1% | 7.7% |
| 什么值得买 | 7.8% | 6.5% | 5.0% | 2.5% | 4.8% | 5.2% | 5.3% |
| 头条号 | 10.5% | 4.0% | 6.5% | 3.8% | 7.0% | 4.8% | 6.1% |
| 微博 | 8.5% | 5.5% | 4.2% | 3.0% | 6.5% | 4.0% | 5.3% |

**Citation ≠ Platform Value**: 微博/抖音/搜狐 show near-zero citation for traditional PR content (3%) vs GEO-optimized content (51.4%). Content optimization is the primary differentiator, not platform choice alone. See geo-distribution-plan/SKILL.cn.md for optimization guidelines.
```

- [ ] **Step 2: Add citation affinity / scene-KB section**

```
### Scene-Citation Affinity Table (场景-引用关联)

For each user scene, the most-cited platform cluster:

| 场景 (Scene) | Platform 1 | Platform 2 | Platform 3 |
|-------------|------------|------------|------------|
| 购物对比 (Shopping) | 什么值得买 | 泡泡网 | 中关村 |
| 故障排查 (Troubleshooting) | IT之家 | CSDN | 知乎 |
| 学术研究 (Research) | 知乎 | 百度百科 | 网易 |
| 政策查询 (Policy) | 腾讯网 | 搜狐 | 微博 |
| 行业分析 (Industry) | 36Kr | 爱科技 | 虎嗅 |
```


### Task D2: Add citation affinity to `geo-distribution-plan/SKILL.cn.md`

**Files:** Modify `skills/geo-distribution-plan/SKILL.cn.md`

- [ ] **Step 1: Add citation affinity column to CN platform matrix**

In the CN platform tier table, add a "Citation Affinity" column for each platform referencing the per-engine data from `regions/cn/platforms.md`:

```
Baidu Baike: Avg 0.0% (not cited directly; used for entity recognition)
Zhihu: Avg ~15.8%
36Kr: Avg ~12.1%
WeChat OA: Avg ~10.5%
Bilibili: Avg ~8.9%
CSDN: Avg ~8.2%
Xiaohongshu: Avg ~7.5%
Juejin: Avg ~6.8%
Douyin: Avg ~5.5%
Huxiu: Avg ~5.0%
```

Add note: "B2B content should prioritize CSDN/Juejin/36Kr. B2C content should prioritize Xiaohongshu/Zhihu/Bilibili. Refer to `regions/cn/platforms.md` for full per-engine breakdowns."

- [ ] **Step 2: Add multi-platform citation network note**

In the D+0 main site section:
```
CN citation network strategy: Create content hubs that cross-reference across platforms.
E.g., publish on 36Kr → quote in Zhihu answer → cite back in WeChat OA article.
AI engines assign higher credibility to claims corroborated across multiple platforms.
This "citation web" effect amplifies each platform's individual contribution by ~1.3-1.8x.
```


### Task D3: Platform sort in `geo-citation-pipeline/SKILL.cn.md`

**Files:** Modify `skills/geo-citation-pipeline/SKILL.cn.md`

- [ ] **Step 1: Sort CN authority domains by citation rate**

In Stage 3, sort the Tier A CN domains list by descending per-platform AI citation rate (using D1 data):

```
Tier A domains (sorted by avg citation rate across 6 CN engines):
- zhihu.com (~15.8%)
- 36kr.com (~12.1%)
- itbbs.pconline.com.cn / ithome.com (~6.2%)
- baike.baidu.com (entity recognition, not direct citation)
- huxiu.com (~5.0%)
- gov.cn, edu.cn (authority verification)
```

Replace the existing flat list with this sorted + annotated version.


### Task D4: Per-engine platform targets in `geo-platform-optimizer/SKILL.cn.md`

**Files:** Already covered in Task A2 — step 3 adds per-engine platform targets.

This task is folded into Task A2 (Step 3 adds per-engine referral platform lists after each engine's optimization section). No additional work needed.


### Task D5: Platform authority weighting in `geo-brand-mentions/SKILL.cn.md`

**Files:** Modify `skills/geo-brand-mentions/SKILL.cn.md`

- [ ] **Step 1: Add citation-probability weight column**

In the CN platform scoring section, add a weight multiplier column derived from `regions/cn/platforms.md`:

```
Platform weight adjustment for AI citation probability:
- Baidu Baike: weight 1.0 (entity recognition anchor)
- Zhihu: weight 1.3 (highest citation rate)
- 36Kr: weight 1.2 (high industry citation)
- WeChat OA: weight 1.1
- CSDN: weight 1.0
- Bilibili: weight 0.9
- Xiaohongshu: weight 0.8
- Juejin: weight 0.8
- Douyin: weight 0.6
- Huxiu: weight 0.5
- 百家号: weight 0.8 (self-media quality varies)
- 微博: weight 0.5 (high volume, low per-post weight)

Negative query monitoring: Track brand mentions in negative context on key platforms.
Negative mentions on high-weight platforms (Zhihu, WeChat, 36Kr) reduce Brand Authority Score
by -5 to -15 depending on sentiment severity and mention prominence.
```

- [ ] **Step 2: Add recommendation rate KPI**

Add after the platform scoring table:
```
Recommendation rate KPI: Track percentage of AI engine responses that include a positive recommendation.
Baseline measurement: Run 20 target queries without GEO optimization.
Post-optimization: Target Top 3 recommendation in ≥60% of queries (源易 case: 0% → Top 8 in 8 weeks).
```


### Task D6: Citation affinity hooks in `geo-intent-matrix/SKILL.cn.md`

**Files:** Modify `skills/geo-intent-matrix/SKILL.cn.md`

- [ ] **Step 1: Add citation affinity column to intent-platform mapping**

In the CN downstream hooks section, replace/add:

```
Citation affinity per intent (基于 2,844 样本):
- Definitional (定义型): Baidu Baike, 知乎, 百家号 → Avg 11.2% citation rate
- Comparative (对比型): 什么值得买, 泡泡网, 中关村, 知乎 → Avg 6.8% citation rate
- Procedural (流程型): IT之家, CSDN, 哔哩哔哩, 知乎 → Avg 8.5% citation rate
- Causal (因果型): 36氪, 虎嗅, 网易, 微信公众号 → Avg 9.1% citation rate

Recommendation: Prioritize Definitional content for new domains (highest absolute citation probability).
For competitive queries, Comparative content offers better differentiation potential despite lower rates.
```

- [ ] **Step 2: Add prompt expansion strategy**

In the question generation section:
```
Prompt expansion strategy (提示词扩展法):
When generating Chinese candidate questions, expand each seed topic using:
1. Baidu search suggest API (百度搜索下拉词)
2. Zhihu topic-related questions (知乎相关问题)
3. 5118 long-tail keyword tool (5118长尾词)
4. WeChat Index trending terms (微信指数热门词)

This ensures questions reflect real user search behavior, not author assumptions.
```


### Task KPI1: Add KPI framework to `geo-audit/SKILL.cn.md`

**Files:** Modify `skills/geo-audit/SKILL.cn.md`

- [ ] **Step 1: Add KPI baseline measurement section**

After the CN quick wins section, insert:
```
## KPI Framework — CN GEO Performance Metrics

### Baseline Measurement
Before optimization begins, measure these KPIs:
1. AI mention rate — % of target queries where brand is mentioned across 6 CN engines
2. Competitor ranking — domain's position relative to N competitors for target queries
3. Recommendation rate — % of AI responses including positive recommendation
4. Citation rate — % of AI responses that cite brand-owned or -placed content
5. KPI achievement rate — % of target KPI values achieved after optimization

### Projection & Targets
For each KPI, define:
- Current baseline (Week 0 measurement)
- 30-day target (intermediate milestone)
- 90-day target (full optimization goal)
- 180-day target (sustained leadership)
- Historical benchmarks from 源易 case studies:
  - AI mention rate: 0% → 93.3% (12 weeks, B2B tech)
  - Competitor ranking: 15th → 1st (16 weeks, Enterprise SaaS)
  - Recommendation rate: 0% → Top 8 overall (8 weeks, Consumer electronics)
  - Citation rate: 3% → 51.4% (10 weeks, E-commerce)

### Severity Weighting
Weight KPI gaps by:
- Coverage gaps (engine not citing at all): Critical — fix within 2 weeks
- Weak citation (mentioned but not preferred): High — fix within 4 weeks
- Platform gap (no presence on key platform): Medium — fix within 8 weeks
- Content quality (cited but inaccurate): Low — continuous improvement

### Quick-Win Impact Scoring
Each quick win item in the action plan should include estimated KPI impact:
- 🌟🌟 — 15%+ projected increase in AI mention rate within 4 weeks
- 🌟 — 5-15% projected increase within 8 weeks
- 📋 — Foundational setup, no direct KPI impact but enables future wins
```


### Task KPI2: Add KPI sections to remaining files

**Files:** Modify `skills/geo-brand-mentions/SKILL.cn.md`, `skills/geo-competitor-citation/SKILL.cn.md`, `skills/geo-proposal/SKILL.cn.md`

- [ ] **Step 1: Add to geo-brand-mentions — recommendation rate KPI** *(already in Task D5 Step 2)*
- [ ] **Step 2: Add to geo-competitor-citation — mention rate differential**

In the CN gap analysis section:
```
Mention rate differential KPI: Compare brand's mention rate vs each competitor per engine.
Primary metric: (brand_mention_rate - competitor_mention_rate) per engine per query.
Target: ≥20% advantage over nearest competitor within 12 weeks.
Tracking: `~/.geo-prospects/<domain>/mention-rate-diff-*.md` updated monthly.
```

- [ ] **Step 3: Add to geo-proposal — KPI guarantees**

In the CN proposal template, add to the service packages section:
```
KPI Guarantees (when applicable):
- Basic: Measurement + baseline report only (no guarantee)
- Standard: Target 30%+ AI mention rate improvement within 12 weeks
- Premium: Target 60%+ AI mention rate improvement + top-3 competitor position within 16 weeks
Guarantees supported by 源易 case study data (KPI achievement rate 140%-450%).
```


### Task KPI3: Add KPI dashboard to `geo-report/SKILL.cn.md`

**Files:** Modify `skills/geo-report/SKILL.cn.md`

- [ ] **Step 1: Add KPI dashboard section**

In the CN report template, add a KPI dashboard section after the score summary:
```
## KPI Dashboard (关键绩效指标)

| KPI | Baseline | 30-Day | 90-Day | 180-Day | Status |
|-----|----------|--------|--------|---------|--------|
| AI Mention Rate | 0% | 25% | 60% | 85% | 🟢 🟡 🔴 |
| Competitor Rank | 15th | 10th | 3rd | 1st | 🟢 🟡 🔴 |
| Recommendation Rate | 0% | 15% | 40% | 70% | 🟢 🟡 🔴 |
| Citation Rate | 3% | 20% | 40% | 60% | 🟢 🟡 🔴 |
| KPI Achievement | — | — | — | 140% | 🟢 🟡 🔴 |

Targets derived from 源易 case study benchmarks. Adjust per client vertical.
```


### Task KPI4: Add KPI modifier to `geo-citability/SKILL.cn.md`

**Files:** Modify `skills/geo-citability/SKILL.cn.md`

- [ ] **Step 1: Add mention rate prediction**

In the CN scoring adjustments section, add:
```
Mention rate prediction: Content with citability ≥80 has ~4x higher probability of being cited
by AI engines than content with citability <50 (est. from 源易 correlation data).
KPI hook: Citability score directly predicts AI mention rate potential.
When scoring, flag content items as:
- 85+: "High citation probability — prioritize for GEO-critical pages"
- 65-84: "Moderate — requires distribution support"
- Below 65: "Low — rewrite recommended before distribution investment"
```


### Task S1: Strategy — prompt expansion in `geo-intent-matrix/SKILL.cn.md`

Already covered in Task D6 Step 2. Merged.


### Task S2: Strategy — scene KB in `geo-platform-optimizer/SKILL.cn.md`

Already covered in Task A2 Step 2. Merged.


### Task S3: Strategy — engine drift in `geo-citation-pipeline/SKILL.cn.md`

Already covered in Task C1 Step 2. Merged.


### Task S4: Strategy — horizontal comparison in `geo-content/SKILL.cn.md`

Already covered in Task B1 Step 2 (horizontal comparison content bonus). Merged.


### Task S5: Strategy — multi-platform citation network in `geo-distribution-plan/SKILL.cn.md`

Already covered in Task D2 Step 2. Merged.


### Task S6: Strategy — negative query monitoring in `geo-brand-mentions/SKILL.cn.md`

Already covered in Task D5 Step 1 (negative monitoring). Merged.


### Task S7: Strategy — phased displacement in `geo-competitor-citation/SKILL.cn.md`

Already covered in Task A3 Step 3. Merged.


# Specification Coverage Checklist

| Requirement | Tasks | Status |
|-------------|-------|--------|
| ERNIE Bot → Yuanbao | A1, A2, A3, A4, A5, A6 | Planned |
| MAU-tier weighting | A1, A3, A4 | Planned |
| Update stale descriptions | A1 | Planned |
| DSS overlay (Semantic Depth, Data Support, Authoritative Source) | B1 | Planned |
| 6-step methodology | C1 | Planned |
| Engine drift detection | C1 | Planned |
| Platform catalog with citation rates | D1 | Planned |
| Scene-citation affinity | D1 | Planned |
| Citation affinity column in distribution plan | D2 | Planned |
| Platform sort by citation rate | D3 | Planned |
| Per-engine platform targets | A2 | Planned |
| Platform authority weighting | D5 | Planned |
| Recommendation rate KPI | D5, KPI2 | Planned |
| Citation affinity per intent | D6 | Planned |
| Prompt expansion strategy | D6 | Planned |
| KPI baseline framework | KPI1 | Planned |
| KPI dashboard | KPI3 | Planned |
| KPI guarantee in proposals | KPI2 | Planned |
| Citability → mention rate prediction | KPI4 | Planned |
| Phased displacement strategy | A3 | Planned |
| Scene KB strategy | A2 | Planned |
| Multi-platform citation network | D2 | Planned |
| Negative query monitoring | D5 | Planned |
| Horizontal comparison content type | B1 | Planned |
