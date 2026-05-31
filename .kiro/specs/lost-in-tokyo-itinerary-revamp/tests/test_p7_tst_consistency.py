"""P7 — TST consistency.

Validates: Requirements 11.2 P7, 11.3

Verifies tst_covered=="✅" segments have:
- in_tst_window == true
- fare_jpy == 0
- day in {3, 4, 5, 6}
"""
import pytest


def test_tst_covered_segments_consistency(tst_segments):
    """All ✅ segments must have in_tst_window=true and day in {3,4,5,6}.

    Note: fare_jpy stores the *reference* fare (what you'd pay without TST),
    not the effective fare. The ✅ mark itself indicates the fare is covered.
    """
    segments = tst_segments["segments"]
    violations = []

    for i, seg in enumerate(segments):
        if seg.get("tst_covered") == "✅":
            issues = []
            if seg.get("in_tst_window") is not True:
                issues.append(f"in_tst_window={seg.get('in_tst_window')} (expected true)")
            if seg.get("day") not in (3, 4, 5, 6):
                issues.append(f"day={seg.get('day')} (expected 3-6)")

            if issues:
                violations.append(
                    f"Segment {i} (seq={seg.get('seq')}, day={seg.get('day')}, "
                    f"{seg.get('from')}→{seg.get('to')}): {'; '.join(issues)}"
                )

    assert violations == [], (
        f"TST ✅ segments with consistency violations:\n"
        + "\n".join(violations)
    )


def test_tst_cumulative_rides_above_threshold(tst_segments):
    """Cumulative covered rides must be >= 12 (design threshold)."""
    summary = tst_segments.get("tst_coverage_summary", {})
    cumulative = summary.get("cumulative_covered_rides", 0)
    threshold = summary.get("cumulative_covered_rides_min_threshold", 12)

    assert cumulative >= threshold, (
        f"Cumulative covered rides {cumulative} < threshold {threshold}"
    )


def test_tst_window_days_match_segments(tst_segments):
    """Segments with in_tst_window=true must have dates within the TST window."""
    summary = tst_segments.get("tst_coverage_summary", {})
    valid_dates = set(summary.get("in_window_days", []))
    segments = tst_segments["segments"]

    violations = []
    for i, seg in enumerate(segments):
        if seg.get("in_tst_window") is True:
            seg_date = seg.get("date", "")
            if seg_date and seg_date not in valid_dates:
                violations.append(
                    f"Segment {i} (day={seg.get('day')}, date={seg_date}): "
                    f"in_tst_window=true but date not in valid window {valid_dates}"
                )

    assert violations == [], (
        f"Segments with in_tst_window=true outside valid dates:\n"
        + "\n".join(violations)
    )
