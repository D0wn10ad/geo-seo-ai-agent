---
name: geo-schema-cn
description: CN-specific schema overrides — Baidu extensions, CN entity defaults, ICP requirements
version: 1.0.0
region: cn
parent: geo-schema
---

# GEO Schema & Structured Data — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base schema skill.

Reference: `regions/cn/schema.md` for detailed CN schema defaults and templates.

---

## Organization Schema (CN Defaults)

Replace the base Organization schema defaults:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[REPLACE: Company Chinese name]",
  "alternateName": "[REPLACE: Company English name if applicable]",
  "url": "[REPLACE: https://example.cn]",
  "logo": "[REPLACE: https://example.cn/logo.png]",
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "CN",
    "addressRegion": "[REPLACE: Province, e.g. 北京/上海/广东]",
    "addressLocality": "[REPLACE: City]",
    "streetAddress": "[REPLACE: District/Street/Number]",
    "postalCode": "[REPLACE: 6-digit code]"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[REPLACE: +86-XXX-XXXXXXX]",
    "contactType": "customer service"
  }
}
```

### sameAs Priority (CN)

Replace Western sameAs platforms with CN equivalents:
1. **Baidu Baike** (https://baike.baidu.com/item/[brand]) — STRONGEST
2. **WeChat Official Account** (https://weixin.qq.com/[brand]) 
3. **Weibo** (https://weibo.com/[brand])
4. **Zhihu** (https://www.zhihu.com/org/[brand])
5. **Douyin** (https://www.douyin.com/user/[brand])
6. **Bilibili** (https://space.bilibili.com/[brand])
7. **Xiaohongshu** (https://www.xiaohongshu.com/user/[brand])

---

## Baidu-Specific Schema Extensions

### Baidu Breadcrumb (百度面包屑导航)
Baidu supports BreadcrumbList with additional CN-specific properties:
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "首页",
      "item": "https://example.cn"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[REPLACE: Category in Chinese]",
      "item": "https://example.cn/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[REPLACE: Page title in Chinese]"
    }
  ]
}
```

### DataRecord for Baidu
Baidu supports DataRecord schema for structured data display in search results:
- Use for product specifications, corporate info, or any tabular data
- Requires `DataRecord` + `DataFeed` wrapper

### MobileApp Schema (for Baidu)
Baidu indexes mobile apps differently. If the brand has a CN app:
```json
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "[REPLACE: App Chinese name]",
  "operatingSystem": "Android, iOS",
  "applicationCategory": "[REPLACE: e.g. BusinessApplication]",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "CNY"
  },
  "availableOnDevice": "iOS, Android"
}
```

---

## Additional CN Schema Checks

### ICP License
Include ICP filing number in Organization schema or as separate meta:
- Recommended: add `identifier` property with ICP number
- Or add as alternateName: `"alternateName": "ICP证: 京ICP备XXXXXXXX号-1"`

### Person Schema (CN)
For Chinese authors, include:
- Chinese name as `name`
- English name as `alternateName` if applicable
- `knowsAbout` in Chinese for topic expertise
- `affiliation` with Chinese organization names
- `sameAs` linking to Zhihu, Weibo, CSDN profiles

### Article Schema (CN)
Add Baidu-compatible fields:
- `author` linked to Person with Chinese credentials
- `publisher` linked to Organization with ICP info
- `inLanguage`: "zh-CN" or "zh-Hans"
- `headline` in Chinese

### Speakable (CN)
For Baidu voice search and Chinese TTS:
- Use CSS selectors that target Chinese-language content sections
- Keep speakable sections concise (50-100 characters in Chinese)
- Test compatibility with Baidu AI voice search

---

## CN Schema Score Adjustments

| Component | Points (CN) | Criteria |
|---|---|---|
| Organization with CN address + ICP | 20 | Present with CN-format address, ICP number, Baidu Baike sameAs |
| Article schema in Chinese | 15 | Present, author as Person, inLanguage zh-CN |
| Person schema with CN credentials | 15 | Present, sameAs to Zhihu/CSDN/Weibo |
| sameAs completeness (CN platforms) | 15 | Baidu Baike (must-have) + 2 CN platforms (10), 4+ (15) |
| Baidu extensions (Breadcrumb, DataRecord) | 10 | At least BreadcrumbList present (10) |
| speakable for Chinese TTS | 10 | Present and targeting Chinese content |
| No deprecated schemas | 5 | Same as base |
| JSON-LD format | 5 | Same as base |
| Validation | 5 | Same as base |

Output file: `GEO-SCHEMA-REPORT-CN.md`
