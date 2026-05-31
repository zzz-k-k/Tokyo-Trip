"""Strategy for generating RawRow lists (simulating CSV input)."""
from hypothesis import strategies as st


@st.composite
def csv_rows_strategy(draw, min_rows=1, max_rows=80):
    """Generate a list of RawRow dicts simulating Favorite places.csv input.

    **Validates: Requirements 11.5**
    """
    n = draw(st.integers(min_value=min_rows, max_value=max_rows))
    rows = []
    for _ in range(n):
        row = {
            "title": draw(st.text(min_size=1, max_size=60,
                                  alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")))),
            "note": draw(st.text(max_size=200)),
            "url": draw(st.from_regex(r"https://www\.google\.com/maps/place/[A-Za-z0-9+%]+", fullmatch=True)),
            "tags": "",
            "comment": "",
        }
        rows.append(row)
    return rows
