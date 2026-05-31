"""P3 — Hard anchor presence.

Validates: Requirements 11.2 P3, 11.3

Verifies 9 Time_Locked_Activities have their key text present in the
corresponding day file.
"""
import pytest


# Each TLA is (day_number, list_of_required_text_fragments)
TLA_ANCHORS = [
    # TLA-4: Tokyo Dome baseball game
    (3, ["18:00", "巨人"]),
    # TLA-5: Hie Shrine Sanno Matsuri
    (5, ["09:00", "山王祭"]),
    # TLA-6: Kabukiza single-act seat (day-6)
    (6, ["歌舞伎座"]),
    # TLA-8: SSFF & ASIA at WITH HARAJUKU HALL (day-6, actual implementation)
    (6, ["WITH HARAJUKU HALL"]),
    # 21_21 Design Sight Soup as Life exhibition (day-5)
    (5, ["21_21 Design Sight"]),
    # Edo-Tokyo Museum reopened (day-7)
    (7, ["江户东京博物馆"]),
    # COGO RYOGOKU checkout (day-7)
    (7, ["10:00", "退房"]),
    # TST activation (day-3)
    (3, ["TST", "激活"]),
    # Komiya Shoten on day-4
    (4, ["小宫商店"]),
]


@pytest.mark.parametrize(
    "day_num,fragments",
    TLA_ANCHORS,
    ids=[
        "TLA4-Tokyo_Dome_18:00",
        "TLA5-Sanno_Matsuri_09:00",
        "TLA6-Kabukiza",
        "TLA8-WITH_HARAJUKU_HALL",
        "21_21_Design_Sight",
        "Edo_Tokyo_Museum",
        "COGO_checkout_10:00",
        "TST_activation",
        "Komiya_Shoten_day4",
    ],
)
def test_tla_anchor_present(day_files, day_num, fragments):
    """Each TLA's key text fragments must appear in the corresponding day file."""
    content = day_files[day_num]
    missing = [f for f in fragments if f not in content]
    assert missing == [], (
        f"Day {day_num}: missing TLA fragments {missing}. "
        f"Expected all of {fragments} to appear in day-{day_num} file."
    )
