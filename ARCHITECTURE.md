# Architecture

Status as of this writing. Things marked UNVERIFIED have not been confirmed by a real run.

## Pipeline (master.py)

    Research -> Book -> Prompts -> SEO -> title sync -> PDF -> Cover
             -> Marketing -> Readiness -> Publish -> Analytics

## Layers

    agents/engines/book_engine       BookEngine, story/niche prompts, QualityChecker
    agents/engines/generation_pipeline   page generation, resume, negative prompt
    agents/engines/trend_engine      TrendEngine, ConfidenceScorer
    agents/engines/intelligence      keyword, pricing, competitor, revenue, portfolio,
                                     multi-market, dashboard, data_sources/
    agents/image_engine              providers (manual works; stability UNVERIFIED;
                                     flux/gemini/openai are stubs), retry wrapper, ImageQA
    agents/seo_agent, seo_scorer     listing text and its checklist score
    agents/publish_readiness         READY / NOT READY verdict with reasons
    agents/pdf_agent, cover_agent    PDF is real; cover is PROMPTS ONLY

## Rules that keep the output honest

- The SEO title is the single title for listing, cover and PDF.
- "Ready for Publishing" comes from PublishReadiness, not from QualityChecker.
  QualityChecker only inspects prompts, never images or the PDF.
- Images live at output/{keyword}/page_NNN.png or page_NNN/image.png.
- The upload checklist reports blockers; it never ticks anything unchecked.
- The manual provider writes prompt.txt only, so a manual-provider book is
  NOT READY by design (all pages are placeholders).

## Known gaps

- No real page image has ever been generated.
- No real cover image exists.
- Market numbers (demand, competition, revenue) are mostly heuristic fallback.
- ImageQA and the SEO score only report; nothing is blocked on them.
- PDF has no bleed (BLEED constant exists but is unused).

## Unverified

- KDP limits used by the scorer and readiness check (title 200, keyword 50,
  description 4000, 7 slots, cover and price rules).
- The Stability request format and key.
- The GitHub Actions workflow result.

## Added since the first refresh

    agents/utils/run_log.py                              run log for master.py (output/logs)
    agents/engines/intelligence/publishing_strategy.py   BundlePlanner, PublishingStrategy
    agents/kdp_rules.py                                  KDP listing limits, VERIFIED_AGAINST_KDP = False
    agents/seo_scorer.py, agents/publish_readiness.py    read their limits from kdp_rules

- master.py --dashboard prints a launch plan and bundles and writes output/business_dashboard/strategy.json. They use heuristic scores, and every niche currently has LOW confidence, so every niche says "test small".
- Data sources cache a failed fetch, so a dead network is tried once.
- The two tests that call the Google Books and Open Library APIs run offline by default (RUN_NETWORK_TESTS=1 uses the real APIs).
- The QA gate has 16 suites.

## Command layer

    agents/command_parser.py   plain request -> master.py arguments (rule-based, not AI)
    master.py --ask            shows the parsed command and its warnings, asks y/N

- --ask never runs without a terminal to confirm in, and never runs an invalid request.
- master.py validates its own arguments: bad --pages, unknown options, missing values, stray words, unknown --season or --provider all stop with exit code 2 before any book is built.
- CommandParser keeps its own season and provider lists; a test checks they match the engine's lists.
- --pages and --age are still ignored by the build. The parser and master.py both say so in a warning.
- There is no job queue yet. It needs one real book to be worth building.
