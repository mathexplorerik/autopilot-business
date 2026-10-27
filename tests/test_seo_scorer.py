"""
SEO scorer tests (V16)
Checks the scorer gives full marks to a complete listing, takes marks
off for each specific problem, and never crashes on bad input.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.seo_scorer import SEOScorer

GOOD = {
    "title": "Lion Coloring Book for Kids Ages 4-8: 40 Fun and Adorable Lion Coloring Pages for Children",
    "subtitle": "A Fun Lion Activity Book for Kids Ages 4-8 Years",
    "description": "Lion coloring pages for children. " * 20,
    "keywords": [
        "lion coloring book for kids",
        "lion coloring pages children",
        "lion activity book ages 4-8",
        "cute lion coloring book",
        "big cat coloring book kids",
        "lion gift for kids",
        "easy lion coloring pages",
    ],
}


def _variant(**changes):
    seo = dict(GOOD)
    seo.update(changes)
    return seo


def _failed(result):
    return [c["name"] for c in result["checks"] if not c["passed"]]


def test_complete_listing_scores_100():
    r = SEOScorer().score(GOOD, "lion")
    assert r["score"] == 100, "complete listing scored " + str(r["score"]) + ": " + str(r["failed"])
    print("[PASS] complete listing scores 100")


def test_checks_add_up_to_100():
    r = SEOScorer().score(GOOD, "lion")
    assert sum(c["max_points"] for c in r["checks"]) == 100, "check weights do not add up to 100"
    print("[PASS] check weights add up to 100")


def test_niche_late_in_title_loses_points():
    late = _variant(title=("A" * 70) + " lion coloring book for kids ages 4-8")
    r = SEOScorer().score(late, "lion")
    assert _failed(r) == ["niche_in_title_start"], "unexpected failures: " + str(_failed(r))
    assert r["score"] == 85, "expected 85, got " + str(r["score"])
    print("[PASS] niche late in the title loses exactly its 15 points")


def test_duplicate_keywords_flagged_ignoring_case():
    kws = list(GOOD["keywords"])
    kws[1] = kws[0].upper()
    r = SEOScorer().score(_variant(keywords=kws), "lion")
    assert "no_duplicate_keywords" in _failed(r), "case-different duplicate was not caught"
    print("[PASS] duplicate keywords are caught even when case differs")


def test_overlong_keyword_flagged():
    kws = list(GOOD["keywords"])
    kws[0] = "lion " + "x" * 60
    r = SEOScorer().score(_variant(keywords=kws), "lion")
    assert "keyword_length" in _failed(r), "a 65-character keyword was accepted"
    print("[PASS] keyword over 50 characters is flagged")


def test_unused_keyword_slots_flagged():
    r = SEOScorer().score(_variant(keywords=GOOD["keywords"][:4]), "lion")
    assert "keyword_slots_used" in _failed(r), "4 of 7 keyword slots was accepted"
    print("[PASS] unused keyword slots are flagged")


def test_description_too_short_and_too_long_flagged():
    short = SEOScorer().score(_variant(description="Lion book."), "lion")
    assert "description_min_length" in _failed(short), "a 10-character description was accepted"
    long_text = SEOScorer().score(_variant(description="lion " * 1000), "lion")
    assert "description_max_length" in _failed(long_text), "a 5000-character description was accepted"
    print("[PASS] too-short and too-long descriptions are flagged")


def test_word_pages_does_not_count_as_an_age():
    no_age = _variant(
        title="Lion Coloring Book for Kids: 40 Fun and Adorable Lion Coloring Pages",
        subtitle="40 pages of fun lion coloring",
    )
    r = SEOScorer().score(no_age, "lion")
    assert "age_range_mentioned" in _failed(r), "the word pages was mistaken for an age mention"
    print("[PASS] the word pages is not mistaken for an age mention")


def test_garbage_input_never_crashes():
    inputs = [
        None,
        {},
        "just text",
        42,
        {"title": 123, "keywords": None, "description": ["a"]},
        {"keywords": "a, b, c"},
    ]
    for item in inputs:
        r = SEOScorer().score(item, "lion")
        assert isinstance(r["score"], int) and 0 <= r["score"] <= 100, "bad score for input " + repr(item)
    assert SEOScorer().score({}, "lion")["score"] == 0, "an empty listing should score 0"
    print("[PASS] bad or empty input never crashes, empty listing scores 0")


def run_all():
    tests = [
        test_complete_listing_scores_100,
        test_checks_add_up_to_100,
        test_niche_late_in_title_loses_points,
        test_duplicate_keywords_flagged_ignoring_case,
        test_overlong_keyword_flagged,
        test_unused_keyword_slots_flagged,
        test_description_too_short_and_too_long_flagged,
        test_word_pages_does_not_count_as_an_age,
        test_garbage_input_never_crashes,
    ]
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            failed += 1
            print("[FAIL] " + test.__name__ + ": " + str(e))
        except Exception as e:
            failed += 1
            print("[ERROR] " + test.__name__ + ": " + type(e).__name__ + ": " + str(e))
    print()
    if failed:
        print(str(failed) + "/" + str(len(tests)) + " SEO scorer tests FAILED")
    else:
        print("All " + str(len(tests)) + " SEO scorer tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
