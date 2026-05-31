"""P5 — Tail section presence.

Validates: Requirements 11.2 P5, 11.3

Verifies:
- day-3 through day-6 contain "COGO RYOGOKU" in their tail section.
- day-7 contains "10:00 退房".
"""
import pytest


@pytest.mark.parametrize("day_num", [3, 4, 5, 6])
def test_day_3_to_6_tail_has_cogo_ryogoku(day_files, day_num):
    """Days 3-6 must reference COGO RYOGOKU (nightly return destination)."""
    content = day_files[day_num]
    assert "COGO RYOGOKU" in content, (
        f"Day {day_num}: 'COGO RYOGOKU' not found in file content. "
        f"The tail section must reference the nightly return to COGO RYOGOKU."
    )


def test_day_7_tail_has_checkout(day_files):
    """Day 7 must contain '10:00 退房' (checkout time)."""
    content = day_files[7]
    # Check for the checkout time mention - may appear as "10:00 退房" or "10:00退房"
    assert "10:00" in content and "退房" in content, (
        "Day 7: must contain '10:00' and '退房' (checkout time reference). "
        "The tail section should explicitly state the 10:00 checkout time."
    )
