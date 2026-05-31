# Implementation Plan：关东 7 日行程文档生成

## Overview

把 design.md 中确定的「60 个保留地点 → 7 个 day-N.md」分配落实为实际的 markdown 文档。任务按"日切片"为主组织：先做基础设施（任务 1）准备 7 个文件骨架与每个地点的元数据卡片，再依序填充 Day 1–Day 7（任务 2–8），然后产出 index.md 总览（任务 9），最后跑 5 条 lint 性质校验（任务 10）。

每个 Place_Profile 是一个独立子任务，便于单独追踪 ≥ 150 字历史背景与 12 字段完整性。Day 6（16 个地点 + 歌舞伎硬锚点 + 必要回头段）拆得更细。Day 5 的"歌舞伎购票提醒"作为独立子任务以满足 P3 性质。

## Tasks

- [x] 1. 基础设施 / 数据准备
  - [x] 1.1 创建 7 个文件骨架
    - 在 `.kiro/specs/japan-7day-itinerary/` 下创建 `day-1-2026-06-03.md`、`day-2-2026-06-04.md`、`day-3-2026-06-05.md`、`day-4-2026-06-06.md`、`day-5-2026-06-07.md`、`day-6-2026-06-08.md`、`day-7-2026-06-09.md`
    - 每个文件预先填入文档头骨架（H1 标题 + 文档头 9 项元数据占位 blockquote）
    - _Requirements: §12.1, §12.2, §14.2_

  - [x] 1.2 抽取 60 个 Place 元数据卡片
    - 解析 `Takeout/Saved/Favorite places.csv`，跳过 Title 为空的行
    - 对 60 个保留地点输出元数据 JSON / 表：`title_jp`、`title_romaji`、`title_cn`、`csv_note`、`url`、推断的 `type`、`major_area`、`sub_area`、`assigned_day`
    - 标注 10 个排除地点（不进入任何 day-N.md）与 2 个机场 / 1 个住宿
    - _Requirements: §1.1, §1.2, §1.3, §1.4, §1.5_

  - [x] 1.3 准备 TST 段落数据表
    - 把 design.md「Tokyo Subway Ticket 使用策略」表整理为 Day 1–Day 7 每段交通的 ✅ / ❌ 数据，供 Day 3–6 文档尾交通费表渲染时引用
    - 标记激活时刻为 6/5 上午、失效时刻为 6/8 同时刻
    - _Requirements: §10.1, §10.2, §10.3, §10.4, §10.6_

  - [x] 1.4 准备酒店 / 行李 / 退房时刻数据
    - 整理三段酒店：6/3 11:00 退川崎 → 16:00 入横滨 FUTARENO；6/4 11:00 退 FUTARENO → 16:00 入 COGO RYOGOKU；6/9 10:00 退 COGO RYOGOKU
    - 整理 Day 1 / Day 2 / Day 7 三套行李方案（投币柜 / 寄存 / 黑猫宅配）作为各日文档头"行李"字段的源
    - _Requirements: §11.1, §11.2, §11.3, §11.4, §11.5, §11.6_

- [x] 2. Day 1（6 月 3 日 周二）— 横滨（8 个地点）
  - [x] 2.1 写 Day 1 文档头
    - 填入：日期 6/3 周二 / 主题「横滨」/ 主要区域序列「新横滨 → 港未来 → 山下 → 伊势佐木」/ 今晨出发 川崎 Hotel Plus Hostel 11:00 退房 / 当晚住宿 GuestHouse FUTARENO 16:00 后入住 / 行李方案 B / 硬约束 11:00 退 + 16:00 入 / TST 状态「未购入」9 项
    - _Requirements: §2.2, §3.1, §3.3, §11.1, §11.4, §14.2_

  - [x] 2.2 写 Day 1 主体 — 新横滨段
    - 子区域导览段
    - Place_Profile：`Shin-Yokohama Ramen Museum`（新横滨拉面博物馆）
    - _Requirements: §3.2, §3.4, §13.1, §13.2_

  - [x] 2.3 写 Day 1 主体 — 港未来段
    - 子区域导览段
    - Place_Profile：`Yokohama Station`
    - Place_Profile：`Yokohama Landmark Tower`
    - Place_Profile：`Yokohama Museum of Art`（核心）
    - Place_Profile：`Yokohama Red Brick Warehouse`
    - _Requirements: §3.2, §3.4, §3.5, §13.1, §13.3, §13.5_

  - [x] 2.4 写 Day 1 主体 — 山下 / 本牧段
    - 子区域导览段
    - Place_Profile：`Yamashita Park`
    - Place_Profile：`Sankeien Garden`（核心，CSV 备注关于 17 栋古建筑必须保留）
    - _Requirements: §3.2, §3.5, §13.1, §13.6_

  - [x] 2.5 写 Day 1 主体 — 伊势佐木段
    - 子区域导览段（夜游定位）
    - Place_Profile：`Isezakichō`
    - _Requirements: §3.2, §3.3, §13.1_

  - [x] 2.6 写 Day 1 文档尾
    - 当日交通费表（每段 JR / 横滨地铁 / 港未来线票价 + TST ❌ 标记）
    - 当晚抵达：横滨站 → GuestHouse FUTARENO 步行预计时长
    - 次日提醒：6/4 11:00 退 FUTARENO + 行李方案 + 镰仓硬约束
    - _Requirements: §9.3, §9.4, §10.5, §11.4, §14.4_

  - [x] 2.7 Day 1 lint
    - 对 Day 1 跑 P4（每个 Place_Profile 12 字段全在 + 类别专属字段）+ P2（序列「新横滨 → 港未来 → 山下 → 伊势佐木」无重复）
    - 输出"通过 / 失败 + 失败地点定位"
    - _Requirements: §9.2, §13.1, §13.6_

- [x] 3. Day 2（6 月 4 日 周三）— 镰仓（6 个地点）
  - [x] 3.1 写 Day 2 文档头
    - 9 项元数据：6/4 周三 / 「镰仓」/ 序列「北镰仓 → 镰仓中心 → 长谷 → 江之电沿线」/ 今晨 GuestHouse FUTARENO 11:00 退 / 当晚 COGO RYOGOKU 16:00 入 / 行李方案 A 或 B / 硬约束 11:00 退 + 16:00 入 / TST「未购入」
    - _Requirements: §2.2, §4.1, §4.4, §11.2, §11.4, §14.2_

  - [x] 3.2 写 Day 2 主体 — 北镰仓段
    - 子区域导览段
    - Place_Profile：`Engaku-ji`（圆觉寺）
    - Place_Profile：`Meigetsu-in`（明月院；6 月梅雨季"明月院蓝"早入园提示 + 雨天替代）
    - _Requirements: §4.2, §4.3, §4.5, §13.1, §13.6_

  - [x] 3.3 写 Day 2 主体 — 镰仓中心段
    - 子区域导览段
    - Place_Profile：`Tsurugaoka Hachimangu`（鹤冈八幡宫）
    - _Requirements: §4.2, §4.3, §13.1, §13.6_

  - [x] 3.4 写 Day 2 主体 — 长谷段
    - 子区域导览段
    - Place_Profile：`Kotoku-in`（高德院 / 镰仓大佛）
    - _Requirements: §4.2, §4.3, §13.1, §13.6_

  - [x] 3.5 写 Day 2 主体 — 江之电沿线段
    - 子区域导览段（推荐自西向东顺序：七里滨 → 镰仓高校前）
    - Place_Profile：`Shichirigahama Beach`（七里滨）
    - Place_Profile：`Kamakurakōkō-Mae Station`（镰仓高校前站）
    - _Requirements: §4.2, §4.3, §13.1_

  - [x] 3.6 写 Day 2 文档尾
    - 当日交通费表（JR 横须贺线 + 江之电 + 横滨 → 两国回程，全部 TST ❌）
    - 当晚抵达：从镰仓 / 大船经 JR 总武线快速到两国 → 步行至 COGO RYOGOKU 预计时长
    - 行李宅配方案提示（黑猫 / 佐川下单时间）
    - 次日提醒：6/5 上午激活 TST 72 小时券 + 18:00 棒球巨蛋硬约束
    - _Requirements: §4.4, §4.6, §9.3, §9.4, §10.6, §11.4, §14.4_

  - [x] 3.7 Day 2 lint
    - 对 Day 2 跑 P4（字段完整性）+ P2（序列「北镰仓 → 中心 → 长谷 → 江之电」无重复）
    - 输出"通过 / 失败 + 失败地点定位"
    - _Requirements: §9.2, §13.1, §13.6_

- [x] 4. Day 3（6 月 5 日 周五）— 东京（上野—秋叶原—水道桥，含棒球，9 个地点）
  - [x] 4.1 写 Day 3 文档头
    - 9 项元数据：6/5 周五 / 「上野 / 本乡 / 秋叶原 / 水道桥（江户文教 + 御宅 + 棒球收尾）」/ 序列「上野 / 本乡 → 秋叶原 → 水道桥」/ 今晨 COGO RYOGOKU / 当晚 COGO RYOGOKU / 行李无 / 硬约束「18:00 巨人 vs 罗德 + TST 上午激活」/ TST 状态「待激活」
    - 文档头开篇明确 TST 72 小时券激活地点（地铁站窗口或便利店）+ 6/5 上午第一次乘车前激活
    - _Requirements: §2.2, §5.1, §5.2, §5.6, §10.1, §10.6, §14.2_

  - [x] 4.2 写 Day 3 主体 — 上野段
    - 子区域导览段
    - Place_Profile：`Ueno Park`
    - Place_Profile：`Tokyo National Museum`
    - Place_Profile：`Kyū-Iwasaki-tei Gardens`（旧岩崎邸庭园）
    - **2026-05-29 修订**：`The University of Tokyo`（东京大学本乡校区）已从 Day 3 移除（优先级低 + 与博物馆段时间冲突）；子区域 1 由"上野 / 本乡 / 东大"缩减为"上野"。
    - _Requirements: §5.3, §13.1, §13.3, §13.6_

  - [x] 4.3 写 Day 3 主体 — 秋叶原段
    - 子区域导览段
    - Place_Profile：`Akihabara`
    - Place_Profile：`Akihabara Electric Town`
    - Place_Profile：`Mandarake Complex`
    - Place_Profile：`Pop Life Department M's`
    - _Requirements: §5.3, §13.1, §13.5_

  - [x] 4.4 写 Day 3 主体 — 水道桥段（含硬锚点）
    - 子区域导览段（强调 16:30 前抵达）
    - Place_Profile：`Tokyo Dome`，硬约束标注「6/5 16:00 开场、18:00 比赛开始、巨人 vs 罗德」+ 入场口 + 检票流程 + 禁带物品
    - _Requirements: §5.1, §5.2, §5.4, §13.1, §13.4_

  - [x] 4.5 写 Day 3 文档尾
    - 当日交通费表（每段标 TST ✅ / ❌；累计 TST 段数）
    - 当晚回程：水道桥 / 后乐园 → 都营大江户线 → 两国 → 步行至 COGO RYOGOKU
    - 次日提醒：6/6 Day 4 主题「新宿 / 中野」+ 早场 M2ビル 出发地铁衔接
    - _Requirements: §5.5, §9.3, §9.4, §10.3, §11.6, §14.4_

  - [x] 4.6 Day 3 lint
    - 对 Day 3 跑 P4（字段完整性，含 TST 段标记）+ P2（序列「上野 → 秋叶原 → 水道桥」无重复）+ P3（含 `Tokyo Dome` + `18:00`）+ P5（末尾指向 COGO RYOGOKU）
    - 输出"通过 / 失败 + 失败地点定位"
    - _Requirements: §5.1, §9.2, §10.3, §11.6, §13.1_

- [x] 5. Day 4（6 月 6 日 周六）— 新宿 / 中野（含 M2ビル + 矢口书店，7 个地点）
  - [x] 5.1 写 Day 4 文档头
    - 9 项元数据：6/6 周六 / 「新宿 / 中野（亚文化 + 御宅 + 黄金街夜游）」/ 序列「世田谷砧 → 千代田神保町 → 新宿 → 中野」/ COGO RYOGOKU 持续 / 行李无 / 硬约束无 / TST「有效中（剩余约 48 小时）」
    - _Requirements: §2.2, §6.1, §6.2, §6.3, §10.2, §10.5, §14.2_

  - [x] 5.2 写 Day 4 主体 — 世田谷砧外延段
    - 子区域导览段（标注为郊外建筑外延）
    - Place_Profile：`M2ビル`（隈研吾，1991；建筑师 / 建成年份 / 设计要点 / 是否进入参观）
    - _Requirements: §6.1, §6.3, §13.1, §13.3_

  - [x] 5.3 写 Day 4 主体 — 千代田神保町段
    - 子区域导览段
    - Place_Profile：`Yaguchi Book Store`（矢口书店；老书店选址典故 + 营业时间）
    - _Requirements: §6.1, §6.3, §13.1, §13.5_

  - [x] 5.4 写 Day 4 主体 — 新宿段
    - 子区域导览段
    - Place_Profile：`Shinjuku Gyoen National Garden`（新宿御苑）
    - Place_Profile：`Kabukicho`
    - Place_Profile：`Shinjuku Golden-Gai`（夜游）
    - Place_Profile：`Tokyo Tonkotsu Ramen Bankara Shinjuku Kabukicho`（餐饮：招牌菜单 + 价格 + 礼仪）
    - _Requirements: §6.1, §6.3, §13.1, §13.2, §13.6_

  - [x] 5.5 写 Day 4 主体 — 中野段
    - 子区域导览段
    - Place_Profile：`Mandarake Nakano`
    - _Requirements: §6.1, §6.3, §13.1, §13.5_

  - [x] 5.6 写 Day 4 文档尾
    - 当日交通费表（标 TST ✅ / ❌；小田急段 ❌、地铁段 ✅）
    - 当晚回程：新宿 / Golden-Gai → 都营大江户线 → 两国 → 步行至 COGO RYOGOKU
    - 次日提醒：6/7 山王祭开祭典礼（神事时刻）+ 赤坂—神乐坂—早稻田主题
    - _Requirements: §9.3, §9.4, §10.3, §11.6, §14.4_

  - [x] 5.7 Day 4 lint
    - 对 Day 4 跑 P4（字段完整性）+ P2（序列「世田谷砧 → 千代田神保町 → 新宿 → 中野」无重复）+ P5（末尾指向 COGO RYOGOKU）
    - _Requirements: §9.2, §11.6, §13.1_

- [x] 6. Day 5（6 月 7 日 周日）— 山王祭 + 隈研吾轴（7 个地点）
  - [x] 6.1 写 Day 5 文档头
    - 9 项元数据：6/7 周日 / 「赤坂 / 永田町 / 六本木 / 神乐坂 / 早稻田（山王祭 + 隈研吾）」/ 序列「赤坂 / 永田町 → 六本木 → 表参道（南青山）→ 神乐坂 / 早稻田」/ COGO RYOGOKU 持续 / 硬约束「09:00 山王祭神事 + 歌舞伎购票 23:55 准备」/ TST「有效中（剩余约 24 小时）」
    - _Requirements: §2.2, §6.1, §6.2, §8.1, §8.3, §10.2, §14.2_

  - [x] 6.2 写 Day 5 主体 — 赤坂 / 永田町段（含山王祭硬锚点）
    - 子区域导览段
    - Place_Profile：`Hie Shrine`（日枝神社），硬锚点标注「山王祭开祭典礼 + 神道仪式时刻表 + 可观礼区域 + 是否预约 / 排队 + 最近车站赤坂 / 溜池山王 / 国会议事堂前」
    - Place_Profile：`Akasaka-Mitsuke Station`
    - Place_Profile：`Akasaka Aonono Wagashi Main Store`（餐饮：招牌大福 + 价格 + 乔布斯典故 CSV 备注必须保留）
    - _Requirements: §8.1, §8.2, §8.3, §13.1, §13.2, §13.4, §13.6_

  - [x] 6.3 写 Day 5 主体 — 六本木 / 表参道（南青山）段
    - 子区域导览段
    - Place_Profile：`Roppongi`
    - Place_Profile：`Nezu Museum`（建筑：隈研吾 + 2009 + 竹林走廊 + 票价）
    - _Requirements: §6.1, §6.3, §13.1, §13.3_

  - [x] 6.4 写 Day 5 主体 — 神乐坂 / 早稻田段
    - 子区域导览段
    - Place_Profile：`Kagurazaka`
    - Place_Profile：`Waseda University`（村上春树图书馆 / 隈研吾 4 号馆，建筑字段必填）
    - _Requirements: §6.1, §6.3, §13.1, §13.3_

  - [x] 6.5 写 Day 5 文档尾
    - 当日交通费表（地铁段 TST ✅ 占比高）
    - 显式说明赤坂 ↔ 神乐坂跨度作为隈研吾主题环不可避免
    - 当晚回程：早稻田 → 东京 Metro 东西线 → 两国
    - _Requirements: §6.3, §9.3, §9.4, §9.5, §10.3, §11.6_

  - [x] 6.6 写 Day 5 文档尾 — 歌舞伎购票提醒（P3 硬要求）
    - 在文档末尾追加 blockquote 提醒：「明日 6/8（周一）为歌舞伎日 + KABUKI WEB 网络开售 6/8 凌晨 0:00 起 + 23:55 准备账号 + 22:00 前确认第五幕开演时间 + 开售 10 分钟内下单」
    - 含购票网址 https://www.kabukiweb.net/
    - _Requirements: §7.3, §7.4, §14.4_

  - [x] 6.7 Day 5 lint
    - 对 Day 5 跑 P4（字段完整性）+ P3（含 `Hie Shrine` + `山王祭` + 文末 `KABUKI WEB`）+ P5（末尾指向 COGO RYOGOKU）
    - _Requirements: §7.4, §8.1, §8.3, §11.6, §13.1_

- [x] 7. Day 6（6 月 8 日 周一）— 涩谷-银座连环 + 歌舞伎（16 个地点，最复杂）
  - [x] 7.1 写 Day 6 文档头
    - 9 项元数据：6/8 周一 / 「涩谷 / 原宿 / 代官山 + 银座 / 丸之内 / 日本桥（建筑时装 + 江户老铺，含歌舞伎座）」/ 序列「涩谷 → 原宿 / 表参道 → 代官山 →（涩谷换乘穿过）→ 银座 → 丸之内 / 东京站 → 日本桥」/ COGO RYOGOKU 持续 / 硬约束「歌舞伎座单幕席第五幕入场 + TST 当日失效」/ TST「有效中（剩余 X 小时，将在 6/8 同时刻失效）」
    - _Requirements: §2.2, §6.1, §6.2, §6.3, §7.1, §7.2, §10.1, §10.2, §14.2_

  - [x] 7.2 写 Day 6 上午段（涩谷 / 原宿 / 代官山，11 个地点）
    - 子区域导览段：明治神宫 9:00 开门 → 代代木公园 → Harakado / WITH HARAJUKU / 根津方向延展 → 代官山蔦屋午饭 → 涩谷 Sky 下午
    - Place_Profile：`Meiji Jingu`（神社字段：开闭园 + 收费 + 季节）
    - Place_Profile：`Meiji Jingu Museum`（建筑：隈研吾 / 2019）
    - Place_Profile：`Tokyu Plaza Harajuku "Harakado"`（建筑：平田晃久 / 2024）
    - Place_Profile：`WITH HARAJUKU HALL`（活动：6/6–9 竞赛单元时刻表 + 入场口）
    - Place_Profile：`LIFORK Harajuku`（活动：6/5–7 特别活动 — 注意展期已部分过；按 §6.6 处理）
    - Place_Profile：`Tsutaya Books Daikanyama`
    - Place_Profile：`Shibuya Sky`（观景：票价 + 预约）
    - Place_Profile：`Mandarake Shibuya`
    - Place_Profile：`LINE CUBE SHIBUYA`（演出场馆）
    - Place_Profile：`d47 Museum`
    - 跳跃 / 锚点辅助：（11 个地点已含 4 涩谷 + 5 原宿 + 1 代官山 + 1 跳跃方向标）
    - _Requirements: §6.1, §6.3, §6.6, §13.1, §13.3, §13.4, §13.6_

  - [x] 7.3 写 Day 6 下午段（银座 / 丸之内 / 日本桥，5 个地点）
    - 子区域导览段：东京 Metro 银座线一线串银座；歌舞伎座 17:00 / 18:00 入场为下午硬锚点
    - Place_Profile：`Apple 銀座`（购物：免税 / 国际寄送）
    - Place_Profile：`S. Watanabe woodcut prints`（购物：浮世绘版画 + 乔布斯典故 CSV 备注必须保留）
    - Place_Profile：`Kabukiza Theatre`（演出硬锚点：4 楼单幕席入口 + 第五场演目梗概 + 上演时长 + 不可换座 + 不可中途返场 + 票价区间 + 购票网址）
    - Place_Profile：`Tokyo Station`
    - Place_Profile：`Marunouchi Tokyo Station Square`
    - Place_Profile：`Nihonbashi Takashimaya Shopping Center`（购物：免税 + 国际寄送）
    - Place_Profile：`Namiki Yabusoba`（餐饮：「只蘸 15–20%」礼仪 + 价格区间）
    - _Requirements: §6.1, §6.3, §7.1, §7.2, §7.3, §13.1, §13.2, §13.4, §13.5_

  - [x] 7.4 写 Day 6 必要回头段说明（代官山 ↔ 涩谷换乘穿过）
    - 在文档主体合适位置插入 blockquote：代官山 → 东急东横线 → 涩谷站换 Metro 银座线 → 银座；东急东横线 ¥190（TST ❌）+ 银座线（TST ✅）；说明回头不可避免（无不经涩谷的直达线）
    - _Requirements: §9.5, §10.3_

  - [x] 7.5 写 Day 6 文档尾
    - 当日交通费表（含必要回头段票价 + TST 标记）
    - 当晚回程：歌舞伎座 → 东京 Metro 日比谷线 + 都营浅草线 → 两国 → 步行至 COGO RYOGOKU
    - 次日提醒：6/9 10:00 退房 + 行李寄存 / 拖行 + NRT / HND 两套路线 + 航班时刻提醒
    - _Requirements: §9.3, §9.4, §9.5, §10.3, §10.4, §11.3, §11.5, §11.6, §14.4_

  - [x] 7.6 Day 6 lint
    - 对 Day 6 跑 P4（字段完整性 + 16 个 Place_Profile 全字段在）+ P2（涩谷被穿过两次必须有显式 blockquote 标注）+ P3（含 `Kabukiza Theatre`）+ P5（末尾指向 COGO RYOGOKU）
    - _Requirements: §7.1, §9.2, §9.5, §11.6, §13.1_

- [x] 8. Day 7（6 月 9 日 周二）— 浅草 + 晴空塔（轻量收尾，5 个地点）
  - [x] 8.1 写 Day 7 文档头
    - 9 项元数据：6/9 周二 / 「浅草 / 两国 / 晴空塔（轻量收尾）」/ 序列「两国 → 浅草 → 押上 → 机场」/ 今晨 COGO RYOGOKU 10:00 退房 / 当晚离日 / 行李三方案（COGO 寄存 / 浅草投币柜 / 拖行）/ 硬约束「10:00 退房 + 航班时刻」/ TST「已失效」
    - _Requirements: §2.2, §6.4, §11.3, §11.5, §14.2_

  - [x] 8.2 写 Day 7 主体 — 浅草段
    - 子区域导览段
    - Place_Profile：`Edosoba Hosokawa`（江户荞麦 细川；午市 11:30 + 米其林一星 + 招牌菜单 + そば湯礼仪）
    - Place_Profile：`Kaminarimon Gate`（雷门）
    - Place_Profile：`Komiya Shoten Japanese Umbrella Shop`（购物：和伞 + 价格 + 国际寄送）
    - Place_Profile：`SMOCO SMOKING&COFFEE BAR 浅草橋店`
    - _Requirements: §6.1, §6.4, §13.1, §13.2, §13.5_

  - [x] 8.3 写 Day 7 主体 — 押上 / 晴空塔段
    - 子区域导览段
    - Place_Profile：`Tokyo Skytree`（观景：票价 + 预约 + 营业时间）
    - _Requirements: §6.1, §6.4, §13.1_

  - [x] 8.4 写 Day 7 文档尾
    - 当日交通费表（TST 已失效，全段 ❌）
    - 机场前往段（替代当晚回程）：从两国 / 押上出发 NRT（京成 Skyliner / N'EX）+ HND（都营浅草线直通京急 / 利木津巴士）两套参考路线 + 时间 + 票价
    - 行李策略说明：方案 A 寄存 COGO + 方案 B 浅草投币柜
    - _Requirements: §9.3, §9.4, §11.3, §11.5, §14.4_

  - [x] 8.5 Day 7 lint
    - 对 Day 7 跑 P4（字段完整性）+ P2（「两国—押上」二次出现属环线豁免，需有显式说明）+ P5（机场段含 `10:00 退房` + `NRT` + `HND`）
    - _Requirements: §9.2, §9.5, §11.3, §11.5, §13.1_

- [x] 9. 写 index.md 总览文档
  - [x] 9.1 列出 7 天的城市 / 主题 / 核心地点摘要
    - 每日一段：日期 + 主题 + 主要区域序列 + 核心地点 3–5 个
    - _Requirements: §12.5, §14.1, §14.2_

  - [x] 9.2 列出 10 个排除地点 + 排除原因摘要
    - 富士山 6 + Hikawa Clock Shop + Metro-City + Mitake + MoN Takanawa
    - _Requirements: §1.2, §12.5_

- [x] 10. 5 条 Lint 性质校验（最终交付前）
  - [x] 10.1 P1 覆盖完整性 lint
    - 扫描 7 个 day-N.md 的所有 `### ` 三级标题；断言 60 个保留 Title 各恰好出现一次；断言 10 个排除 Title 不出现
    - 输出"通过 / 失败 + 失败 Title 定位"
    - _Validates: §1.1, §1.2, §1.3, §6.1, §12.3, §12.4_

  - [x] 10.2 P2 序列单调性 lint
    - 解析每个 day-N.md 文档头的「主要区域序列」行，分割后断言去重等于原序列；若不等，则同文档内必须存在 `> 环线说明` blockquote
    - 输出"通过 / 失败 + 失败日定位"
    - _Validates: §2.3, §6.3, §9.1, §9.2, §9.5_

  - [x] 10.3 P3 硬锚点性 lint
    - grep day-3 含 `Tokyo Dome` + `18:00`
    - grep day-5 含 `Hie Shrine` + `山王祭`
    - grep day-6 含 `Kabukiza Theatre`
    - grep day-5 文档末尾含 `KABUKI WEB`
    - 输出"通过 / 失败 + 失败锚点定位"
    - _Validates: §5.1, §7.1, §7.2, §7.4, §8.1, §8.3_

  - [x] 10.4 P4 字段完整性 lint
    - 对每个 `### ` 块匹配 12 个必填子字段（中日罗马字三语标题 / 类型 / 位置 / 历史与背景 ≥ 150 字 / 看点 ≥ 3 / 推荐玩法 / 票务 / 双交通方案 / 周边联动 / 消费档次 / 注意事项 / CSV 原始备注 blockquote）
    - 对文档头匹配 9 项元数据；对文档尾匹配交通表 + 次日提醒
    - 对 6/5–6/8 期间累计 TST ✅ 段数断言 ≥ 12
    - 输出"通过 / 失败 + 失败地点定位"
    - _Validates: §2.2, §9.1, §9.3, §9.4, §10.3, §10.4, §13.1, §13.2, §13.3, §13.4, §13.5, §13.6, §13.7, §14.1, §14.2, §14.3, §14.4_

  - [x] 10.5 P5 收尾性 lint
    - 对 day-3 / day-4 / day-5 / day-6 末尾 grep `COGO RYOGOKU` + `两国`
    - 对 day-7 末尾 grep `机场` + `10:00 退房` + (`NRT` 或 `HND`)
    - 输出"通过 / 失败 + 失败日定位"
    - _Validates: §11.3, §11.5, §11.6, §12.2_

## Notes

- 任务按"日切片"组织：先做基础设施（任务 1）再依序填充 Day 1 → Day 7（任务 2–8），最后产出 index.md（任务 9）与 5 条 lint 性质校验（任务 10）。
- 每个 Place_Profile 是独立子任务，便于单独追踪 ≥ 150 字历史背景与 12 字段完整性。
- Day 6（16 个地点 + 歌舞伎硬锚点 + 必要回头段）拆得最细，分上午段（11 个）+ 下午段（5 个）+ 必要回头段说明 + 文档尾。
- Day 5 的「歌舞伎购票提醒」（任务 6.6）是 P3 性质的硬要求，作为独立子任务。
- 每个日内 lint 子任务（X.7 / 4.6 / 6.7 / 7.6 / 8.5）针对该日的 P2 + P4 + 相关 P3/P5 做即时验证；任务 10 是 7 个文档全集合的 5 条 lint 总验证。
- 排除清单（10 个）已固定，不会出现 Mitake 备选 / MoN Takanawa 备选等已剔除内容。

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4"] },
    { "id": 1, "tasks": ["2.1", "3.1", "4.1", "5.1", "6.1", "7.1", "8.1"] },
    { "id": 2, "tasks": ["2.2", "3.2", "4.2", "5.2", "6.2", "7.2", "8.2"] },
    { "id": 3, "tasks": ["2.3", "3.3", "4.3", "5.3", "6.3", "7.3", "8.3"] },
    { "id": 4, "tasks": ["2.4", "3.4", "4.4", "5.4", "6.4", "7.4"] },
    { "id": 5, "tasks": ["2.5", "3.5", "5.5"] },
    { "id": 6, "tasks": ["2.6", "3.6", "4.5", "5.6", "6.5", "7.5", "8.4"] },
    { "id": 7, "tasks": ["6.6"] },
    { "id": 8, "tasks": ["2.7", "3.7", "4.6", "5.7", "6.7", "7.6", "8.5"] },
    { "id": 9, "tasks": ["9.1"] },
    { "id": 10, "tasks": ["9.2"] },
    { "id": 11, "tasks": ["10.1", "10.2", "10.3", "10.4", "10.5"] }
  ]
}
```
