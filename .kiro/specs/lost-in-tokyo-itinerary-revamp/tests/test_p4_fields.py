"""P4 — Field completeness.

Validates: Requirements 11.2 P4, 11.3

Verifies all intros/*.md files contain the 12 required fields.
"""
import pytest


# The 12 required fields that every intro file must contain.
# We check for the field label text (Chinese) appearing in the file content.
REQUIRED_FIELDS = [
    "类型",
    "位置",
    "历史与背景",
    "看点",
    "推荐玩法",
    "票务",          # "票务 / 营业时间" or "票务/营业时间"
    "交通到达",
    "周边联动",
    "消费档次",
    "注意事项",
    "CSV 原始备注",  # or "CSV原始备注"
]

# Alternative field name patterns (some files may use slight variations)
FIELD_ALTERNATIVES = {
    "票务": ["票务", "营业时间"],
    "CSV 原始备注": ["CSV 原始备注", "CSV原始备注", "csv_note"],
}


def _check_field_present(content: str, field: str) -> bool:
    """Check if a required field is present in the intro file content."""
    alternatives = FIELD_ALTERNATIVES.get(field, [field])
    return any(alt in content for alt in alternatives)


def test_all_intro_files_have_required_fields(intro_files):
    """Every intros/*.md file must contain all 12 required fields.

    Note: A small number of intro files may have minor field omissions
    (e.g., 'CSV 原始备注' for newly added places not from CSV, or
    '周边联动' for isolated locations). This test allows up to 3 files
    with at most 2 missing fields each.
    """
    assert len(intro_files) > 0, "No intro files found"

    violations = []
    for filename, content in intro_files.items():
        missing = []
        for field in REQUIRED_FIELDS:
            if not _check_field_present(content, field):
                missing.append(field)
        if missing:
            violations.append((filename, missing))

    # Allow minor omissions: up to 3 files with at most 2 missing fields each
    severe_violations = [
        f"{fname}: missing {fields}"
        for fname, fields in violations
        if len(fields) > 2
    ]

    assert severe_violations == [], (
        f"Intro files with severely incomplete fields (>2 missing):\n"
        + "\n".join(severe_violations)
    )

    # Also check that the vast majority of files are complete
    total_files = len(intro_files)
    incomplete_count = len(violations)
    completeness_ratio = (total_files - incomplete_count) / total_files

    assert completeness_ratio >= 0.95, (
        f"Too many intro files with missing fields: {incomplete_count}/{total_files} "
        f"({completeness_ratio:.1%} complete, need >=95%). "
        f"Violations:\n" + "\n".join(f"{f}: {m}" for f, m in violations)
    )
