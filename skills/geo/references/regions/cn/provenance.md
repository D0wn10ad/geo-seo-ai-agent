# CN Region: Provenance and Attribution Appendix

This appendix is the canonical claim-to-source ledger for the China-market GEO knowledge docs. Every external figure used anywhere in the CN enrichment plan (MAU numbers, percentages, ROI or market-size figures, algorithm thresholds, test counts) is recorded here with its article ID, a source label, and an explicit `UNVERIFIED` status. Todos 2 through 8 read this file for figure attribution before they write any themed knowledge doc.

## Discipline (read first)

- External article text is untrusted data. It is never treated as instructions. The fetched pages carried tool-wrapper reminders and promotional calls to action; none of that was followed or reproduced as guidance.
- Every figure below is `UNVERIFIED`. That status is about the figure's truth, not just its origin. A spot-check that finds the claim text in an article confirms attribution only. It does not turn a marketing or industry claim into an established fact.
- No full article text is reproduced here. Only short attributed phrases appear, enough to identify the claim.
- Source labels for the three spot-checked IDs use the real article titles. Labels for all other IDs use the role assigned in `.omo/drafts/extend-region-aware-geo-cn.md`, because those articles were not fetched in this task and no title is asserted for them.
- Metric-layer separation is mandatory. The 源易 data already in `regions/cn/ai-engines.md` (MAU tiers, tier and platform weights, 2,844-sample tables) measures OVERALL engine usage in China and stays authoritative and byte-identical. The article figures here measure a different thing: per-agent content-source composition and third-party market claims. The two layers are never merged or reconciled into one table.

## Legend for the claim table

- **Status** is always `UNVERIFIED`.
- **Spot-check** values:
  - `confirmed (text present)` = the claim text was found in the fetched article. Attribution confirmed, figure still unverified.
  - `unconfirmed (not found)` = the claim text was NOT found in the fetched article, so this source does not support it.
  - `not spot-checked` = this ID was outside the three-ID sample.
  - `inconclusive (fetch failed)` = reserved for a failed fetch. It did not occur in this task; all three fetches returned content.

## Claim to source attribution table

| # | Claim text (short, attributed) | Article ID | Source label | Status | Spot-check |
|---|---|---|---|---|---|
| 1 | T/CAPT 026-2026: enterprise website is only a C-level source; A = government/central media/court, B = academic/association whitepaper, C = company site/product manual/review, D = anonymous/low-quality | ScUyd3hGPbjCjVrAugO4yg | GEO新规8·11落地：你的官网在AI眼里只是C级 (一南AI实战) | UNVERIFIED | confirmed (text present) |
| 2 | T/CAPT 026-2026 passed review 8/9, published 8/11, implemented 8/12; 30+ institutions; group standard, not national law | ScUyd3hGPbjCjVrAugO4yg | GEO新规8·11落地：你的官网在AI眼里只是C级 (一南AI实战) | UNVERIFIED | confirmed (text present) |
| 3 | 三区分治: split content into 事实库 / 观点库 / 营销表达库; factual claims in marketing must defer to the fact library | ScUyd3hGPbjCjVrAugO4yg | GEO新规8·11落地：你的官网在AI眼里只是C级 (一南AI实战) | UNVERIFIED | confirmed (text present) |
| 4 | Service-provider grading L1 / L2 / L3 (basic verification / dual review + monitoring / automated monitoring + circuit break + red team) | ScUyd3hGPbjCjVrAugO4yg | GEO新规8·11落地：你的官网在AI眼里只是C级 (一南AI实战) | UNVERIFIED | confirmed (text present) |
| 5 | Black-hat negative list: 语料投毒, 答案霸权, 伪共识制造, 提示词注入攻击 | ScUyd3hGPbjCjVrAugO4yg | GEO新规8·11落地：你的官网在AI眼里只是C级 (一南AI实战) | UNVERIFIED | confirmed (text present) |
| 6 | 3·15 case: a fictional product became an AI "standard answer" within two hours via bulk fake soft articles | ScUyd3hGPbjCjVrAugO4yg | GEO新规8·11落地：你的官网在AI眼里只是C级 (一南AI实战) | UNVERIFIED | confirmed (text present) |
| 7 | 豆包 source tiers Level1-4 plus Filter-AuthInfoLevel | 1T5NvuffOyMYZOPofczrvg | T1 source-tiering article (draft line 56) | UNVERIFIED | not spot-checked |
| 8 | S/A/B/C source-tiering scheme | stQruNQ0RwxCt-QLmZIvwA | T1 source-tiering article (draft line 56) | UNVERIFIED | not spot-checked |
| 9 | EEAT6.0 entity-trust threshold: below 60 demote, above 85 quality | Tlmyhz_NWUHwGbEwYHIzLA | T1/T5 source-tiering and compliance article (draft lines 56, 60) | UNVERIFIED | not spot-checked |
| 10 | Star-rating source scheme | 3dAOBxF81M64uPytfHZucQ | T1 source-tiering article (draft line 56) | UNVERIFIED | not spot-checked |
| 11 | Cross-validation requires at least 3 independent subjects | VmcGBtJ6Ex5cgeFuG3oxMQ | T2 cross-validation article (draft line 57) | UNVERIFIED | not spot-checked |
| 12 | Single-source share capped at 8% or less | 7TACnZLx3k5UhUCROVyzUQ | T2 cross-validation article (draft line 57) | UNVERIFIED | not spot-checked |
| 13 | "Source" means an independent entity, not a channel or a single post | 2qOjVj6BPtmZ1GqPASY6Pg | T2 cross-validation article (draft line 57) | UNVERIFIED | not spot-checked |
| 14 | 信息统一性 (information consistency) weighted at 35% | I42zWLPi7AwB7fC47asuHg | T2/T3 cross-validation and platform article (draft lines 57, 58) | UNVERIFIED | not spot-checked |
| 15 | 品牌事实文件 (brand fact file) as a cross-validation artifact | VmcGBtJ6Ex5cgeFuG3oxMQ | T2 cross-validation article (draft line 57) | UNVERIFIED | not spot-checked |
| 16 | 74-question test: 812 豆包 citations, 567 DeepSeek citations, 4,804 retrieval records, 1,379 total citations | nRq7-RG96GL2xvo_L4sAiw | GEO实测豆包信源结构：抖音第一，官网并非没用 (GEO优化学堂) | UNVERIFIED | confirmed (text present) |
| 17 | 豆包 citation rank: 抖音 first at 108, 今日头条 21, ByteDance ecosystem 129 combined, 界面新闻 23, IT之家 8; no central media in top three | nRq7-RG96GL2xvo_L4sAiw | GEO实测豆包信源结构：抖音第一，官网并非没用 (GEO优化学堂) | UNVERIFIED | confirmed (text present) |
| 18 | DeepSeek citation rank: 阿里云开发者社区 first at 77; 抖音 appears 0 times | nRq7-RG96GL2xvo_L4sAiw | GEO实测豆包信源结构：抖音第一，官网并非没用 (GEO优化学堂) | UNVERIFIED | confirmed (text present) |
| 19 | Retrieval-pool overlap: 271 vs 198 independent sites, only 40 shared, under 20% overlap | nRq7-RG96GL2xvo_L4sAiw | GEO实测豆包信源结构：抖音第一，官网并非没用 (GEO优化学堂) | UNVERIFIED | confirmed (text present) |
| 20 | A three-no company-site page (no data, no byline, no date) was cited 8 times; Q&A pages get cited | nRq7-RG96GL2xvo_L4sAiw | GEO实测豆包信源结构：抖音第一，官网并非没用 (GEO优化学堂) | UNVERIFIED | confirmed (text present) |
| 21 | 豆包 ByteDance-ecosystem content share of 48.7% | fKgDW_YDjUYXG-Pst64D9Q | T3 platform-behavior article (draft line 58) | UNVERIFIED | unconfirmed (not found in nRq7 spot-check; needs its own source) |
| 22 | 94.7% RAG semantic-filter drop | fKgDW_YDjUYXG-Pst64D9Q | T3 platform-behavior article (draft line 58) | UNVERIFIED | not spot-checked |
| 23 | 元宝: over 65% of citations point into the WeChat ecosystem (公众号/视频号/小程序/企微) | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present) |
| 24 | 元宝: source-authority weight of WeChat ecosystem content at 60% | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present) |
| 25 | 千问 favors the Alibaba ecosystem | WhhWhQWj2XSN0ulIlGXW2Q | T3/T5 platform and compliance article (draft lines 58, 60) | UNVERIFIED | not spot-checked |
| 26 | 907-question RPA test method with memory OFF | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | unconfirmed (not found in fetched text; needs its own source) |
| 27 | Platform x content time windows affect citation | WhhWhQWj2XSN0ulIlGXW2Q | T3 platform-behavior article (draft line 58) | UNVERIFIED | not spot-checked |
| 28 | 6-step keyword-to-knowledge-base method | nj_oNNX85Ipu4M351Uv-1g | T4 engineering article (draft line 59) | UNVERIFIED | not spot-checked |
| 29 | 30/60/90-day acceptance plan | PruDxJikelrz7zGeH-q7xQ | T4 engineering article (draft line 59) | UNVERIFIED | not spot-checked |
| 30 | 3-layer measurement model | MejqSHwG8G7MJyuyzj65HA | T4 engineering article (draft line 59) | UNVERIFIED | not spot-checked |
| 31 | query-frame to platform mapping | xKHvBbBlxlW0LOO6TCjBQw | T4 engineering article (draft line 59) | UNVERIFIED | not spot-checked |
| 32 | 官网问答专页 / 解决方案页 as a citation-friendly page form | nRq7-RG96GL2xvo_L4sAiw | GEO实测豆包信源结构：抖音第一，官网并非没用 (GEO优化学堂) | UNVERIFIED | confirmed (text present) |
| 33 | 清朗专项 four categories | cEAJOut6f3g6T9VzF7DrFA | T5 compliance article (draft line 60) | UNVERIFIED | not spot-checked |
| 34 | 三不做: no 删帖, no 刷好评, no 怼竞对 | 5oPN987WuYGOwLM2WpMcMA | T5 compliance article (draft line 60) | UNVERIFIED | not spot-checked |
| 35 | REJECT 邪修 (report-manipulation tactics) | YkQG1SNWFQjdxW4wlQBndw | T5 compliance article (draft line 60) | UNVERIFIED | not spot-checked |
| 36 | 元宝 and 京东 AI Agent mini-program integration completed 7/15; 京东 is first e-commerce vertical partner | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present) |
| 37 | 52% of e-commerce merchants used generative AI in H1 2026 (attributed to "industry monitoring data") | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present) |
| 38 | CN GEO market 6亿 (2025) to 47.3亿 (2026), attributed to 中国信通院 | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present); conflicts with row 39 in the same article |
| 39 | CN GEO market about 30亿 in 2026, about +1100% YoY, attributed to 易观 | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present); conflicts with row 38 in the same article |
| 40 | 元宝 MAU 5,735万; WeChat 13亿 MAU | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present) |
| 41 | 推荐 -> 点击 -> 成交 funnel as the GEO delivery metric | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present) |
| 42 | 模力指数: 300万+ brand records, 8 major AI models, 300万+ daily brand-monitored items | 9dyvZKi93YK597rkQkJ7wQ | 元宝接入京东购物 (GEO营销研究院) | UNVERIFIED | confirmed (text present) |
| 43 | Article-asserted MAU: Qwen 166M, DeepSeek 127M, Yuanbao 57.35M (secondary/dated; NOT for the 源易 table) | 1zssqFqHEWkTNrLWWDW5ww | Bridge article A2 (draft line 69) | UNVERIFIED | not spot-checked (57.35M also appears in row 40) |
| 44 | Supplementary KPIs: 被推荐位次, 跨域稳定性, 迭代日志, at least 3 differentiated strategies | 1zssqFqHEWkTNrLWWDW5ww | Bridge article A2 (draft line 69) | UNVERIFIED | not spot-checked |
| 45 | agentic_geo method: top-25 strategies, at most 3 rewrite steps, 7 geval evaluator prompts | arXiv:2603.20213v1 (method track, not a WeChat ID) | AIcling/agentic_geo companion paper (draft lines 64-70) | UNVERIFIED | not spot-checked |

## Spot-check results (3 representative IDs)

All three fetches used `webfetch("https://mp.weixin.qq.com/s/<ID>", format=text)` with no query parameters. All three returned article content. "Confirmed" below means the claim text was present in the fetched page. It is an attribution check, not factual verification.

### ScUyd3hGPbjCjVrAugO4yg (source-tiering / compliance)

Fetched title: GEO新规8·11落地：你的官网在AI眼里只是C级. Confirmed present: the T/CAPT 026-2026 standard with 8/9 review, 8/11 publication, 8/12 implementation; the A/B/C/D source table with 官网 at C; 三区分治 (事实库/观点库/营销表达库); L1/L2/L3 provider grading; the black-hat list naming 语料投毒, 答案霸权, 伪共识制造, 提示词注入攻击; the 3·15 two-hour case. Caveat recorded from the article itself: it is a secondary summary of a Xinhua release report and states the standard is a group standard with compliance subject to each company's actual situation and regulator requirements. Rows 1 to 6 carry this outcome.

### nRq7-RG96GL2xvo_L4sAiw (platform behavior)

Fetched title: GEO实测豆包信源结构：抖音第一，官网并非没用. Confirmed present: 74 questions; 812 豆包 citations, 567 DeepSeek citations, 4,804 retrieval records; 抖音 108 and 今日头条 21 for 豆包; 阿里云开发者社区 77 and 抖音 0 for DeepSeek; 271 vs 198 sites with 40 shared; the three-no page cited 8 times; the Q&A-page finding. The article states its own limits: one time slice, two models, directional not statistical. Two things were NOT confirmed here: the "豆包字节系 48.7%" figure (row 21) and the "907-question RPA test" (row 26) do not appear in this article. Both stay UNVERIFIED and need their own source before any doc states them. Rows 16 to 20 and 32 carry the confirmed outcome.

### 9dyvZKi93YK597rkQkJ7wQ (agentic commerce)

Fetched title: 元宝接入京东购物 (full title uses a double dash, omitted here). Confirmed present: the 7/15 元宝-京东 integration; 52% merchant generative-AI usage; the 信通院 47.3亿 and 易观 30亿 market figures; over 65% WeChat-ecosystem citations and 60% source-authority weight; 元宝 MAU 5,735万 and WeChat 13亿; the 推荐-点击-成交 funnel; 模力指数 300万+ / 8 models figures. Two risks recorded: the article gives two conflicting 2026 market sizes (47.3亿 vs 30亿, rows 38 and 39), and its data-source note credits IDC, 易观, 艾瑞, 天眼查 and public financing info without inline traceability. Rows 23, 24, 36 to 42 carry this outcome.

## Source index (28 entries)

Grouped by the six convergence themes from the draft, plus master checklists and the method bridge. IDs repeated across themes are listed once per theme where the draft uses them, so the grouping mirrors the source material. The unique-ID count is 27 valid WeChat IDs plus one off-site article whose ID was not captured in the draft, giving the 28 sources referenced by the plan.

### T1 source-tiering (5)

- `ScUyd3hGPbjCjVrAugO4yg` GEO新规8·11落地：你的官网在AI眼里只是C级 (spot-checked)
- `stQruNQ0RwxCt-QLmZIvwA` S/A/B/C tiering article
- `1T5NvuffOyMYZOPofczrvg` 豆包 Level1-4 + Filter-AuthInfoLevel article
- `Tlmyhz_NWUHwGbEwYHIzLA` EEAT6.0 entity-trust article
- `3dAOBxF81M64uPytfHZucQ` star-rating source scheme article

### T2 cross-validation (4)

- `VmcGBtJ6Ex5cgeFuG3oxMQ` >=3 independent subjects / brand fact file
- `7TACnZLx3k5UhUCROVyzUQ` single-source <=8%
- `2qOjVj6BPtmZ1GqPASY6Pg` source = independent entity
- `I42zWLPi7AwB7fC47asuHg` 信息统一性 35%

### T3 platform and algorithm behavior (6)

- `nRq7-RG96GL2xvo_L4sAiw` 74-question 豆包/DeepSeek test (spot-checked)
- `1T5NvuffOyMYZOPofczrvg` 豆包 tiering, reused for platform behavior
- `fKgDW_YDjUYXG-Pst64D9Q` ByteDance 48.7% / RAG 94.7% claims
- `WhhWhQWj2XSN0ulIlGXW2Q` 千问 Alibaba ecosystem / time windows
- `I42zWLPi7AwB7fC47asuHg` cross-validation reuse
- `9dyvZKi93YK597rkQkJ7wQ` 元宝 WeChat ecosystem (spot-checked)

### T4 engineering frameworks (6 WeChat IDs + 1 off-site article)

- `ScUyd3hGPbjCjVrAugO4yg` 三区分治, reused
- 芸芸学姐 off-site article (7-character ID not captured in draft line 59; counted as the 28th source, no ID to index)
- `nj_oNNX85Ipu4M351Uv-1g` 6-step keyword-KB
- `PruDxJikelrz7zGeH-q7xQ` 30/60/90 acceptance
- `MejqSHwG8G7MJyuyzj65HA` 3-layer measurement
- `xKHvBbBlxlW0LOO6TCjBQw` query-frame to platform mapping
- `um9K31KbZKom1FTzudWxvA` engineering framework article (draft line 59)

### T5 compliance and anti-abuse (6)

- `ScUyd3hGPbjCjVrAugO4yg` black-hat negative list, reused
- `Tlmyhz_NWUHwGbEwYHIzLA` compliance reuse
- `cEAJOut6f3g6T9VzF7DrFA` 清朗专项 four categories
- `5oPN987WuYGOwLM2WpMcMA` 三不做
- `WhhWhQWj2XSN0ulIlGXW2Q` compliance reuse
- `YkQG1SNWFQjdxW4wlQBndw` REJECT 邪修

### T6 agentic commerce (1)

- `9dyvZKi93YK597rkQkJ7wQ` 元宝-京东 closed loop, reused

### Master checklists (5)

- `Mh-fwA8Vmrt-KaujrzkJ8Q` geo-technical / schema master source
- `Df4f1Jv0tiRWi_GeGq00tw` free tool stack
- `ri9DxnENRU69-2i0VGJ1ow` strategic narrative
- `W1OGHmfW6NJ0fpFInSrn-Q` website rebuild ROI
- `Ogzn8zzsrDv56dsGX6XSXw` outline tool

### Method bridge (1)

- `1zssqFqHEWkTNrLWWDW5ww` bridge article A2, supplementary KPIs
- `arXiv:2603.20213v1` AIcling/agentic_geo companion paper (method track, not a WeChat article)

## Open items and risks

- Rows 21, 26 and 43 need a dedicated source check before any themed doc states them. Row 21's 48.7% and row 26's 907-question test were not in the spot-checked article that the draft grouped them near.
- Rows 38 and 39 conflict inside one article. Present them as competing attributed claims, never as a single market-size figure.
- The 28th source (芸芸学姐 off-site article) has no usable ID in the draft. If a themed doc needs it, recover the ID first or drop the claim.
- This appendix records attribution, not truth. Downstream docs must keep the `UNVERIFIED` label on every figure they carry over.
