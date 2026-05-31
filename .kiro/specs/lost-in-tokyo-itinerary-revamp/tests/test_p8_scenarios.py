"""P8 — Cost scenario totals.

Validates: Requirements 11.2 P8, 11.3

Verifies each day's "成本场景对比" table exists in the day file.
"""
import re
import pytest


@pytest.mark.parametrize("day_num", [1, 2, 3, 4, 5, 6, 7])
def test_cost_scenario_table_exists(day_files, day_num):
    """Each day file must contain a '成本场景对比' section."""
    content = day_files[day_num]
    assert "成本场景对比" in content, (
        f"Day {day_num}: '成本场景对比' table not found in day file."
    )


@pytest.mark.parametrize("day_num", [1, 2, 3, 4, 5, 6, 7])
def test_cost_scenario_has_both_scenarios(day_files, day_num):
    """Each day's cost scenario table must have both 场景 A and 场景 B rows."""
    content = day_files[day_num]

    # Find the cost scenario section
    scenario_section_match = re.search(
        r"成本场景对比.*?(?=\n##|\n---|\Z)", content, re.DOTALL
    )
    if not scenario_section_match:
        pytest.fail(f"Day {day_num}: could not locate '成本场景对比' section")

    section = scenario_section_match.group(0)

    assert "场景 A" in section or "场景A" in section, (
        f"Day {day_num}: '场景 A' row not found in cost scenario table"
    )
    assert "场景 B" in section or "场景B" in section, (
        f"Day {day_num}: '场景 B' row not found in cost scenario table"
    )


@pytest.mark.parametrize("day_num", [1, 2, 3, 4, 5, 6, 7])
def test_cost_scenario_has_jpy_amounts(day_files, day_num):
    """Each cost scenario table must contain JPY amounts (¥ symbol + number)."""
    content = day_files[day_num]

    # Find the cost scenario section
    scenario_section_match = re.search(
        r"成本场景对比.*?(?=\n##|\n---|\Z)", content, re.DOTALL
    )
    if not scenario_section_match:
        pytest.skip(f"Day {day_num}: no cost scenario section found")

    section = scenario_section_match.group(0)

    # Check for yen amounts (¥ followed by digits)
    yen_pattern = re.compile(r"¥[\d,]+")
    amounts = yen_pattern.findall(section)

    assert len(amounts) >= 2, (
        f"Day {day_num}: expected at least 2 JPY amounts in cost scenario table, "
        f"found {len(amounts)}: {amounts}"
    )
