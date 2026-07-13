# Roadmap

## V12 (Current) ✅ — Foundation

- QA Stable (4-suite gate: Semantic, Story, Regression, Stress)
- Theme Consistency (season as accessory model)
- Character Memory (species-aware, book-consistent)
- Blueprint Planner (rich metadata: chapters, difficulty curve, reserved fields)
- Educational Modes (alphabet, numbers, colors, shapes)
- Emotional Progression (flow scoring, ~94% average quality)

## V13 — Master Command System

- Command Parser (natural language -> structured build request)
- Job Manager (queue, track, retry generation jobs)
- Pipeline Orchestrator (routes requests to the right engine:
  story/niche/educational, coordinates multi-step builds)

## V14 — Coloring Book Generator (deepen existing engine)

- Scene Planner refinements
- Prompt Builder refinements
- Image Pipeline (actual image generation wiring, not just prompts)

## V15 — Book Builder

- PDF Generator
- Cover Generator
- Export System (multi-format output)

## V16 — Publishing Intelligence

- SEO Automation
- Metadata Generator
- Publishing Package assembly

## V17 — Multi-platform Publishing

- Amazon KDP Upload
- Draft2Digital
- Multi-platform Publishing

---

## Principle

"BUILD STATUS: RELEASE READY" means the current foundation is stable —
not that the project is complete. Each version above builds on a
verified, QA-gated baseline. Do not skip the QA gate (`python3
tests/run_all.py`) before starting work on the next version.
