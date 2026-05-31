"""Strategy for generating Place instances."""
from hypothesis import strategies as st

MAJOR_AREAS = [
    "新横滨", "横滨—港未来", "横滨—山下公园 / 元町", "横滨—伊势佐木 / 关内",
    "北镰仓", "镰仓中心", "长谷", "江之电沿线",
    "东京—上野 / 本乡 / 东大", "东京—秋叶原", "东京—水道桥 / 后乐园",
    "东京—千代田 / 神保町", "东京—新宿", "东京—中野", "东京—涩谷",
    "东京—原宿 / 表参道", "东京—代官山", "东京—银座",
    "东京—丸之内 / 东京站", "东京—日本桥", "东京—赤坂 / 永田町",
    "东京—六本木", "东京—神乐坂 / 早稻田", "东京—浅草",
    "东京—两国 / 押上 / 晴空塔",
]

PLACE_TYPES = [
    "餐饮", "庭园", "美术馆", "神社", "寺院", "商业街",
    "演出", "体育场", "观景", "建筑", "交通节点", "校园", "购物", "公园",
]


@st.composite
def place_strategy(draw):
    """Generate a Place dict."""
    return {
        "title_romaji": draw(st.text(min_size=3, max_size=40, alphabet=st.characters(whitelist_categories=("L", "N", "Z")))),
        "title_cn": draw(st.text(min_size=1, max_size=30)),
        "title_jp": draw(st.text(min_size=1, max_size=30)),
        "type": draw(st.sampled_from(PLACE_TYPES)),
        "major_area": draw(st.sampled_from(MAJOR_AREAS)),
        "sub_area": draw(st.text(min_size=1, max_size=50)),
        "assigned_day": draw(st.one_of(st.none(), st.integers(min_value=1, max_value=7))),
        "is_excluded": False,
        "csv_note": draw(st.one_of(st.none(), st.text(max_size=100))),
        "url": draw(st.from_regex(r"https://www\.google\.com/maps/place/[A-Za-z0-9+%]+", fullmatch=True)),
    }
