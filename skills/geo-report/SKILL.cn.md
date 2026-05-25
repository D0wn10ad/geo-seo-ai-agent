---
name: geo-report-cn
description: CN region override for GEO client report — Chinese-language template, CN scores, CN platforms
version: 1.0.0
region: cn
parent: geo-report
---

# GEO 客户报告 — 中国市场覆盖

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Replace the English-language report template with the Chinese-language template below.
Use CN-specific scoring labels, platforms, crawlers, and brand authorities throughout.

Reference: `regions/cn/ai-engines.md` and `regions/cn/platforms.md` for CN engine and platform details.

---

## GEO 就绪度分数计算 (GEO Readiness Score — CN)

### Component Weights (CN)

| Component | Weight | Source Skill |
|---|---|---|
| 中国 AI 平台就绪度 | 30% | geo-platform-optimizer-cn |
| 内容质量与 E-E-A-T | 25% | geo-content-cn |
| 技术基础 | 15% | geo-technical-cn |
| 结构化数据与 Schema | 15% | geo-schema-cn |
| 品牌权威性与实体存在 | 15% | geo-brand-mentions-cn |

The CN weighting increases AI Platform Readiness from 25% to 30% because the China market has more diverse AI engines (6 vs 5), and Baidu AI Search alone commands over 80% of CN search market share.

### 分数公式 (Score Formula)
```
GEO Score (CN) = (Platform Score * 0.30) + (Content Score * 0.25) + (Technical Score * 0.15) + (Schema Score * 0.15) + (Brand Score * 0.15)
```

Round to the nearest integer. Cap at 100.

### 分数含义 (Score Interpretation — CN)

| 分数范围 | 等级 | 客户描述 |
|---|---|---|
| 85-100 | 优秀 | 您的网站在 AI 搜索中具备极佳的可发现性。专注于保持和扩大优势。 |
| 70-84 | 良好 | 扎实的基础，存在明确的优化机会。针对性优化将带来显著效果。 |
| 55-69 | 中等 | 网站在 AI 就绪度方面存在差距，竞争对手可能正在利用这些差距。 |
| 40-54 | 低于平均 | 您的网站在 AI 搜索结果中存在显著的可见性障碍。如不采取行动，品牌可能在 AI 生成答案中被忽略。 |
| 0-39 | 亟待改善 | 存在关键的 AI 就绪度问题，需要立即采取行动。 |

---

## 报告模板 (Report Template — CN)

The complete report follows this exact structure. All section headers and content should be in Chinese unless the domain content is explicitly English-language.

---

### 第一部分：执行摘要 (Executive Summary)

Write exactly ONE paragraph (4-6 sentences) in Chinese covering:
- 分析范围（域名、页面数量、分析日期、地区：中国）
- 整体 GEO 就绪度分数及其含义（"XX/100，属于[等级]水平"）
- 最重要的发现（正面或负面均可）
- 排名前三的优先建议
- 商业影响描述（"实施这些建议预计可将 AI 驱动流量提高约 XX%..."）

**语气**：自信、直接、专业。避免行业术语。以顾问向客户交付结果的口吻撰写。

### 第二部分：GEO 就绪度分数 (GEO Readiness Score)

```
## GEO 就绪度分数：XX/100 — [等级]
```

| 评估维度 | 分数 | 权重 | 加权得分 |
|---|---|---|---|
| 中国 AI 平台就绪度 | XX/100 | 30% | XX |
| 内容质量与 E-E-A-T | XX/100 | 25% | XX |
| 技术基础 | XX/100 | 15% | XX |
| 结构化数据 | XX/100 | 15% | XX |
| 品牌权威性 | XX/100 | 15% | XX |
| **总分** | | | **XX/100** |

### 第三部分：中国 AI 平台可见性概览 (CN AI Visibility Dashboard)

```markdown
## 中国 AI 平台可见性概览

| AI 平台 | 就绪度分数 | 主要差距 | 优先行动 |
|---|---|---|---|
| 百度 AI 搜索 (Baidu AI) | XX/100 | [一行描述] | [一行描述] |
| 豆包 (Doubao) | XX/100 | [一行描述] | [一行描述] |
| 文心一言 (ERNIE Bot) | XX/100 | [一行描述] | [一行描述] |
| 通义千问 (Qwen) | XX/100 | [一行描述] | [一行描述] |
| Kimi (月之暗面) | XX/100 | [一行描述] | [一行描述] |
| DeepSeek (深度求索) | XX/100 | [一行描述] | [一行描述] |
```

Add a CN explanation paragraph: "这些分数反映了您的内容被各中国 AI 搜索平台引用的可能性。分数低于 50 分表明在该平台上存在显著的引用障碍。在中国市场，百度 AI 搜索由于占据超过 80% 的搜索份额，应作为首要优化目标。"

### 第四部分：AI 爬虫访问状态 (AI Crawler Access — CN)

```markdown
## AI 爬虫访问状态

| 爬虫 | 所属平台 | 状态 | 影响 | 建议 |
|---|---|---|---|---|
| BaiduSpider | 百度搜索 + 百度 AI | 允许/阻止 | 关键 | [行动] |
| Bytespider | 字节跳动/豆包/抖音 | 允许/阻止 | 高 | [行动] |
| Sogou Spider | 搜狗搜索 | 允许/阻止 | 高 | [行动] |
| 360Spider | 360 搜索 | 允许/阻止 | 中 | [行动] |
| YisouSpider | 夸克/UC/神马搜索 | 允许/阻止 | 中 | [行动] |
| GPTBot | ChatGPT / OpenAI | 允许/阻止 | 中 | [行动] |
| Googlebot | Google 搜索 | 允许/阻止 | 低(CN) | [行动] |
```

Add CN-specific translation: "阻止 AI 爬虫访问您的网站，相当于在营业时间关闭店铺大门。如果爬虫无法访问您的网站，其背后的 AI 平台就无法引用您的内容。在中国市场，BaiduSpider 是所有爬虫中最关键的——它是百度 AI 搜索和文心一言的数据来源。"

### 第五部分：品牌权威性分析 (Brand Authority — CN)

```markdown
## 品牌权威性分析

| 平台 | 存在状态 | 详情 | 对 AI 可见性的影响 |
|---|---|---|---|
| 百度百科 (Baidu Baike) | 有/无 | [详情] | 极高 — 中国 AI 引擎最强实体信号 |
| 知乎 (Zhihu) | 有/无 | [详情] | 高 — 百度 AI 和 DeepSeek 重要引用来源 |
| 微信公众号 (WeChat OA) | 有/无 | [详情] | 高 — 微信搜索及中国 AI 引擎信号 |
| 小红书 (Xiaohongshu) | 有/无 | [详情] | 中高 — 消费品和生活方式查询引用 |
| Bilibili (B站) | 有/无 | [详情] | 中 — 科技、教育类品牌信号 |
| CSDN/稀土掘金 | 有/无 | [详情] | 中 — 开发者社区技术品牌信号 |
```

Add CN translation: "AI 平台通过跨多个权威来源交叉验证您的品牌来建立信任。每个平台上的准确、一致的品牌存在都会增加您的内容在 AI 回答中被引用的可能性。百度百科是中国 AI 引擎最强的实体信号——拥有经过认证的百度百科词条是任何品牌在中国 AI 搜索策略中的首要任务。"

### 第六部分：可被引用性分析 (Citability Analysis — CN)

#### 最易被引用的前 5 个页面
For each page in Chinese:
- URL
- 为何可被引用（结构、深度、E-E-A-T 信号）
- 一项可进一步提高其被引用概率的改进建议

#### 最不易被引用的前 5 个页面
For each page:
- URL
- 为何不易被引用（内容单薄、结构不佳、信号缺失）
- 具体的重写或重构建议

**商业影响**："最易被引用的页面是您出现在 AI 生成答案中的最佳候选。改进最不易被引用的 5 个页面是您在 AI 可见性方面最具投资回报率的内容投入。"

### 第七部分：技术健康摘要 (Technical Health Summary — CN)

```markdown
## 技术健康摘要

| 检查项 | 状态 | 商业影响 |
|---|---|---|
| ICP 备案 | 有/无/不适用 | [合规性及百度信任影响] |
| 服务器端渲染 (SSR) | 有/部分/无 | [对 AI 爬虫可见性的影响] |
| 移动端优化 | 良好/需改善/较差 | [对百度移动优先索引的影响] |
| 中国 CDN/主机 | 有/无 | [对中国用户访问速度的影响] |
| HTTPS 与安全头部 | 良好/需改善/较差 | [对信任信号的影响] |
| 页面加载速度 | 快/中等/慢 | [对用户体验和抓取预算的影响] |
| 百度站长验证 | 已设置/未设置 | [对百度抓取和索引的影响] |
```

**关键发现标注**：如果缺少 SSR，需要突出标注："您的网站使用客户端渲染，这意味着 AI 爬虫访问时看到的是空白页面。这是 AI 搜索可见性方面最具影响力的技术问题。在问题解决之前，大多数 AI 平台无法引用您的内容。"

If ICP license is missing and site targets China users: "注意：如果您的网站托管在中国大陆服务器上，ICP 备案是法律要求。缺少 ICP 备案不仅影响百度 AI 抓取，还可能面临合规风险。"

### 第八部分：结构化数据与 Schema

```markdown
## 结构化数据与 Schema

### 当前实施情况
| Schema 类型 | 存在 | 状态 | AI 影响 |
|---|---|---|---|
| 组织 (Organization) | 是/否 | [有效/问题] | 关键 — 实体识别 |
| 文章 + 作者 (Article + Author) | 是/否 | [有效/问题] | 高 — E-E-A-T 信号 |
| sameAs (实体链接) | 是/否 | [数量]个链接 | 关键 — 跨平台实体图谱 |
| 百度兼容 Schema | 是/否 | [有效/问题] | 高 — 百度 AI 优化 |
| 面包屑 (BreadcrumbList) | 是/否 | [有效/问题] | 中 — 导航上下文 |
```

Note for CN if Baidu-compatible schema is missing: "已为您准备了适用于百度 AI 搜索的结构化数据代码，见技术附录。您的开发团队可以在短时间内将这些代码部署到网站上。"

### 第九部分：llms.txt 状态

```markdown
## llms.txt — AI 内容指南

| 文件 | 状态 | 建议 |
|---|---|---|
| /llms.txt | 存在/缺失 | [行动] |
| /llms-zh.txt | 存在/缺失 | [行动 — 中文 AI 指南] |
```

Add CN context: "llms.txt 是一个新兴标准（类似于 robots.txt），用于告知 AI 系统您的网站内容及最重要的页面。对于中国市场，建议同时提供英文和中文版本的 llms.txt 文件，以同时覆盖国际和中国 AI 引擎。"

### 第十部分：优先行动计划 (Prioritized Action Plan — CN)

This is the most important section. Organize by timeline and impact with CN-specific actions.

```markdown
## 优先行动计划

### 速赢项（本周内完成）
*高影响、低投入 — 可立即实施*

| # | 行动 | 影响 | 投入 | 影响平台 |
|---|---|---|---|---|
| 1 | 在 robots.txt 中允许 BaiduSpider 和 Bytespider | 高 | 1 小时 | 百度 AI、豆包 |
| 2 | 在百度站长平台验证网站并提交 sitemap | 高 | 2 小时 | 百度 AI 搜索、文心一言 |
| 3 | 添加百度站点验证 meta 标签 | 中 | 30 分钟 | 百度 AI 搜索 |
| 4 | 检查并设置 html lang=zh-CN | 中 | 1 小时 | 所有中国 AI 引擎 |
| 5 | 为已有内容添加发布日期 | 中 | 2 小时 | 豆包、DeepSeek |
```

**CN Quick Win criteria**: Can be done in < 4 hours by one person. Examples:
- Unblock BaiduSpider and Bytespider in robots.txt
- Verify site in Baidu Zhanzhang (百度站长平台) and submit sitemap
- Add Baidu site verification meta tag
- Set correct `<html lang="zh-CN">` attribute
- Add publication dates to existing content (Doubao favors freshness)
- Add author bylines with Chinese credentials
- Create/claim Baidu Baike entry foundation

```markdown
### 中期改进项（本月内完成）
*显著影响、适度投入 — 需要内容或技术变更*

| # | 行动 | 影响 | 投入 | 影响平台 |
|---|---|---|---|---|
| 1 | 申请或完善百度百科词条 | 极高 | 3-7 天 | 百度 AI、文心一言、DeepSeek |
| 2 | 用中文问答式标题重构前 10 个页面 | 高 | 2-3 天 | 所有中国 AI 引擎 |
| 3 | 在知乎上建立品牌问答存在 | 高 | 1-2 天 | 百度 AI、DeepSeek |
| 4 | 实施完整的 Schema.org + 百度兼容标记 | 高 | 3-5 天 | 百度 AI、文心一言、Kimi |
| 5 | 创建中文 llms.txt 文件 | 中 | 1 天 | 所有 AI 引擎 |
```

**CN Medium-Term criteria**: 1-5 days of work. Examples:
- Apply/improve Baidu Baike entry (longest lead time item — start early)
- Restructure top pages with Chinese question headings and direct answers
- Establish brand presence on Zhihu (answered questions, official account)
- Implement comprehensive Schema.org + Baidu-compatible markup
- Optimize for Baidu mobile standards (AMP/MIP not required but responsive design is)
- Create Chinese llms.txt file
- Check and fix ICP license display in page footer

```markdown
### 战略举措（本季度内完成）
*长期竞争优势，需要持续投入*

| # | 行动 | 影响 | 投入 | 影响平台 |
|---|---|---|---|---|
| 1 | 建立活跃的知乎机构号并持续输出 | 高 | 持续 | 百度 AI、DeepSeek |
| 2 | 在字节跳动生态中建立品牌存在（抖音+今日头条） | 高 | 持续 | 豆包 |
| 3 | 开发小红书品牌内容策略 | 中高 | 持续 | 豆包、Kimi |
| 4 | 在 CSDN/掘金发布技术内容（技术品牌） | 中 | 持续 | DeepSeek、Kimi |
| 5 | 如适用，建设淘宝/天猫品牌店 | 中 | 持续 | 通义千问 |
```

**CN Strategic criteria**: Ongoing effort over weeks/months. Examples:
- Build Baidu Baike verified entity presence with complete content
- Develop active Zhihu institutional account (机构号) with Q&A strategy
- Create Douyin/Toutiao content aligned with search queries
- Build Xiaohongshu brand presence with quality notes
- Establish CSDN/Juejin technical content for developer brand
- For e-commerce: build Taobao/Tmall store presence (Qwen signal)
- Implement long-form technical content strategy for Kimi (200K+ context)
- Consider server-side rendering if currently client-rendered

### 预估影响 (Estimated Impact — CN)

"基于行业基准和本次审计中发现的具体差距:
- **速赢项**可使您的 GEO 分数提高约 [X-Y] 分
- **全面实施**本行动计划可将您的 GEO 分数提升至约 [XX]/100
- 考虑到百度在中国搜索市场超过 80% 的份额，以及 AI 搜索在中国搜索引擎中的快速增长，改进的 AI 可见性预计可带来每月约 **¥X,XXX - ¥XX,XXX** 的额外有机搜索价值"

Use conservative estimates. Base the RMB figure on:
- Current estimated organic traffic value (from analytics or industry benchmarks)
- Baidu holds ~80%+ CN search market share with AI search expanding rapidly
- A 10-point GEO score improvement typically correlates with a 15-25% increase in AI citation frequency

### 第十一部分：竞争对手对比 (Competitor Comparison — CN)

If competitor URLs were analyzed alongside the primary domain:

```markdown
## 竞争对手对比

| 指标 | [您的品牌] | [竞争对手 1] | [竞争对手 2] |
|---|---|---|---|
| GEO 总分 | XX/100 | XX/100 | XX/100 |
| 百度 AI 就绪度 | XX/100 | XX/100 | XX/100 |
| 豆包就绪度 | XX/100 | XX/100 | XX/100 |
| 文心一言就绪度 | XX/100 | XX/100 | XX/100 |
| 通义千问就绪度 | XX/100 | XX/100 | XX/100 |
| Kimi 就绪度 | XX/100 | XX/100 | XX/100 |
| DeepSeek 就绪度 | XX/100 | XX/100 | XX/100 |
| Schema 覆盖率 | [详情] | [详情] | [详情] |
| 百度百科存在 | 有/无 | 有/无 | 有/无 |
| 知乎权威性 | [详情] | [详情] | [详情] |
| SSR 状态 | 有/无 | 有/无 | 有/无 |
```

### 您的优势
[具体领域，品牌表现优于竞争对手]

### 您的差距
[竞争对手具备优势的具体领域，及缩小差距的行动计划]

---

### 第十二部分：附录 (Appendix — CN)

```markdown
## 附录

### 方法论
本次 GEO 审计采用以下方法:
- **分析页面**: [具体 URL 列表]
- **地区**: 中国 (CN)
- **评估平台**: 百度 AI 搜索、豆包 (Doubao)、文心一言 (ERNIE Bot)、通义千问 (Qwen)、Kimi (月之暗面)、DeepSeek (深度求索)
- **技术检查**: HTTP 头部、robots.txt、HTML 源码分析、结构化数据验证
- **内容评估**: E-E-A-T 框架（经验、专业、权威、信任）
- **Schema 验证**: JSON-LD 解析与 Schema.org 标准合规性
- **分析日期**: [日期]

### 数据来源
- 各 AI 平台官方文档
- 百度搜索质量评估指南
- Schema.org 完整类型层次
- 行业引用研究（Zyppy、Authoritas、Semrush AI 搜索研究）
- Core Web Vitals 阈值 (web.dev)
- AI 爬虫用户代理文档（各平台官方文档）

### 术语表

| 术语 | 定义 |
|---|---|
| GEO | 生成式搜索引擎优化 — 优化内容以被 AI 搜索平台引用 |
| E-E-A-T | 经验、专业、权威、信任 — Google 内容质量框架 |
| SSR | 服务器端渲染 — 在服务器端生成 HTML 以便爬虫无需 JavaScript 即可读取内容 |
| ICP 备案 | 互联网内容提供商备案 — 中国法律要求的网站备案 |
| 百度站长平台 | Baidu Zhanzhang — 百度网站管理员工具 |
| JSON-LD | JavaScript Object Notation for Linked Data — 推荐的结构化数据格式 |
| sameAs | Schema.org 属性，将实体链接到其他平台上的账号 |
| llms.txt | 用于引导 AI 系统了解网站内容的建议标准文件 |
| CWV | Core Web Vitals — 谷歌页面体验指标 (LCP, INP, CLS) |
```

---

## 格式与语气指南 — CN

### 格式
- 使用清晰的 Markdown 格式：表格、标题 (H2/H3)、要点列表、加粗强调
- 数据用表格呈现，建议用要点列表，关键术语用加粗
- 段落之间留一个空行以提高可读性
- 使用水平线 (---) 分隔主要部分
- 所有 URL 使用绝对路径

### 语气
- **专业且易懂** — 面向企业主而非开发者
- **自信直接** — 以结论形式陈述发现，而非可能性
- **以行动为导向** — 每个发现都应关联到具体行动
- **商业影响为核心** — 将技术问题转化为业务成果
- 避免：不加解释的行业术语、模棱两可的语言、被动语态、过多免责声明
- 使用："您的网站[具备/不具备]..."、"我们建议..."、"这将影响..."

### 货币框架
- 使用人民币 (RMB/¥) 进行价值计算
- 参考百度在中国搜索市场的份额来解释影响程度
- "将百度 AI 就绪度从 35 提高到 70 可将百度 AI 搜索中的存在感提高约 50%"
- "百度百科词条建设（预计 5-10 个工作日内容准备）可将您的实体识别分数从 20 提高到 80"

保守估算。明确说明假设条件。切勿承诺具体结果。

---

## 输出

生成 **GEO-CLIENT-REPORT-<DOMAIN>-CN.md** 使用以上完整模板，填入实际审计数据。报告应:
- 约 3,000-6,000 字
- 可直接发送给客户，无需编辑
- 内容自包含（不引用其他报告文件 — 所有相关数据均已包含）
- 可打印且可展示（清晰的 Markdown 格式）
