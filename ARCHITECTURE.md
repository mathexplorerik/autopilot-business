# Architecture

## Layered Overview

    BookEngine (orchestrator)
        |
        +-- NicheSelector / ThemePlanner / PagePlanner (metadata)
        +-- CharacterProfileGenerator (V12.2)
        +-- RecurringMotifsGenerator (V12.3)
        +-- ScenePlanner (blueprint-side scene preview)
        +-- TitleGenerator / SubtitleGenerator
        +-- BlueprintGenerator (assembles final blueprint dict)
        +-- QualityChecker
        +-- EducationEngine (V12.5, bypasses animal pipeline)
        |
        +-- GenerationPipeline (actual page generation)
                |
                +-- AnimalEngine.build()
                        |
                        +-- StoryPlanner (beats, chapters, complexity curve)
                        +-- RelationshipEngine (action -> pose/expression/prop)
                        +-- SUBJECT_* data (habitats, actions, props, locations,
                        |   wearables, story-beat overrides)
                        +-- Season accessory injection
                        +-- Character memory accessory injection
                        +-- Recurring motif injection
                        +-- GrammarEngine (a/an correctness)

## Two Book Modes

- **story** (book_type="story"): single fixed subject, story_mode=True,
  full 40-beat narrative arc, character memory active.
- **niche** (book_type="niche"): multiple subjects rotate per page, no
  story continuity, no character memory.
- **educational** (book_type="educational"): bypasses AnimalEngine
  entirely, driven by EducationEngine + agents/data/education/*.

## QA Layer

Four independent suites, run together via tests/run_all.py:

1. test_semantic_consistency.py -- cross-field correctness
2. test_story_mode_quality.py -- narrative arc + emotional flow
3. test_100_prompt_quality.py -- random-mode regression
4. test_stress_500_books.py -- large-scale randomized validation

Shared detection logic lives in tests/qa_common.py so fixes to one
detector propagate to every test file automatically.
