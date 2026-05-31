"""Strategy for generating tst-segments.json segment entries."""
from hypothesis import strategies as st

LINES = [
    "都营大江户线", "都营浅草线", "都营新宿线", "都营三田线",
    "东京 Metro 银座线", "东京 Metro 丸之内线", "东京 Metro 日比谷线",
    "东京 Metro 千代田线", "东京 Metro 东西线", "东京 Metro 半蔵门线",
    "东京 Metro 南北线", "东京 Metro 副都心线", "东京 Metro 有乐町线",
    "JR 山手线", "JR 总武线", "JR 中央线", "小田急", "东急东横线", "京成 Skyliner",
]


@st.composite
def tst_segment_strategy(draw):
    """Generate a TST segment dict."""
    day = draw(st.integers(min_value=1, max_value=7))
    in_window = day in (3, 4, 5, 6)
    line = draw(st.sampled_from(LINES))
    is_metro_toei = not line.startswith("JR") and line not in ("小田急", "东急东横线", "京成 Skyliner")
    tst_covered = "✅" if (in_window and is_metro_toei) else "❌"
    fare = 0 if tst_covered == "✅" else draw(st.integers(min_value=140, max_value=3000))
    return {
        "day": day,
        "seq": draw(st.integers(min_value=1, max_value=10)),
        "from": draw(st.text(min_size=2, max_size=30)),
        "to": draw(st.text(min_size=2, max_size=30)),
        "line": line,
        "fare_jpy": fare,
        "tst_covered": tst_covered,
        "in_tst_window": in_window,
    }
