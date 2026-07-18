"""
=========================================
Negative / Edge-Case Test Suite
=========================================
Every feature going forward should get a matching entry
here: what happens when input is invalid, empty, missing,
or corrupted - not just when everything goes right. This
is what a "happy path only" test suite misses, and exactly
the kind of bug this whole session kept finding by hand.

Categories covered:
  - Invalid input (bad subject, bad season, bad book_type)
  - Empty data (empty keyword, zero pages)
  - Missing image (already-covered by manual provider design,
    verified here explicitly)
  - Failed quality check (inject a broken page, confirm the
    status correctly flips to "Needs Review")
  - Corrupted metadata (missing/malformed blueprint fields)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.engines.animal_engine import AnimalEngine
from agents.engines.book_engine.book_engine import BookEngine
from agents.engines.book_engine.quality_checker import QualityChecker
from agents.analytics_agent import AnalyticsAgent


def test_invalid_subject_does_not_crash():
    """An unrecognized animal name should still produce a valid prompt (safe fallback), not crash."""
    engine = AnimalEngine()
    r = engine.build("totally_not_a_real_animal_xyz", page_number=1, total_pages=40, story_mode=True)
    assert r.get("positive"), "Invalid subject produced an empty prompt instead of a safe fallback"
    print("[PASS] invalid subject falls back safely, no crash")


def test_invalid_season_does_not_crash():
    """An unrecognized season string should be ignored gracefully, not crash or corrupt output."""
    engine = AnimalEngine()
    r = engine.build("lion", page_number=1, total_pages=40, story_mode=True, season="not_a_real_season")
    assert r.get("positive"), "Invalid season crashed or produced empty output"
    print("[PASS] invalid season string ignored safely, no crash")


def test_empty_keyword_rejected_clearly():
    """
    An empty/whitespace keyword should be rejected with a clear,
    early ValueError - NOT silently accepted, and NOT allowed to
    surface as a deep, confusing RuntimeError after 10 retries
    (which is what happened before this was fixed).
    """
    from agents.book_agent import BookAgent
    agent = BookAgent()
    try:
        agent.create_book(keyword="   ", book_type="niche", age_group="kids")
        raise AssertionError("Empty/whitespace keyword was silently accepted - should have raised ValueError")
    except ValueError as e:
        assert "empty" in str(e).lower(), f"ValueError raised but message is unclear: {e}"
        print(f"[PASS] empty keyword rejected with a clear, early error: {e}")
    except Exception as e:
        raise AssertionError(
            f"Empty keyword raised the WRONG exception type ({type(e).__name__}: {e}) - "
            "expected a clear ValueError, not a deep pipeline crash"
        )


def test_zero_pages_does_not_crash():
    """A book_type/age_group combination that yields 0 pages should not crash generation."""
    engine = AnimalEngine()
    try:
        result = engine.build("lion", page_number=1, total_pages=0, story_mode=True)
        # total_pages=0 is a degenerate case - just confirm no crash, not specific content
        print(f"[PASS] total_pages=0 handled without crash (complexity={result.get('complexity')})")
    except Exception as e:
        raise AssertionError(f"total_pages=0 crashed generation: {type(e).__name__}: {e}")


def test_failed_quality_check_flips_status():
    """Injecting a broken page (duplicate + env conflict) must flip status to 'Needs Review', not silently pass."""
    checker = QualityChecker()
    blueprint = {
        "title": "Test Book",
        "subtitle": "Test Subtitle",
        "theme": "Test Theme",
        "total_pages": 2,
        "generated_pages": [
            {
                "page": 1,
                "positive": "Cute baby lion, at a savanna trail, surrounded by snow-covered cabin",
                "scene": "savanna trail",
                "background": "snow-covered cabin",
                "complexity": "simple",
            },
            {
                "page": 2,
                # exact duplicate of page 1's prompt - must be caught
                "positive": "Cute baby lion, at a savanna trail, surrounded by snow-covered cabin",
                "scene": "savanna trail",
                "background": "snow-covered cabin",
                "complexity": "simple",
            },
        ],
    }
    result = checker.validate(blueprint)
    assert not result["valid"], "QualityChecker passed a blueprint with duplicate prompts AND an environment conflict"
    assert len(result["issues"]) >= 2, f"Expected at least 2 issues (duplicate + env conflict), got {result['issues']}"
    print(f"[PASS] broken blueprint correctly flagged invalid: {len(result['issues'])} issues found")


def test_missing_metadata_fields_reported_not_crashed():
    """A blueprint missing required fields should report issues, not raise."""
    checker = QualityChecker()
    blueprint = {}  # completely empty - every required field missing
    try:
        result = checker.validate(blueprint)
    except Exception as e:
        raise AssertionError(f"QualityChecker crashed on empty blueprint instead of reporting issues: {e}")
    assert not result["valid"], "Empty blueprint was reported as valid"
    assert len(result["issues"]) >= 4, f"Expected multiple missing-field issues, got {result['issues']}"
    print(f"[PASS] empty/corrupted blueprint reported as invalid with {len(result['issues'])} issues, no crash")


def test_missing_image_produces_placeholder_not_crash():
    """The manual provider path (no image file present) must not crash page assembly."""
    from agents.image_engine.providers.manual_provider import ManualProvider
    provider = ManualProvider()
    result = provider.generate(prompt="test prompt", negative_prompt="test negative", output_path="/tmp/qa_negative_test_output")
    assert result.get("success"), "ManualProvider did not report success for its own no-op path"
    print("[PASS] manual provider (no real image) completes without crash, as designed")


def test_analytics_reflects_failed_quality():
    """AnalyticsAgent must report 'Needs Review' (not a hardcoded success string) when quality is invalid."""
    fake_book = {
        "title": "Fake Book",
        "subtitle": "Fake Subtitle",
        "total_pages": 1,
        "quality": {"valid": False, "issues": ["forced failure for negative test"]},
        "status": "Needs Review",
    }
    analytics = AnalyticsAgent()
    result = analytics.generate(report={"niche": "test", "resolved_niche": "test"}, book=fake_book)
    assert result.get("status") == "Needs Review", (
        f"AnalyticsAgent reported '{result.get('status')}' for a failed-quality book - "
        "status is not truly wired to quality.valid"
    )
    print("[PASS] analytics status correctly reflects failed quality check")


def run_all():
    tests = [
        test_invalid_subject_does_not_crash,
        test_invalid_season_does_not_crash,
        test_empty_keyword_rejected_clearly,
        test_zero_pages_does_not_crash,
        test_failed_quality_check_flips_status,
        test_missing_metadata_fields_reported_not_crashed,
        test_missing_image_produces_placeholder_not_crash,
        test_analytics_reflects_failed_quality,
        test_content_safety_blocks_unsafe_prompt,
        test_pricing_intelligence_edge_cases,
        test_bestseller_intelligence_edge_cases,
        test_competitor_intelligence_edge_cases,
        test_portfolio_planner_edge_cases,
        test_multi_market_optimizer_edge_cases,
        test_business_dashboard_edge_cases,
    ]
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"[ERROR] {test.__name__}: {type(e).__name__}: {e}")

    print()
    if failed:
        print(f"{failed}/{len(tests)} negative tests FAILED")
    else:
        print(f"All {len(tests)} negative tests PASSED")
    return failed == 0




def test_content_safety_blocks_unsafe_prompt():
    """A book containing a clearly unsafe word must fail quality validation."""
    from agents.engines.book_engine.quality_checker import QualityChecker
    checker = QualityChecker()
    blueprint = {
        "title": "Cute Animals",
        "subtitle": "Fun for kids",
        "theme": "Animals",
        "total_pages": 1,
        "generated_pages": [
            {"page": 1, "positive": "A lion holding a knife menacingly", "complexity": "simple"},
        ],
    }
    result = checker.validate(blueprint)
    assert not result["valid"], "QualityChecker did not flag an unsafe word in a prompt"
    assert any("CONTENT SAFETY" in issue for issue in result["issues"]), \
        f"Expected a CONTENT SAFETY issue, got: {result['issues']}"
    print("[PASS] content safety check blocks a clearly unsafe prompt")


def test_pricing_intelligence_edge_cases():
    """Pricing must never crash or suggest a below-cost price on bad input."""
    from agents.engines.intelligence.pricing_intelligence import PricingIntelligence
    pi = PricingIntelligence()

    r1 = pi.suggest_price(0, 50, 50)
    assert r1["suggested_price"] > 0, "Zero pages produced a non-positive price"

    r2 = pi.suggest_price(-5, 50, 50)
    assert r2["suggested_price"] > 0, "Negative pages produced a non-positive price"

    r3 = pi.suggest_price(40, 999, 50)
    assert r3["suggested_price"] > 0, "Out-of-range demand score crashed or broke pricing"

    r4 = pi.suggest_price(40, 50, 50, marketplace="not_a_real_marketplace")
    assert r4["marketplace"] == "amazon", "Unknown marketplace did not fall back safely"

    r5 = pi.suggest_price(40, None, None)
    assert r5["suggested_price"] > 0, "None scores crashed pricing instead of defaulting"

    r6 = pi.suggest_price(500, 50, 50, marketplace="amazon")
    assert r6["suggested_price"] > r6["print_cost"], "Suggested price is below print cost - would lose money on every sale"

    print("[PASS] pricing intelligence handles zero/negative pages, out-of-range scores, unknown marketplace, None scores")




def test_bestseller_intelligence_edge_cases():
    from agents.engines.intelligence.bestseller_intelligence import BestsellerIntelligence
    bi = BestsellerIntelligence()
    assert bi.analyze(None, None, None)["bestseller_pattern_match"] is False
    assert bi.analyze(500, -50, 999)["bestseller_pattern_match"] in (True, False)
    print("[PASS] bestseller intelligence handles None/out-of-range scores without crash")


def test_competitor_intelligence_edge_cases():
    from agents.engines.intelligence.competitor_intelligence import CompetitorIntelligence
    ci = CompetitorIntelligence()
    assert ci.analyze("lion", None)["competition_tier"] in ("low", "moderate", "high")
    assert ci.analyze("lion", 500)["competition_tier"] == "high"
    assert ci.analyze("lion", -50)["competition_tier"] == "low"
    assert ci.analyze("", 50)["competition_tier"] in ("low", "moderate", "high")
    print("[PASS] competitor intelligence handles None/out-of-range scores and empty niche without crash")


def test_portfolio_planner_edge_cases():
    """PortfolioPlanner wraps ResearchEngine.analyze() per niche - must
    handle an empty niche list and a niche that makes analyze() raise,
    without crashing the whole portfolio run."""
    from agents.engines.intelligence.portfolio_planner import PortfolioPlanner
    from agents.engines.research_engine import ResearchEngine

    engine = ResearchEngine()
    pp = PortfolioPlanner(engine)

    r1 = pp.analyze_portfolio([])
    assert r1["ranked_niches"] == [], "Empty niche list should produce an empty ranking, not crash"
    assert r1["top_pick"] is None, "Empty niche list should have no top_pick"

    r2 = pp.analyze_portfolio([""])
    assert r2["niches_analyzed"] == 1
    assert isinstance(r2["ranked_niches"], list)

    print("[PASS] portfolio planner handles empty niche list and a problematic niche without crashing the whole run")


def test_multi_market_optimizer_edge_cases():
    from agents.engines.intelligence.multi_market_optimizer import MultiMarketOptimizer
    mmo = MultiMarketOptimizer()
    r = mmo.compare(0, demand_score=None, competition_score=None)
    assert r["recommended_marketplace"] in mmo.marketplaces
    for marketplace, data in r["by_marketplace"].items():
        assert data["estimated_monthly_revenue"] >= 0, f"{marketplace} produced negative revenue"
    print("[PASS] multi-market optimizer handles zero pages and None scores without crash")


def test_business_dashboard_edge_cases():
    from agents.engines.intelligence.business_dashboard import BusinessDashboard
    bd_missing = BusinessDashboard("this_directory_does_not_exist_xyz")
    r1 = bd_missing.generate()
    assert r1["total_books"] == 0, "Missing directory should report 0 books, not crash"

    import tempfile, os
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "broken.json"), "w") as f:
            f.write("not valid json {{{")
        bd_corrupt = BusinessDashboard(tmpdir)
        r2 = bd_corrupt.generate()
        assert r2["corrupted_files_skipped"] == 1, "Corrupted JSON file was not detected/skipped correctly"
    print("[PASS] business dashboard handles missing directory and corrupted JSON files without crash")
if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
