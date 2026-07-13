# Changelog

## V12.5 — Educational Modes
- Added alphabet, numbers, colors, shapes coloring book generation
- Integrated via `book_type="educational"` in BookEngine.build()
- Zero regressions (4/4 QA suites clean)

## V12.4 — Emotional Progression
- Added emotion-transition scoring system (qa_common.py)
- Confirmed ~94% average emotional flow quality across all subjects
- Added jarring-transition detection to story QA suite

## V12.3.2 — Season/Habitat Fix
- Redesigned season as a festive accessory (not weather/environment override)
- Fixed garden/bamboo habitat word-overlap by diversifying HABITATS data
- Season model now architecturally cannot contradict habitat text

## V12.3.1 — Semantic QA Layer
- Added tests/test_semantic_consistency.py (pose/action, scene/background,
  companion/species, home/species, season/environment, complexity/content)
- Added tests/qa_common.py shared helpers (head_noun, shared_word_overlap,
  environment_conflicts, complexity_content_mismatch)

## V12.3 — Theme Consistency
- Season wiring through full pipeline (BookEngine -> GenerationPipeline ->
  AnimalEngine)
- Recurring visual motifs (2 fixed elements, evenly rotating every 4 pages)

## V12.2 / V12.2.1 — Character Memory
- CharacterProfileGenerator: species, personality, wearable accessory,
  companion, favorite activity, home environment
- Curated species-aware wearables/companions/homes (SUBJECT_WEARABLES,
  COMPANIONS, HOME_ENVIRONMENTS)

## V12.1 — Book Blueprint Planner
- Rich blueprint output: book_mode, chapters, difficulty_curve, reserved
  fields for character_profile / recurring_elements / learning_objective
- Dynamic page count by book_type (story=40, niche=50)

## V11 — Story Engine Foundation
- StoryPlanner: 40 concrete story beats across 5 chapters
  (Introduction, Exploration, Activities, Adventure, Wrap-up)
- Beat-aware actions, poses, expressions
- Wired story_mode through the full production pipeline
- 40-page uniqueness and scene/background redundancy fixes

## Pre-V11 — Core Bug Fixes
- Fixed duplicate ACTION_INDEX keys (17 mis-categorized actions)
- Fixed RelationshipEngine.best_match() crash and Scorer nested-class bug
- Fixed grammar (a/an) via GrammarEngine
- Added habitat system (25 animals, 13 habitat categories)
