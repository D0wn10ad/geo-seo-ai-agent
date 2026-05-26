---
name: geo-platform-optimizer-cn
description: CN-specific platform optimization overrides — Baidu AI, Doubao, Yuanbao, Qwen, Kimi, DeepSeek
version: 1.0.0
region: cn
parent: geo-platform-optimizer
---

# GEO Platform Optimizer — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Replace the Western platform rubrics (Google AIO, ChatGPT, Perplexity, Gemini, Copilot)
with the CN engine rubrics below. Scoring structure (content signals, entity recognition,
technical access) mirrors the base skill but uses CN-specific criteria.

Reference: `regions/cn/ai-engines.md` for detailed per-engine rubrics.

---

## Platform 1: Baidu AI Search (Baidu AI 搜索)

Replaces: Google AI Overviews

### How Baidu AI Selects Sources
- Baidu's ERNIE-powered AI search pulls from its own index (80%+ CN market share)
- Strongly favors Baidu Baike entries, Baidu Zhidao (Q&A), and Baidu-owned properties
- Prefers Chinese-language content with proper Baidu SEO (百度优化)
- Baidu's AI summaries prioritize authoritative sources with ICP licenses
- Freshness matters more than in Google — Baidu AI favors recently updated content

### Optimization Checklist
1. **Baidu Baike presence**: Ensure brand has a verified Baidu Baike entry. This is the #1 entity signal for Baidu AI.
2. **Chinese-language Q&A**: Use question headings in Chinese (e.g., "什么是...", "如何...") matching Baidu search queries.
3. **Baidu-friendly formatting**: Clear paragraphs, proper Chinese punctuation, numbered lists for processes.
4. **Mobile optimization**: Baidu prioritizes mobile-friendly sites for AI summaries (m-site or responsive).
5. **Baidu站长平台 (Webmaster Tools)**: Verify site in Baidu Zhanzhang and submit sitemap.

### Scoring Rubric (0-100)
- Baidu Baike + entity signals: 35 points
- Content signals (Q&A, structure, Chinese language): 35 points
- Baidu technical access (robots.txt, sitemap, site speed): 30 points
Referral info: Most-cited platforms for this engine: Baidu Baike, Zhihu, 36Kr, 百家号

---

## Platform 2: Doubao (豆包) — ByteDance AI

Replaces: ChatGPT Web Search

### How Doubao Selects Sources
- Doubao is ByteDance's AI assistant, deeply integrated with Douyin (TikTok CN)
- Heavily indexes Douyin content, Toutiao (news aggregator), and Xigua Video
- Values visual content with accompanying text descriptions
- ByteDance's proprietary model favors content from its ecosystem

### Optimization Checklist
1. **Douyin presence**: Active Douyin (抖音) account with regular video content mentioning the brand
2. **Toutiao articles**: Content published on Toutiao (今日头条) for news/article discovery
3. **Visual + text pairing**: Ensure every image/video has Chinese text description
4. **ByteDance ecosystem**: Leverage Xigua Video (西瓜视频) for long-form content

### Scoring Rubric (0-100)
- Douyin/Toutiao ecosystem presence: 35 points
- Content adaptability (visual + text): 35 points
- Technical access: 30 points
Referral info: Most-cited platforms for this engine: Xiaohongshu, WeChat, Zhihu, Bilibili

---

## Platform 3: Yuanbao (腾讯元宝) — Tencent

Replaces: Google Gemini

### How Yuanbao Sources Content
- Yuanbao (元宝) is Tencent's AI assistant, integrated with WeChat (微信) and QQ ecosystems
- Strongly indexes content from WeChat Official Accounts, QQ News, and Tencent News
- Leverages Tencent's knowledge graph built from social and media ecosystem data
- Prefers content with demonstrated social proof (shares, likes, reading counts)

### Optimization Checklist
1. **WeChat Official Account**: Maintain branded WeChat Official Account (微信公众号) with regular content
2. **QQ News/腾讯新闻**: Publish/promote content on Tencent News platforms
3. **Social engagement signals**: High-quality content that generates WeChat shares and reads
4. **Tencent ecosystem**: Leverage QQ Channels, Tencent Video, and Weixin Read
5. **Structured data**: Schema markup compatible with Tencent's content parsing

### Scoring Rubric (0-100)
- Tencent ecosystem presence (WeChat/QQ): 40 points
- Content engagement signals: 30 points
- Technical access: 30 points
Referral info: Most-cited platforms for this engine: WeChat, QQ News, Zhihu, 搜狐

---

## Platform 4: Tongyi Qianwen (通义千问) — Alibaba

Replaces: Perplexity AI

### How Tongyi Selects Sources
- Alibaba's LLM, integrated with Alibaba Cloud, Taobao, Tmall, and 1688
- Prefers content from Alibaba ecosystem partners and verified merchants
- E-commerce and product-related content strongly favored
- Values detailed product descriptions, reviews, and comparison content

### Optimization Checklist
1. **Alibaba ecosystem**: Presence on Taobao/Tmall (for e-commerce) or Alibaba Cloud marketplace (for SaaS)
2. **Product content**: Detailed, structured product descriptions with specifications
3. **Chinese customer reviews**: Genuine review volume on Alibaba platforms
4. **Comparison content**: Product comparisons and buying guides in Chinese

### Scoring Rubric (0-100)
- Alibaba ecosystem presence: 35 points
- Content quality (detail, structure): 35 points
- Community signals (reviews, ratings): 30 points
Referral info: Most-cited platforms for this engine: CSDN, Juejin, Zhihu, 36Kr

---

## Platform 5: Kimi (月之暗面) — Moonshot AI

Replaces: Bing Copilot

### How Kimi Selects Sources
- Moonshot AI's Kimi is known for long-context processing (200K+ tokens)
- Heavily indexes Chinese web content, especially long-form articles
- Favors comprehensive, in-depth content that leverages its long-context advantage
- Used frequently for research, analysis, and document processing queries
- Strong with technical/professional content domains

### Optimization Checklist
1. **Long-form Chinese content**: 3000+ word comprehensive articles
2. **Technical depth**: Detailed documentation, whitepapers, technical analysis
3. **Professional credentials**: Clear author expertise signals
4. **Clear structure**: Well-organized long content with headings, summaries, and citations

### Scoring Rubric (0-100)
- Content depth and comprehensiveness: 40 points
- Technical/professional signals: 30 points
- Structure and accessibility: 30 points
Referral info: Most-cited platforms for this engine: 微信公众号, Zhihu, 小红书, 豆瓣

---

## Platform 6: DeepSeek (深度求索)

Additional CN engine not replacing a specific Western one.

### How DeepSeek Selects Sources
- Open-weight model gaining rapid adoption in CN enterprise
- Sources from general web index with strong developer/technical community focus
- Valued for cost-effectiveness and transparency by Chinese developers
- Prefers well-structured, factual content with clear attribution

### Optimization Checklist
1. Standard Chinese SEO best practices apply
2. Technical documentation in Chinese
3. Developer community presence (CSDN, Juejin, GitHub CN)
4. Original research and data

### Scoring Rubric (0-100)
- Developer community presence: 30 points
- Technical content quality: 40 points
- Open/attribution signals: 30 points
Referral info: Most-cited platforms for this engine: GitHub, CSDN, Zhihu, technical docs

---

## 📋 Scene Knowledge Base Strategy (场景知识库)

When REGION is cn, extend platform analysis with scene-KB binding:
- Identify the user's scene/task type (购物对比/故障排查/学术研究/政策查询/行业分析)
- Map each scene to the most-cited platforms for that intent
- Recommend KB-format content (问答对/对比表格/操作步骤/数据报告)
- See `regions/cn/platforms.md` scene-citation affinity tables

---

## Cross-Platform Comparison (CN)

After scoring all 6 CN platforms, identify:
- **Strongest CN platform**: Highest score with explanation
- **Weakest CN platform**: Lowest score with gap analysis
- **CN platform synergies**: Actions that improve multiple CN platforms (e.g., Baidu Baike helps both Baidu AI Search and ERNIE)
- **Output file**: `GEO-PLATFORM-OPTIMIZATION-CN.md`
