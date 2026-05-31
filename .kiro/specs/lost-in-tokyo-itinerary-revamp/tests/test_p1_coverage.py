"""P1 — Coverage completeness.

Validates: Requirements 11.1 P1, 11.3

Verifies:
- All `included` titles from places.json appear in at least one day file.
- All `excluded` titles do NOT appear in any day file as `### ` headings.
"""
import re


def _extract_h3_titles(day_files: dict) -> set:
    """Extract all ### heading titles from all day files."""
    titles = set()
    for content in day_files.values():
        for m in re.finditer(r"^### (.+)$", content, re.MULTILINE):
            titles.add(m.group(1).strip())
    return titles


def _extract_link_targets(day_files: dict) -> str:
    """Concatenate all day file content for substring search."""
    return "\n".join(day_files.values())


def _normalize_for_search(text: str) -> str:
    """Normalize text for fuzzy matching — strip parenthetical suffixes."""
    # Remove parenthetical notes like （46F 展望 / OMO Base）
    import re
    return re.sub(r"[（(][^）)]*[）)]", "", text).strip()


def test_included_titles_appear_in_day_files(places, day_files):
    """Every included place must appear in at least one day file."""
    all_content = _extract_link_targets(day_files)

    missing = []
    for place in places["included"]:
        title_cn = place.get("title_cn", "")
        title_romaji = place.get("title_romaji", "")
        title_jp = place.get("title_jp", "")

        # Check if any of the three title variants appears in day files
        # Either as a ### heading or as text content (link text, inline mention)
        found = False
        for title in (title_cn, title_romaji, title_jp):
            if title and title in all_content:
                found = True
                break

        # If not found with full title, try normalized (without parenthetical notes)
        if not found:
            for title in (title_cn, title_romaji, title_jp):
                if not title:
                    continue
                normalized = _normalize_for_search(title)
                if normalized and normalized in all_content:
                    found = True
                    break
                # Also try just the first part before any special chars
                short = title.split("（")[0].split("(")[0].strip()
                if short and len(short) >= 3 and short in all_content:
                    found = True
                    break
                # Try without spaces (Japanese text often omits spaces)
                no_space = title.replace(" ", "")
                if no_space and no_space in all_content:
                    found = True
                    break

        if not found:
            missing.append(f"{title_cn} / {title_romaji}")

    assert missing == [], f"Included places not found in any day file: {missing}"


def test_excluded_titles_not_in_day_headings(places, day_files):
    """No excluded place should appear as a ### heading in any day file."""
    h3_titles_raw = _extract_h3_titles(day_files)
    # Flatten to a single searchable string for substring matching
    h3_joined = " ||| ".join(h3_titles_raw)

    violations = []
    for place in places["excluded"]:
        title_cn = place.get("title_cn", "")
        title_romaji = place.get("title_romaji", "")
        title_jp = place.get("title_jp", "")

        for title in (title_cn, title_romaji, title_jp):
            if title and title in h3_joined:
                violations.append(f"{title_cn} / {title_romaji} (matched: '{title}')")
                break

    assert violations == [], f"Excluded places found as ### headings: {violations}"
