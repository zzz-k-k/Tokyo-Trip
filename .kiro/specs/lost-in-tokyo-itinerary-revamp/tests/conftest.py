"""Shared fixtures for PBT tests."""
import json
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[4]  # workspace root


@pytest.fixture(scope="session")
def places():
    """Load places.json as dict."""
    with open(ROOT / "places.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def tst_segments():
    """Load tst-segments.json as dict."""
    with open(ROOT / "tst-segments.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def day_files():
    """Return dict mapping day number (1-7) to file content string."""
    result = {}
    for n in range(1, 8):
        dates = {1: "2026-06-03", 2: "2026-06-04", 3: "2026-06-05",
                 4: "2026-06-06", 5: "2026-06-07", 6: "2026-06-08", 7: "2026-06-09"}
        path = ROOT / f"day-{n}-{dates[n]}.md"
        result[n] = path.read_text(encoding="utf-8")
    return result


@pytest.fixture(scope="session")
def intro_files():
    """Return dict mapping filename to content for all intros/*.md files."""
    intros_dir = ROOT / "intros"
    return {p.name: p.read_text(encoding="utf-8") for p in intros_dir.glob("intro-*.md")}
