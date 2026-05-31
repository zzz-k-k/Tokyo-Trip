# Project Guidelines — 锅巴的奇妙冒险之迷失东京 (Tokyo Trip GitBook)

## Project Overview

This is a HonKit-based GitBook site for a 7-day Kanto (Yokohama / Kamakura / Tokyo) travel itinerary. The site is deployed to GitHub Pages via `.github/workflows/deploy-gitbook.yml`.

## Architecture

- **Day plan files** (`day-N-YYYY-MM-DD.md`): Compact route-only format with links to intro files
- **Introduction files** (`intros/intro-{romaji-id}.md`): Detailed Place_Profile documents
- **SUMMARY.md**: HonKit table of contents — **only files listed here are rendered as pages**
- **Data files**: `places.json`, `tst-segments.json`, `build_places.py`
- **Tests**: `.kiro/specs/lost-in-tokyo-itinerary-revamp/tests/` (pytest + hypothesis)

## Critical Rules

### 1. SUMMARY.md is the single source of truth for HonKit pages

- A file MUST be listed in `SUMMARY.md` to appear on the deployed site
- A file listed in `SUMMARY.md` MUST exist on disk — otherwise HonKit produces broken-link warnings
- When deleting a file, ALWAYS remove its entry from `SUMMARY.md` in the same commit
- When creating a new page, ALWAYS add it to `SUMMARY.md`

### 2. index.md must stay concise

- `index.md` is the landing page ("7 日行程总览")
- It should contain ONLY: header metadata + 7-day quick overview cards with links to day-N.md
- Do NOT put detailed per-day summaries, excluded place lists, or other verbose content in index.md
- Detailed content belongs in the individual day-N.md files or intros/*.md files

### 3. Git hygiene

- Use `git add <specific files>` instead of `git add -A` to avoid accidentally staging:
  - `__pycache__/`, `.venv/`, `*.pyc`, `*.dmg`, `_book/`, `node_modules/`
- The `.gitignore` already excludes: `_book`, `__pycache__/`, `*.pyc`, `*.dmg`
- Always verify `git status` before committing to catch unintended files
- Push to a feature branch first for large changes; merge to main only when ready to deploy

### 4. HonKit build validation

- Run `npm run build` before pushing to verify no broken-link / TOC warnings
- Check `_book/index.html` `<title>` tag reflects the correct site name
- The deploy workflow triggers on push to `main` — every push to main triggers a live deployment

### 5. Day file format (post-refactor)

Day files use the compact "动线提示 + 链接" format:
```markdown
- HH:MM ｜ {地点中文名}（{Major_Area}）→ [详细介绍](intros/intro-{romaji-id}.md)
  - 最近车站：{station} {exit} 步行 {N} 分钟（TST ✅/❌）
  - 票务：{price or 免费}
  - 时间窗：{arrival}–{departure} {brief activity}
```

Do NOT put full Place_Profile content (历史与背景, 看点, etc.) back into day files. That content lives in `intros/`.

### 6. Python environment

- Use `uv` for virtual environment and dependency management
- Dependencies: `pytest`, `hypothesis` (defined in `pyproject.toml`)
- Run tests: `uv run pytest .kiro/specs/lost-in-tokyo-itinerary-revamp/tests/ -v`

### 7. File naming conventions

- Intro files: `intros/intro-{romaji-id}.md` (kebab-case, lowercase, no underscores)
- Day files: `day-{N}-{YYYY-MM-DD}.md`
- Spec files: `.kiro/specs/{feature-name}/` (requirements.md, design.md, tasks.md)

## Common Mistakes to Avoid

1. **Forgetting to update SUMMARY.md** when adding/removing pages → broken links or invisible pages
2. **Putting verbose content in index.md** → cluttered landing page with "出格" text
3. **Using `git add -A`** → accidentally committing binary files, __pycache__, .venv
4. **Deleting a file without removing its SUMMARY.md entry** → HonKit broken-link warning
5. **Pushing directly to main without build verification** → broken deployment
