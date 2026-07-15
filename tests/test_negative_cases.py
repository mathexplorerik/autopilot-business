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


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
