# Implementation Plan

## Overview

本任务清单对应 spec `lost-in-tokyo-itinerary-revamp` 的 8 项联合改造 + PBT 编写 + HonKit 构建验证，共 71 个顶层任务，分 10 个任务组（A ~ J）。

## Tasks

### 任务组 A：站点更名（design §5 / requirements §1）

- [x] 1. (任务组 A) 替换 book.json 的 title 与 description 字段
  - 涉及文件：`/book.json`
  - 把 `"title"` 字段值替换为「锅巴的奇妙冒险之迷失东京」
  - 把 `"description"` 字段值替换为「锅巴的奇妙冒险之迷失东京 — 2026 年 6 月关东 7 日（横滨 / 镰仓 / 东京）」
  - _Requirements: 1.1_

- [x] 2. (任务组 A) 替换 README.md 顶部一级标题
  - 涉及文件：`/README.md`
  - 首个 `# ` 行替换为「# 锅巴的奇妙冒险之迷失东京 GitBook」
  - _Requirements: 1.2_

- [x] 3. (任务组 A) 替换 SUMMARY.md 顶部一级标题
  - 涉及文件：`/SUMMARY.md`
  - 首个 `# ` 行替换为「# 锅巴的奇妙冒险之迷失东京」
  - _Requirements: 1.3_

- [x] 4. (任务组 A) 替换 index.md 顶部一级标题
  - 涉及文件：`/index.md`
  - 首个 `# ` 行替换为「# 锅巴的奇妙冒险之迷失东京 — 7 日行程总览（2026-06-03 ~ 2026-06-09）」
  - _Requirements: 1.4_

- [x] 5. (任务组 A) build_places.py verifying-identifiers 检查记录
  - 涉及文件：`/build_places.py`（仅检查不修改）
  - 执行 `grep -n -E "(Tokyo Trip|japan-7day-itinerary)" build_places.py`
  - 确认文件不含旧硬编码字符串；记录检查结论与时间戳
  - _Requirements: 1.5, 1.6_

### 任务组 B：撤销小宫商店购伞主观时间安排 + 客观重排到 Day 4（design §11 / requirements §9）

- [x] 6. (任务组 B) 删除 day-3 文档头标题与主要区域序列中的购伞前置字样
  - 涉及文件：`/day-3-2026-06-05.md`
  - 标题删除「日本桥 / 」+「购伞前置 + 」
  - 主要区域序列删除「日本桥小伝马町 → 」前缀
  - _Requirements: 9.1_

- [x] 7. (任务组 B) 删除 day-3 「## 子区域 0：日本桥小伝马町（小宫商店购伞前置段）」整段
  - 涉及文件：`/day-3-2026-06-05.md`
  - 从子区域 0 标题到下一个 `## 子区域 1` 之间的所有内容整段删除（约 80 行）
  - _Requirements: 9.1_

- [x] 8. (任务组 B) 精修 day-3 头部"TST 状态"字段
  - 涉及文件：`/day-3-2026-06-05.md`
  - 删除"...因新增小宫商店购伞前置..."字样
  - 改为「6/5 上午激活（首段：都营大江户线 两国 → 上野御徒町；72 小时窗口 6/5 上午 → 6/8 上午同时刻）」
  - _Requirements: 9.1_

- [x] 9. (任务组 B) 从 day-7 中移出 Komiya Place_Profile 段
  - 涉及文件：`/day-7-2026-06-09.md`
  - 移除 Komiya Shoten 的 `### ` 段落（该内容将在任务 10 中迁入 day-4）
  - _Requirements: 9.1_

- [x] 10. (任务组 B) day-4 新增小宫商店子地点 + 神保町 ↔ 小伝马町往返动线行
  - 涉及文件：`/day-4-2026-06-06.md`
  - 在子区域 1「千代田 / 神保町」之后新增「## 子区域：东京—日本桥（Nihonbashi）」
  - 新增 `### 小宫商店（小宮商店 / Komiya Shoten）` 动线行，时刻 11:35–12:00
  - 新增段间交通：神保町站 都营浅草线 → 小伝马町（¥0 / TST ✅）+ 返程同路线
  - _Requirements: 9.2_

- [x] 11. (任务组 B) day-4 头部硬约束新增第 5 项
  - 涉及文件：`/day-4-2026-06-06.md`
  - 在硬约束列表追加「11:30 前抵达小伝马町（小宫商店周日定休、周六 11:00–18:00 营业）」
  - _Requirements: 9.3, 9.7_

- [x] 12. (任务组 B) 修改 places.json 中 Komiya Shoten 的 assigned_day 与区域字段
  - 涉及文件：`/places.json`
  - `assigned_day` 从 7 改为 4
  - `major_area` 改为「东京—日本桥」
  - `sub_area` 改为「日本橋小伝馬町 14-2」
  - 同步 `by_day.day_7` 数组移除 + `by_day.day_4` 数组新增
  - _Requirements: 9.2_

- [x] 13. (任务组 B) 修改 build_places.py PLACE_PLAN 字典 Komiya Shoten 键
  - 涉及文件：`/build_places.py`
  - `day=4`、`major_area="东京—日本桥"`、`sub_area="日本橋小伝馬町 14-2"`
  - _Requirements: 9.2_

- [x] 14. (任务组 B) tst-segments.json Day 4 追加神保町 ↔ 小伝马町往返 2 段
  - 涉及文件：`/tst-segments.json`
  - 在 Day 4 segments 数组追加 2 段（都营浅草线，TST ✅，fare_jpy: 0）
  - 重新计算 `tst_coverage_summary.cumulative_covered_rides` = 21
  - _Requirements: 9.6_

### 任务组 C：江户东京博物馆纳入 Day 7（design §7 / requirements §4）

- [x] 15. (任务组 C) day-7 新增「### 江户东京博物馆」动线行 + 头部硬约束
  - 涉及文件：`/day-7-2026-06-09.md`
  - 新增动线行：10:15–11:30 江户东京博物馆（步行 8 分钟从 COGO RYOGOKU）
  - 头部硬约束新增第 3 项「江户东京博物馆 09:30–17:30（周一定休，6/9 周二开馆）」
  - _Requirements: 4.3_

- [x] 16. (任务组 C) 新建 intros/intro-edo-tokyo-museum.md
  - 涉及文件：`/intros/intro-edo-tokyo-museum.md`（新建）
  - 按 design §7.3 内容大纲，含 12 个必含字段 + 建筑专属字段
  - 含 Official_Verification_Status：已重开 2026-03-31 + 三条信息源 URL
  - _Requirements: 4.5, 4.2_

- [x] 17. (任务组 C) places.json 新增 Edo-Tokyo Museum 条目
  - 涉及文件：`/places.json`
  - 在 `included` 数组新增条目：assigned_day=7, major_area="东京—两国 / 押上 / 晴空塔", type="博物馆"
  - _Requirements: 4.6_

- [x] 18. (任务组 C) build_places.py PLACE_PLAN 追加 Edo-Tokyo Museum
  - 涉及文件：`/build_places.py`
  - 追加 `"Edo-Tokyo Museum": dict(day=7, type="博物馆", major_area="东京—两国 / 押上 / 晴空塔", sub_area="横网 1-4-1")`
  - _Requirements: 4.6_

### 任务组 D：21_21 Design Sight 纳入 Day 5（design §9 / requirements §6）

- [x] 19. (任务组 D) day-5 新增「### 21_21 Design Sight」动线行 + 头部硬约束
  - 涉及文件：`/day-5-2026-06-07.md`
  - 新增动线行：13:45–14:30 21_21 Design Sight「Soup as Life」企画展
  - 头部硬约束新增第 2 项「21_21 Design Sight 访问时段必须落在 [2026-03-27, 2026-08-28) 展期窗口内」
  - _Requirements: 6.3, 6.4_

- [x] 20. (任务组 D) 新建 intros/intro-21-21-design-sight.md
  - 涉及文件：`/intros/intro-21-21-design-sight.md`（新建）
  - 按 design §9.4 内容大纲，含 12 个必含字段 + 建筑专属字段 + 演出/美术展专属字段
  - 含 Official_Verification_Status：「Soup as Life」展期 [2026-03-27, 2026-08-28) + 信息源 URL
  - _Requirements: 6.4, 6.1, 6.2_

- [x] 21. (任务组 D) places.json 新增 21_21 Design Sight 条目
  - 涉及文件：`/places.json`
  - 在 `included` 数组新增条目：assigned_day=5, major_area="东京—六本木", type="美术馆 / 建筑"
  - _Requirements: 6.6_

- [x] 22. (任务组 D) build_places.py PLACE_PLAN 追加 21_21 Design Sight
  - 涉及文件：`/build_places.py`
  - 追加 `"21_21 Design Sight": dict(day=5, type="美术馆 / 建筑(安藤忠雄,2007)", major_area="东京—六本木", sub_area="东京 Midtown Garden")`
  - _Requirements: 6.6_

### 任务组 E：介绍文档抽离 + SUMMARY 重组 + 区域层级修正（design §6 / requirements §2 / §3）

- [x] 23. (任务组 E) 创建 intros/ 子目录
  - 涉及文件：`/intros/`（新建目录）
  - 在仓库根目录创建 `intros/` 子目录
  - _Requirements: 2.2_

- [x] 24. (任务组 E) 抽离 Day 1 横滨段地点档案为独立介绍文档（约 11 个地点）
  - 涉及文件：`/day-1-2026-06-03.md` + `/intros/intro-*.md`（新建约 11 个文件）
  - 把 day-1 中每个 `### {地点中文名}` 下的 Place_Profile 段落抽离为 `intros/intro-{romaji-id}.md`
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 25. (任务组 E) 抽离 Day 2 镰仓段地点档案（约 7 个地点）
  - 涉及文件：`/day-2-2026-06-04.md` + `/intros/intro-*.md`（新建约 7 个文件）
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 26. (任务组 E) 抽离 Day 3 上野—秋叶原—水道桥段地点档案（约 9 个地点）
  - 涉及文件：`/day-3-2026-06-05.md` + `/intros/intro-*.md`（新建约 9 个文件）
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 27. (任务组 E) 抽离 Day 4 神保町—新宿—中野段地点档案（约 9 个地点含小宫商店）
  - 涉及文件：`/day-4-2026-06-06.md` + `/intros/intro-*.md`（新建约 9 个文件）
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 28. (任务组 E) 抽离 Day 5 赤坂—六本木—神乐坂—早稻田段地点档案（约 8 个地点含 21_21）
  - 涉及文件：`/day-5-2026-06-07.md` + `/intros/intro-*.md`（新建约 8 个文件）
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 29. (任务组 E) 抽离 Day 6 上半涩谷—原宿—代官山段地点档案（约 8 个地点）
  - 涉及文件：`/day-6-2026-06-08.md` + `/intros/intro-*.md`（新建约 8 个文件）
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 30. (任务组 E) 抽离 Day 6 下半银座—丸之内—日本桥—歌舞伎座段地点档案（约 8 个地点）
  - 涉及文件：`/day-6-2026-06-08.md` + `/intros/intro-*.md`（新建约 8 个文件）
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 31. (任务组 E) 抽离 Day 7 浅草—两国—晴空塔段地点档案（约 5 个地点含江户东京博物馆）
  - 涉及文件：`/day-7-2026-06-09.md` + `/intros/intro-*.md`（新建约 5 个文件）
  - _Requirements: 2.1, 2.2, 2.6_

- [x] 32. (任务组 E) 改写 day-1 中每个 ### 段落为「动线提示 + 链接」格式
  - 涉及文件：`/day-1-2026-06-03.md`
  - 每个 `### {地点中文名}` 段落改为单行「- HH:MM ｜ {地点中文名}（{区域}）→ [详细介绍](intros/intro-xxx.md)」+ 缩进子项 1（最近车站）+ 子项 2（票价）+ 子项 3（时间窗）
  - 保留 Navigation_Essentials 五项
  - _Requirements: 2.3, 2.4, 2.9, 2.11_

- [x] 33. (任务组 E) 改写 day-2 中每个 ### 段落为「动线提示 + 链接」格式
  - 涉及文件：`/day-2-2026-06-04.md`
  - _Requirements: 2.3, 2.4, 2.9, 2.11_

- [x] 34. (任务组 E) 改写 day-3 中每个 ### 段落为「动线提示 + 链接」格式
  - 涉及文件：`/day-3-2026-06-05.md`
  - _Requirements: 2.3, 2.4, 2.9, 2.11_

- [x] 35. (任务组 E) 改写 day-4 中每个 ### 段落为「动线提示 + 链接」格式
  - 涉及文件：`/day-4-2026-06-06.md`
  - _Requirements: 2.3, 2.4, 2.9, 2.11_

- [x] 36. (任务组 E) 改写 day-5 中每个 ### 段落为「动线提示 + 链接」格式
  - 涉及文件：`/day-5-2026-06-07.md`
  - _Requirements: 2.3, 2.4, 2.9, 2.11_

- [x] 37. (任务组 E) 改写 day-6 中每个 ### 段落为「动线提示 + 链接」格式
  - 涉及文件：`/day-6-2026-06-08.md`
  - _Requirements: 2.3, 2.4, 2.9, 2.11_

- [x] 38. (任务组 E) 改写 day-7 中每个 ### 段落为「动线提示 + 链接」格式
  - 涉及文件：`/day-7-2026-06-09.md`
  - _Requirements: 2.3, 2.4, 2.9, 2.11_

- [x] 39. (任务组 E) SUMMARY.md 新增「## 景点介绍（按区域）」章节
  - 涉及文件：`/SUMMARY.md`
  - 按 25 个 Major_Area 编号 1→25 顺序组织所有 Introduction_Document 链接
  - 格式：`### {Major_Area 中文}（{Romaji}）` + `* [{地点中文名}](intros/intro-{romaji-id}.md)`
  - _Requirements: 2.7_

- [x] 40. (任务组 E) 区域 / 子地点层级修正验证
  - 涉及文件：`/day-1-2026-06-03.md` ~ `/day-7-2026-06-09.md`
  - 运行 `grep -n "^## " day-*.md` 确认所有 `## ` 标题仅对应 Major_Area
  - 运行 `grep -n "^### " day-*.md` 确认所有 `### ` 标题仅对应子地点
  - 确认不出现层级跳跃（`# ` 直接到 `### `）
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.6_

### 任务组 F：上野公园重排时刻（design §8 / requirements §5）

- [x] 41. (任务组 F) day-3 中「### 上野恩赐公园」动线行时刻调整为 10:20–11:50
  - 涉及文件：`/day-3-2026-06-05.md`
  - 不动 places.json / build_places.py（已存在分支，仅修改时刻）
  - _Requirements: 5.2, 5.3a_

- [x] 42. (任务组 F) 新建 intros/intro-ueno-park.md
  - 涉及文件：`/intros/intro-ueno-park.md`（新建）
  - 按抽离规则，含 12 个必含字段 + 庭园 / 公园专属字段
  - _Requirements: 5.4, 2.6_

### 任务组 G：すし銚子丸 待办标记（design §10 / requirements §8，默认决策 8.4-① 不纳入）

- [x] 43. (任务组 G) Day 5 文档加占位 blockquote 提示銚子丸待核实
  - 涉及文件：`/day-5-2026-06-07.md`
  - 在文档尾「次日提醒」段前加 `> ⚠️ すし銚子丸 6 月店庆感谢祭三项核实（活动期间 / 解体秀 / 优惠）待用户旅行前 1 周自行核实（官网 https://www.choshimaru.co.jp/）`
  - _Requirements: 8.4_

- [x] 44. (任务组 G) Day 6 文档加占位 blockquote 提示銚子丸待核实
  - 涉及文件：`/day-6-2026-06-08.md`
  - 同上格式
  - _Requirements: 8.4_

### 任务组 H：Cost_Scenario_Comparison 表落地（design §11.6 / requirements §9.5 / §10.4）

- [x] 45. (任务组 H) day-1 文档尾「当日交通费推算」表更新为场景 A / 场景 B 双行
  - 涉及文件：`/day-1-2026-06-03.md`
  - 场景 A：¥1,470（Suica 直付）；场景 B：¥1,470（横滨日不在 TST 期内，与 A 相同）
  - _Requirements: 9.5, 10.4_

- [x] 46. (任务组 H) day-2 文档尾「当日交通费推算」表更新为场景 A / 场景 B 双行
  - 涉及文件：`/day-2-2026-06-04.md`
  - 场景 A：¥2,200；场景 B：¥2,200（镰仓日不在 TST 期内）
  - _Requirements: 9.5, 10.4_

- [x] 47. (任务组 H) day-3 文档尾「当日交通费推算」表更新为场景 A / 场景 B 双行
  - 涉及文件：`/day-3-2026-06-05.md`
  - 场景 A：¥810；场景 B：¥150（TST ✅ 覆盖大部分段，仅 JR ¥150 不覆盖）
  - _Requirements: 9.5, 10.4_

- [x] 48. (任务组 H) day-4 文档尾「当日交通费推算」表更新为场景 A / 场景 B 双行
  - 涉及文件：`/day-4-2026-06-06.md`
  - 场景 A：¥1,770（含神保町 ↔ 小伝马町 ¥360）；场景 B：¥510（仅小田急段不覆盖）
  - _Requirements: 9.5, 10.4_

- [x] 49. (任务组 H) day-5 文档尾「当日交通费推算」表更新为场景 A / 场景 B 双行
  - 涉及文件：`/day-5-2026-06-07.md`
  - 场景 A：¥1,260；场景 B：¥0（TST ✅ 全段覆盖）
  - _Requirements: 9.5, 9.5a, 10.4_

- [x] 50. (任务组 H) day-6 文档尾「当日交通费推算」表更新为场景 A / 场景 B 双行
  - 涉及文件：`/day-6-2026-06-08.md`
  - 场景 A：¥1,830；场景 B：¥510（仅 JR + 东急段不覆盖）
  - _Requirements: 9.5, 10.4_

- [x] 51. (任务组 H) day-7 文档尾「当日交通费推算」表更新为场景 A / 场景 B 双行
  - 涉及文件：`/day-7-2026-06-09.md`
  - 场景 A NRT：¥2,940 / HND：¥1,180；场景 B：与 A 相同（TST 已失效）
  - _Requirements: 9.5, 10.4_

- [x] 52. (任务组 H) tst-segments.json 重新核算 cumulative_covered_rides
  - 涉及文件：`/tst-segments.json`
  - 确认 cumulative_covered_rides = 21（Day 3: 3 + Day 4: 7 + Day 5: 6 + Day 6: 5 = 21）
  - 与 design §11.7 一致
  - _Requirements: 9.6_

### 任务组 I：PBT 编写（design §16 / requirements §11）

- [x] 53. (任务组 I) 创建 tests/ 目录 + pytest.ini + conftest.py
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/pytest.ini`（新建）+ `/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/conftest.py`（新建）
  - pytest.ini 设置 max_examples=100、deadline=None、--hypothesis-show-statistics
  - conftest.py 含 places / tst_segments / day_files / intro_files 四组 session fixtures
  - _Requirements: 11.5_

- [x] 54. (任务组 I) 创建 tests/strategies/__init__.py + csv_strategy.py
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/strategies/__init__.py` + `csv_strategy.py`（新建）
  - csv_rows_strategy() 生成 RawRow 列表
  - _Requirements: 11.5_

- [x] 55. (任务组 I) 创建 tests/strategies/place_strategy.py
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/strategies/place_strategy.py`（新建）
  - place_strategy() 生成 Place 实例
  - _Requirements: 11.5_

- [x] 56. (任务组 I) 创建 tests/strategies/tla_strategy.py
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/strategies/tla_strategy.py`（新建）
  - tla_strategy() 生成 Time_Locked_Activity
  - _Requirements: 11.5_

- [x] 57. (任务组 I) 创建 tests/strategies/tst_strategy.py
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/strategies/tst_strategy.py`（新建）
  - tst_segment_strategy() 生成 tst-segments.json segment
  - _Requirements: 11.5_

- [x] 58. (任务组 I) 创建 tests/strategies/scenario_strategy.py
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/strategies/scenario_strategy.py`（新建）
  - scenario_strategy() 生成 Cost_Scenario
  - _Requirements: 11.5_

- [x] 59. (任务组 I) [PBT] 编写 test_p1_coverage.py（覆盖完整性）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p1_coverage.py`（新建）
  - 验证 included titles ⊆ day subtitles + excluded titles ∩ day subtitles == ∅
  - _Requirements: 11.1 P1, 11.3_

- [x] 60. (任务组 I) [PBT] 编写 test_p2_monotonic.py（序列单调性）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p2_monotonic.py`（新建）
  - 验证每日 Major_Area 序列无重复（除显式标注环线外）
  - _Requirements: 11.2 P2, 11.3_

- [x] 61. (任务组 I) [PBT] 编写 test_p3_anchors.py（硬锚点性）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p3_anchors.py`（新建）
  - 验证 9 项 TLA 在对应 day-N.md 中存在关键文本
  - _Requirements: 11.2 P3, 11.3_

- [x] 62. (任务组 I) [PBT] 编写 test_p4_fields.py（字段完整性）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p4_fields.py`（新建）
  - 验证所有 intros/*.md 含 12 个必含字段 + 类别专属字段
  - _Requirements: 11.2 P4, 11.3_

- [x] 63. (任务组 I) [PBT] 编写 test_p5_tail.py（收尾性）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p5_tail.py`（新建）
  - 验证 day-3 ~ day-6 文末含「COGO RYOGOKU」；day-7 含「10:00 退房」
  - _Requirements: 11.2 P5, 11.3_

- [x] 64. (任务组 I) [PBT] 编写 test_p6_time_windows.py（营业时间窗）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p6_time_windows.py`（新建）
  - 验证所有 TLA 时段落在对应 Place_Profile 官方营业时间窗内
  - _Requirements: 11.2 P6, 11.3_

- [x] 65. (任务组 I) [PBT] 编写 test_p7_tst_consistency.py（TST 一致性）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p7_tst_consistency.py`（新建）
  - 验证 tst_covered: ✅ 的段 in_tst_window == true + fare_jpy == 0 + day ∈ {3,4,5,6}
  - _Requirements: 11.2 P7, 11.3_

- [x] 66. (任务组 I) [PBT] 编写 test_p8_scenarios.py（Cost_Scenario 合计）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_p8_scenarios.py`（新建）
  - 验证每个 Cost_Scenario 的 day 合计 = 当日计费段 fare_jpy 之和，容差 ≤ ¥50
  - _Requirements: 11.2 P8, 11.3_

- [x] 67. (任务组 I) [Lint] 编写 test_extras.py（文件存在性 + 内部链接有效性）
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/test_extras.py`（新建）
  - 验证所有 included 地点对应的 intros/*.md 文件存在
  - 验证 day-N.md 中所有内部链接指向存在的文件
  - _Requirements: 10.2, 10.3, 10.8_

### 任务组 J：HonKit 构建 + Lint 验证（design §13 / requirements §10）

- [x] 68. (任务组 J) [Lint] npm run build 构建验证
  - 涉及文件：`/package.json`、`/_book/`（输出）
  - 执行 `npm run build`，检查 stderr 无 broken-link / TOC / 标题层级警告
  - 确认 `_book/` 正常生成
  - _Requirements: 10.1, 10.9_

- [x] 69. (任务组 J) [Lint] grep 旧名「Tokyo Trip 2026」确认仅引用上下文残留
  - 涉及文件：`/` 全站
  - 执行 `grep -rn "Tokyo Trip 2026" . --include="*.md" --include="*.json"`
  - 确认仅在引用上下文（README 修订流程建议代码块 / 索引页历史记录）中出现，非头部标题 / 菜单项
  - _Requirements: 1.6_

- [x] 70. (任务组 J) [Lint] 检查 _book/index.html <title> 反映新标题
  - 涉及文件：`/_book/index.html`
  - 确认 `<title>` 标签值含「锅巴的奇妙冒险之迷失东京」
  - _Requirements: 1.7_

- [x] 71. (任务组 J) [PBT] 运行 pytest 验证 8 条 PBT 全部通过
  - 涉及文件：`/.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/`
  - 执行 `pytest --hypothesis-show-statistics -v`
  - 确认 P1 ~ P8 + extras 全部 PASSED（max_examples=100）
  - _Requirements: 11.3_

---

## Notes

- 任务粒度：每个任务可由 spec-task-execution 子代理在一次会话内完成。
- PBT 类任务标题带「PBT」标记；纯 Lint 类任务带「Lint」标记。
- 任务组 G（銚子丸）按默认决策 8.4-① 不纳入，仅加占位 blockquote；用户旅行前 1 周核实后可改决策。
- UENO WELCOME PASSPORT 已确认无法购买，本 tasks.md 不含任何相关任务。

## Task Dependency Graph

```json
{
  "waves": [
    {
      "id": "wave-1",
      "name": "Wave 1: 独立基础改造",
      "tasks": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 41, 42, 43, 44],
      "dependsOn": []
    },
    {
      "id": "wave-2",
      "name": "Wave 2: 介绍文档抽离 + SUMMARY 重组",
      "tasks": [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
      "dependsOn": ["wave-1"]
    },
    {
      "id": "wave-3",
      "name": "Wave 3: Cost_Scenario 表落地",
      "tasks": [45, 46, 47, 48, 49, 50, 51, 52],
      "dependsOn": ["wave-2"]
    },
    {
      "id": "wave-4",
      "name": "Wave 4: PBT 编写",
      "tasks": [53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67],
      "dependsOn": ["wave-3"]
    },
    {
      "id": "wave-5",
      "name": "Wave 5: HonKit 构建 + Lint 验证",
      "tasks": [68, 69, 70, 71],
      "dependsOn": ["wave-4"]
    }
  ]
}
```

**依赖说明**：
- A / B / C / D / F 独立可并行
- E 依赖 B + C + D + F 完成（抽离需要先确定所有地点的 day 归属与新增 / 移出地点）
- G 可与 E 并行
- H 依赖 E + G 完成
- I 依赖 H 完成（PBT 需要全部数据落地）
- J 依赖 I 完成 + 所有其他任务组完成
