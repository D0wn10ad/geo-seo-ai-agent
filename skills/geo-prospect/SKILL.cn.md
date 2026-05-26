---
name: geo-prospect-cn
description: CN-region CRM overrides — Chinese labels, RMB deal values, CN pipeline stages
version: 1.0.0
region: cn
parent: geo-prospect
---

# GEO Prospect Manager — China Market Overrides

**Load this file alongside `SKILL.md` when REGION is `cn`.**
Apply the following UI label and content overrides to the base prospect workflow.

---

## Pipeline Stage Labels (CN)

| Base English | Chinese Label | Status Value |
|---|---|---|
| Lead | 潜在客户 | `lead` |
| Qualified | 已确认 | `qualified` |
| Proposal Sent | 已提案 | `proposal` |
| Won | 已成交 | `won` |
| Lost | 已流失 | `lost` |

All commands output Chinese labels instead of English. The underlying JSON status values remain the same (`lead`, `qualified`, `proposal`, `won`, `lost`).

---

## Field Label Overrides

When rendering prospect details or table headers, use these CN field labels:

| Base English | Chinese Label |
|---|---|
| Company | 公司名称 |
| Domain | 网址 |
| Status | 状态 |
| Region | 地区 |
| GEO Score | GEO评分 |
| Value | 合同金额 |
| Monthly Value | 月费 |
| Contact Name | 联系人 |
| Contact Email | 联系邮箱 |
| Industry | 行业 |
| Country | 国家 |
| Notes | 备注 |
| Created At | 创建时间 |
| Updated At | 更新时间 |
| Contract Start | 合同开始 |
| Contract Months | 合同期限(月) |
| Pipeline | 销售管道 |
| Revenue Forecast | 收入预测 |
| Active Clients | 活跃客户 |
| Committed MRR | 已确认月经常性收入 |

---

## Currency

All monetary values in RMB (¥):
- Display as `¥12,500` instead of `€12,500`
- Pipeline value computation uses ¥, not EUR
- When creating prospects with monthly value estimates, ask in RMB (`月费预估 (¥)`)

---

## CN Region Pipeline View

### `/geo prospect list cn`

Override to filter prospects where `region == "CN"` and render with Chinese labels:

```
GEO销售管道 — 2026年3月
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
编号       网址                 公司名称          状态     GEO评分  金额
───────  ────────────────────  ─────────────  ────────  ───────  ──────
PRO-001  example.cn            示例公司         已成交    72/100   ¥12,000
PRO-005  baijing.cn            佰竞科技         已确认    38/100   ¥8,500
PRO-008  shangmao.cn           尚茂科技         潜在客户   —        —

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
管道: 1 潜在客户 | 1 已确认 | 0 已提案 | 1 已成交 | 0 已流失
已确认月经常性收入: ¥12,000 | 管道价值: ¥8,500
```

### `/geo prospect pipeline cn`

Revenue-focused pipeline summary filtered to CN region:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEO销售管道汇总 — 中国区 — 2026年3月
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

阶段          数量   预期月费       备注
────────────  ────  ────────────  ─────────────────────
潜在客户        2     ¥16,000/mo   新发现
已确认          1     ¥5,500/mo    准备提案
已提案          1     ¥8,000/mo    等待签约
已成交          3     ¥48,500/mo   活跃客户(月经常性收入)
已流失          2     —            预算冻结/不再适用

已确认月经常性收入:         ¥48,500
管道(已确认+):             ¥13,500
总潜力:                   ¥62,000/mo → ¥744,000/年

下一步行动:
→ PRO-002 (acme.cn): 发送提案 — GEO评分 38/100 (转化潜力大)
→ PRO-007 (shop.cn): 跟进 — 提案已发送8天
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Chinese Notes Support

### `/geo prospect note <id-or-domain> "<text>"`

When adding notes to a prospect record, the text may contain Chinese characters. Ensure:

1. JSON storage handles UTF-8 correctly (Python `json.dumps(ensure_ascii=False)`)
2. Terminal output preserves Chinese characters
3. Notes with mixed Chinese/English are fully supported

### Auto-note Localization

When using `/geo prospect status` or other auto-note commands, use Chinese for auto-generated notes:

| Action | Chinese Auto-note |
|---|---|
| Status change to `qualified` | "状态已更改为：已确认" |
| Status change to `proposal` | "状态已更改为：已提案" |
| Status change to `won` | "状态已更改为：已成交" |
| Status change to `lost` | "状态已更改为：已流失" — 原因: <reason> |
| After quick audit | "快速检测完成。GEO评分: XX/100。" |
| After full audit | "完整检测完成。GEO评分: XX/100。检测报告已保存。" |

---

## Prospect Creation Overrides (CN)

### `/geo prospect new <domain>`

When `--region cn` is active or CN is auto-detected:

1. Override region detection — set region to `CN` without asking
2. Ask for these fields with Chinese prompts:
   - `联系人 (Contact Name):` (optional)
   - `联系邮箱 (Contact Email):`
   - `月费预估 (¥) (Monthly Value Estimate):` (optional)
   - Confirm region is `CN`
3. Skip multi-language detection dialog — CN-only mode
4. Store record with `region: "CN"` in JSON
5. Suggest next step in Chinese: `运行 /geo prospect audit <domain> 为此客户评分`

---

## Data File Considerations

- The same `~/.geo-prospects/prospects.json` file is shared across all regions
- Prospects with `region: "CN"` co-exist with other regions in the same JSON
- All CN overrides are UI/display-layer only — the underlying data model is unchanged
- No separate CN database file is needed

---

## Output

- All commands print Chinese-language confirmation + relevant status
- Numeric values (scores, counts) remain in Arabic numerals — only labels and currency change
- JSON database is unchanged from the base skill
