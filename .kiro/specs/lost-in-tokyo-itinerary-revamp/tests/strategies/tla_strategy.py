"""Strategy for generating Time_Locked_Activity instances."""
from hypothesis import strategies as st


@st.composite
def tla_strategy(draw):
    """Generate a Time_Locked_Activity dict."""
    day = draw(st.integers(min_value=1, max_value=7))
    hour_start = draw(st.integers(min_value=6, max_value=21))
    minute_start = draw(st.sampled_from([0, 15, 30, 45]))
    duration_min = draw(st.integers(min_value=30, max_value=180))
    return {
        "day": day,
        "start_time": f"{hour_start:02d}:{minute_start:02d}",
        "duration_minutes": duration_min,
        "name": draw(st.text(min_size=3, max_size=40)),
        "venue": draw(st.text(min_size=3, max_size=40)),
        "is_hard_anchor": True,
    }
