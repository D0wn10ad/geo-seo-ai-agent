# China AI Engine Evaluation Criteria

When auditing for the China market (region=cn), replace the 5 Western AI engine checks
with these 6 Chinese AI engines. Each engine has its own sourcing behavior and content
preferences, similar to how the Western engines differ from each other.

## MAU-Tier Weighting

Composite China GEO score = weighted average across all engines using these QuestMobile MAU tiers:

| Tier | Engine | MAU | Weight |
|------|--------|-----|--------|
| S | Doubao (豆包) | 315M | 1.00 |
| A | Qwen (通义千问) | 202M | 0.64 |
| A | DeepSeek (深度求索) | 132M | 0.42 |
| B | Yuanbao (腾讯元宝) | 109M | 0.35 |
| B | Kimi (月之暗面) | 24M | 0.08 |
| B | Baidu AI Search | N/A | 0.35 |

Weighting derived from QuestMobile MAU data. Composite score = weighted average across all engines using these tiers.

## Baidu AI Search (百度AI搜索)

Baidu's AI search integrates ERNIE LLM with Baidu's index. It prioritizes:
- Baidu Baike entries (strongest entity signal)
- Baidu Zhidao (百度知道) Q&A content
- Authoritative .gov.cn and .edu.cn domains
- Content with clear Chinese-language citations
- Pages with Baidu schema extensions (breadcrumb, article)

**Most-cited referral platforms (源易 2,844-sample data):**
1. Baidu Baike (百度百科)
2. Zhihu (知乎)
3. 36Kr
4. 百家号 (Baijiahao)

**Scoring criteria:**
- Entity recognition via Baidu Baike: 30 points
  - 归因提示 (attributed, UNVERIFIED): EEAT6.0 实体信任阈值，低于 60 降权、高于 85 视为优质 (文章 ID `Tlmyhz_NWUHwGbEwYHIzLA`, provenance row 9, UNVERIFIED, 未抽查确认)。此为归因指导，非本工具评分参数，不改变上方分值。
- Content authority signals (gov/edu links): 25 points
  - 归因提示 (attributed, UNVERIFIED): 多源交叉验证，单一来源占比上限 ≤8%，且需 ≥3个独立主体 (independent subject) 交叉印证；"来源" 指独立实体而非同一渠道的多篇帖子 (见 cross-validation.md, provenance rows 11-13, 文章 ID `VmcGBtJ6Ex5cgeFuG3oxMQ` / `7TACnZLx3k5UhUCROVyzUQ` / `2qOjVj6BPtmZ1GqPASY6Pg`, UNVERIFIED)。纯官方新闻稿/通稿来源 -60% 折损 (UNVERIFIED, CN 算法规则集, 尚无独立 provenance 行)。以上为归因指导，非本工具评分参数，不改变上方分值。
- Chinese language quality: 25 points
- Technical access (BaiduSpider allowed): 20 points

## Doubao (豆包)

ByteDance's AI assistant integrated with Toutiao ecosystem. 315M MAU (Tier S).
Approach to citation: Aggressively cites short-form content from ByteDance-owned platforms,
prioritizes recency and engagement signals over domain authority alone.

Preferences:
- Short-form, scannable content (Doubao favors concise answers)
- Content from Douyin/Toutiao ecosystem
- Fresh content (prioritizes recent publications)
- Visual-rich content (images, video embeds)

**Strengths:** Massive user base, strong at consumer lifestyle questions, excellent at synthesizing trending topics.
**Weaknesses:** Can prioritize engagement over factual accuracy, weaker on technical/enterprise topics.

**Most-cited referral platforms (源易 2,844-sample data):**
1. Xiaohongshu (小红书)
2. WeChat (微信公众号)
3. Zhihu (知乎)
4. Bilibili (哔哩哔哩)

内容来源构成层 (content-source composition, 与上方 源易 整体使用率排名分离，非第二张并列排名表): 另一组 74 问题实测 (文章 ID `nRq7-RG96GL2xvo_L4sAiw`, provenance row 16-17, UNVERIFIED) 给出不同的取源排序作为替代视角：抖音 (Douyin) 排 #1，108 次引用 (UNVERIFIED, nRq7)；今日头条 (头条号) 21 次引用 (UNVERIFIED, nRq7)；字节系生态合计 129 次引用 (UNVERIFIED, nRq7, row 17)。另有相互竞争的归因声称：字节系内容占比约 48.7% (UNVERIFIED, 文章 ID `fKgDW_YDjUYXG-Pst64D9Q`, provenance row 21, 未抽查确认)。129 次引用与 48.7% 单位与来源不同，不可合并为单一数值。此层只描述内容来源构成，不改动上方 源易 排名或 MAU 分层表。

**Scoring criteria:**
- Content conciseness and scanability: 30 points
- Freshness (published within 90 days): 25 points
  - 归因提示 (attributed, UNVERIFIED): 陈旧内容时效折损 0.2× (UNVERIFIED, CN 算法规则集, 尚无独立 provenance 行)。此为归因指导，非本工具评分参数，不改变上方分值。
- Cross-platform presence on ByteDance properties: 25 points
  - 归因提示 (attributed, UNVERIFIED): 跨平台取源需 ≥3个独立主体交叉印证、单一来源占比 ≤8% (见 cross-validation.md, provenance rows 11-12, UNVERIFIED)。此为归因指导，非本工具评分参数，不改变上方分值。
- Multi-format content (text + images): 20 points

## Yuanbao (腾讯元宝, Tencent Yuanbao)

Tencent's AI assistant integrated with WeChat/QQ ecosystem. 109M MAU (Tier B).
API patterns are similar to ERNIE Bot (文心一言) — both use similar structured data expectations
and citation formats. Migration note: Yuanbao has largely replaced ERNIE Bot in consumer-facing
scoring benchmarks as of Q1 2026, though ERNIE's API patterns may still be referenced for legacy
integration compatibility.

Approach to citation: Strong WeChat ecosystem preference, favors content that appears in
Tencent's content graph (WeChat Official Accounts, QQ News, Tencent Video).

Preferences:
- WeChat Official Account content (strongest signal)
- QQ News and Tencent media properties
- Social-share validated content
- Content with clear Tencent-friendly formatting

**Strengths:** Deep WeChat integration, strong social proof signals, excellent at lifestyle/recommendations.
**Weaknesses:** Limited outside WeChat ecosystem, weaker on pure technical topics.

**Most-cited referral platforms (源易 2,844-sample data):**
1. WeChat (微信公众号)
2. QQ News (腾讯新闻)
3. Zhihu (知乎)
4. 搜狐 (Sohu)

**Scoring criteria:**
- WeChat ecosystem presence: 30 points
  - 归因提示 (attributed, UNVERIFIED): 微信生态内容同样需 ≥3个独立主体交叉印证、单一来源占比 ≤8%，避免把同一账号多篇帖子算作多源 (见 cross-validation.md, provenance rows 11-13, UNVERIFIED)。此为归因指导，非本工具评分参数，不改变上方分值。
- Social share validation: 25 points
- Tencent-friendly formatting: 25 points
- Structured data completeness: 20 points

## Qwen (通义千问)

Alibaba's LLM, featuring Qwen2.5 series, integrated with Alibaba Cloud and Taobao/Tmall e-commerce
ecosystem. 202M MAU (Tier A). Approach to citation: Favors e-commerce transaction content,
Alibaba-hosted technical documentation, and content with clear product attribution.

Preferences:
- E-commerce content from Taobao/Tmall ecosystem (strong product/transaction focus)
- Technical documentation and developer content on Alibaba Cloud
- Alibaba Cloud-hosted content (CDN affinity)
- Content with clear logical structure

**Strengths:** Best-in-class for product/commercial questions, strong e-commerce integration, excellent technical docs.
**Weaknesses:** Can be biased toward Alibaba properties, less strong on independent research.

**Most-cited referral platforms (源易 2,844-sample data):**
1. CSDN
2. Juejin (掘金)
3. Zhihu (知乎)
4. 36Kr

**Scoring criteria:**
- E-commerce/technical content quality: 30 points
  - 归因提示 (attributed, UNVERIFIED): 纯官方新闻稿/通稿来源 -60% 折损 (UNVERIFIED, CN 算法规则集, 尚无独立 provenance 行)；实体信任参考 EEAT6.0 阈值，低于 60 降权、高于 85 视为优质 (文章 ID `Tlmyhz_NWUHwGbEwYHIzLA`, provenance row 9, UNVERIFIED)。此为归因指导，非本工具评分参数，不改变上方分值。
- Logical content structure: 25 points
- Alibaba ecosystem presence: 25 points
- Server-side rendering (no JS dependency): 20 points

## Kimi (月之暗面)

Mooncake AI's assistant, focused on long-context understanding. 24M MAU (Tier B).
Approach to citation: Deeply cites long-form content, research papers, and comprehensive
articles. Excels at processing 100K+ token contexts.

Preferences:
- Long-form, comprehensive content
- Detailed technical documentation
- Academic and research-oriented content
- Well-organized content with clear hierarchy

**Strengths:** Unmatched long-context processing, excellent for research/deep dives, strong academic citations.
**Weaknesses:** Smaller user base, slower response times, weaker on quick lookup queries.

**Most-cited referral platforms (源易 2,844-sample data):**
1. 微信公众号 (WeChat Official Accounts)
2. Zhihu (知乎)
3. 小红书 (Xiaohongshu)
4. 豆瓣 (Douban)

**Scoring criteria:**
- Content depth and comprehensiveness: 35 points
- Clear heading hierarchy and organization: 25 points
- Academic/research quality signals: 20 points
  - 归因提示 (attributed, UNVERIFIED): 学术/研究主张需 ≥3个独立主体交叉印证、单一来源占比 ≤8% (见 cross-validation.md, provenance rows 11-12, UNVERIFIED)。此为归因指导，非本工具评分参数，不改变上方分值。
- Proper citation and references: 20 points

## DeepSeek (深度求索)

Independent Chinese AI lab, known for technical excellence and the R1 reasoning model.
132M MAU (Tier A). Approach to citation: Prioritizes technical accuracy, developer
ecosystem content, and sources that enable chain-of-thought reasoning.

Preferences:
- Technical and scientific content (especially developer-focused)
- Code snippets and technical documentation
- Well-structured factual content that supports chain-of-thought
- Open-source and developer ecosystem presence (GitHub, technical forums)

**Strengths:** Best technical reasoning in Chinese market, R1 model excels at complex problem-solving, strong developer focus.
**Weaknesses:** Less strong on consumer lifestyle questions, smaller brand recognition outside tech circles.

**Most-cited referral platforms (源易 2,844-sample data):**
1. GitHub
2. CSDN
3. Zhihu (知乎)
4. Technical documentation sites

内容来源构成层 (content-source composition, 与上方 源易 整体使用率排名分离，非第二张并列排名表): 同一组 74 问题实测 (文章 ID `nRq7-RG96GL2xvo_L4sAiw`, provenance row 18, UNVERIFIED) 给出不同的取源排序作为替代视角：阿里云开发者社区 排 #1，77 次引用 (UNVERIFIED, nRq7)；抖音 (Douyin) 在该实测中 ABSENT，出现 0 次引用 (UNVERIFIED, nRq7)，并非 DeepSeek 的偏好来源，真实来源为开发者社区。此层只描述内容来源构成，不改动上方 源易 排名或 MAU 分层表。

**Scoring criteria:**
- Technical depth and accuracy: 30 points
  - 归因提示 (attributed, UNVERIFIED): 纯官方新闻稿/通稿来源 -60% 折损；技术主张需 ≥3个独立主体交叉印证、单一来源占比 ≤8% (见 cross-validation.md, provenance rows 11-13, UNVERIFIED)。此为归因指导，非本工具评分参数，不改变上方分值。
- Code/infographic formatting quality: 25 points
- Developer ecosystem presence (GitHub, tech forums): 25 points
- Content structure and clarity: 20 points
