"""Strategy for generating Cost_Scenario entries."""
from hypothesis import strategies as st


@st.composite
def scenario_strategy(draw):
    """Generate a Cost_Scenario dict."""
    scenario_name = draw(st.sampled_from(["场景 A（Suica 直付）", "场景 B（TST 72h）"]))
    pass_name = "无" if "A" in scenario_name else "Tokyo Subway Ticket ¥1,500"
    daily_costs = [draw(st.integers(min_value=0, max_value=5000)) for _ in range(7)]
    return {
        "name": scenario_name,
        "pass": pass_name,
        "pass_price_jpy": 0 if pass_name == "无" else 1500,
        "daily_costs_jpy": daily_costs,
        "total_jpy": sum(daily_costs) + (1500 if pass_name != "无" else 0),
    }
