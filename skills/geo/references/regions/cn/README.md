# CN 区域知识库索引 (China Region Knowledge Index)

这是中国市场 GEO 审计的知识文档导航页，供审计员和 `SKILL.cn.md` 覆盖文件查阅。它只负责指路：告诉你每份文档解决什么问题、什么时候该打开它。具体结论请进入对应文档阅读，本页不复述任何文档正文。

## 如何使用本索引 (how to use this index)

1. 先读 `provenance.md`。任何外部数字、阈值或市场声称，都要先在这里查它的文章 ID、来源标签和 `UNVERIFIED` 状态。
2. 判断来源可信度时打开 `source-tiering.md`，用统一的 `CN-T1` 至 `CN-T4` 分层，不要直接引用任何外部方案的字母标签。
3. 判断一条实体主张是否被印证，打开 `cross-validation.md`。
4. 想知道某个智能体从哪些来源取内容，打开 `platform-behavior.md`。注意那里的百分比是内容来源占比，不是市场占有率。
5. 要落地改造动作，打开 `engineering-playbooks.md`；遇到合规边界，打开 `compliance-anti-abuse.md`，红线只列禁止项，不可当作操作指引。
6. 要报告补充观测指标或了解外部研究方法背景，打开 `kpi-and-method.md`。
7. 需要权威的整体使用率、平台权重和 schema 默认值时，回到下面三份核心区域数据文档。

## 核心区域数据 (authoritative base data)

这三份是既有的中国区基础数据，属于权威层，保持逐字节不变。

| 文档 | 覆盖内容 |
|---|---|
| [ai-engines.md](ai-engines.md) | 中国区 6 个 AI 引擎的评估标准、QuestMobile MAU 分层权重表，以及各引擎的取源偏好。这是权威的整体使用率层。 |
| [platforms.md](platforms.md) | 中国区 6 个品牌平台（百度百科、知乎等）的验证方法、评分标准和权重，用于 AI 实体识别。 |
| [schema.md](schema.md) | 中国区结构化数据默认值，含 Organization 模板、百度 schema 扩展和 sameAs 平台清单。 |

## 主题知识文档 (themed knowledge docs)

这七份是本次新增的主题文档。除工具内部派生的指标外，其中的外部数字全部为 `UNVERIFIED`，只作归因报告，不作事实使用。

| 文档 | 覆盖内容 |
|---|---|
| [provenance.md](provenance.md) | 主张到来源的权威台账：45 条带归因的声称，每条标注文章 ID、来源标签和抽查结果，附 28 个来源的索引。查任何数字的出处都从这里开始。 |
| [source-tiering.md](source-tiering.md) | 统一的来源可信度模型：`CN-T1` 至 `CN-T4` 四层加两个横切门，把五套互相冲突的外部分层方案映射到同一套内部标签。 |
| [cross-validation.md](cross-validation.md) | 多源交叉验证的五条规则：独立主体数、单一来源上限、来源的定义、信息统一性、品牌事实文件。用于判断一条实体主张是否被独立来源印证。 |
| [platform-behavior.md](platform-behavior.md) | 豆包、元宝、DeepSeek、千问各自的平台与算法行为，以及按智能体划分的内容来源占比。这里的百分比是内容来源构成，不是整体使用率。 |
| [engineering-playbooks.md](engineering-playbooks.md) | 七套可落地的工程打法：三区分治、query-frame 映射、问答专页改造、问题知识库、30/60/90 天验收、三层测量、被调用合规分。 |
| [compliance-anti-abuse.md](compliance-anti-abuse.md) | 合规红线清单：黑帽负面清单、清朗专项、三不做、REJECT 邪修、客户人工审核。只描述如何识别、拒绝和上报违规，不提供任何操作指引。 |
| [kpi-and-method.md](kpi-and-method.md) | 第一部分为六个只报告的补充 CN KPI，第二部分为 agentic_geo 方法说明（仅文档参考，不移植任何机器学习代码）。 |

## 指标层分离提醒 (metric-layer separation)

三层数据回答不同问题，绝不合并，也绝不用一层去校正另一层：

- 源易整体使用率表（见 `ai-engines.md`）：衡量各引擎在中国市场的整体使用情况，权威且逐字节不变，不在主题文档中重述。
- 按智能体划分的内容来源占比（见 `platform-behavior.md`）：衡量每个智能体从哪些来源取内容，是独立的指标层，全部 `UNVERIFIED`。
- 来源可信度分层（见 `source-tiering.md`）：衡量某类来源有多可信，是第三层，与上面两层分开。

补充 KPI 和 agentic_geo 方法概念（见 `kpi-and-method.md`）既不属于以上任何一层，也不接入评分公式。

## 权重不变声明 (no weight change)

本索引及全部主题文档都不改变任何评分权重。全局 25/20/20/15/10/10 和中国区 20/30/15/10/15/10 保持不变。所有归因数字只作报告，不接入 GEO Score 公式，不写进 `regions/profiles.yaml`，也不新增任何评分维度或权重键。
