# China Schema & Structured Data Guidance

When auditing for the China market (region=cn), apply these schema defaults and
checks in addition to the standard schema.org validation.

## Default Organization Schema

Replace the US-default Organization template with China-specific values:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Brand Name]",
  "url": "[Website URL]",
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "CN"
  },
  "sameAs": [
    "https://baike.baidu.com/item/[Brand]",
    "https://weixin.qq.com/[BrandOA]",
    "https://weibo.com/[BrandWeibo]",
    "https://zhihu.com/org/[BrandZhihu]"
  ]
}
```

## Baidu-Specific Schema Extensions

Baidu recognizes standard schema.org types plus several Baidu-specific extensions:

### Baidu Breadcrumb
Standard BreadcrumbList works, but Baidu also supports a specialized breadcrumb:
```json
{
  "@context": "https://ziyuan.baidu.com/contexts/cambrian.jsonld",
  "@id": "[Page URL]",
  "title": "[Page Title]",
  "description": "[Meta Description]",
  "pubDate": "[Publication Date in YYYY-MM-DD format]",
  "upDate": "[Last Updated in YYYY-MM-DD format]"
}
```

### Baidu Article Extension
For news/article content, add Baidu's Article data source:
```json
{
  "@context": "https://ziyuan.baidu.com/contexts/cambrian.jsonld",
  "@id": "[Article URL]",
  "appid": "[Baidu App ID, if available]"
}
```

### Baidu Site Verification
Include Baidu Webmaster Tools verification in HTML `<head>`:
```html
<meta name="baidu-site-verification" content="[verification-code]" />
```

## sameAs Platform Priority

For CN region, the recommended sameAs platforms in order of importance:

| Platform | URL Pattern | Priority |
|----------|-------------|----------|
| Baidu Baike (百度百科) | `baike.baidu.com/item/[Brand]` | Highest |
| WeChat (微信) | WeChat OA QR or profile | High |
| Weibo (微博) | `weibo.com/[Brand]` | High |
| Zhihu (知乎) | `zhihu.com/org/[Brand]` | Medium |
| Bilibili (B站) | `space.bilibili.com/[UID]` | Medium |
| Douyin (抖音) | `douyin.com/user/[UID]` | Medium |

## Schema Checks Unique to CN

In addition to standard schema.org validation:

1. **Baidu verification meta tag present?** — Necessary for Baidu Webmaster Tools
2. **Baidu breadcrumb JSON-LD present?** — Improves Baidu SERP display
3. **sameAs includes Chinese platforms?** — Baidu Baike is the strongest entity signal
4. **Article dates in YYYY-MM-DD format?** — Required by Baidu
5. **No Google-only schema patterns?** — E.g., Google-speakable, Google-Review
6. **ICP filing in footer?** — Required by Chinese law, visible to crawlers

## Baidu Search Rich Results

Baidu supports these rich result types (check eligibility):

- **Site Links** — For branded searches (requires Baidu Webmaster Tools)
- **Breadcrumb** — Via Baidu breadcrumb extension or standard BreadcrumbList
- **Article** — News and article content (requires Baidu Article extension)
- **Image** — Baidu Image search optimization (requires ImageObject schema)

Note: Baidu's rich result capabilities are more limited than Google's. The focus
should be on entity recognition via Baidu Baike and structured data completeness,
rather than rich result eligibility.
