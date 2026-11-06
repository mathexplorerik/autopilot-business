# Roadmap

## Done and verified by the QA gate (12 suites)
Story engine, character memory, season accessories, educational modes,
market intelligence, data sources with provenance and confidence, SEO title
and score, ImageQA (synthetic images only), resume, retry/backoff,
publish readiness, honest upload checklist, cost tracker, run log,
bundle and launch-plan suggestions (heuristic), dashboard CLI test.

## Blocked on a real image
1. A valid image-provider key (Stability key currently returns 401).
2. Generate one image and look at it.
3. Tune ImageQA thresholds on it, then wire ImageQA into the pipeline.
4. Generate a full 40-page book (check cost first).

## Cover
Cover agent writes prompts only. Needs a real front/back/spine file.
Spine width depends on page count and paper; check the current KDP calculator.

## To confirm against KDP
Limits in the Unverified section of ARCHITECTURE.md, and bleed size.

## Later
Extra trim sizes and bleed (need KDP numbers), niche discovery (needs real data),
other image providers, command system.
