---
name: geo-report-pdf-cn
description: CN-specific PDF report generator overrides — CJK font rendering, CN platform/engine naming, Chinese field labels, CN output file
version: 1.0.0
region: cn
parent: geo-report-pdf
---

# GEO PDF Report Generator — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following adjustments to the base PDF generation workflow.

---

## CJK Font Configuration

The base script at `scripts/generate_pdf_report.py` uses Helvetica for all text rendering. Helvetica does **not** support CJK characters. Before any other setup, ensure CJK fonts are available and registered.

### 1. Install a CJK TTF Font

Create a `fonts/` directory at the project root and add Noto Sans SC:

```bash
mkdir -p fonts
# Download Noto Sans SC from Google Fonts or use a system-provided font:
# - Linux: /usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf
# - macOS: ~/Library/Fonts/NotoSansSC-Regular.ttf
# - Or download from: https://fonts.google.com/noto/specimen/Noto+Sans+SC
#
# Copy to project fonts/:
cp /path/to/NotoSansSC-Regular.ttf fonts/
cp /path/to/NotoSansSC-Bold.ttf fonts/
```

If Noto Sans SC is unavailable, alternatives (in order of preference):
- **Source Han Sans SC** (`SourceHanSansSC-Regular.otf`) — Adobe/Google, same design
- **WenQuanYi Micro Hei** (`wqy-microhei.ttc`) — commonly pre-installed on Linux
- **SimSun** / **SimHei** — Windows CJK fallback (licensed, may not redistribute)

### 2. Register CJK Font in ReportLab

When calling `scripts/generate_pdf_report.py`, first register the CJK font by passing a modified invocation. The script itself does not import `TTFont` — you must either:

**Option A: Patch the script at call time** — Prepend font registration via Python:

```bash
python3 -c "
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('NotoSansSC', 'fonts/NotoSansSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSansSC-Bold', 'fonts/NotoSansSC-Bold.ttf'))
import sys; sys.argv = ['generate_pdf_report.py', '/tmp/geo-audit-data.json', 'GEO-REPORT-CN-example.pdf']
exec(open('scripts/generate_pdf_report.py').read())
"
```

**Option B: Create a thin wrapper script** (`scripts/generate_pdf_report_cn.py`):

```python
#!/usr/bin/env python3
"""CN-aware wrapper — registers CJK fonts before calling base generator."""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('NotoSansSC', 'fonts/NotoSansSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSansSC-Bold', 'fonts/NotoSansSC-Bold.ttf'))

# Replace Helvetica references in the base script
import generate_pdf_report as base
# The base script uses fontName='Helvetica' and fontName='Helvetica-Bold'
# throughout. After registration, map 'Helvetica' -> 'NotoSansSC' and
# 'Helvetica-Bold' -> 'NotoSansSC-Bold'. This can be done post-import
# by monkey-patching the paragraph styles and table styles.
```

**Option C (Recommended)**: Run the script with an environment variable or CLI flag to tell it to use CJK fonts. If the base script does not support this, prefer Option A for simplicity.

### CJK Text Handling in ReportLab

Key considerations when rendering Chinese text:

| Concern | Solution |
|---------|----------|
| Font size | CJK glyphs are wider than Latin — reduce body font size by ~0.5pt vs Helvetica equivalent |
| Line height | CJK needs ~1.5x line height vs Latin for readability — increase `leading` in ParagraphStyle |
| Word wrapping | ReportLab's `Paragraph` wraps CJK correctly if `fontName` points to a registered TTFont |
| Spacing | CJK does not use word spaces — set `wordWrap='CJK'` in ParagraphStyle for proper break |
| Gauge labels | Score gauge text will render Chinese labels (e.g., "优秀" instead of "Excellent") — ensure font handles these glyphs |
| Mixed content | English+Chinese text (e.g., "GEO 得分 65/100") renders fine if the CJK font has Latin glyphs (Noto Sans SC does) |

Add a `wordWrap='CJK'` parameter to all `ParagraphStyle` definitions that will contain Chinese text:

```python
style = ParagraphStyle(
    'CNBody',
    fontName='NotoSansSC',
    fontSize=9,
    leading=14,
    wordWrap='CJK',
    alignment=TA_LEFT,
)
```

---

## CN Engine Names in Visualizations

Replace Western engine names in all charts, tables, and score gauges:

### Platform Readiness Chart Labels

| Western (base) | CN Replacement |
|---|---|
| Google AI Overviews | 百度 AI 搜索 (Baidu AI Search) |
| ChatGPT | 豆包 (Doubao) |
| Perplexity | 通义千问 (Tongyi Qianwen) |
| Gemini | 文心一言 (ERNIE Bot) |
| Bing Copilot | Kimi 月之暗面 (Moonshot AI) |

Add an additional bar for **DeepSeek (深度求索)** if data is available.

### AI Crawler Table Column

| Western Crawler | CN Crawler | Platform (CN) |
|---|---|---|
| GPTBot | GPTBot | ChatGPT / Doubao |
| ClaudeBot | ClaudeBot | Claude (limited CN reach) |
| Google-Extended | Google-Extended | Google / Baidu cross-ref |
| PerplexityBot | PerplexityBot | Perplexity / Tongyi cross-ref |
| CCBot | CCBot | Common Crawl / general |
| — | **BaiduSpider** | Baidu AI Search / ERNIE |
| — | **Bytespider** | Doubao / Douyin |
| — | **Sogou Spider** | Sogou Search |
| — | **360Spider** | 360 Search |

Ensure the crawler status table is wide enough for the longer Chinese platform names.

---

## CN JSON Schema — Chinese Field Names

When building the audit JSON for the PDF generator, add CN-specific fields alongside (or replacing) the English ones:

```json
{
    "url": "https://example.cn",
    "brand_name": "Example 公司",
    "brand_name_cn": "范例公司",
    "date": "2026-02-18",
    "region": "cn",
    "geo_score": 65,
    "scores": {
        "ai_citability": 62,
        "brand_authority": 78,
        "content_eeat": 74,
        "technical": 72,
        "schema": 45,
        "platform_optimization": 59
    },
    "platforms": {
        "百度 AI 搜索": 68,
        "豆包": 62,
        "通义千问": 55,
        "文心一言": 60,
        "Kimi 月之暗面": 50,
        "DeepSeek": 45
    },
    "crawler_access": {
        "BaiduSpider": {"platform": "百度 AI 搜索", "status": "Allowed", "recommendation": "保持允许"},
        "Bytespider": {"platform": "豆包", "status": "Blocked", "recommendation": "建议解除限制"},
        "Sogou": {"platform": "搜狗搜索", "status": "Allowed", "recommendation": "保持允许"},
        "360Spider": {"platform": "360搜索", "status": "Not Found", "recommendation": "建议在 robots.txt 中设置"}
    },
    "executive_summary": "一份关于网站在中国AI搜索引擎中可见性的GEO审计报告中文摘要...",
    "findings": [
        {
            "severity": "critical",
            "title": "百度爬虫访问受限",
            "description": "BaiduSpider 被 robots.txt 限制，导致百度AI搜索无法索引关键内容。"
        }
    ],
    "quick_wins": ["添加 ICP 备案号到页脚", "创建百度百科词条"],
    "medium_term": ["优化中文内容结构", "部署 CN CDN"],
    "strategic": ["建立百度站长平台验证", "开发中文FAQ内容"]
}
```

Use `brand_name_cn` for the cover page title when the brand has both English and Chinese names. If `brand_name_cn` is absent, fall back to `brand_name`.

---

## CN Output Filename

Generate the PDF with a CN-specific prefix:

```bash
python3 scripts/generate_pdf_report.py /tmp/geo-audit-data.json \
    "GEO-REPORT-CN-[domain]-$(date +%Y-%m-%d).pdf"
```

Pattern: `GEO-REPORT-CN-{domain}-{YYYY-MM-DD}.pdf`

Examples:
- `GEO-REPORT-CN-example.cn-2026-02-18.pdf`
- `GEO-REPORT-CN-范例公司-2026-02-18.pdf`

---

## Adjusted Workflow for CN

Replace Step 6 of the base skill with:

### Step 6 (CN): Run PDF Generator with CJK Support

```bash
# 1. Build the CN-aware JSON with Chinese field names and CN engine data
cat > /tmp/geo-audit-data-cn.json << 'ENDJSON'
{ ... CN JSON with Chinese labels ... }
ENDJSON

# 2. Generate with CJK font registration prepended
python3 << 'PYEOF'
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('NotoSansSC', 'fonts/NotoSansSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSansSC-Bold', 'fonts/NotoSansSC-Bold.ttf'))

# Run the base generator
import sys
sys.argv = ['generate_pdf_report.py', '/tmp/geo-audit-data-cn.json',
            'GEO-REPORT-CN-example-2026-02-18.pdf']
exec(open('scripts/generate_pdf_report.py').read())
PYEOF
```

The CJK font must be registered **before** any ReportLab imports happen in the base script. Using `exec(open(...).read())` after registration ensures this ordering.

---

## Page Layout Adjustments for CJK

| Element | Adjustment |
|---------|-----------|
| Cover page title | Use `brand_name_cn` (Chinese name) as primary, English name as subtitle |
| Score gauge label | Replace "Excellent" with "优秀", "Good" with "良好", "Fair" with "一般", "Poor" with "较差" |
| Section headings | Use Chinese headings: "执行摘要" (Executive Summary), "得分概览" (Score Overview), "平台分析" (Platform Analysis), "关键发现" (Key Findings), "行动计划" (Action Plan) |
| Color palette | No change — the base palette works for CN clients |
| Table column widths | Widen by ~15% for Chinese text (CJK glyphs are wider per character) |
| Page size | Keep US Letter or switch to A4 if preferred in CN market — both are accepted |
| Confidential watermark | Use Chinese: "机密文件" or "保密" instead of "Confidential" |

---

## Score Interpretation Labels (CN)

| Score Range | English Label | Chinese Label |
|---|---|---|
| 80-100 | Excellent | 优秀 |
| 60-79 | Good | 良好 |
| 40-59 | Fair | 一般 |
| 0-39 | Poor | 较差 |

---

## Notes (CN)

- The base script at `scripts/generate_pdf_report.py` is **not modified** — all CN adaptations happen at invocation time via font registration and JSON data structure changes
- If `reportlab` does not have `TTFont` support, ensure `pip install reportlab[ttfont]` or check that `reportlab.pdfbase.ttfonts` is available
- Noto Sans SC covers all Chinese characters (Simplified), plus Latin, CJK symbols, and punctuation — it is the recommended single font for CN reports
- For Traditional Chinese (Hong Kong / Taiwan), use `NotoSansTC` or `NotoSansHK` instead
- The font files are **not committed to the repo** — the user must download them; the SKILL.md should link to [Google Noto Fonts](https://fonts.google.com/noto) for download instructions
- Test CJK rendering by generating a 1-page sample before running the full report
