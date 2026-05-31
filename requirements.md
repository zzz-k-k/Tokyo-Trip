# Requirements Document

## Introduction

本 spec 用于为用户规划一次为期七天的关东地区旅行（横滨 → 镰仓 → 东京），起讫日期为 2026 年（或对应年份）的 **6 月 3 日至 6 月 9 日**。输入数据为 `Takeout/Saved/Favorite places.csv`（用户在 Google Maps 中收藏的兴趣地点）。

**最终交付物**为 7 个 markdown 文档（一天一个），每个文档对当天涉及的每个地点做"事无巨细"的深度介绍。本需求文档只规定每天涵盖**哪些地点**，不规定具体动线（步行顺序、分钟级时间表）。

规划必须满足：地理聚拢以最小化交通成本、不走回头路、充分利用东京地铁卡、命中两个硬时间锚点（东京巨蛋棒球赛、歌舞伎座单幕席），并尊重三段酒店的入住/退房时间。

## Glossary

- **行程规划器（Itinerary_Planner）**：本 spec 所交付的、把候选地点分配到 7 天的规划制品（包括最终的 7 个 md 文档）。
- **候选地点（Candidate_Place）**：`Favorite places.csv` 中 `Title` 列非空的一行。
- **排除地点（Excluded_Place）**：富士山相关地点与非日本地点的并集；具体清单见需求 1。
- **保留地点（Included_Place）**：候选地点扣除排除地点之后剩余的集合。
- **每日计划文档（Day_Plan_Document）**：7 个 markdown 文件之一，文件名格式 `day-{N}-{date}.md`（N ∈ 1..7）。
- **地点档案（Place_Profile）**：每日计划文档中针对单个保留地点的章节。
- **东京地铁卡（Tokyo_Subway_Ticket）**：可购买的 24/48/72 小时无限次乘车券，覆盖东京地铁（Tokyo Metro）全线与都营地下铁（Toei Subway）全线，**不覆盖** JR、私铁（小田急、东急、京急、京成、东武等）、新干线。
- **东京地铁卡有效期（TST_Validity_Window）**：从激活时刻起的连续 24/48/72 小时。
- **棒球赛事（Baseball_Event）**：6 月 5 日（周五）东京巨蛋（Tokyo Dome）「读卖巨人 vs 千叶罗德海洋」一战；16:00 开场，18:00 比赛开始。
- **歌舞伎事件（Kabuki_Event）**：在歌舞伎座（Kabukiza Theatre）观看「六月大歌舞伎 第五场 / 第五幕」的一次单幕席（一幕見席）观演。
- **单幕席（Hitomakumi_Seat）**：歌舞伎座 4 楼的当日 / 前一日开售的单幕观演席位，仅观看一幕，不可换座。
- **山王祭事件（Sannou_Festival_Event）**：6 月 7 日（周六）日枝神社（Hie Shrine）山王祭开祭典礼（神道仪式）。
- **入住时间（Checkin_Time）/ 退房时间（Checkout_Time）**：用户三段住宿的具体时点；参见需求 11。
- **走回头路（Backtracking）**：在同一日内或相邻两日间，向**已离开**的城市 / 主要区域反向移动一次或以上的行程段。
- **主要区域（Major_Area）**：在交通成本评估中视为一个"节点"的地理单元，例如「横滨港未来」「鎌倉/北鎌倉」「上野—秋叶原—两国」「新宿—涩谷—原宿」「丸之内—银座—日本桥」「六本木—赤坂」「文京区水道桥」等。

## Requirements

### 需求 1：从 CSV 中筛选保留地点

**用户故事：** 作为用户，我希望规划器自动剔除富士山相关与非日本的地点，这样剩下的地点都是真正可以纳入此次行程的候选项。

#### 验收标准（Acceptance Criteria）

1. THE 行程规划器 SHALL 读取 `Takeout/Saved/Favorite places.csv` 并使用 `Title` 列非空的所有行作为候选地点。
2. THE 行程规划器 SHALL 将以下 10 个地点标记为排除地点，且不出现在任何每日计划文档中：`Mount Fuji`、`忍野八海`、`Hirano beach`、`Arakura Fuji Sengen Shrine`、`Lake Yamanaka`、`Lake Kawaguchi`、`Hikawa Clock Shop`、`Metro-City`、`Mitake`、`MoN Takanawa: The Museum of Narratives`。

> **排除原因说明：**
>
> - `Mount Fuji`、`忍野八海`、`Hirano beach`、`Arakura Fuji Sengen Shrine`、`Lake Yamanaka`、`Lake Kawaguchi`：均为富士山相关地点，本次行程不安排富士山方向。
> - `Hikawa Clock Shop`、`Metro-City`：非日本地点（位于本次行程之外的国家 / 地区），自动剔除。
> - `Mitake`（御岳山）：地处奥多摩，整套登山徒步往返 ≥ 6 小时；用户决定本次行程保城内主题日，不再以"半天加进去"或"整日替换"的形式纳入御岳山一日徒步，故剔除。
> - `MoN Takanawa: The Museum of Narratives`：地理上位于高轮 / 品川，与本次行程第 6 日「涩谷—原宿—代官山—银座」主题日的地铁动线不顺路（需绕 JR 山手线一段且不在 Tokyo Subway Ticket 覆盖范围内）；用户决定本次行程暂时剔除。

3. WHEN 计算保留地点集合时，THE 行程规划器 SHALL 将保留地点定义为「候选地点 − 排除地点」。
4. THE 行程规划器 SHALL 将 `Narita International Airport` 与 `Haneda Airport` 视为参考地点：仅当某日行程包含机场出发或抵达时，才将其分配进对应的每日计划文档；否则不强制安排。
5. THE 行程规划器 SHALL 将 `COGO RYOGOKU` 视为住宿地点而非游览地点，不为其建立独立地点档案，但应在第 3–7 日文档的开头作为住宿信息列出。
6. IF 某个保留地点同时出现在用户后续追加的"必去"清单与某条排除规则中，THEN THE 行程规划器 SHALL 优先遵循排除规则并在文档中给出剔除原因。

### 需求 2：七日整体结构

**用户故事：** 作为用户，我希望整个行程按"横滨 → 镰仓 → 东京"由西向东推进，这样我从川崎出发到两国住宿，整体方向单调，不浪费交通时间。

#### 验收标准

1. THE 行程规划器 SHALL 将 7 天分配为：第 1 日（6 月 3 日 周二）横滨、第 2 日（6 月 4 日 周三）镰仓、第 3 日（6 月 5 日 周五）东京、第 4 日（6 月 6 日 周六）东京、第 5 日（6 月 7 日 周日）东京、第 6 日（6 月 8 日 周一）东京、第 7 日（6 月 9 日 周二）东京。
2. THE 行程规划器 SHALL 在每日计划文档头部以醒目格式列出：日期、星期、当日主题（横滨 / 镰仓 / 东京-子区域）、当日早晨出发地（前一晚住宿）、当晚住宿地。
3. WHEN 排布 7 天的城市顺序时，THE 行程规划器 SHALL 保持单调向东推进：川崎（夜 0）→ 横滨（夜 1）→ 两国（夜 2 起常驻）；不允许在同一日内回到已结束的城市。
4. WHERE 候选地点总数超过单日合理负载，THE 行程规划器 SHALL 优先保留具有强主题关联（如建筑师作品、动漫亚文化、文豪/江户老铺、隈研吾建筑串联）的地点，并在每日文档中说明取舍理由。

### 需求 3：第 1 日（6 月 3 日）— 横滨

**用户故事：** 作为用户，我希望第 1 日完整覆盖横滨港未来与伊势佐木一带的兴趣点，并在傍晚抵达 GuestHouse FUTARENO。

#### 验收标准

1. WHEN 安排第 1 日时，THE 行程规划器 SHALL 假定当日早晨 11:00 之前从 Hotel Plus Hostel TOKYO KAWASAKI（川崎）退房并寄存或携带行李前往横滨。
2. THE 行程规划器 SHALL 将以下保留地点全部分配到第 1 日：`Yokohama Station`、`Yokohama Landmark Tower`、`Yokohama Museum of Art`、`Yokohama Red Brick Warehouse`、`Yamashita Park`、`Sankeien Garden`、`Isezakichō`、`Shin-Yokohama Ramen Museum`。
3. WHEN 第 1 日结束时，THE 行程规划器 SHALL 将当晚住宿设定为 GuestHouse FUTARENO（横滨），入住时间 16:00 之后，并在文档中提示用户入住后再外出夜游伊势佐木 / 红砖仓库。
4. WHERE 第 1 日地点跨越「新横滨—港未来—本牧—伊势佐木」三个子区域，THE 行程规划器 SHALL 在文档中将地点按子区域聚合呈现，并标注每个子区域的主导交通方式（JR / 横滨地铁 / 港未来线 / 步行）。
5. IF 当日时间不足以覆盖全部 8 个地点，THEN THE 行程规划器 SHALL 在文档中明确标注哪些地点为「核心」（必去）、哪些为「机动」（可舍弃）；其中 `Sankeien Garden` 与 `Yokohama Museum of Art` 必须列为核心。

### 需求 4：第 2 日（6 月 4 日）— 镰仓

**用户故事：** 作为用户，我希望第 2 日把镰仓的所有兴趣点走完，并在傍晚带着行李抵达东京两国的 COGO RYOGOKU。

#### 验收标准

1. WHEN 安排第 2 日时，THE 行程规划器 SHALL 假定当日早晨 11:00 之前从 GuestHouse FUTARENO 退房并携带行李或使用宅配。
2. THE 行程规划器 SHALL 将以下保留地点全部分配到第 2 日：`Engaku-ji`、`Meigetsu-in`、`Tsurugaoka Hachimangu`、`Kotoku-in`、`Kamakurakōkō-Mae Station`、`Shichirigahama Beach`。
3. WHEN 排布第 2 日的镰仓内部顺序时，THE 行程规划器 SHALL 推荐「北镰仓（圆觉寺 → 明月院）→ 镰仓站（鹤冈八幡宫）→ 长谷（高德院）→ 江之电沿线（七里滨 → 镰仓高校前）」的单向行进路径，避免在 JR 横须贺线 / 江之电之间反复折返。
4. WHEN 第 2 日结束时，THE 行程规划器 SHALL 安排用户在 16:00 之后从镰仓 / 藤泽方向乘 JR 东海道线或湘南新宿线返回东京，并在 COGO RYOGOKU（两国）入住。
5. WHERE 第 2 日是 6 月梅雨季，THE 行程规划器 SHALL 在 `Meigetsu-in` 的地点档案中明确标注当日早入园（建议开门进园）以观赏明月院蓝（绣球花）的最佳时段，并提供雨天替代方案。
6. IF 用户当日选择把行李从横滨直接宅配到两国 COGO RYOGOKU，THEN THE 行程规划器 SHALL 在文档中给出宅配（黑猫 / 佐川）下单与交付时点的提示。

### 需求 5：第 3 日（6 月 5 日 周五）— 东京（含棒球）

**用户故事：** 作为用户，我希望第 3 日的整条动线在傍晚自然汇入东京巨蛋，让我准时坐进 18:00 开打的棒球赛。

#### 验收标准

1. THE 行程规划器 SHALL 将 `Tokyo Dome` 分配到第 3 日，并在地点档案中标注硬约束：「6 月 5 日 16:00 开场、18:00 比赛开始，巨人 vs 罗德」。
2. WHEN 第 3 日下午 ≥ 16:30 时，THE 行程规划器 SHALL 要求用户已抵达水道桥 / 后乐园站附近，地点档案中应明确入场口、检票流程与禁带物品。
3. THE 行程规划器 SHALL 将以下保留地点分配到第 3 日，并按"自西向东最终落点东京巨蛋"的方向聚合：建议安排 `Ueno Park`、`Tokyo National Museum`、`Kyū-Iwasaki-tei Gardens`、`Akihabara`、`Akihabara Electric Town`、`Mandarake Complex`、`Pop Life Department M's` 中的若干个；最终是否全部纳入第 3 日由规划器在文档中说明取舍理由，但 `Tokyo Dome` 必入。
4. IF 第 3 日下午地点过多导致 16:30 前无法抵达水道桥，THEN THE 行程规划器 SHALL 把超载的地点改派到第 4–7 日中地理上相容的某一日。
5. WHEN 第 3 日结束时，THE 行程规划器 SHALL 安排用户从水道桥 / 后乐园 / 饭田桥 经都营大江户线 / 都营浅草线返回 COGO RYOGOKU（两国）。
6. WHERE 用户尚未办理东京地铁卡（Tokyo_Subway_Ticket），THE 行程规划器 SHALL 建议用户在第 3 日上午激活东京地铁卡 72 小时券（覆盖 6/5–6/8），并在第 3 日文档开头明确激活地点（建议在地铁站窗口或便利店购入）。

### 需求 6：第 4 日至第 7 日（6 月 6 日–9 日）— 东京其余地点

**用户故事：** 作为用户，我希望东京剩余的几十个地点按"主题 + 区域"被合理切成 4 天，每天的地点都互相靠近。

#### 验收标准

1. THE 行程规划器 SHALL 将以下保留地点全部、且仅一次地分配到第 4–7 日中的某一天：
   `S. Watanabe woodcut prints`、`Nezu Museum`、`WITH HARAJUKU HALL`、`SMOCO SMOKING&COFFEE BAR 浅草橋店`、`Kaminarimon Gate`、`LINE CUBE SHIBUYA`、`Mandarake Nakano`、`Kabukicho`、`Mandarake Shibuya`、`M2ビル`、`Edosoba Hosokawa`、`Tokyu Plaza Harajuku "Harakado"`、`Yaguchi Book Store`、`Tokyo Tonkotsu Ramen Bankara Shinjuku Kabukicho`、`TabioMEN`、`Akasaka-Mitsuke Station`、`Euro Live`、`Tokyo Station`、`Marunouchi Tokyo Station Square`、`Nihonbashi Takashimaya Shopping Center`、`Namiki Yabusoba`、`LIFORK Harajuku`、`Hie Shrine`、`Shinjuku Golden-Gai`、`Komiya Shoten Japanese Umbrella Shop`、`Tokyo Skytree`、`Kabukiza Theatre`、`Tsutaya Books Daikanyama`、`Kagurazaka`、`d47 Museum`、`Shibuya Sky`、`Waseda University`、`Shinjuku Gyoen National Garden`、`RAGTAG`、`Akasaka Aonono Wagashi Main Store`、`Roppongi`、`Meiji Jingu`、`Meiji Jingu Museum`、`Apple 銀座`、`Tabio`。
   （第 3 日已经分配走的 `Akihabara`、`Akihabara Electric Town`、`Mandarake Complex`、`Pop Life Department M's`、`Ueno Park`、`Tokyo National Museum`、`Kyū-Iwasaki-tei Gardens`、`Tokyo Dome` 不重复出现。）
2. THE 行程规划器 SHALL 为第 4–7 日各设定一个主题，且四日之间不得共享主题；推荐主题集合为：「新宿—中野（亚文化 + 御宅 + 黄金街夜游）」、「涩谷—原宿—代官山（建筑 + 时装 + 美术馆）」、「丸之内—银座—日本桥（江户老铺 + 文房 + 百货）」、「赤坂—六本木—神乐坂—早稻田（隈研吾建筑 + 文豪江户）」中四选四。
3. WHEN 同一主题的地点跨多个区域时，THE 行程规划器 SHALL 在该日地点序列中按"环线 / 单向"顺序排布（如新宿 → 中野不返回新宿、涩谷 → 原宿 → 代官山不返回涩谷），不得出现跨区域反复横跳。
4. WHERE 第 7 日（6/9）当日 10:00 必须从 COGO RYOGOKU 退房，THE 行程规划器 SHALL 把第 7 日设为「轻量日」：当日地点数量 ≤ 第 4–6 日单日地点数量的中位数；并在文档中预留行李寄存与机场前往时间（若用户当日离日）。
5. IF 用户在第 4–7 日中存在尚未消费完的东京地铁卡时间，THEN THE 行程规划器 SHALL 在文档中提示当日剩余的有效小时数，并优先选用 Tokyo Metro / Toei 路线。
6. WHERE 候选地点中存在仅有日期范围说明的展览 / 放映（如 `WITH HARAJUKU HALL` 6/6–9 竞赛单元、`Euro Live` 6/2–4 竞赛单元、`LIFORK Harajuku` 6/5–7 特别活动、`MoN Takanawa` 开幕红毯），THE 行程规划器 SHALL 把这些地点排进其展期与本行程交集的某一日；其中 `Euro Live` 因展期早于第 3 日，应在文档中标注「展期已结束」并改为外观打卡或剔除。

### 需求 7：歌舞伎座单幕席选日与购票

**用户故事：** 作为用户，我希望规划器从 6/3–6/9 中选一天看一场「六月大歌舞伎 第五场 / 第五幕」，并提醒我前一天在线订单幕席。

#### 验收标准

1. THE 行程规划器 SHALL 将 `Kabukiza Theatre` 分配到 6 月 3 日至 6 月 9 日中的某一天，作为当日地点之一。
2. WHEN 选择歌舞伎日时，THE 行程规划器 SHALL 优先选 6 月 6 日（周六）、6 月 8 日（周一）、或 6 月 9 日（周二）中的一天，且当日不得与 `Tokyo Dome`（6/5 必占）、镰仓全日（6/4）、横滨全日（6/3）冲突。
3. THE Kabuki_Event 地点档案 SHALL 包含：单幕席当日 / 前一日的在线开售时刻、购票网址、票价区间、入场口（4 楼专用入口）、所选幕次（第五场）的演目梗概、上演时长、座席规则（不可换座、不可中途返场）。
4. WHEN 当日选定后，THE 行程规划器 SHALL 在选定日的**前一天**的每日计划文档末尾加入提醒：「明日 X 月 X 日为歌舞伎日，请于今日某时（按官方开售时刻）登录歌舞伎 WEB 单幕席购票」。
5. IF 选定日为 6 月 9 日（周二，最后一日），THEN THE 行程规划器 SHALL 在文档中评估第五场的开演与散场时间是否与机场航班冲突；若冲突则改选 6 月 6 日或 6 月 8 日。

### 需求 8：山王祭开祭典礼（6 月 7 日）

**用户故事：** 作为用户，我希望 6 月 7 日的东京日里能去日枝神社看山王祭开祭典礼。

#### 验收标准

1. THE 行程规划器 SHALL 将 `Hie Shrine` 分配到第 5 日（6 月 7 日 周日）。
2. THE Hie Shrine 地点档案 SHALL 标注：山王祭开祭典礼是神道仪式、当日的神事时刻表、可观礼区域与是否需要预约 / 排队、最近的地铁站（赤坂、溜池山王、国会议事堂前）。
3. WHEN 6 月 7 日同时安排其他地点时，THE 行程规划器 SHALL 让当日地点位于「赤坂—永田町—六本木—神乐坂」沿线，使日枝神社成为当日的地理重心而非外延点。

### 需求 9：交通成本最小化与不走回头路

**用户故事：** 作为用户，我希望整张行程图看起来不像在城市里来回拉扯，而是一条尽量单调推进的路线。

#### 验收标准

1. THE 行程规划器 SHALL 在每日计划文档头部给出「当日主要区域序列」（例如「上野 → 秋叶原 → 水道桥」），且序列中相邻两个主要区域之间应可由单一交通段（一次换乘以内）连通。
2. WHEN 评估某日是否走回头路时，THE 行程规划器 SHALL 验证：当日**主要区域序列**中，没有任何主要区域出现两次（出发地与终点恰好相同的环线除外，且环线必须明示）。
3. THE 行程规划器 SHALL 在每日计划文档结尾给出「当日推算交通费」清单，列出每段移动的方式（JR / 地铁 / 私铁 / 步行）、单段票价或在 Tokyo_Subway_Ticket 覆盖范围内的标记、估算合计金额。
4. WHEN 跨日衔接（前一晚住宿 → 当日首个地点；当日末个地点 → 当晚住宿）需要交通时，THE 行程规划器 SHALL 把这两段也纳入"当日交通"计算并显式列出。
5. IF 某日的"主要区域序列"中存在重复主要区域，THEN THE 行程规划器 SHALL 在文档中显式说明回头的不可避免性（例如：当日歌舞伎座结束后必须回到两国住宿）并给出该回头段的票价与必要性。

### 需求 10：东京地铁卡使用率最大化

**用户故事：** 作为用户，我会买东京地铁卡，希望在它的有效窗口里被"压榨"到极限。

#### 验收标准

1. THE 行程规划器 SHALL 在第 3 日的文档中推荐 Tokyo Subway Ticket **72 小时券**，并将其有效期界定为 6 月 5 日激活时刻至 6 月 8 日同一时刻。
2. WHEN TST_Validity_Window 处于活动状态时，THE 行程规划器 SHALL 把该时间段内市内移动的**默认交通方式**设为 Tokyo Metro / Toei Subway，仅在 Metro / Toei 完全不到的目的地（如代官山仅东急东横线、镰仓需 JR、新横滨需 JR、机场需京急 / 京成）才允许使用 JR / 私铁。
3. THE 行程规划器 SHALL 在第 3–6 日的「当日推算交通费」清单中，单独标记每一段「TST 已覆盖」或「TST 未覆盖（XXX 元）」。
4. WHEN 计算 TST 的"压榨度"时，THE 行程规划器 SHALL 在第 6 日（TST 失效日）文档结尾给出三日内 Tokyo Metro / Toei 的累计乘车次数估算，且该次数 SHALL ≥ 12 次（对应单日 ≥ 4 次的强使用强度）。
5. WHERE 镰仓日（6/4）与可能的横滨日（6/3）以 JR / 私铁为主，THE 行程规划器 SHALL 不将这两日纳入 TST 有效期，避免把 TST 浪费在地铁不到达的区域。
6. IF 用户已购入但尚未激活 TST，THEN THE 行程规划器 SHALL 在第 3 日开头明确「在 6 月 5 日上午第一次乘地铁前激活」的指引，并提醒「激活以乘车刷卡为准，不是购买时刻」。

### 需求 11：住宿、行李与退房 / 入住约束

**用户故事：** 作为用户，我希望规划尊重三段酒店的入住与退房时间，并在有行李那两天给出可执行的搬运方案。

#### 验收标准

1. THE 行程规划器 SHALL 在第 1 日文档头部标注：当日早晨 11:00 从 Hotel Plus Hostel TOKYO KAWASAKI 退房，当晚 16:00 之后入住 GuestHouse FUTARENO（横滨）。
2. THE 行程规划器 SHALL 在第 2 日文档头部标注：当日早晨 11:00 从 GuestHouse FUTARENO 退房，当晚 16:00 之后入住 COGO RYOGOKU（两国）。
3. THE 行程规划器 SHALL 在第 7 日文档头部标注：当日早晨 10:00 从 COGO RYOGOKU 退房。
4. WHEN 第 1 日与第 2 日存在跨城市搬运行李的情况时，THE 行程规划器 SHALL 在文档中给出至少一种行李解决方案（车站投币柜 Coin Locker / 酒店寄存 / 黑猫宅配 / 佐川宅配）并附操作要点。
5. WHERE 第 7 日用户可能携带行李前往机场，THE 行程规划器 SHALL 在第 7 日文档中给出从两国出发到 NRT（成田 / 京成 Skyliner 或 N'EX）和 HND（羽田 / 京急或机场利木津）的两种参考路线、所需时间与票价区间。
6. WHILE 第 3–7 日常驻 COGO RYOGOKU 期间，THE 行程规划器 SHALL 在每日文档末尾标注「当晚回程：当日末个地点 → 两国站 → 步行至 COGO RYOGOKU」的预期总时长。

### 需求 12：最终交付物 — 7 个 markdown 文档

**用户故事：** 作为用户，我希望最终拿到 7 个独立的 markdown 文件，一天一个，方便我随身阅读。

#### 验收标准

1. THE 行程规划器 SHALL 在 `.kiro/specs/japan-7day-itinerary/` 目录下，**或**用户指定的最终输出目录下，创建 7 个 markdown 文件，文件名格式为 `day-{N}-{YYYY-MM-DD}.md`，N ∈ 1..7。
2. THE 行程规划器 SHALL 保证 7 个文件互相独立，每一个文件都可单独打印 / 单独阅读，不依赖其他文件的上下文（必要的硬约束如「歌舞伎需前一晚购票」由前一日文档显式重复说明）。
3. WHEN 同一个保留地点理论上可纳入多个日期时，THE 行程规划器 SHALL 把它仅写入唯一一个每日计划文档，避免内容重复。
4. THE 行程规划器 SHALL 保证「每个保留地点都恰好出现在一个每日计划文档中（机场地点除非真的使用否则可不出现）」这一覆盖完整性。
5. THE 行程规划器 SHALL 在 7 个文件之外，再交付一个 `index.md` 总览文件（可选），列出 7 天的城市 / 主题 / 核心地点；index.md 不替代每日文档。

### 需求 13：每个地点档案必须包含的内容字段

**用户故事：** 作为用户，我希望每个地点都被"事无巨细"地讲清楚，越深度越好。

#### 验收标准

1. THE 地点档案 SHALL 至少包含以下字段，每个字段单独成段或单独成行：
   - 地点中文名 / 日文名 / 罗马字名
   - 类型（庭园 / 美术馆 / 神社 / 商业街 / 拉面店 / 体育场 / 其他）
   - 位置（地址 + 最近车站 + 步行分钟数）
   - 历史与背景（≥ 150 字的介绍）
   - 看点（核心看点列表，至少 3 条）
   - 推荐玩法（用户在此停留的"动作"，例如「在三层宝塔下拍一张」「点 100% 十割荞麦面 Seiro」）
   - 票务 / 营业时间（含定休日；价格写入实际数字而非"门票便宜"等模糊表达）
   - 交通到达（从前一个地点出发、与从两国 COGO RYOGOKU 出发两套路线，至少给出一种）
   - 周边联动（步行 10 分钟内可去的其他保留地点）
   - 消费档次（人均日元区间）
   - 注意事项（拍照禁忌 / 着装 / 排队 / 雨天替代 / 节假日等）
   - 用户原始备注的引用（来自 CSV `Note` 列；如果有人物典故如乔布斯版画 / 大福，必须保留）
2. WHERE 地点是餐饮店（如 `Edosoba Hosokawa`、`Namiki Yabusoba`、`Tokyo Tonkotsu Ramen Bankara Shinjuku Kabukicho`、`Akasaka Aonono Wagashi Main Store`），THE 地点档案 SHALL 额外包含：招牌菜单 + 价格区间、点单暗号 / 礼仪（如 Namiki Yabusoba 的"只蘸 15–20%"传统）。
3. WHERE 地点是建筑作品（如 `Nezu Museum`、`M2ビル`、`Meiji Jingu Museum`、`Waseda University` 村上春树图书馆、`MoN Takanawa`），THE 地点档案 SHALL 额外包含：建筑师姓名、建成年份、设计要点、可否进入参观、参观免费 / 收费。
4. WHERE 地点涉及活动 / 演出（如 `Tokyo Dome` 棒球、`Kabukiza Theatre` 歌舞伎、`Hie Shrine` 山王祭、`WITH HARAJUKU HALL` / `LIFORK Harajuku` / `MoN Takanawa` 电影节单元），THE 地点档案 SHALL 额外包含：活动当日时间表、票价 / 是否需预约、入场口与流程、可否带食物 / 摄影。
5. WHERE 地点是商品 / 购物点（如 `Tabio` / `TabioMEN`、`RAGTAG`、`Komiya Shoten Japanese Umbrella Shop`、`S. Watanabe woodcut prints`、`Apple 銀座`、`Nihonbashi Takashimaya`），THE 地点档案 SHALL 额外包含：主营商品类目、价格区间、是否支持免税、是否支持寄国际。
6. WHERE 地点是公园 / 庭园 / 神社 / 寺庙（如 `Sankeien Garden`、`Yamashita Park`、`Ueno Park`、`Shinjuku Gyoen`、`Meiji Jingu`、`Engaku-ji`、`Meigetsu-in`、`Tsurugaoka Hachimangu`、`Kotoku-in`、`Hie Shrine`、`Kyū-Iwasaki-tei Gardens`），THE 地点档案 SHALL 额外包含：开闭园时间、是否收费、最佳季节 / 最佳时段、是否允许带饮食 / 摄影。
7. IF 某地点的某个字段无法在公开信息内核实，THEN THE 行程规划器 SHALL 在该字段标注「待用户实地确认」并给出可查询的官方网址。

### 需求 14：文档语言与格式

**用户故事：** 作为用户，我希望最终的 md 文档统一使用中文撰写，方便我直接阅读。

#### 验收标准

1. THE 行程规划器 SHALL 使用简体中文撰写每日计划文档与 index.md；地名 / 店名 / 演目名等专有名词在首次出现时以「中文（日文 / 英文原名）」的双语并列形式给出，之后段落可只用中文。
2. THE 行程规划器 SHALL 使用 markdown 二级标题（`##`）划分日内子区域、使用三级标题（`###`）作为单个地点档案的标题。
3. WHEN 引用价格时，THE 行程规划器 SHALL 使用「日元 / JPY」单位，避免 RMB 换算；如必要给出 RMB 估算时，应同时标注汇率假设。
4. THE 行程规划器 SHALL 在每个每日计划文档末尾追加「次日提醒」段落，重复次日的硬约束（如棒球票、歌舞伎购票、退房时间、机场航班）。
