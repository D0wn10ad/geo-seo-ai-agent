---
name: geo-technical-cn
description: CN-specific technical SEO overrides — ICP, Baidu crawlers, China CDN, Baidu verification
version: 1.0.0
region: cn
parent: geo-technical
---

# GEO Technical SEO — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following additional checks and adjustments to the base technical audit.

---

## Additional Category: China-Specific Checks (10 bonus points)

When auditing a site targeting the China market, add these checks alongside the base 8 categories.

### CN-1: ICP License (ICP备案)

**Required for**: Any website hosted on servers within mainland China.
**Check**: Scan page footer for ICP filing number format: `京ICP备XXXXXXXX号-X` or `沪ICP备XXXXXXXX号-X`.
**Scoring**:
- ICP license present and valid: 4 points
- ICP license absent but could be required: -2 points (flag as compliance risk)
- Not applicable (site not hosted in CN): N/A

### CN-2: Baidu Webmaster Tools Verification

**Check**: Scan HTML `<head>` for `<meta name="baidu-site-verification" content="...">`.
**Scoring**:
- Present: 2 points
- Absent: 0 points (recommend adding)

### CN-3: China CDN or Hosting

**Check for CN-based hosting/CDN**:
- Check if site uses a China CDN provider (阿里云CDN, 腾讯云CDN, 网宿科技, 又拍云)
- Check if site resolves to a mainland China IP
- If site targets CN users but is hosted outside China, flag latency risk
**Scoring**:
- China-hosted: 2 points
- Global CDN with China PoP: 1 point
- No China CDN: 0 points (flag as performance risk)

### CN-4: Baidu Crawler Access in robots.txt

**Check robots.txt for**:
- `User-agent: BaiduSpider` rules
- `User-agent: Sogou` (搜狗) rules
- `User-agent: 360Spider` (360搜索) rules
- Ensure these CN crawlers are NOT blocked or restricted on important content
**Scoring**:
- All CN crawlers allowed on key paths: 2 points
- Some restrictions: 1 point
- CN crawlers blocked: -2 points

### CN-5: Baidu-Specific Meta Tags

**Check for Baidu-specific meta tags**:
- `<meta name="applicable-device" content="pc,mobile">` (device adaptation)
- `<meta http-equiv="Cache-Control" content="no-transform">` (prevent proxy transformation)
- `baidu-site-verification` (already checked above)
**Scoring**:
- Present and correct: 1 point (bonus)

### CN-6: Chinese Language SEO

**Check**:
- `<html lang="zh-CN">` or `zh-Hans` correctly set
- hreflang tags for CN audience: `zh-CN`, `zh-Hans`, `zh-Hant` as appropriate
- Content encoding: UTF-8 (GB2312 is legacy, rare on modern sites)
**Scoring**:
- Correct lang + hreflang: 1 point
- Issues: 0 points

---

## Adjusted AI Crawler Table (CN)

When auditing for CN market, add these crawlers to the base crawler check:

| Crawler | User-Agent | Platform |
|---|---|---|
| BaiduSpider | BaiduSpider | Baidu Search + Baidu AI |
| Bytespider | Bytespider | ByteDance / Doubao / Douyin |
| Sogou Spider | Sogou web spider | Sogou Search |
| 360Spider | 360Spider | 360 Search |

---

## Updated Scoring for CN

| Category | Weight (CN) | Max Points |
|---|---|---|
| Server-Side Rendering / JS Dependency | 25% | 25 |
| Meta Tags & Indexability | 10% | 10 |
| Crawlability (robots.txt, sitemap) | 15% | 15 |
| Security Headers | 5% | 5 |
| Core Web Vitals Risk | 10% | 10 |
| Mobile Optimization | 15% | 15 |
| URL Structure | 5% | 5 |
| Response Headers & Status | 5% | 5 |
| Additional Checks | 5% | 5 |
| China-Specific (ICP, Baidu, CDN) | 10% | 10 |

Mobile weight is increased for CN because a majority of Chinese users access the web via mobile devices, and Baidu's mobile-first index is stricter than Google's.

Output file: `GEO-TECHNICAL-AUDIT-CN.md`
