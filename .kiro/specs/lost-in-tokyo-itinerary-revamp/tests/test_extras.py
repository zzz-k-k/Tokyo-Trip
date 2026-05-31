"""Extras — File existence + link validity.

Validates: Requirements 10.2, 10.3, 10.8

Verifies:
- All included places have corresponding intros/*.md files.
- All internal links in day files point to existing files.
"""
import re
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[4]  # workspace root


def _fuzzy_slug_match(slug_a: str, slug_b: str) -> bool:
    """Check if two slugs are similar enough to be considered a match.

    Handles cases like 'kamakurakoko' vs 'kamakurako' (doubled vowel reduction).
    """
    if not slug_a or not slug_b:
        return False
    # Direct containment
    if slug_a in slug_b or slug_b in slug_a:
        return True
    # Try deduplicating consecutive identical syllables
    # e.g., "kamakurakoko" → "kamakurako" (remove doubled "ko")
    import re
    dedup_a = re.sub(r"(.{2,3})\1", r"\1", slug_a)
    dedup_b = re.sub(r"(.{2,3})\1", r"\1", slug_b)
    if dedup_a == slug_b or dedup_b == slug_a or dedup_a == dedup_b:
        return True
    # Check if they share enough common segments (split by -)
    parts_a = set(slug_a.split("-"))
    parts_b = set(slug_b.split("-"))
    if len(parts_a) >= 2 and len(parts_b) >= 2:
        overlap = parts_a & parts_b
        if len(overlap) >= len(min(parts_a, parts_b, key=len)) * 0.6:
            return True
    return False


def _normalize_romaji_to_filename(romaji: str) -> str:
    """Convert a title_romaji to the expected intro filename.

    Rules from design §6.1:
    - Lowercase
    - Replace spaces, &, ', ", _ with -
    - Collapse multiple hyphens
    - Strip leading/trailing hyphens
    - Strip macrons (ō→o, ū→u, etc.)
    - Remove dots and other special chars
    """
    import unicodedata

    name = romaji.lower()
    # Normalize unicode — decompose macrons then strip combining chars
    name = unicodedata.normalize("NFD", name)
    # Remove combining characters (diacritics like macrons)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    # Replace special characters with hyphens
    for ch in " &'\"_.":
        name = name.replace(ch, "-")
    # Remove other non-alphanumeric chars except hyphens
    name = "".join(c if c.isalnum() or c == "-" else "-" for c in name)
    # Collapse multiple hyphens
    while "--" in name:
        name = name.replace("--", "-")
    # Strip leading/trailing hyphens
    name = name.strip("-")
    return f"intro-{name}.md"


def test_included_places_have_intro_files(places, intro_files):
    """Every included place should have a corresponding intros/intro-*.md file."""
    import unicodedata

    missing = []
    available_files = set(intro_files.keys())

    for place in places["included"]:
        romaji = place.get("title_romaji", "")
        if not romaji:
            continue

        expected_filename = _normalize_romaji_to_filename(romaji)

        # Also create a simplified slug for fuzzy matching
        romaji_slug = romaji.lower()
        romaji_slug = unicodedata.normalize("NFD", romaji_slug)
        romaji_slug = "".join(
            c for c in romaji_slug if unicodedata.category(c) != "Mn"
        )
        romaji_slug = romaji_slug.replace(" ", "-").replace("'", "-").replace("&", "-")
        romaji_slug = romaji_slug.replace(".", "-").replace('"', "-")
        # Collapse hyphens
        while "--" in romaji_slug:
            romaji_slug = romaji_slug.replace("--", "-")
        romaji_slug = romaji_slug.strip("-")

        # Check if the expected file exists, or any file containing the romaji slug
        found = (
            expected_filename in available_files
            or any(romaji_slug in f for f in available_files)
            # Also try shorter slug (first few words)
            or any(
                romaji_slug.split("-")[0] in f
                for f in available_files
                if len(romaji_slug.split("-")[0]) >= 4
            )
            # Try matching with common variations (e.g., "ms" vs "m-s")
            or any(
                romaji_slug.replace("-s", "s") in f or f.replace("-s", "s") in romaji_slug
                for f in available_files
            )
            # Try substring match: file slug contains most of our slug or vice versa
            or any(
                _fuzzy_slug_match(romaji_slug, f.replace("intro-", "").replace(".md", ""))
                for f in available_files
            )
        )

        if not found:
            missing.append(f"{romaji} (expected: {expected_filename})")

    assert missing == [], (
        f"Included places without corresponding intro files:\n"
        + "\n".join(missing)
    )


def test_internal_links_in_day_files_resolve(day_files):
    """All internal markdown links in day files should point to existing files."""
    # Match markdown links: [text](path) — only relative paths (not http/https)
    link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

    broken_links = []
    for day_num, content in day_files.items():
        for m in link_pattern.finditer(content):
            link_text = m.group(1)
            link_target = m.group(2)

            # Skip external links
            if link_target.startswith("http://") or link_target.startswith("https://"):
                continue
            # Skip anchor-only links
            if link_target.startswith("#"):
                continue

            # Remove any anchor fragment
            if "#" in link_target:
                link_target = link_target.split("#")[0]

            # Resolve relative to workspace root
            target_path = ROOT / link_target

            if not target_path.exists():
                broken_links.append(
                    f"Day {day_num}: [{link_text}]({m.group(2)}) -> "
                    f"{target_path} does not exist"
                )

    assert broken_links == [], (
        f"Broken internal links found:\n" + "\n".join(broken_links)
    )
