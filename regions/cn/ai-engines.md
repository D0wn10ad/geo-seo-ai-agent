# China AI Engine Evaluation Criteria

When auditing for the China market (region=cn), replace the 5 Western AI engine checks
with these 6 Chinese AI engines. Each engine has its own sourcing behavior and content
preferences, similar to how the Western engines differ from each other.

## Baidu AI Search (百度AI搜索)

Baidu's AI search integrates ERNIE LLM with Baidu's index. It prioritizes:
- Baidu Baike entries (strongest entity signal)
- Baidu Zhidao (百度知道) Q&A content
- Authoritative .gov.cn and .edu.cn domains
- Content with clear Chinese-language citations
- Pages with Baidu schema extensions (breadcrumb, article)

**Scoring criteria:**
- Entity recognition via Baidu Baike: 30 points
- Content authority signals (gov/edu links): 25 points
- Chinese language quality: 25 points
- Technical access (BaiduSpider allowed): 20 points

## Doubao (豆包)

ByteDance's AI assistant integrated with Toutiao ecosystem. Preferences:
- Short-form, scannable content (Doubao favors concise answers)
- Content from Douyin/Toutiao ecosystem
- Fresh content (prioritizes recent publications)
- Visual-rich content (images, video embeds)

**Scoring criteria:**
- Content conciseness and scanability: 30 points
- Freshness (published within 90 days): 25 points
- Cross-platform presence on ByteDance properties: 25 points
- Multi-format content (text + images): 20 points

## ERNIE Bot (文心一言)

Baidu's flagship LLM. Shares data sources with Baidu Search but with:
- Stronger preference for structured data (schema.org)
- Emphasis on factual, well-sourced claims
- Prefers content with clear authorship
- Heavier weight on Baidu ecosystem presence

**Scoring criteria:**
- Structured data completeness: 30 points
- Factual density with citations: 30 points
- Author credentials presence: 20 points
- Baidu ecosystem integration: 20 points

## Qwen (通义千问)

Alibaba's LLM, integrated with Alibaba Cloud ecosystem. Preferences:
- E-commerce content from Taobao/Tmall ecosystem
- Technical documentation and developer content
- Alibaba Cloud-hosted content (CDN affinity)
- Content with clear logical structure

**Scoring criteria:**
- E-commerce/technical content quality: 30 points
- Logical content structure: 25 points
- Alibaba ecosystem presence: 25 points
- Server-side rendering (no JS dependency): 20 points

## Kimi (月之暗面)

Mooncake AI's assistant, focused on long-context understanding. Preferences:
- Long-form, comprehensive content (Kimi excels at processing 100K+ tokens)
- Detailed technical documentation
- Academic and research-oriented content
- Well-organized content with clear hierarchy

**Scoring criteria:**
- Content depth and comprehensiveness: 35 points
- Clear heading hierarchy and organization: 25 points
- Academic/research quality signals: 20 points
- Proper citation and references: 20 points

## DeepSeek (深度求索)

Independent Chinese AI lab, known for technical excellence. Preferences:
- Technical and scientific content
- Code snippets and technical documentation
- Well-structured factual content
- Open-source and developer ecosystem presence

**Scoring criteria:**
- Technical depth and accuracy: 30 points
- Code/infographic formatting quality: 25 points
- Developer ecosystem presence (GitHub, tech forums): 25 points
- Content structure and clarity: 20 points
