# Changelog

## V16 - Honest publishing (not yet confirmed with a real image)
- Run log (agents/utils/run_log.py): every master.py run is saved to output/logs/run_<time>.log, colour codes removed, newest 30 kept
- BundlePlanner and PublishingStrategy: launch order with reasons, and bundles of related niches. Shown by master.py --dashboard and saved to output/business_dashboard/strategy.json. Built on heuristic scores; all 23 niches have LOW confidence, so every niche says "test small"
- Test for master.py --dashboard (deletes old outputs first, runs it for real)
- KDP listing limits moved to agents/kdp_rules.py (values still unverified)
- Data sources remember a failed fetch (Google Books made 2 attempts, now 1); the two network tests run offline unless RUN_NETWORK_TESTS=1
- QA gate is now 12 suites
- PublishReadiness: READY only with real images, cover, price, categories, safe listing
- upload_checklist.txt reports blockers instead of ticking everything
- SEO title is the single title across listing, cover and PDF
- SEOScorer (checklist score, limits UNVERIFIED), ImageQA (thresholds UNVERIFIED)
- Resume per page by prompt fingerprint; negative prompt now reaches providers
- --provider flag wired; duplicate image call and hardcoded "manual" removed
- PDF reads output/{keyword}/ (stale PNGs no longer counted as found)
- Retry/backoff with fail-fast on permanent errors; StabilityProvider written, UNVERIFIED
- Cost tracker, pinned requirements, GitHub Actions workflow (run UNSEEN)

## V13-V14 - Market intelligence and evidence-aware data
- Research, keyword, competitor, pricing, revenue, portfolio, multi-market, dashboard
- Pluggable data sources (heuristic, Google Books, Open Library), provenance, confidence


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
