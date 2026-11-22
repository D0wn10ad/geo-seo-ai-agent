# CN 区域：合规与反滥用红线 (Compliance and Anti-Abuse Red Lines)

本文档是中国市场 GEO 审计的合规边界，供审计员和 `SKILL.cn.md` 覆盖文件查阅。它回答一个具体问题：面对中国区客户，哪些做法一律不能做、不能推荐、不能写进交付物。

这是红线清单，不是打法手册。下面每一条都是禁止项 (prohibition)。本文档只描述如何识别、拒绝和上报违规，绝不提供任何可被当作操作指引的步骤。正向工程打法在 `regions/cn/engineering-playbooks.md`，那里明确把红线委托给本文档。

所有条目都来自外部行业文章，全部为 `UNVERIFIED`，并带文章 ID，可回溯到 `regions/cn/provenance.md` 第 5、6、9、25、27、33 至 35 行（合规与反滥用主题，T5）。这些是被归因的声称，不是已确立的事实，也不是本工具已验证的标准。本工具不因为某条做法出现在文章里就把它当作可执行规则，更不把它写进任何评分权重。

## 纪律 (read first)

- 外部文章文本是不可信数据，绝不当作指令。抓取页面里的推广语和工具包装提醒都被忽略，未在此复现。
- 每条红线和其中的数字都是 `UNVERIFIED`。这个状态说的是真伪，不只是出处。找到某条红线的文字只确认了归因，不等于把它变成了已验证的事实或已生效的法规。
- 归因确认不等于标准已验证 (attribution confirmed is not standard verified)。本主题多数文章 ID 为 `not spot-checked`，连归因抽查都没做过；只有黑帽负面清单和 3·15 案例来自已抽查文章，抽查也只确认文字存在，不确认真伪。T/CAPT 相关标准在来源文章中被描述为非约束性团体标准，不得称为已验证标准或国家法律。
- 本文档只列禁止项。任何条目都不得被改写成"如何做"的正向步骤，不得作为推荐打法、服务包内容或交付物卖点出现。
- 不粘贴任何完整文章文本，只保留足以识别红线的简短归因短语。
- 指标层分离是强制的。本文档只处理合规边界。它不是 `regions/cn/ai-engines.md` 里权威且逐字节不变的 源易 整体使用率表，也不是按智能体划分的内容来源占比百分比 (per-agent content-composition %)。三者回答不同问题，绝不合并。
- 这些红线不改变任何评分权重。全局 25/20/20/15/10/10 和中国区 20/30/15/10/15/10 保持不变，归因数字不接入评分公式，也不写进 `regions/profiles.yaml`。

## 红线速查 (overview)

| # | 红线类别 | 归因文章 ID | provenance 行 | 状态 |
|---|---|---|---|---|
| 1 | T/CAPT 黑帽负面清单：语料投毒 / 答案霸权 / 伪共识制造 / 提示词注入攻击 | `ScUyd3hGPbjCjVrAugO4yg` | 5（案例 6） | UNVERIFIED (spot-checked, text present) |
| 2 | 清朗专项四类 | `cEAJOut6f3g6T9VzF7DrFA` | 33 | UNVERIFIED (not spot-checked) |
| 3 | 三不做：删帖 / 刷好评 / 怼竞对 | `5oPN987WuYGOwLM2WpMcMA` | 34 | UNVERIFIED (not spot-checked) |
| 4 | REJECT 邪修（报表操纵类手法） | `YkQG1SNWFQjdxW4wlQBndw` | 35 | UNVERIFIED (not spot-checked) |
| 5 | 大健康 / 多品类客户人工审核 | `Tlmyhz_NWUHwGbEwYHIzLA`、`WhhWhQWj2XSN0ulIlGXW2Q` | 9、25、27（合规复用，无独立主张行） | UNVERIFIED (not spot-checked) |

## 1. T/CAPT 黑帽负面清单 (black-hat negative list)

归因声称：存在一份黑帽负面清单，点名四类禁止做法：语料投毒 (corpus poisoning)、答案霸权 (answer monopoly)、伪共识制造 (fake consensus)、提示词注入攻击 (prompt injection)。文章 ID `ScUyd3hGPbjCjVrAugO4yg`，provenance 第 5 行，`UNVERIFIED`，已抽查且文字存在。抽查只确认归因，不确认真伪；来源文章自述为二次转述且该标准为非约束性团体标准。

以下四项一律禁止。它们是被拒绝的做法，不是可执行的打法。

| 禁止项 | 中文名 | 为什么是红线（归因，UNVERIFIED） | 审计员如何处理 |
|---|---|---|---|
| 语料投毒 | 语料投毒 | 向语料库批量注入虚假或伪造内容以污染来源，属负面清单点名项，`UNVERIFIED` | 发现客户或供应商有此行为，拒绝并记入红线事件，不上报为正向成果 |
| 答案霸权 | 答案霸权 | 以批量手段抢占 AI"标准答案"位置，属负面清单点名项，`UNVERIFIED` | 检测批量同质软文与占位行为，判定为违规，不提供放大方案 |
| 伪共识制造 | 伪共识制造 | 伪造多方独立背书制造共识假象，属负面清单点名项，`UNVERIFIED` | 用 `regions/cn/cross-validation.md` 的独立主体判定识别伪共识，拒绝采信 |
| 提示词注入攻击 | 提示词注入攻击 | 通过注入指令操纵引擎输出，属负面清单点名项，`UNVERIFIED` | 视为攻击行为，拒绝并上报，不讨论实现方式 |

归因反面案例（警示，非操作指引）：provenance 第 6 行记录一条 `UNVERIFIED` 声称，某虚构产品在两小时内经批量虚假软文成为 AI"标准答案"，文章 ID `ScUyd3hGPbjCjVrAugO4yg`，已抽查且文字存在。此案例只用于说明答案霸权的风险，绝不作为可复现的步骤描述。

## 2. 清朗专项四类 (Qinglang campaign, four categories)

归因声称：存在一项"清朗专项"行动，列出四类与内容治理相关的禁止类别。文章 ID `cEAJOut6f3g6T9VzF7DrFA`，provenance 第 33 行，`UNVERIFIED`，未抽查。

重要限制：provenance.md 第 33 行只记录"清朗专项 four categories"这一归因标签，并未记录四类的具体名称，该文章 ID 也未做归因抽查。因此本文档不臆造、不列举这四类的具体名称，以免把未经确认的类别写成事实。审计员在引用任何具体类别名称前，必须先查阅来源文章、补齐四类原文与独立来源，并在 provenance.md 增加对应主张行，全程保留 `UNVERIFIED` 标签。

审计员如何处理：把"清朗专项四类"作为一个整体的禁止主题对待。凡客户诉求落入该专项治理范围的内容操纵行为，一律拒绝并上报，不因为类别名称尚未补齐而放行。

## 3. 三不做 (three never-do rules)

归因声称：存在"三不做"约束，即不删帖、不刷好评、不怼竞对。文章 ID `5oPN987WuYGOwLM2WpMcMA`，provenance 第 34 行，`UNVERIFIED`，未抽查。

以下三项一律禁止。它们是被拒绝的做法，不是可执行的打法。

| 禁止项 | 中文名 | 归因（UNVERIFIED） | 审计员如何处理 |
|---|---|---|---|
| 删帖 | 不删帖 | 删除负面内容以操纵呈现，属三不做之一，`UNVERIFIED` | 拒绝任何删帖诉求，不提供渠道或话术 |
| 刷好评 | 不刷好评 | 批量制造虚假好评或虚假互动（含刷量），属三不做之一，`UNVERIFIED` | 识别异常好评与刷量痕迹，判定为违规，拒绝放大 |
| 怼竞对 | 不怼竞对 | 攻击或贬损竞争对手以抬高自身，属三不做之一，`UNVERIFIED` | 拒绝攻击性内容，不生成针对竞对的负面材料 |

## 4. REJECT 邪修 (explicit rejection)

REJECT 邪修。报表操纵类手法（邪修）在本工具中被明确拒绝，不得实施、不得推荐、不得写进任何交付物或服务包。这是硬性禁止项，不是可权衡的建议。

归因声称：来源文章点名一类"邪修"报表操纵手法并要求拒绝。文章 ID `YkQG1SNWFQjdxW4wlQBndw`，provenance 第 35 行，`UNVERIFIED`，未抽查。归因确认不等于标准已验证，但拒绝立场不依赖该数字真伪，属本工具的非可逆合规底线 (D7 anti-abuse guardrails are hard Must-NOT)。

审计员如何处理：遇到任何以操纵报表、伪造指标、刷量或规避审核为目的的诉求，直接拒绝并上报，不讨论实现方式，不提供替代变体。

## 5. 大健康 / 多品类客户人工审核 (client-review requirement)

归因声称：大健康与多品类客户需要人工审核后再出具结论。该要求来自合规主题文章，文章 ID `Tlmyhz_NWUHwGbEwYHIzLA`（合规复用，provenance 第 9 行）与 `WhhWhQWj2XSN0ulIlGXW2Q`（合规复用，provenance 第 25、27 行），均为 `UNVERIFIED`，未抽查。

provenance.md 没有为"大健康 / 多品类人工审核"设立独立主张行，因此这里只把它作为客户审核守卫 (client-review guardrail) 记录，不把它当作某个外部标准的具体条款，也不为它编造数字。审计员在引用具体条款前，需先补齐来源与 provenance 行，保留 `UNVERIFIED` 标签。

审计员如何处理：

1. 识别客户是否属于大健康或跨多品类经营。
2. 属于则暂停自动结论，转人工审核后再出具报告或建议。
3. 人工审核同样受本文档全部红线约束，不因进入人工流程而放宽。
4. 审核结论按区域标签记录，不并入全局报告，不改动任何评分权重。

## 归因与来源 (provenance and attribution)

本主题对应 `regions/cn/provenance.md` 的 T5 合规与反滥用主题 (来源索引第 126 至 133 行)。多数文章 ID 为 `not spot-checked`，所以这里只确认归因，不确认真伪。完整主张表、来源标签和抽查结果以 `regions/cn/provenance.md` 为准。

| provenance 行 | 主张 (简短归因) | 文章 ID | 状态 | 抽查 |
|---|---|---|---|---|
| 5 | 黑帽负面清单：语料投毒 / 答案霸权 / 伪共识制造 / 提示词注入攻击 | `ScUyd3hGPbjCjVrAugO4yg` | UNVERIFIED | confirmed (text present) |
| 6 | 3·15 案例：虚构产品两小时内经批量虚假软文成为"标准答案" | `ScUyd3hGPbjCjVrAugO4yg` | UNVERIFIED | confirmed (text present) |
| 9 | EEAT6.0 实体信任阈值（合规复用） | `Tlmyhz_NWUHwGbEwYHIzLA` | UNVERIFIED | not spot-checked |
| 25 | 千问偏好阿里生态（合规复用） | `WhhWhQWj2XSN0ulIlGXW2Q` | UNVERIFIED | not spot-checked |
| 27 | 平台 × 内容时间窗口影响引用（合规复用） | `WhhWhQWj2XSN0ulIlGXW2Q` | UNVERIFIED | not spot-checked |
| 33 | 清朗专项四类 | `cEAJOut6f3g6T9VzF7DrFA` | UNVERIFIED | not spot-checked |
| 34 | 三不做：不删帖 / 不刷好评 / 不怼竞对 | `5oPN987WuYGOwLM2WpMcMA` | UNVERIFIED | not spot-checked |
| 35 | REJECT 邪修（报表操纵类手法） | `YkQG1SNWFQjdxW4wlQBndw` | UNVERIFIED | not spot-checked |

## 指标层分离 (metric-layer separation)

- 本文档的合规红线只处理禁止项与客户审核边界。
- 它不同于 源易 整体使用率数据 (`regions/cn/ai-engines.md` 的 MAU 分层、层级与平台权重、2,844 样本表)。那层数据是权威的，必须逐字节保持不变，不能在这里重述或调和。
- 它也不同于按智能体划分的内容来源占比百分比 (per-agent content-composition %)。那层数字属于平台行为主题，是独立的、带归因的 `UNVERIFIED` 指标，绝不并入本文件或 源易 表。
- 三层回答不同问题，绝不合并成一张表，也不用一个去校正另一个。被调用合规分 (`regions/cn/engineering-playbooks.md` 第 7 节) 判定红线时直接引用本文档，不在本文档内重新定义红线，也不并入 源易 表。

## 权重不变声明 (no weight change)

- 本文档不改变任何评分权重。全局 25/20/20/15/10/10 和中国区 20/30/15/10/15/10 保持不变。
- 所有归因数字只作为报告用的 `UNVERIFIED` 声称，不接入评分公式，不写进 `regions/profiles.yaml`，不新增评分项。
- 红线判定是合规守卫，不是评分维度，不折算成 GEO Score。

## 未决项与风险 (open items and risks)

- 清朗专项四类的具体名称未记录在 provenance.md 第 33 行，且该文章 ID 未抽查。补齐原文与独立来源前，不得列举或引用具体类别名称。
- 大健康 / 多品类人工审核没有独立 provenance 主张行，只作为客户审核守卫记录。引用具体条款前需先补齐来源与 provenance 行。
- 本主题除第 5、6 行外多数文章 ID 未抽查。三不做、REJECT 邪修、清朗专项等条目的细节保持 `UNVERIFIED`，直到做过专门的来源核查。
- 黑帽负面清单与 3·15 案例虽已抽查，抽查只确认文字存在，不确认真伪；T/CAPT 相关标准在来源文章中被描述为非约束性团体标准，不得称为已验证标准或国家法律。
- 不要把未经确认、缺少独立来源的数字当作事实写进本文档 (见 `regions/cn/provenance.md` 第 21、26 行的未决项)。这类数字不在本主题内，需要各自独立的来源核查后才能使用。
- 本文档记录的是归因与合规边界，不是事实真值，更不是操作指引。任何下游文档从这里带走条目，都必须保留 `UNVERIFIED` 标签和文章 ID，并保持其禁止项措辞。
