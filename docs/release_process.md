# Release Process

Before any merge to `main` or tagging a new release:

1. Run the full QA gate:

2. Confirm the final line reads:

3. Only if all 4 suites pass (Semantic, Story, Regression, Stress),
   proceed with commit/merge/tag.

4. If any suite fails, do NOT release. Fix the failing suite, add
   a regression test for the specific bug if one doesn't already
   exist, then re-run the full gate before retrying.

## Suite Coverage

- **Semantic** — pose/action, scene/background, companion/species,
  home/species, season/environment conflicts, prop/accessory duplicates,
  complexity/content alignment
- **Story** — 40-page beat sequence, chapter progression, complexity
  progression, scene/background redundancy, season/habitat conflicts
- **Regression** — 100 random-mode books, crash/duplicate/grammar checks
- **Stress** — 500 books across all subjects, seasons, book types,
  age groups, including unknown/fallback subjects


