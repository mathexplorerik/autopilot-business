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
