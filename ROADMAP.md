# Roadmap

## V11 — Story Engine Foundation ✅
- 40-beat narrative arc across 5 chapters
- Beat-aware actions, poses, expressions
- Emotional progression (flow scoring, ~94% average quality)

## V12 — Book Generation Foundation ✅
- QA Stable (6-suite gate: Semantic, Story, Regression, Negative, Pipeline, Stress)
- Theme Consistency (season as accessory model)
- Character Memory (species-aware, book-consistent)
- Blueprint Planner (rich metadata: chapters, difficulty curve)
- Educational Modes (alphabet, numbers, colors, shapes)

## V13 — Market Intelligence ✅
- Smart Research Engine (niche resolution, audience/theme/style analysis)
- Bestseller Intelligence (demand/competition/profit/evergreen via TrendEngine)
- Keyword Intelligence (ranked long-tail keyword opportunities)
- Competitor Intelligence (competition-tier positioning strategy)
- Pricing Intelligence (marketplace-aware price suggestions)
- Revenue Predictor (monthly/annual revenue estimates)
- Portfolio Planner (multi-niche ranking)
- Multi-Market Optimizer (Amazon/Etsy/Gumroad comparison)
- Business Dashboard (consolidated business snapshot)
- Series Management (SeriesPlanner - persistent character across a series)
- Security/hygiene: filename sanitization, content-safety blocklist, .gitignore cleanup

## V14 — Evidence-Aware Data Architecture ✅
- Pluggable BaseMarketDataSource interface (heuristic default, real-API-ready)
- Google Books + Open Library real data source plugins
- Provenance Tracking (which fields are real data vs fallback)
- Confidence Scoring (HIGH/MEDIUM/LOW per report)
- Confidence-Aware Ranking (Portfolio/Dashboard rank by evidence quality, not just raw optimism)

## V15 — Coloring Book Generator Deepening (IN PROGRESS)
- Image Pipeline retry/backoff infrastructure - DONE (with_retry wrapper, BaseProvider integration)
- Real provider implementation (Flux/Gemini/Stability/OpenAI) - BLOCKED: needs API keys + network, must be done on developer machine, not this sandbox
- Scene Planner refinements - NOT STARTED
- Prompt Builder refinements - NOT STARTED

## V16 — Book Builder
- PDF Generator refinements
- Cover Generator refinements
- Export System (multi-format output: EPUB, print-ready PDF variants)

## V17 — Publishing Intelligence
- SEO Automation
- Metadata Generator
- Publishing Package assembly

## V18 — Multi-platform Publishing
- Amazon KDP Upload
- Draft2Digital
- Multi-platform Publishing

## V19 — Master Command System
- Command Parser (natural language -> structured build request)
- Job Manager (queue, track, retry generation jobs)
- Pipeline Orchestrator

---

## Principle

"BUILD STATUS: RELEASE READY" means the current foundation is stable -
not that the project is complete. Each version above builds on a
verified, QA-gated baseline. Do not skip the QA gate (`python3
tests/run_all.py`) before starting work on the next version.

## Note on Parallel Development

This repository has been worked on by multiple concurrent sessions.
Before starting new work, always run `git log --oneline -10` and
`python3 tests/run_all.py` to confirm the actual current state -
this file is a snapshot, not a live source of truth.
