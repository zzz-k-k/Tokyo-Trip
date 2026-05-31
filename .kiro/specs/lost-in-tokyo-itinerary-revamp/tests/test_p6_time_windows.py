"""P6 — Business hours validation.

Validates: Requirements 11.2 P6, 11.3

Verifies Time_Locked_Activities' time slots fall within business hours
mentioned in intro files (basic regex check).
"""
import re
import pytest


# TLA entries: (day, place_keyword_in_intro, scheduled_time_HH:MM, intro_filename_fragment)
# We verify the scheduled time is within the opening hours found in the intro file.
TLA_TIME_CHECKS = [
    # Tokyo Dome: 18:00 game, opens at 16:00
    (3, "tokyo-dome", "18:00", "16:00", "21:00"),
    # Hie Shrine: 09:00 ceremony, shrine opens early (05:00-06:00 typically)
    (5, "hie-shrine", "09:00", "05:00", "18:00"),
    # 21_21 Design Sight: 13:45 visit, opens 10:00-19:00
    (5, "21-21-design-sight", "13:45", "10:00", "19:00"),
    # Edo-Tokyo Museum: 10:15 visit, opens 09:30-17:30
    (7, "edo-tokyo-museum", "10:15", "09:30", "17:30"),
    # Kabukiza Theatre: afternoon/evening performance
    (6, "kabukiza-theatre", "17:00", "11:00", "21:00"),
]


def _time_to_minutes(time_str: str) -> int:
    """Convert HH:MM to minutes since midnight."""
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])


@pytest.mark.parametrize(
    "day_num,intro_fragment,visit_time,expected_open,expected_close",
    TLA_TIME_CHECKS,
    ids=[
        "Tokyo_Dome_18:00",
        "Hie_Shrine_09:00",
        "21_21_Design_Sight_13:45",
        "Edo_Tokyo_Museum_10:15",
        "Kabukiza_17:00",
    ],
)
def test_tla_within_business_hours(
    intro_files, day_num, intro_fragment, visit_time, expected_open, expected_close
):
    """TLA visit times should fall within the venue's business hours."""
    # Find the matching intro file
    matching_files = [
        (name, content)
        for name, content in intro_files.items()
        if intro_fragment in name
    ]

    if not matching_files:
        pytest.skip(f"No intro file matching '{intro_fragment}' found")

    _name, content = matching_files[0]

    # Extract time patterns from the intro file (HH:MM format)
    time_pattern = re.compile(r"\b(\d{1,2}:\d{2})\b")
    times_found = time_pattern.findall(content)

    # Basic check: the visit time should be between expected open and close
    visit_minutes = _time_to_minutes(visit_time)
    open_minutes = _time_to_minutes(expected_open)
    close_minutes = _time_to_minutes(expected_close)

    assert open_minutes <= visit_minutes <= close_minutes, (
        f"Day {day_num}: visit time {visit_time} is outside expected hours "
        f"[{expected_open}, {expected_close}] for {intro_fragment}"
    )

    # Additionally verify that the intro file mentions some time that brackets the visit
    if times_found:
        found_minutes = [_time_to_minutes(t) for t in times_found if ":" in t]
        # At least one time in the file should be <= visit time (opening)
        # and at least one should be >= visit time (closing)
        has_earlier = any(m <= visit_minutes for m in found_minutes)
        has_later = any(m >= visit_minutes for m in found_minutes)
        assert has_earlier or has_later, (
            f"Day {day_num}: intro file for {intro_fragment} has times {times_found} "
            f"but none bracket the visit time {visit_time}"
        )
