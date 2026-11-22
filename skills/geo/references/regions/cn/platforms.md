# China Brand Platform Evaluation

When auditing for the China market (region=cn), replace the 5 Western brand platforms
with these 6 Chinese platforms. Each platform has different verification methods,
scoring criteria, and importance for AI entity recognition.

## Baidu Baike (百度百科) — Weight: 25%

The single strongest entity signal for Chinese AI search. Equivalent to Wikipedia for
Western markets. Baidu Baike entries are heavily cited by Yuanbao, Doubao, and
other Chinese AI engines.

**Verification method:**
1. Use WebFetch to search: `baike.baidu.com/item/[Brand Name]`
2. Check for official/verified entry (蓝V认证)
3. Record entry completeness (sections, images, references)
4. Note last update date

**Scoring:**
- Official verified entry with full content: 100 points
- Entry exists but minimal content: 50 points
- Entry exists but outdated (>1 year): 30 points
- No entry: 0 points

## Zhihu (知乎) — Weight: 20%

China's Quora-equivalent. Highly cited by Chinese AI engines for Q&A and
expert opinion content. Brand mentions in high-quality Zhihu answers signal
authority.

**Verification method:**
1. Use WebFetch to search: `zhihu.com/search?q=[Brand Name]`
2. Check for brand-related questions and answers
3. Evaluate answer quality (upvotes, author credentials)
4. Check for official Zhihu account (机构号)

**Scoring:**
- Official account with active Q&A presence: 100 points
- Multiple high-quality brand mentions: 70 points
- Some mentions but sparse: 40 points
- No presence: 0 points

## WeChat OA (公众号) — Weight: 20%

WeChat Official Accounts are critical for Chinese brand presence. Content from
WeChat OAs appears in Weixin Search and is cited by Chinese AI platforms.

**Verification method:**
1. Use WebFetch to search: `weixin.qq.com` or `sogou.com/weixin`
2. Check for official WeChat OA
3. Evaluate article quality and posting frequency
4. Note follower count signals (if available)

**Scoring:**
- Active OA with regular, high-quality articles: 100 points
- OA exists but infrequent posting: 50 points
- No OA found: 0 points

## Xiaohongshu (小红书) — Weight: 15%

RED is a lifestyle and product discovery platform. Strong influence on consumer
brand perception in China. Content frequently cited by AI engines for product
and lifestyle queries.

**Verification method:**
1. Use WebFetch to search: `xiaohongshu.com/search_result?keyword=[Brand Name]`
2. Check for brand-related notes/posts
3. Evaluate note quality, engagement, and recency
4. Check for brand collaboration content

**Scoring:**
- Active brand presence with quality notes: 100 points
- Some organic mentions but no official presence: 50 points
- No meaningful presence: 0 points

## Bilibili (B站) — Weight: 10%

China's YouTube equivalent for medium-to-long-form video. Important for tech,
education, and entertainment brands. Bilibili content is increasingly cited by AI.

**Verification method:**
1. Use WebFetch to search: `search.bilibili.com/all?keyword=[Brand Name]`
2. Check for brand-related videos
3. Evaluate video quality, views, and recency
4. Check for official Bilibili account

**Scoring:**
- Official account with quality video content: 100 points
- Brand mentioned in third-party videos: 50 points
- No presence: 0 points

## Douyin (抖音) — Weight: 10%

ByteDance's short-video platform. Massive user base in China. Short-form video
content cited by Doubao and other ByteDance AI products.

**Verification method:**
1. Use WebFetch to search: `douyin.com/search/[Brand Name]`
2. Check for brand account and content
3. Evaluate video count and engagement signals
4. Note if brand has verified Douyin account

**Scoring:**
- Verified account with active content: 100 points
- Some organic content but no official account: 50 points
- No presence: 0 points

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

> **Citation ≠ Platform Value**: 微博/抖音/搜狐 show near-zero citation for traditional PR content (3%) vs GEO-optimized content (51.4%). Content optimization is the primary differentiator, not platform choice alone. See geo-distribution-plan/SKILL.cn.md for optimization guidelines.

## Scene-Citation Affinity Table (场景-引用关联)

| 场景 (Scene) | Platform 1 | Platform 2 | Platform 3 |
|-------------|------------|------------|------------|
| 购物对比 (Shopping) | 什么值得买 | 泡泡网 | 中关村 |
| 故障排查 (Troubleshooting) | IT之家 | CSDN | 知乎 |
| 学术研究 (Research) | 知乎 | 百度百科 | 网易 |
| 政策查询 (Policy) | 腾讯网 | 搜狐 | 微博 |
| 行业分析 (Industry) | 36Kr | 爱科技 | 虎嗅 |
