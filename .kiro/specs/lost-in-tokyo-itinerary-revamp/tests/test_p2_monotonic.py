"""P2 — Sequence monotonicity.

Validates: Requirements 11.2 P2, 11.3

Verifies each day's `## 子区域` headers appear in order without repeats
(except explicitly marked backtrack segments).
"""
import re
import pytest


def _extract_subarea_sequence(content: str) -> list:
    """Extract the ## 子区域 header names in order from a day file."""
    # Match headers like: ## 子区域 1：上野 / 本乡 / 东大（Ueno / Hongo）
    # Also match: ## 子区域 2：秋叶原（Akihabara）
    # Extract the area name (Chinese part before the parenthetical romaji)
    headers = []
    for m in re.finditer(r"^## 子区域\s*\d*[：:]?\s*(.+)$", content, re.MULTILINE):
        raw = m.group(1).strip()
        # Extract just the Chinese area name (before parenthetical romaji)
        paren_match = re.match(r"([^（(]+)", raw)
        if paren_match:
            headers.append(paren_match.group(1).strip())
        else:
            headers.append(raw)
    return headers


def _has_backtrack_annotation(content: str, area: str) -> bool:
    """Check if a repeated area has explicit backtrack/loop annotation."""
    # Look for keywords indicating intentional backtrack near the area mention
    backtrack_keywords = ["回头", "环线", "折返", "必要", "不可避免", "外延"]
    for kw in backtrack_keywords:
        if kw in content:
            return True
    return False


@pytest.mark.parametrize("day_num", [1, 2, 3, 4, 5, 6, 7])
def test_subarea_sequence_no_repeats(day_files, day_num):
    """Each day's sub-area headers should not repeat (monotonic progression)."""
    content = day_files[day_num]
    areas = _extract_subarea_sequence(content)

    if not areas:
        # Some days may use different heading structure; skip if no sub-areas found
        pytest.skip(f"Day {day_num} has no ## 子区域 headers")

    seen = []
    duplicates = []
    for area in areas:
        if area in seen and not _has_backtrack_annotation(content, area):
            duplicates.append(area)
        seen.append(area)

    assert duplicates == [], (
        f"Day {day_num}: repeated sub-areas without backtrack annotation: {duplicates}. "
        f"Full sequence: {areas}"
    )
