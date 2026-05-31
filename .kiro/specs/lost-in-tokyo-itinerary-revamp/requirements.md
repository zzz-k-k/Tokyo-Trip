# Requirements Document

## Introduction

本 spec 是对现有"东京旅行 GitBook"（出行日期 2026-06-03 周三 ~ 2026-06-09 周二，共 7 天）的整体重构与扩展。原项目已交付 7 个每日计划文档（`day-1-2026-06-03.md` ~ `day-7-2026-06-09.md`）+ `index.md`/`SUMMARY.md`/`README.md`/`book.json`/`places.json`/`tst-segments.json`/`lodging-luggage.json`/`build_places.py`，并通过 GitHub Actions（`.github/workflows/deploy-gitbook.yml`）部署到 GitHub Pages。

本次改造聚焦 8 项变更：① 站点更名为「锅巴的奇妙冒险之迷失东京」；② 抽离每日规划文档中的"介绍文本"为独立 .md 文档，每日规划文档只保留行程动线；③ 修正"区域"与"子地点"的标题层级；④ 把"江户东京博物馆"纳入行程并完成开放性核实（已联网核实截至 2026-03-31 已重新开放，无须替代方案）；⑤ 把"上野公园"纳入行程（如已存在则无变更）；⑥ 把"六本木 21_21 Design Sight"纳入行程并体现 2026-06-03 ~ 2026-06-09 期间的企画展信息（已联网核实「Soup as Life」企画展 2026-03-27 起开展）；⑦ 核查并纳入「すし銚子丸 6 月店庆感谢祭」（含金枪鱼解体秀场次 / 价格优惠）；⑧ 撤销「将小宫商店购伞计划提前到东京第一天」这一主观时间决定，按「不动时间锁死活动 + 整体交通费最小」客观重排小宫商店及全部剩余子地点的归属日（小宫商店仍保留为子地点纳入行程）。

最终交付物保持与现项目一致：7 个每日计划 markdown 文档 + 抽离的独立介绍文档若干 + 更新后的 `SUMMARY.md`/`README.md`/`index.md`/`book.json`/`build_places.py`/`places.json`/`tst-segments.json`/`lodging-luggage.json`，整站可通过 `npm run build` 渲染为 HonKit 静态站点并通过既有 GitHub Actions 工作流发布到 GitHub Pages。

## Glossary

- **GitBook 站点（GitBook_Site）**：本仓库根目录下由 HonKit（npm `honkit` ≥ 5.x）构建的多页 markdown 文档站点；构建产物输出到 `_book/`，并由 `.github/workflows/deploy-gitbook.yml` 自动部署到 GitHub Pages。
- **每日计划文档（Day_Plan_Document）**：根目录下 `day-{N}-{YYYY-MM-DD}.md`（N ∈ 1..7）文件，描述当天的行程动线（时间、交通、地点、移动顺序、关键提示）。
- **介绍文档（Introduction_Document）**：抽离自 Day_Plan_Document 的、专讲单个地点（或单个紧密相关地点群）的"历史与背景 / 看点 / 类型 / 票务 / 推荐玩法 / 注意事项"等知识性内容的独立 markdown 文件，存放于根目录或专用子目录中（具体路径在 design 阶段决定）。
- **介绍文档分组（Introduction_Group）**：`SUMMARY.md` 中用于聚合 Introduction_Document 的章节（建议命名为「景点介绍」或「介绍文档」，最终命名在 design 阶段决定）。
- **区域（Major_Area）**：每日动线上一级地理单元，例如「港未来」「丸之内」「下北泽」「赤坂 / 永田町」「浅草」；与 design.md 中已定义的 23 个 major_area 枚举对齐。
- **子地点（Sub_Place）**：从属于某个区域的具体打卡点（餐厅、神社、博物馆、商店等）；从 places.json 的 `included` 数组取值。
- **时间锁死活动（Time_Locked_Activity）**：当日内必须在某个具体时刻或时段完成的活动，例如已预订餐厅、定时演出（歌舞伎座单幕席 / SSFF & ASIA 短片节场次 / 山王祭 09:00 神事）、闭馆时间、新干线 / 飞机时刻、酒店入住时刻 / 退房时刻。
- **行程规划器（Itinerary_Planner）**：本 spec 所交付的、把候选地点分配到 7 天并按"时间锁死活动 + 交通费最小"约束重排的规划制品（包括 7 个每日计划文档 + 抽离介绍文档 + 更新后的数据 / 元数据文件）。
- **官方核实状态（Official_Verification_Status）**：针对外部活动 / 展览 / 营业状态的核实结论，取值为「确认开放 / 在期内」「确认未开放 / 不在期内」「无法核实 / 待用户实地确认」三种之一；核实时间戳与信息来源 URL 必须随附。
- **行程交通费（Itinerary_Transit_Cost）**：7 天内所有"段间移动 + 跨日衔接"票价之和（JPY），单位为日元，**按结算场景（Cost_Scenario）独立计算**——同一份 7 日行程在不同票务结算方式下产出不同的 Itinerary_Transit_Cost 数值；design.md 不再做"重排前 vs 重排后"的对比，仅做"通票场景 vs Suica 直付场景"的并列对比（详见 Cost_Scenario / Cost_Scenario_Comparison 定义）。
- **成本场景（Cost_Scenario）**：针对同一份 7 日行程的不同票务结算方式（如全程 Suica 直付 / 应用 Tokyo Subway Ticket 72 小时券 / 应用 TST + 都营一日券 / 东京 Metro 24h 券 等组合），每个场景产出独立的 7 日合计 JPY 与每日分项 JPY；本 spec 至少覆盖 2 个场景——场景 A（全程 Suica 直付，不持任何通票，所有段按官方票价直付）+ 场景 B（应用本次行程实际使用的所有通票组合，初版至少含 Tokyo Subway Ticket 72 小时券，后续可由 design 阶段决定是否纳入 都营一日券 / 东京 Metro 24h 券 等其他通票），最多场景数由 design 阶段按实际通票数量决定。
- **成本场景对比（Cost_Scenario_Comparison）**：design.md 中对至少 2 个 Cost_Scenario 的并列对比表（行 = day、列 = 场景、单元格 = 该日该场景下的 JPY 合计 + 关键段票价拆分；末行为 7 日合计），每个场景必须列出该场景所选通票名称 + 通票本身价格（计入合计）+ 7 日合计 JPY + 每日分项 JPY；当任意场景的总交通费为 ¥0 时（如 TST 全覆盖 + 全步行），仍须在表格中列出 ¥0 + 该场景所用通票名称（即使通票为 None / Suica 直付），不允许整行省略。
- **江户东京博物馆（Edo_Tokyo_Museum）**：墨田区横网 1-4-1 的市立博物馆，2022 年起大规模改修长期闭馆，**2026-03-31 重新开馆**（联网核实，photoguide.jp 与 NHK 报道均确认）。
- **江戸東京たてもの園（Edo_Tokyo_Open_Air_Architectural_Museum）**：小金井市的江户东京博物馆分馆「江戸東京たてもの園」，独立运营、长期开放；本 spec 将其作为 Edo_Tokyo_Museum 的备选替代场所之一（仅在 Edo_Tokyo_Museum 实际不开放时启用）。
- **21_21 Design Sight**：港区赤坂 9-7-6 东京 Midtown 内的设计美术馆；本 spec 涉及的 2026-06-03 ~ 2026-06-09 期间企画展为「Soup as Life」（已联网核实，2026-03-27 起，2026-08 之前持续在展）。
- **すし銚子丸店庆感谢祭（Choshimaru_Anniversary_Fair）**：すし銚子丸 6 月店庆活动；本次行程是否纳入需在 design 阶段基于官方核实结果（含日期 / 场次门店 / 解体秀时间 / 优惠内容）决策。
- **小宫商店日次再分配（Komiya_Day_Reassignment）**：原 Day 3 文档中安排的「都营浅草线 → 东日本桥 → 小伝马町 小宫商店购伞」前置段是用户的主观时间决定；本次按用户决策**撤销该主观时间决定**（不再绑定 Day 1 / Day 3 上午前置段），但**保留小宫商店作为子地点仍纳入本次 7 日行程**，其 `assigned_day` 由 design 阶段以「最小化整体交通费 Itinerary_Transit_Cost」为目标函数客观决定（约束：Time_Locked_Activity 在窗口内 + 当日 Major_Area 单调推进 + TST 失效时刻不变 + 与小伝马町地理顺路的 day 优先）。
- **places.json**：由 `build_places.py` 从 `Favorite places.csv` + 用户后续修订指示构建出的地点元数据 JSON，结构由 `build_places.py` 维护；本次将新增地点纳入 PLACE_PLAN 并重新构建。
- **tst-segments.json**：每段交通的 TST 覆盖与票价估算 JSON，由 design 阶段维护；本次重排后需同步更新。
- **PBT（Property-Based_Testing）**：性质测试；本 spec 的 PBT 焦点为 `build_places.py` 的纯函数式数据处理 + 行程一致性校验（地点存在性 / 时间窗不重叠 / 时间锁死活动落在营业时间内）。

## Requirements

### Requirement 1: 站点更名为「锅巴的奇妙冒险之迷失东京」

**User Story:** 作为站点维护者，我希望整个 GitBook 站点统一更名为「锅巴的奇妙冒险之迷失东京」，所有出现旧名 "Tokyo Trip 2026" 或类似硬编码标题的地方都被替换，避免新旧标题在站点不同位置混杂出现。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 将 `book.json` 的 `title` 字段值替换为「锅巴的奇妙冒险之迷失东京」；本 AC 与 Requirement 1.2 ~ 1.5 之间为独立更新关系，每个文件可独立完成更名而不必与其他文件原子化捆绑（用户已确认允许独立更新）。
2. THE Itinerary_Planner SHALL 将 `README.md` 的顶部一级标题（首个 `# ` 行）替换为「锅巴的奇妙冒险之迷失东京 GitBook」。
3. THE Itinerary_Planner SHALL 将 `SUMMARY.md` 的顶部一级标题（首个 `# ` 行）替换为「锅巴的奇妙冒险之迷失东京」。
4. THE Itinerary_Planner SHALL 将 `index.md` 的顶部一级标题（首个 `# ` 行）替换为「锅巴的奇妙冒险之迷失东京 — 7 日行程总览（2026-06-03 ~ 2026-06-09）」。
5. WHEN `build_places.py` 文件中存在硬编码的旧标题字符串（如 "Tokyo Trip 2026" 或 "japan-7day-itinerary"）时，THE Itinerary_Planner SHALL 将其更新为「锅巴的奇妙冒险之迷失东京」对应的标识符或保留为内部 `spec` 路径不动（具体处理方式在 design 阶段明确）；**当 `build_places.py` 中不含旧硬编码字符串时，本 AC 仍然适用 —— Itinerary_Planner SHALL 在 design 阶段执行一次"verifying identifiers"检查，确认文件内的所有当前标识符（如 spec 路径、PLACE_PLAN 注释中的 spec 名）已与「锅巴的奇妙冒险之迷失东京」在概念上对应（即使无字符串需修改，本检查动作 SHALL 仍被执行并将结论写入 design.md）**。
6. THE Itinerary_Planner SHALL 在站点根目录通过 `grep` 验证：除"行程介绍 / 历史背景"中作为引用上下文出现的 "Tokyo Trip 2026" 字符串外，没有任何文档头部标题或菜单项仍使用旧名。
7. WHEN `npm run build` 在更名后执行时，THE Itinerary_Planner SHALL 保证 HonKit 构建无错误产出，`_book/index.html` 的 `<title>` 标签值反映新标题。

### Requirement 2: 抽离每日规划中的"介绍文本"为独立介绍文档

**User Story:** 作为读者，我希望每日规划文档（`day-N.md`）只保留"动线信息"（时间、交通、地点、移动顺序、关键提示），把"地点介绍 / 历史与背景 / 看点 / 类型 / 票务详情"等长篇知识性内容抽离到独立的介绍文档中，规划文档读起来短而清晰，介绍文档可作百科式独立阅读。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 为 7 个每日规划文档（`day-1-2026-06-03.md` ~ `day-7-2026-06-09.md`）中所有当前以"### {地点中文名}"层级展开的"地点档案（Place_Profile）"段落抽离为独立的 Introduction_Document。
2. THE Itinerary_Planner SHALL 为每个被抽离的地点档案生成一个独立的 markdown 文件，文件名严格采用 kebab-case 命名规范（仅小写字母 + 数字 + 连字符 `-`，不允许下划线 / 大写 / 空格 / 全角字符；建议格式：`intro-{romaji-id}.md`，最终命名规则在 design 阶段决定）。
3. WHEN 一个地点档案被抽离后，THE Day_Plan_Document SHALL 在原地点出现位置改用一行简短的"动线提示 + 链接"代替（建议格式：`- HH:MM｜{地点中文名}（{所属区域}）→ [详细介绍](intro-xxx.md)`，具体格式在 design 阶段决定）。
4. THE Day_Plan_Document SHALL 保留以下"动线信息"内容：① 当日主题简述；② 主要区域序列；③ 每个地点的到达时刻 / 离开时刻；④ 段间交通方式（线路 + 票价 + TST 标记）；⑤ 关键提示（行李策略 / 时间锁死活动入场流程 / 雨天替代）；⑥ 文档头硬约束区块；⑦ 文档尾"当晚回程"或"次日提醒"。
5. THE Day_Plan_Document SHALL 不再包含完整的"历史与背景 ≥ 150 字"段落、不再包含详尽的"看点列表"、不再包含"建筑师 + 建成年份 + 设计要点"等深度字段；这些内容全部移入对应的 Introduction_Document。
6. THE Introduction_Document SHALL 至少包含 design.md `Place_Profile` 模板中定义的所有字段（见 design.md「类别专属字段」与 requirements.md §13 的 12 个必含字段）。
7. THE Itinerary_Planner SHALL 在 `SUMMARY.md` 中新增一个 Introduction_Group 章节（建议命名「景点介绍」或「介绍文档」，最终在 design 阶段决定），按"区域 → 子地点"层级组织所有 Introduction_Document 的链接。
8. WHERE 同一个地点在两个或多个 Day_Plan_Document 中被引用（例如某个区域横跨两天），THE Itinerary_Planner SHALL 仅生成一份 Introduction_Document 并在多个每日文档中复用同一链接。
9. IF 某个地点档案抽离后，原 Day_Plan_Document 中关于该地点的"动线必需"信息（开闭门时间、最近车站、票价数字、入场口流程）也被一并移除，THEN THE Itinerary_Planner SHALL 在 Day_Plan_Document 的对应动线行中保留这些"动线必需"字段的精简版本（只保留时刻 / 站名 / 票价 / 入场口），不重复展开背景介绍；本 AC 与下文 Requirement 2.11 共同保证 Day_Plan_Document 始终包含完整的 Navigation_Essentials，即"读者仅看 Day_Plan_Document 即可完成当日导航"。即便 Place_Profile 抽离过程因其他原因（如脚本失败 / 数据缺失）部分失败，**交通方式（线路 / 票价）+ 入场口 / 检票流程关键步骤**这两类信息 SHALL 始终被保留在 Day_Plan_Document 的动线行内，不允许丢失（最近车站名 / 步行分钟数可在极端情况下临时缺失但需在 design.md 中标注"待补"）。
10. WHEN HonKit 构建时，THE Itinerary_Planner SHALL 保证所有从 Day_Plan_Document 链接到 Introduction_Document 的相对路径都能解析成功，构建无 broken-link 警告。

11. THE Day_Plan_Document SHALL 始终保留以下"导航必需信息（Navigation_Essentials）"，即便对应内容也存在于被抽离的 Introduction_Document 中也不允许从 Day_Plan_Document 中移除：① 每个子地点的最近车站名 + 出口编号 + 步行分钟数；② 每个子地点的当日访问开始时刻 / 结束时刻（HH:MM）；③ 每段交通的线路名 + 票价 + TST 标记；④ 时间锁死活动的入场口 / 检票流程关键步骤（如歌舞伎座 4 楼単幕席专用入口、东京巨蛋检票口编号、SSFF & ASIA HALL 入场口）；⑤ 当日所属区域（Major_Area）名称（用于读者快速定位）。这五项构成"读者仅看 Day_Plan_Document 即可完成当日导航"的最小集合。

### Requirement 3: 修正每日规划中"区域"与"子地点"的标题层级

**User Story:** 作为读者，我希望每日规划文档的标题层级反映"区域 → 子地点"的从属关系：区域是上一级标题（`## `），子地点是下一级标题（`### `）；目前部分文档把同一区域内的多个子地点设置成了与区域同级的 `## ` 标题，导致目录结构错乱。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 审查 7 个 Day_Plan_Document（`day-1-2026-06-03.md` ~ `day-7-2026-06-09.md`），识别所有"子地点（Sub_Place）"被错误使用 `## ` 二级标题的位置。
2. THE Itinerary_Planner SHALL 将每日规划文档中的"区域"层级统一使用 `## ` 二级标题，**且同时满足以下两点**：① 标题层级精确为 `## `（不允许 `# ` 或 `### `）；② 标题文本格式严格采用 `## 子区域 N：{区域中文名}（{Major_Area_Romaji}）` 模式（N 从 1 起递增、`：` 与 `（）` 必须为全角、Romaji 取自 design.md 中已定义的 23 个 major_area 枚举对应表）。
3. THE Itinerary_Planner SHALL 将每日规划文档中的"子地点"层级统一使用 `### ` 三级标题，**且同时满足以下两点**：① 标题层级精确为 `### `（不允许 `## ` 或 `#### `）；② 标题文本格式严格采用 `### {地点中文名}（{日文名} / {Romaji}）` 模式（中文名为优先显示文字、`（` 为全角、`/` 前后各一个半角空格，日文名 + Romaji 取自 places.json 的 `title_jp` + `title_romaji` 字段）。
4. THE Itinerary_Planner SHALL 保证每日规划文档的标题层级正确性仅基于"`## ` 仅用于区域 + `### ` 仅用于子地点 + 不出现层级跳跃（如 `# ` 直接到 `### `）"三条规则判定，不强制要求每个 `### ` 子地点必须紧邻其上的 `## ` 区域之下；即"孤儿子地点"（无所属区域的 `### ` 标题）允许存在但应在 design 阶段评估并尽量避免（在 Requirement 3.5 的跨区域归属修正中处理）。
5. WHERE 一个地点跨越两个区域（例如沿江之电从七里滨到镰仓高校前的两站），THE Itinerary_Planner SHALL 把它分配到两个区域之中的主区域（在 design 阶段决定主区域归属），不允许重复出现在两个 `## ` 区域下；**该跨区域归属修正的执行顺序应在 Requirement 3.1 ~ 3.4 的基本标题层级修正全部完成之后**。
6. WHEN 修正层级后，THE Itinerary_Planner SHALL 保证 HonKit 渲染的目录树（`_book/{day-N}.html` 内嵌的 `nav` 或 `gitbook-plugin-toc`）正确反映"区域 → 子地点"两级嵌套，无层级跳跃（如 `# ` 直接到 `### `）。

### Requirement 4: 纳入「江户东京博物馆」并完成开放性核实

**User Story:** 作为旅行者，我希望把江户东京博物馆纳入行程；考虑到该馆 2022 年起长期改修，需要先核实 2026-06-03 ~ 2026-06-09 期间的开放状态，若仍未重开则提供「江戸東京たてもの園（小金井）」作为替代方案。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 在 design 阶段开始前完成江户东京博物馆的 Official_Verification_Status，核实结论必须含时间戳与信息来源 URL（例如官方公告页 / 报道页）。
2. THE Itinerary_Planner SHALL 接受以下核实结果作为依据：江户东京博物馆已于 **2026-03-31** 完成 4 年大规模改修后重新开馆（来源：[photoguide.jp 2026-04 报道](https://photoguide.jp/log/2026/04/edo-tokyo-museum-reopened-permanent-exhibition/) + [TOKYO MX「江戸東京博物館」リニューアルオープン报道](https://news.yahoo.co.jp/articles/f91867c4705146b91054128798bc6044db8d3e28) + [edo-tokyo-museum.or.jp 重开记念豊臣兄弟特别展告知](http://www.edo-tokyo-museum.or.jp/kr/news/toyotomi2026/)）；**因博物馆重开日（2026-03-31）严格早于本次行程开始日（2026-06-03），即满足"重开日 < 行程开始日"判定，故 2026-06-03 ~ 2026-06-09 期间确认开放**，无需在期内逐日核实。

3. THE Itinerary_Planner SHALL 把"江户东京博物馆"作为子地点纳入某一日的行程，且 `assigned_day` 必须严格落在 {1, 2, 3, 4, 5, 6, 7} 内（不允许超出本次 7 日行程范围；地理上推荐 Day 7 两国 / 押上段，因博物馆地址为墨田区横网 1-4-1，距 COGO RYOGOKU 步行约 8 分钟；最终归属日由 design 阶段按"时间锁死活动 + 交通费最小"约束决定）。
4. IF 在 design 或 task 阶段重新核实时发现博物馆因临时设施 / 节庆 / 突发原因在 2026-06-03 ~ 2026-06-09 内闭馆，THEN THE Itinerary_Planner SHALL 启用替代方案：把「江戸東京たてもの園（小金井）」作为子地点纳入行程，并在 Day_Plan_Document 中显式说明替换原因 + 替代地点的开放时间 + 交通方式；**此时 Introduction_Document 与 places.json 的对应条目 SHALL 仅为实际进入行程的场馆生成 / 维护**——即启用替代方案时仅生成「江戸東京たてもの園」的 Introduction_Document 与 places.json 条目，不为已被替换出行程的「江户东京博物馆」生成或保留对应条目。
5. THE Itinerary_Planner SHALL 为江户东京博物馆生成 Introduction_Document，至少包含：开闭门时间（含定休日）、票价、最近车站、改修后的常设展更新点（如 2026 年战争证言映像新展）、与两国国技馆 / COGO RYOGOKU / 江戸蕎麦 ほそ川 等周边地点的步行联动关系。

5a. IF Introduction_Document 因系统错误 / 数据缺失等原因生成失败，THEN THE Itinerary_Planner SHALL 仍允许「江户东京博物馆」作为子地点保留在行程中（places.json + Day_Plan_Document 动线行 + SUMMARY.md 链接占位均不撤回），并在 design.md 与 tasks.md 中记录"Introduction_Document 待补"作为未完成项，由用户后续单独处理；不允许因 Introduction_Document 生成失败而把博物馆从行程中移除。
6. THE Itinerary_Planner SHALL 在 places.json 的 `included` 数组中新增对应条目，由 `build_places.py` 的 `PLACE_PLAN` 字典管理 `assigned_day` / `major_area` / `sub_area` / `type` 字段。

### Requirement 5: 纳入「上野公园」（如已存在则忽略）

**User Story:** 作为旅行者，我希望确认上野公园已纳入行程；如已存在则不做改动，如不存在则补充进 Day 3 上野段。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 检查 `day-1-2026-06-03.md` ~ `day-7-2026-06-09.md` 7 个文档与 `places.json` 的 `included` 数组，验证是否已存在以「上野公园 / Ueno Park / 上野恩賜公園」为标识的子地点。
2. WHEN 检查结果为"已存在"（places.json 中 `Ueno Park` 条目已分配到 Day 3、Major_Area 为「东京—上野 / 本乡 / 东大」）时，THE Itinerary_Planner SHALL 不做任何新增动作，仅在本次重构中确认其继续被纳入；同时在 design 阶段决定 Day 3 重排后该子地点的新时刻 / 新顺序。
3. IF 检查结果为"不存在"，THEN THE Itinerary_Planner SHALL 把「上野公园」作为子地点新增到 Day 3 的「东京—上野 / 本乡 / 东大」区域内；**仅在该新增地点的实际添加（Day_Plan_Document 动线行写入 + SUMMARY.md 链接 + Introduction_Document 创建均成功）完成之后**，再按需更新 `places.json` 与 `build_places.py` 的 `PLACE_PLAN`；如新增地点添加在任一步失败，则不允许部分更新 `places.json` / `build_places.py`，必须回滚已完成的本部分写入。

3a. WHEN 检查结果为"已存在"且仅需重排（例如调整 Day 3 内的访问时段或顺序）时，THE Itinerary_Planner SHALL **不更新** `places.json` 与 `build_places.py` 的 `PLACE_PLAN`（这些数据文件仅在新增 / 删除地点时更新，重排不动数据），仅修改 Day_Plan_Document 与对应 Introduction_Document（如必要）。
4. THE Itinerary_Planner SHALL 在 design 阶段同步生成 / 更新「上野公园」对应的 Introduction_Document（如已抽离则继续维护、如新增则生成）。

### Requirement 6: 纳入「六本木 21_21 Design Sight」并体现 2026-06-03 ~ 2026-06-09 期间企画展

**User Story:** 作为旅行者，我希望把 21_21 Design Sight 纳入行程；同时由于该馆每两个月轮换一次企画展，需要联网核实 2026-06-03 ~ 2026-06-09 期间在展的企画展信息，把它体现在 Introduction_Document 与 Day_Plan_Document 的"看点"中。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 在 design 阶段开始前完成 21_21 Design Sight 在 2026-06-03 ~ 2026-06-09 期间企画展的 Official_Verification_Status，核实结论必须含时间戳与信息来源 URL（官网 https://www.2121designsight.jp/ 为准）。
2. THE Itinerary_Planner SHALL 接受以下核实结果作为依据：当前在展的企画展为「Soup as Life」（开展日 **2026-03-27**，根据官网 [21_21 DESIGN SIGHT - Soup as Life](https://2121designsight.jp/en/program/soup/)），由设计师 Natsumi Toyama 担任 director，主题以"汤"作为食 / 衣 / 住设计的最简营养形态；后续展览「Learning from 'Hōjōki': Tiny Architecture Reweaves Life」于 **2026-08-28** 开展（[miyakeissey.org 公告](https://miyakeissey.org/en/2121designsight/upcoming/)），故 2026-06-03 ~ 2026-06-09 期间「Soup as Life」企画展确认在展；**且 Itinerary_Planner SHALL 强制要求本次行程的实际访问时段（含入馆时刻 + 出馆时刻）严格全程落在「Soup as Life」展期 [2026-03-27, 2026-08-28) 之内**——即整段访问 SHALL 处于展期窗口内（不允许出现"入馆在展期内、出馆超出展期"的情形）。
3. THE Itinerary_Planner SHALL 把「21_21 Design Sight」作为子地点纳入某一日的行程（地理上推荐 Day 5 六本木段，因馆址在港区赤坂 9-7-6 东京 Midtown Garden 内，距日枝神社 / 根津美术馆步行可达；最终归属日由 design 阶段按"时间锁死活动 + 交通费最小"约束决定）。
4. THE Itinerary_Planner SHALL 在对应 Day_Plan_Document 的动线行中标注「Soup as Life」企画展的展期与本次访问的时段，并在 Introduction_Document 中详写展览主题 / director / 看点 / 票价 / 营业时间。
5. WHEN 在 design 或 task 阶段重新核实时发现「Soup as Life」企画展提前闭幕或时段调整，THE Itinerary_Planner SHALL 在 Day_Plan_Document 中标注「待用户实地确认」并提供官网 URL 兜底。
6. THE Itinerary_Planner SHALL 在 places.json 的 `included` 数组中新增「21_21 Design Sight」条目（建筑师安藤忠雄 2007，由 `build_places.py` 的 `PLACE_PLAN` 字典管理 `assigned_day` / `major_area` / `sub_area` / `type` 字段）。

### Requirement 7: 不再考虑「UENO WELCOME PASSPORT」

**User Story:** 作为旅行者，我已确认 UENO WELCOME PASSPORT 当前已无法购买，因此本次行程不再考虑纳入该通票，无须在 design 阶段做任何核查或条件性分支。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 不再把「UENO WELCOME PASSPORT」纳入本次 7 日行程；用户已于本次精修中确认（user_confirmed）该通票已无法购买，故无须在 design 阶段进行 Official_Verification_Status 核查、无须做条件性纳入决策、无须在 Cost_Scenario_Comparison 中为该通票预留 B2 子场景。
2. THE Itinerary_Planner SHALL 不在 places.json 中为 UENO WELCOME PASSPORT 创建任何独立 Place_Profile 条目（它是票券产品而非地理打卡点），且 Day 3 上野段 SHALL 不再为该通票预留任何 blockquote 占位说明、"待用户实地确认"说明或注释行。
3. THE Itinerary_Planner SHALL 把所有 Day_Plan_Document 中上野段的票价默认值统一设为「按各文化设施单独入场票价之和」（不再因通票而条件性切换），并在文档尾"当日交通费推算"对应行按该口径合计。
4. WHERE 既有任何 Day_Plan_Document 文本中残留有 `UENO WELCOME PASSPORT 待用户实地确认` 类的占位 blockquote 或注释行，THE Itinerary_Planner SHALL 在 design 阶段一并移除，不允许残留在最终文档中。

### Requirement 8: 核查并纳入「すし銚子丸 6 月店庆感谢祭」

**User Story:** 作为旅行者，我希望联网核查「すし銚子丸（Sushi Choshi-maru）6 月店庆感谢祭」（官网 https://www.choshimaru.co.jp/ ）的三项关键信息：(a) 活动是否在 2026-06-03 ~ 2026-06-09 期间举行；(b) 是否包含金枪鱼解体秀及具体场次门店与时间；(c) 活动期间的价格优惠内容；然后把该用餐地点插入到行程中合适的一天。

#### Acceptance Criteria

1. WHEN design 阶段开始时（即首次进入 design.md 撰写流程时），THE Itinerary_Planner SHALL 必须把「すし銚子丸 6 月店庆感谢祭」的三项核实作为前置条件全部完成，且不允许在三项中任意一项未完成的状态下进入 design 主体撰写；核实结论必须分别覆盖以下三项并各自附带时间戳与信息来源 URL：(a) 活动期间是否与 2026-06-03 ~ 2026-06-09 重叠；(b) 是否包含金枪鱼解体秀（マグロ解体ショー）及具体场次门店 / 时间；(c) 活动期间的价格优惠内容（例如店铺整体打折、特价单品菜单、积分翻倍等）。
2. WHEN 核实结论为「(a) 活动确认在期内 + (b) 至少有 1 家解体秀场次门店在东京都内地铁可达」时，THE Itinerary_Planner SHALL 把「すし銚子丸」作为子地点纳入与解体秀场次时间最匹配、且不与已有时间锁死活动冲突的某一日的行程（最终归属日 + 具体门店在 design 阶段决定）。
3. WHEN 核实结论为「(a) 活动在期内 + (b) 解体秀场次都不在东京都内地铁可达」时，THE Itinerary_Planner SHALL 仍把"すし銚子丸"作为普通的家庭式回转寿司用餐选项纳入某一日（无解体秀 / 仅享活动期间通用价格优惠），并在 Day_Plan_Document 标注解体秀的实际门店与时间，告知用户"无解体秀的优惠版本"。
4. WHEN 核实结论为「活动不在期内 / 已结束 / 信息无法核实」时，THE Itinerary_Planner SHALL 提供两套备选：① 改用「江戸蕎麦 ほそ川」(Day 7 已纳入) / 「並木藪蕎麦」(Day 6 已纳入) / 「Tokyo Tonkotsu Ramen Bankara 新宿歌舞伎町店」(Day 4 已纳入) 中任一作为本日餐饮替代；② 保留"すし銚子丸"作为非店庆期常规用餐选项纳入某一日；在 design 阶段评估并选其一。
5. THE Itinerary_Planner SHALL 为「すし銚子丸」（最终选定的具体门店）生成 Introduction_Document，至少包含：门店地址 / 最近车站 / 营业时间 / 招牌菜单 + 价格区间 / 解体秀时段（如有）/ 优惠内容（如有）/ 排队提示 / 是否可预约。
6. THE Itinerary_Planner SHALL 在 places.json 的 `included` 数组中新增「すし銚子丸 {门店名}」条目，由 `build_places.py` 的 `PLACE_PLAN` 字典管理 `assigned_day` / `major_area` / `sub_area` / `type` 字段。

### Requirement 9: 撤销 Day 1 小宫商店购伞的主观时间安排，按"时间锁死活动 + 交通费最小"客观重排小宫商店及全部剩余子地点的归属日

**User Story:** 作为旅行者，我希望撤销「东京第一天前往小宫商店购伞」这一主观时间决定，但保留小宫商店作为子地点继续纳入行程；其归属日改由"在不影响所有时间锁死活动的前提下，整体交通费用最小化"目标函数客观决定。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 从所有 Day_Plan_Document、`tst-segments.json`、`SUMMARY.md` 中识别并移除"把小宫商店购伞绑定在 Day 1 / Day 3 上午前置段"的所有动线痕迹（包括硬编码的 09:00 / 10:00 出门去日本桥小伝马町前置段叙述、文档头主题中的『购伞前置』字样、以及任何明示 / 暗示该购伞计划被钉死在 Day 1 / Day 3 的语句）；THE Itinerary_Planner SHALL **保留**「小宫商店（Komiya Shoten Japanese Umbrella Shop）」作为子地点在 `places.json`、`build_places.py` 的 `PLACE_PLAN`、`SUMMARY.md` 的景点介绍章节中的元数据条目，仅把其 `assigned_day` 字段改由 AC 9.4 的目标函数客观决定。
2. THE Itinerary_Planner SHALL 在 design 阶段把「小宫商店」的 `assigned_day` 作为决策变量，按 AC 9.4 的目标函数（最小化跨 7 天的整体交通费 Itinerary_Transit_Cost，按 Cost_Scenario A 全程 Suica 直付计）+ 约束（所有 Time_Locked_Activity 落在其官方营业时间窗内 + 当日 Major_Area 单调推进 + TST 失效时刻不变 + 与小伝马町地理顺路的 day 优先）求解，得出该子地点的最终归属日 `assigned_day ∈ {1..7}`；不允许把该地点彻底删除，也不允许保留 Day 1 / Day 3 的硬编码安排作为决策结果。
3. THE Itinerary_Planner SHALL 在 design 阶段先识别本次行程的所有 Time_Locked_Activity，至少包含：① 三段酒店的退房 / 入住时刻（Hotel Plus Hostel TOKYO KAWASAKI 退房 11:00、GuestHouse FUTARENO 退房 11:00 / 入住 16:00、COGO RYOGOKU 退房 10:00 / 入住 16:00）；② 6/5 18:00 Tokyo Dome 比赛（16:00 开场）；③ 6/7 09:00 日枝神社山王祭神事；④ 6/8 「六月大歌舞伎」第五场夜场（具体时刻按 KABUKI WEB 公告）；⑤ 6/8 闭幕的「Chi.」联动展（如保留则 6/7 必访）；⑥ 6/6 15:10 SSFF & ASIA WITH HARAJUKU HALL 短片节场次；⑦ 6/9 当晚航班时刻（待用户提供）；⑧ 各被纳入景点的开闭门 / 营业时间（江户东京博物馆 / 21_21 Design Sight / 银座歌舞伎座 / すし銚子丸 解体秀 / 各神社等）；⑨ TST 72 小时券激活窗口与失效时刻。
4. THE Itinerary_Planner SHALL 把所有 Time_Locked_Activity 锁定后，再按"整体交通费最小"对剩余子地点重新分配 day + 时段顺序，目标函数为最小化跨 7 天的 Itinerary_Transit_Cost（合计 JPY），约束为：所有 Time_Locked_Activity 落在其官方营业时间内、当日子地点序列在地理上单调推进（不出现可避免的回头）、TST 72 小时券激活时刻 / 失效时刻不变（6/5 上午激活 → 6/8 上午同时刻失效）。
5. THE Itinerary_Planner SHALL 在 design.md 中包含一个独立的"成本场景对比（Cost_Scenario_Comparison）"小节，列出至少 2 个 Cost_Scenario 的 7 日总交通费并列对比；至少必须覆盖：
   - **场景 A：全程 Suica 直付**——不持任何通票，所有段按官方票价直付；
   - **场景 B：应用本次行程实际使用的所有通票组合**——初版至少含 Tokyo Subway Ticket 72 小时券；如 design 阶段判定额外纳入了第二张通票（例如 都营一日券 / 东京 Metro 24h 券），则场景 B 应再细分为 B1（仅基础通票）/ B2（基础 + 附加通票）等子场景；最少 2 个场景，最多由 design 阶段按实际通票数量决定。
   每个场景必须给出：① 7 日合计 JPY 数字；② 每日分项 JPY 数字（按 day 维度）；③ 各场景所选通票名称；④ 通票本身价格（计入合计）。"重排"不再是触发对比的事件——即使 Day 1 / Day 3 等被重排，design.md 也无需重新做"重排前 vs 重排后"对比；只需每次有动线变更或通票方案变更时刷新"成本场景对比"小节内的数字即可。

5a. WHERE 任意 Cost_Scenario 的总交通费为 ¥0（例如 TST 全覆盖 + 全步行），THE Itinerary_Planner SHALL 仍在 Cost_Scenario_Comparison 表格中列出 ¥0 + 该场景所用通票名称（即使通票为 None / Suica 直付），不允许整行省略；无须在 design.md 中区分零成本的具体来源（无论是 TST 全覆盖、全步行、与已购票券打包等何种原因，统一记为该场景"7 日合计 ¥0"即可，无需额外分类说明）。
6. THE Itinerary_Planner SHALL 同步更新 `tst-segments.json` 的 `segments` 数组反映重排后的真实段落、TST 覆盖标记与每段票价，并保证 `tst_coverage_summary.cumulative_covered_rides ≥ 12`（与 design.md §10.4 阈值一致）。
7. THE Itinerary_Planner SHALL 在每个被重排的 Day_Plan_Document 头部硬约束区块更新对应"硬约束"列表，与 Time_Locked_Activity 集合一致。

### Requirement 10: 动线一致性、文档可构建、链接有效性、价格 / 开放时间核实（非功能性）

**User Story:** 作为站点维护者与旅行者，我希望整个站点在改造完成后仍保持构建可用、链接无失效、动线数据与 places.json / tst-segments.json / lodging-luggage.json 互相一致，且所有引用的"价格 / 开放时间"信息都有官方核实状态标注。

#### Acceptance Criteria

1. WHEN 改造完成后执行 `npm run build` 时，THE GitBook_Site SHALL 构建无错误地生成 `_book/` 静态站点，HonKit 不打印任何 broken-link 警告 / TOC 警告 / 标题层级警告。
2. THE Itinerary_Planner SHALL 保证 7 个 Day_Plan_Document 中提到的所有子地点都能在 `places.json` 的 `included` 数组中找到对应条目（罗马字 title 或日文 title 精确匹配），即"动线 vs 数据"覆盖完整性约束。
3. THE Itinerary_Planner SHALL 保证 `places.json` 的 `included` 数组中所有 `assigned_day ∈ {1..7}` 的条目都至少在对应 Day_Plan_Document 的某一行被引用（即"数据 vs 动线"反向覆盖完整性约束）。
4. THE Itinerary_Planner SHALL 保证每个 Day_Plan_Document 的"当日交通费推算"表格的合计金额 = 当日所有非 TST 覆盖段票价之和（与 `tst-segments.json` 中 `day == N + tst_covered != ✅` 的段落 `fare_jpy` 之和一致，差额 ≤ ¥50 视为四舍五入误差）；其他 Cost_Scenario 同样适用相同容差校验（即每个 Cost_Scenario 都必须保证 day 合计 = 该场景下当日所有计费段票价之和，容差 ≤ ¥50）。
5. THE Itinerary_Planner SHALL 保证每个 Time_Locked_Activity 的时段（开演 / 入场 / 神事 / 闭馆等）在对应 Day_Plan_Document 中的时间窗与 Introduction_Document 中标注的官方营业时间不冲突（即活动时点必须落在官方营业时间窗内）。
6. THE Itinerary_Planner SHALL 为所有引用的"票价数字 / 营业时间 / 定休日 / 活动展期"提供 Official_Verification_Status，**且无论核实结论如何（已确认 / 已确认未存续 / 无法核实），文档中必须随附至少一个官方信息来源 URL（官网 / 官方告知页 / 官方社交账号公告）**；当核实结论为「无法核实 / 待用户实地确认」时，文档中必须显式标注"待用户实地确认"+ 至少一个官方 URL（用于用户旅行前自行核实）。
7. THE Itinerary_Planner SHALL 保证 7 个 Day_Plan_Document 中没有任何 `## ` 二级标题的"区域"在同一日内重复出现两次（"必要回头段"如 Day 6 涩谷换乘穿过、Day 5 隈研吾环线必须显式注明并不计入重复）。
8. THE Itinerary_Planner SHALL 保证所有从 Day_Plan_Document 与 `index.md` 链接到 Introduction_Document 的相对路径都能在 GitHub Pages 部署后可访问（即不产生 404）。
9. WHERE 改造引入新的内部链接（如 SUMMARY.md 中的 Introduction_Group 章节），THE Itinerary_Planner SHALL 在本地 `npm run build` 前后对比 `_book/` 输出的文件清单，确保新增 / 删除的 HTML 文件与 markdown 一一对应，无遗漏。

### Requirement 11: PBT（Property-Based Testing）覆盖纯函数式数据处理与行程一致性

**User Story:** 作为站点维护者，我希望能用属性测试覆盖 `build_places.py` 的纯函数式数据处理与 7 个 Day_Plan_Document 的行程一致性校验，让"地点存在性 / 时间窗不重叠 / 时间锁死活动落在官方营业时间内"等关键性质有自动化检测。

#### Acceptance Criteria

1. THE Itinerary_Planner SHALL 在 task 阶段为 `build_places.py` 的 `parse_csv` / `categorize` / `PLACE_PLAN` 数据处理纯函数引入 Hypothesis（Python PBT 库）属性测试，至少覆盖以下性质：
   - 性质 P1：对任意有效 CSV 输入，`included + excluded + airports + lodgings` 的 Title 集合 = CSV 非空 Title 集合（覆盖完整性）；
   - 性质 P2：对任意有效 CSV 输入，所有 `included` 条目的 `assigned_day` 在 {1..7} 内或为 None；
   - 性质 P3：对任意有效 CSV 输入，所有 `excluded` 条目的 `is_excluded == true`，且其 Title 必须在 `EXCLUDED_TITLES` 集合内。
2. THE Itinerary_Planner SHALL 在 task 阶段为 7 个 Day_Plan_Document + `places.json` + `tst-segments.json` 的"行程一致性"引入 Hypothesis 属性测试，至少覆盖以下性质：
   - 性质 P4：每个 Day_Plan_Document 中以 `### {地点中文名}` 形式出现的子地点必须在 `places.json` 的 `included` 数组中存在对应 `assigned_day == N` 条目；
   - 性质 P5：每天活动时间窗（动线行的「HH:MM 起 → HH:MM 止」）不互相重叠（同一日内任意两个子地点的活动时段不交叠）；
   - 性质 P6：所有 Time_Locked_Activity 的时段必须落在对应 Introduction_Document 中标注的官方营业时间窗内（开演 ≥ 开门时刻 + 入场结束 ≤ 闭门时刻）；
   - 性质 P7：`tst-segments.json` 中标记 `tst_covered: ✅` 的段落，其 `in_tst_window: true`，且 `fare_jpy: 0`（一致性）。
   - 性质 P8：对每个 Cost_Scenario，`day` 合计 = 当日所有计费段（按该场景计费规则）的 `fare_jpy` 之和，容差 ≤ ¥50。
3. WHEN 性质测试在 task 阶段被执行时，THE Itinerary_Planner SHALL 让所有性质（P1 ~ P8）以默认 `Hypothesis settings.max_examples = 100` 通过；任何失败必须 fix 后重跑通过。
4. WHERE PBT 涉及外部服务（如查询 21_21 Design Sight 当期展期）时，THE Itinerary_Planner SHALL 不在 PBT 中调用真实 HTTP，而是以"已核实结果"作为输入数据 mock；外部服务可用集成测试单独覆盖（不在 PBT 范围内）。
5. THE Itinerary_Planner SHALL 在 design 阶段为每个性质（P1 ~ P8）写明测试范围、生成器（Hypothesis strategies）、验证函数与失败示例的处理路径，并在 task 阶段产出对应的 `tests/` 目录与 `pytest.ini` / `conftest.py` 等配置（具体目录结构在 design 阶段决定）。
