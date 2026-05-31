#!/usr/bin/env python3
"""
Task 1.2: 抽取 60 个 Place 元数据卡片

读取 Takeout/Saved/Favorite places.csv，按 design.md 的规则：
  1. 跳过 Title 为空的行
  2. 标注 10 个排除地点（excluded）
  3. 分离 2 个机场（airports）与 1 个住宿（lodgings）
  4. 对 included 推断 type / major_area / sub_area / assigned_day
  5. 输出 places.json

补充：design.md 中需要 Place_Profile 的 `Kabukiza Theatre`（§7.1）不在 CSV 中，
作为 phantom 包含项追加，csv_note 留空，url 取官方网站。
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path("/Users/shiwen/Downloads/CodexProjects/Travel_Plan")
CSV_PATH = ROOT / "Takeout" / "Saved" / "Favorite places.csv"
OUT_PATH = ROOT / ".kiro" / "specs" / "japan-7day-itinerary" / "places.json"

# ---------------------------------------------------------------------------
# 1. design.md "排除规则" — 10 条
EXCLUDED_TITLES = {
    "Mount Fuji",
    "忍野八海",
    "Hirano beach",
    "Arakura Fuji Sengen Shrine",
    "Lake Yamanaka",
    "Lake Kawaguchi",
    "Hikawa Clock Shop",
    "Metro-City",
    "Mitake",
    "MoN Takanawa: The Museum of Narratives",
}

EXCLUSION_REASONS = {
    "Mount Fuji": "富士山本体；本次行程跳过富士五湖区域。",
    "忍野八海": "富士山外围水景；用户备注「据说很坑」。",
    "Hirano beach": "山中湖畔的天鹅与富士山观景点；富士山外围。",
    "Arakura Fuji Sengen Shrine": "新仓山浅间神社（富士山观景塔）；富士山外围。",
    "Lake Yamanaka": "山中湖；富士山外围。",
    "Lake Kawaguchi": "河口湖；富士山外围。",
    "Hikawa Clock Shop": "山梨县富士吉田市本町通的钟表店；地理上不在关东。",
    "Metro-City": "place_id 前缀 0x35b26531 不属于日本；该地点为首尔 Metro-City，韩国数据。",
    "Mitake": "御岳山位于奥多摩，整套登山徒步往返 ≥ 6 小时；用户决定保城内主题日。",
    "MoN Takanawa: The Museum of Narratives": "高轮 / 品川一带，与 Day 6 涩谷—银座主题日动线不顺路（需绕 JR 山手线，非 TST 覆盖）。",
}

AIRPORT_TITLES = {"Narita International Airport", "Haneda Airport"}
LODGING_TITLES = {"COGO RYOGOKU"}

# ---------------------------------------------------------------------------
# 2. 主要区域（Major_Area）枚举（design.md）
# 同时给出每个保留地点的 major_area / sub_area / day / type
# 列表来源：requirements §3.2 / §4.2 / §5.3 / §6.1 + design 主体说明
PLACE_PLAN = {
    # ---------------- Day 1 — 横滨（8）----------------
    "Shin-Yokohama Ramen Museum":
        dict(day=1, type="餐饮 / 主题博物馆", major_area="新横滨",
             sub_area="新横滨站北口"),
    "Yokohama Station":
        dict(day=1, type="交通节点", major_area="横滨—港未来",
             sub_area="横滨站"),
    "Yokohama Landmark Tower":
        dict(day=1, type="观景 / 摩天楼", major_area="横滨—港未来",
             sub_area="港未来 21 号街区"),
    "Yokohama Museum of Art":
        dict(day=1, type="美术馆", major_area="横滨—港未来",
             sub_area="港未来美术馆段"),
    "Yokohama Red Brick Warehouse":
        dict(day=1, type="商业街 / 历史建筑", major_area="横滨—港未来",
             sub_area="新港地区"),
    "Yamashita Park":
        dict(day=1, type="公园", major_area="横滨—山下公园 / 元町",
             sub_area="山下公园海岸线"),
    "Sankeien Garden":
        dict(day=1, type="庭园", major_area="横滨—山下公园 / 元町",
             sub_area="本牧三之谷（庭园核心）"),
    "Isezakichō":
        dict(day=1, type="商业街", major_area="横滨—伊势佐木 / 关内",
             sub_area="伊势佐木商店街（夜游）"),

    # ---------------- Day 2 — 镰仓（6）----------------
    "Engaku-ji":
        dict(day=2, type="寺院", major_area="北镰仓",
             sub_area="JR 北镰仓站东口"),
    "Meigetsu-in":
        dict(day=2, type="寺院 / 庭园", major_area="北镰仓",
             sub_area="明月谷（绣球花路径）"),
    "Tsurugaoka Hachimangu":
        dict(day=2, type="神社", major_area="镰仓中心",
             sub_area="若宫大路顶端"),
    "Kotoku-in":
        dict(day=2, type="寺院 / 大佛", major_area="长谷",
             sub_area="长谷大佛境内"),
    "Shichirigahama Beach":
        dict(day=2, type="海岸 / 观景", major_area="江之电沿线",
             sub_area="七里滨海岸（江之电七里滨站）"),
    "Kamakurakōkō-Mae Station":
        dict(day=2, type="交通节点 / 观景打卡", major_area="江之电沿线",
             sub_area="镰仓高校前道口"),

    # ---------------- Day 3 — 上野 / 秋叶原 / 水道桥（8）----------------
    "Ueno Park":
        dict(day=3, type="公园", major_area="东京—上野 / 本乡 / 东大",
             sub_area="上野恩赐公园"),
    "Tokyo National Museum":
        dict(day=3, type="博物馆", major_area="东京—上野 / 本乡 / 东大",
             sub_area="上野公园北端（东京国立博物馆本馆 + 东洋馆）"),
    "Kyū-Iwasaki-tei Gardens":
        dict(day=3, type="庭园 / 历史建筑", major_area="东京—上野 / 本乡 / 东大",
             sub_area="池之端（旧岩崎邸庭园）"),
    "Akihabara":
        dict(day=3, type="商业街", major_area="东京—秋叶原",
             sub_area="秋叶原中央通"),
    "Akihabara Electric Town":
        dict(day=3, type="商业街 / 御宅", major_area="东京—秋叶原",
             sub_area="电器街（昭和通西侧）"),
    "Mandarake Complex":
        dict(day=3, type="购物 / 御宅", major_area="东京—秋叶原",
             sub_area="秋叶原 8 层 Mandarake 总店"),
    "Pop Life Department M's":
        dict(day=3, type="购物 / 御宅", major_area="东京—秋叶原",
             sub_area="秋叶原成人塔"),
    "Tokyo Dome":
        dict(day=3, type="体育场 / 演出", major_area="东京—水道桥 / 后乐园",
             sub_area="后乐园 / 水道桥（巨人主场）"),

    # ---------------- Day 4 — 新宿 / 中野（7）----------------
    "M2ビル":
        dict(day=4, type="建筑（隈研吾，1991）",
             major_area="东京—世田谷砧（外延）",
             sub_area="祖师谷大藏 / 砧；现为东京 Memolead 殡仪馆"),
    "Yaguchi Book Store":
        dict(day=4, type="书店 / 老铺", major_area="东京—千代田 / 神保町",
             sub_area="神保町书店街（街边书架）"),
    "Shinjuku Gyoen National Garden":
        dict(day=4, type="庭园 / 公园", major_area="东京—新宿",
             sub_area="新宿御苑（千驮谷 / 大木户 / 新宿门）"),
    "Kabukicho":
        dict(day=4, type="商业街 / 夜游", major_area="东京—新宿",
             sub_area="歌舞伎町一番街"),
    "Shinjuku Golden-Gai":
        dict(day=4, type="商业街 / 夜游", major_area="东京—新宿",
             sub_area="花园神社旁的小巷酒场群（夜游）"),
    "Tokyo Tonkotsu Ramen Bankara Shinjuku Kabukicho":
        dict(day=4, type="餐饮（豚骨拉面）", major_area="东京—新宿",
             sub_area="歌舞伎町（YouTube 直播摄像头位）"),
    "Mandarake Nakano":
        dict(day=4, type="购物 / 御宅", major_area="东京—中野",
             sub_area="中野百老汇商城 2–4 楼"),

    # ---------------- Day 5 — 赤坂 / 六本木 / 神乐坂 / 早稻田（7）----------------
    "Hie Shrine":
        dict(day=5, type="神社", major_area="东京—赤坂 / 永田町",
             sub_area="日枝神社（山王祭开祭典礼）"),
    "Akasaka-Mitsuke Station":
        dict(day=5, type="交通节点", major_area="东京—赤坂 / 永田町",
             sub_area="赤坂见附站周边"),
    "Akasaka Aonono Wagashi Main Store":
        dict(day=5, type="餐饮（和菓子）", major_area="东京—赤坂 / 永田町",
             sub_area="赤坂青野本店（乔布斯大福）"),
    "Roppongi":
        dict(day=5, type="商业街", major_area="东京—六本木",
             sub_area="六本木 Hills / Midtown 之间"),
    "21_21 Design Sight":
        dict(day=5, type="美术馆 / 建筑（安藤忠雄，2007）",
             major_area="东京—六本木",
             sub_area="东京 Midtown Garden"),
    "Nezu Museum":
        dict(day=5, type="美术馆 / 建筑（隈研吾，2009）",
             major_area="东京—原宿 / 表参道（南青山段）",
             sub_area="南青山 6 丁目（竹林走廊 + 庭园）"),
    "Kagurazaka":
        dict(day=5, type="商业街 / 历史巷弄", major_area="东京—神乐坂 / 早稻田",
             sub_area="神乐坂坂道—兵库横丁"),
    "Waseda University":
        dict(day=5, type="校园 / 建筑（隈研吾 4 号馆）",
             major_area="东京—神乐坂 / 早稻田",
             sub_area="早稻田校园 4 号馆（村上春树图书馆）"),

    # ---------------- Day 6 — 涩谷 / 原宿 / 代官山 + 银座 / 丸之内 / 日本桥 ----------------
    # 上午段（涩谷 / 原宿 / 代官山）
    "Meiji Jingu":
        dict(day=6, type="神社", major_area="东京—原宿 / 表参道",
             sub_area="代代木公园西侧（明治神宫本殿）"),
    "Meiji Jingu Museum":
        dict(day=6, type="美术馆 / 建筑（隈研吾，2019）",
             major_area="东京—原宿 / 表参道",
             sub_area="明治神宫南参道入口附近"),
    "Tokyu Plaza Harajuku “Harakado”":
        dict(day=6, type="商业街 / 建筑（平田晃久，2024）",
             major_area="东京—原宿 / 表参道",
             sub_area="神宫前神宫桥交叉口（屋顶花园）"),
    "WITH HARAJUKU HALL":
        dict(day=6, type="演出 / 活动会场",
             major_area="东京—原宿 / 表参道",
             sub_area="WITH HARAJUKU 大厦（6/6–9 竞赛单元）"),
    "LIFORK Harajuku":
        dict(day=6, type="演出 / 活动会场",
             major_area="东京—原宿 / 表参道",
             sub_area="原宿（6/5–7 特别活动；展期与 Day 6 部分重叠）"),
    "Tsutaya Books Daikanyama":
        dict(day=6, type="书店 / 复合文化", major_area="东京—代官山",
             sub_area="代官山 T-SITE"),
    "Shibuya Sky":
        dict(day=6, type="观景", major_area="东京—涩谷",
             sub_area="涩谷 Scramble Square 屋顶展望"),
    "Mandarake Shibuya":
        dict(day=6, type="购物 / 御宅", major_area="东京—涩谷",
             sub_area="涩谷 BEAM 旁地下店"),
    "LINE CUBE SHIBUYA":
        dict(day=6, type="演出 / 公会堂", major_area="东京—涩谷",
             sub_area="涩谷区立公会堂（电影节颁奖礼场）"),
    "d47 Museum":
        dict(day=6, type="美术馆 / 设计", major_area="东京—涩谷",
             sub_area="涩谷 Hikarie 8F"),
    "Euro Live":
        dict(day=6, type="演出 / 活动会场（展期已结束）",
             major_area="东京—涩谷",
             sub_area="道玄坂 Euro Space 旁；展期 6/2–4，本次行程仅外观"),
    "TabioMEN":
        dict(day=6, type="购物（袜子）", major_area="东京—涩谷",
             sub_area="涩谷 / 表参道（Tabio 男士线）"),
    "Tabio":
        dict(day=6, type="购物（袜子）", major_area="东京—涩谷",
             sub_area="涩谷 / 表参道沿线 Tabio 主线"),
    "RAGTAG":
        dict(day=6, type="购物 / 中古设计师服饰",
             major_area="东京—涩谷",
             sub_area="涩谷店（设计师品牌中古）"),
    # 下午段（银座 / 丸之内 / 日本桥）
    "S. Watanabe woodcut prints":
        dict(day=6, type="购物（浮世绘版画 / 老铺）",
             major_area="东京—银座",
             sub_area="银座 8 丁目（乔布斯版画典故）"),
    "Apple 銀座":
        dict(day=6, type="购物 / Apple Store", major_area="东京—银座",
             sub_area="银座 3 丁目（美国本土外第一家）"),
    "Tokyo Station":
        dict(day=6, type="交通节点 / 历史建筑",
             major_area="东京—丸之内 / 东京站",
             sub_area="丸之内中央口（辰野金吾红砖站舍）"),
    "Marunouchi Tokyo Station Square":
        dict(day=6, type="历史建筑 / 广场",
             major_area="东京—丸之内 / 东京站",
             sub_area="丸之内中央广场（重要文化财）"),
    "Nihonbashi Takashimaya Shopping Center":
        dict(day=6, type="购物（百货）", major_area="东京—日本桥",
             sub_area="日本桥高岛屋本馆（重要文化财）"),
    "Namiki Yabusoba":
        dict(day=6, type="餐饮（江户荞麦 / 老铺）",
             major_area="东京—浅草",
             sub_area="并木通（雷门西侧 1 分钟）"),
    # 注：Namiki Yabusoba 地理上属浅草，但 requirements §6.1 明确把它放在 Day 4–7
    # 任意一天；design.md "Day 6 下午段" 显式纳入 Day 6（与银座—日本桥同晚收尾），
    # 故 assigned_day = 6。

    # ---------------- Day 7 — 浅草 + 晴空塔（5）----------------
    "Edosoba Hosokawa":
        dict(day=7, type="餐饮（江户荞麦 / 米其林一星）",
             major_area="东京—两国 / 押上 / 晴空塔",
             sub_area="墨田区龟泽（两国本地午市）"),
    "Edo-Tokyo Museum":
        dict(day=7, type="博物馆", major_area="东京—两国 / 押上 / 晴空塔",
             sub_area="横网 1-4-1"),
    "Kaminarimon Gate":
        dict(day=7, type="神社 / 寺院 / 商业街",
             major_area="东京—浅草",
             sub_area="浅草寺雷门（仲见世通起点）"),
    "Komiya Shoten Japanese Umbrella Shop":
        dict(day=4, type="购物（和伞 / 老铺）",
             major_area="东京—日本桥",
             sub_area="日本橋小伝馬町 14-2"),
    "SMOCO SMOKING&COFFEE BAR 浅草橋店":
        dict(day=7, type="餐饮（吸烟咖啡店）",
             major_area="东京—浅草",
             sub_area="浅草桥站附近"),
    "Tokyo Skytree":
        dict(day=7, type="观景 / 电波塔",
             major_area="东京—两国 / 押上 / 晴空塔",
             sub_area="押上 SOLAMACHI 塔顶展望台"),
}

# ---------------------------------------------------------------------------
# 3. design.md §7：Kabukiza Theatre 是必入 Place_Profile，但不在 CSV 中
PHANTOM_PLACES = [
    {
        "title_jp": "歌舞伎座",
        "title_romaji": "Kabukiza Theatre",
        "title_cn": "歌舞伎座",
        "csv_note": None,
        "url": "https://www.kabuki-za.co.jp/",
        "type": "演出 / 剧场（隈研吾 + 三代目设计团队 / 2013 复原）",
        "major_area": "东京—银座",
        "sub_area": "银座 4 丁目（晴海通与昭和通交叉口）",
        "assigned_day": 6,
        "source": "requirements §7.1（不在 CSV，按硬锚点要求纳入 Day 6 单幕席）",
    },
]

# ---------------------------------------------------------------------------
# 4. 中文别名（CSV Note 中没有给出中文标题时，用此查表 / 否则保留 Note 作 csv_note）
TITLE_CN = {
    "S. Watanabe woodcut prints": "渡边木版画 / 渡辺木版美術画舗",
    "Akihabara Electric Town": "秋叶原电器街",
    "Kotoku-in": "高德院（镰仓大佛）",
    "Nezu Museum": "根津美术馆",
    "WITH HARAJUKU HALL": "WITH HARAJUKU HALL（原宿活动会场）",
    "SMOCO SMOKING&COFFEE BAR 浅草橋店": "SMOCO 吸烟咖啡店 浅草桥店",
    "Meigetsu-in": "明月院（绣球花寺）",
    "Kaminarimon Gate": "雷门（浅草寺总门）",
    "Yokohama Museum of Art": "横滨美术馆",
    "Shichirigahama Beach": "七里滨",
    "Yokohama Station": "横滨站",
    "LINE CUBE SHIBUYA": "LINE CUBE SHIBUYA（涩谷公会堂）",
    "Mandarake Nakano": "Mandarake 中野店（中野百老汇）",
    "Kamakurakōkō-Mae Station": "镰仓高校前站",
    "Kabukicho": "歌舞伎町",
    "Mandarake Shibuya": "Mandarake 涩谷店",
    "Engaku-ji": "圆觉寺",
    "Kyū-Iwasaki-tei Gardens": "旧岩崎邸庭园",
    "M2ビル": "M2 大厦（隈研吾 / 现东京 Memolead 殡仪馆）",
    "Tsurugaoka Hachimangu": "鹤冈八幡宫",
    "Edosoba Hosokawa": "江户荞麦 细川（江戸蕎麦 ほそ川）",
    "Edo-Tokyo Museum": "江户东京博物馆",
    "Tokyo National Museum": "东京国立博物馆",
    "Tokyu Plaza Harajuku “Harakado”": "东急广场原宿 Harakado",
    "Yaguchi Book Store": "矢口书店",
    "Tokyo Tonkotsu Ramen Bankara Shinjuku Kabukicho": "豚骨拉面 Bankara 新宿歌舞伎町店",
    "Ueno Park": "上野恩赐公园",
    "TabioMEN": "Tabio MEN（男士袜专门店）",
    "Yokohama Red Brick Warehouse": "横滨红砖仓库",
    "Shin-Yokohama Ramen Museum": "新横滨拉面博物馆",
    "Meiji Jingu": "明治神宫",
    "Akasaka-Mitsuke Station": "赤坂见附站",
    "Euro Live": "Euro Live（涩谷剧场）",
    "Tokyo Station": "东京站（丸之内站舍）",
    "Marunouchi Tokyo Station Square": "丸之内东京站广场",
    "Nihonbashi Takashimaya Shopping Center": "日本桥高岛屋",
    "Yokohama Landmark Tower": "横滨地标大厦",
    "Namiki Yabusoba": "并木薮荞麦",
    "Isezakichō": "伊势佐木大街",
    "LIFORK Harajuku": "LIFORK 原宿（原宿活动空间）",
    "Hie Shrine": "日枝神社",
    "Shinjuku Golden-Gai": "新宿黄金街",
    "Komiya Shoten Japanese Umbrella Shop": "小宫商店（和伞老铺）",
    "Tokyo Skytree": "东京晴空塔",
    "Tokyo Dome": "东京巨蛋",
    "Tsutaya Books Daikanyama": "代官山蔦屋书店（T-SITE）",
    "Yamashita Park": "山下公园",
    "Kagurazaka": "神乐坂",
    "d47 Museum": "d47 Museum（涩谷 Hikarie 8F）",
    "Shibuya Sky": "涩谷 SKY",
    "Waseda University": "早稻田大学（村上春树图书馆）",
    "Pop Life Department M's": "Pop Life Department M's（秋叶原成人塔）",
    "Sankeien Garden": "三溪园",
    "Mandarake Complex": "Mandarake 总店（秋叶原）",
    "Shinjuku Gyoen National Garden": "新宿御苑",
    "RAGTAG": "RAGTAG（设计师品牌中古店）",
    "Akasaka Aonono Wagashi Main Store": "赤坂青野和菓子本店",
    "Akihabara": "秋叶原",
    "Roppongi": "六本木",
    "21_21 Design Sight": "21_21 Design Sight",
    "Meiji Jingu Museum": "明治神宫博物馆",
    "Apple 銀座": "Apple 银座",
    "Tabio": "Tabio（袜子专门店）",
    # 排除地点
    "Mount Fuji": "富士山",
    "忍野八海": "忍野八海",
    "Hirano beach": "平野浜",
    "Arakura Fuji Sengen Shrine": "新仓富士浅间神社",
    "Lake Yamanaka": "山中湖",
    "Lake Kawaguchi": "河口湖",
    "Hikawa Clock Shop": "Hikawa 钟表店（富士吉田本町通）",
    "Metro-City": "Metro-City（首尔，非日本）",
    "Mitake": "御岳山",
    "MoN Takanawa: The Museum of Narratives": "MoN Takanawa（高轮叙事博物馆）",
    # 机场 / 住宿
    "Narita International Airport": "成田国际机场",
    "Haneda Airport": "羽田机场",
    "COGO RYOGOKU": "COGO RYOGOKU（两国住宿）",
}

# 日文 / 罗马字（首选项）
TITLE_JP = {
    "S. Watanabe woodcut prints": "渡辺木版美術画舗",
    "Akihabara Electric Town": "秋葉原電気街",
    "Kotoku-in": "高徳院",
    "Nezu Museum": "根津美術館",
    "WITH HARAJUKU HALL": "WITH HARAJUKU HALL",
    "SMOCO SMOKING&COFFEE BAR 浅草橋店": "SMOCO SMOKING&COFFEE BAR 浅草橋店",
    "Meigetsu-in": "明月院",
    "Kaminarimon Gate": "雷門",
    "Yokohama Museum of Art": "横浜美術館",
    "Shichirigahama Beach": "七里ヶ浜",
    "Yokohama Station": "横浜駅",
    "LINE CUBE SHIBUYA": "LINE CUBE SHIBUYA（渋谷公会堂）",
    "Mandarake Nakano": "まんだらけ 中野店（中野ブロードウェイ）",
    "Kamakurakōkō-Mae Station": "鎌倉高校前駅",
    "Kabukicho": "歌舞伎町",
    "Mandarake Shibuya": "まんだらけ 渋谷店",
    "Engaku-ji": "円覚寺",
    "Kyū-Iwasaki-tei Gardens": "旧岩崎邸庭園",
    "M2ビル": "M2 ビル",
    "Tsurugaoka Hachimangu": "鶴岡八幡宮",
    "Edosoba Hosokawa": "江戸蕎麦 ほそ川",
    "Edo-Tokyo Museum": "江戸東京博物館",
    "Tokyo National Museum": "東京国立博物館",
    "Tokyu Plaza Harajuku “Harakado”": "東急プラザ原宿「ハラカド」",
    "Yaguchi Book Store": "矢口書店",
    "Tokyo Tonkotsu Ramen Bankara Shinjuku Kabukicho": "東京豚骨拉麺ばんから 新宿歌舞伎町店",
    "Ueno Park": "上野恩賜公園",
    "TabioMEN": "Tabio MEN",
    "Yokohama Red Brick Warehouse": "横浜赤レンガ倉庫",
    "Shin-Yokohama Ramen Museum": "新横浜ラーメン博物館",
    "Meiji Jingu": "明治神宮",
    "Akasaka-Mitsuke Station": "赤坂見附駅",
    "Euro Live": "ユーロライブ",
    "Tokyo Station": "東京駅",
    "Marunouchi Tokyo Station Square": "丸の内東京駅広場",
    "Nihonbashi Takashimaya Shopping Center": "日本橋髙島屋ショッピングセンター",
    "Yokohama Landmark Tower": "横浜ランドマークタワー",
    "Namiki Yabusoba": "並木藪蕎麦",
    "Isezakichō": "伊勢佐木町",
    "LIFORK Harajuku": "LIFORK 原宿",
    "Hie Shrine": "日枝神社",
    "Shinjuku Golden-Gai": "新宿ゴールデン街",
    "Komiya Shoten Japanese Umbrella Shop": "小宮商店",
    "Tokyo Skytree": "東京スカイツリー",
    "Tokyo Dome": "東京ドーム",
    "Tsutaya Books Daikanyama": "代官山 蔦屋書店",
    "Yamashita Park": "山下公園",
    "Kagurazaka": "神楽坂",
    "d47 Museum": "d47 MUSEUM",
    "Shibuya Sky": "渋谷スカイ",
    "Waseda University": "早稲田大学",
    "Pop Life Department M's": "ポップライフデパート M's（秋葉原）",
    "Sankeien Garden": "三溪園",
    "Mandarake Complex": "まんだらけ コンプレックス",
    "Shinjuku Gyoen National Garden": "新宿御苑",
    "RAGTAG": "ラグタグ",
    "Akasaka Aonono Wagashi Main Store": "赤坂青野 和菓子本店",
    "Akihabara": "秋葉原",
    "Roppongi": "六本木",
    "21_21 Design Sight": "21_21 デザインサイト",
    "Meiji Jingu Museum": "明治神宮ミュージアム",
    "Apple 銀座": "Apple 銀座",
    "Tabio": "タビオ",
    # 排除
    "Mount Fuji": "富士山",
    "忍野八海": "忍野八海",
    "Hirano beach": "平野浜",
    "Arakura Fuji Sengen Shrine": "新倉富士浅間神社",
    "Lake Yamanaka": "山中湖",
    "Lake Kawaguchi": "河口湖",
    "Hikawa Clock Shop": "ヒカワ時計店",
    "Metro-City": "Metro-City（韓国・ソウル）",
    "Mitake": "御岳山",
    "MoN Takanawa: The Museum of Narratives": "MoN 高輪",
    # 机场 / 住宿
    "Narita International Airport": "成田国際空港",
    "Haneda Airport": "羽田空港",
    "COGO RYOGOKU": "COGO 両国",
}


def romaji_for(title: str) -> str:
    """Title 字段在 CSV 里多为英文 / 罗马字；直接用 Title 即可，
    个别全日文 / 全中文 Title 单独修正。"""
    overrides = {
        "忍野八海": "Oshino Hakkai",
        "M2ビル": "M2 Building",
        "SMOCO SMOKING&COFFEE BAR 浅草橋店": "SMOCO Smoking & Coffee Bar Asakusabashi",
        "Tokyu Plaza Harajuku “Harakado”": "Tokyu Plaza Harajuku Harakado",
        "Apple 銀座": "Apple Ginza",
    }
    return overrides.get(title, title)


def parse_csv():
    rows = []
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = (row.get("Title") or "").strip()
            if not title:
                continue
            rows.append({
                "title": title,
                "note": (row.get("Note") or "").strip(),
                "url": (row.get("URL") or "").strip(),
            })
    return rows


def categorize(rows):
    excluded, airports, lodgings, included = [], [], [], []
    for r in rows:
        t = r["title"]
        record = {
            "title_jp": TITLE_JP.get(t, t),
            "title_romaji": romaji_for(t),
            "title_cn": TITLE_CN.get(t, t),
            "csv_note": r["note"] or None,
            "url": r["url"],
        }
        if t in EXCLUDED_TITLES:
            record.update({
                "is_excluded": True,
                "exclusion_reason": EXCLUSION_REASONS[t],
                "assigned_day": None,
            })
            excluded.append(record)
        elif t in AIRPORT_TITLES:
            record.update({
                "kind": "airport",
                "type": "交通节点 / 机场",
                "assigned_day": None,
                "note": "参考地点：仅 Day 7 实际从此机场离日时纳入；不创建独立 Place_Profile。",
            })
            airports.append(record)
        elif t in LODGING_TITLES:
            record.update({
                "kind": "lodging",
                "type": "住宿",
                "assigned_day": None,
                "note": "Day 3–7 的常驻住宿；不创建独立 Place_Profile，在每日文档头/尾出现。",
            })
            lodgings.append(record)
        else:
            plan = PLACE_PLAN.get(t)
            if plan is None:
                # design / requirements 没有明确分配 → 标记 unassigned
                record.update({
                    "type": "未指定",
                    "major_area": "未指定",
                    "sub_area": "未指定",
                    "assigned_day": None,
                    "warning": "design.md / requirements.md 未对该地点指定 day，需补充。",
                })
            else:
                record.update({
                    "type": plan["type"],
                    "major_area": plan["major_area"],
                    "sub_area": plan["sub_area"],
                    "assigned_day": plan["day"],
                })
            included.append(record)
    return included, excluded, airports, lodgings


def main():
    rows = parse_csv()
    included, excluded, airports, lodgings = categorize(rows)

    # 注入 phantom Kabukiza Theatre
    for ph in PHANTOM_PLACES:
        included.append(ph)

    # 按 day 分组（仅 included）
    by_day = {d: [] for d in range(1, 8)}
    unassigned = []
    for p in included:
        d = p.get("assigned_day")
        if d in by_day:
            by_day[d].append(p["title_romaji"])
        else:
            unassigned.append(p["title_romaji"])

    summary = {
        "csv_total_non_empty_rows": len(rows),
        "excluded_count": len(excluded),
        "airports_count": len(airports),
        "lodgings_count": len(lodgings),
        "included_count": len(included),
        "phantom_count": len(PHANTOM_PLACES),
        "expected_per_design": {
            "csv_rows": 73,
            "included": 60,
            "excluded": 10,
            "airports": 2,
            "lodging": 1,
        },
        "by_day_counts": {f"day_{d}": len(by_day[d]) for d in range(1, 8)},
        "unassigned_titles": unassigned,
        "discrepancy_notes": [
            f"CSV 实际有 {len(rows)} 行非空 Title（design.md 声称 73）。",
            f"按 design 排除规则后 included = {len(included)}（含 1 个 phantom Kabukiza Theatre），design 声称 60。",
            "Kabukiza Theatre 是 requirements §7.1 强制入选的 Place_Profile，但不在 CSV 中——已作为 phantom 添加，csv_note 为 null。",
            "TabioMEN / Tabio / RAGTAG / Euro Live 在 requirements §6.1 中列出但 design 各日总数未显式纳入；本 JSON 按地理就近分配到 Day 6（涩谷段）。Euro Live 展期已结束（6/2–4），按 §6.6 文档中标注「展期已结束 / 外观打卡」。",
        ],
    }

    out = {
        "metadata": {
            "task": "1.2 抽取 60 个 Place 元数据卡片",
            "source_csv": str(CSV_PATH.relative_to(ROOT)),
            "design_doc": ".kiro/specs/japan-7day-itinerary/design.md",
            "schema_version": "1.0",
            "summary": summary,
        },
        "included": sorted(included, key=lambda p: (p.get("assigned_day") or 99,
                                                    p.get("major_area") or "",
                                                    p["title_romaji"])),
        "by_day": {
            "day_1": [p for p in included if p.get("assigned_day") == 1],
            "day_2": [p for p in included if p.get("assigned_day") == 2],
            "day_3": [p for p in included if p.get("assigned_day") == 3],
            "day_4": [p for p in included if p.get("assigned_day") == 4],
            "day_5": [p for p in included if p.get("assigned_day") == 5],
            "day_6": [p for p in included if p.get("assigned_day") == 6],
            "day_7": [p for p in included if p.get("assigned_day") == 7],
            "unassigned": [p for p in included if p.get("assigned_day") not in range(1, 8)],
        },
        "excluded": excluded,
        "airports": airports,
        "lodgings": lodgings,
    }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
