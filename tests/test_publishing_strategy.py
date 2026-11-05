"""
Publishing strategy tests (V16)
Checks ranking, the test-small rule for low confidence, grouping into
bundles, and that bad or error rows never crash anything.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.engines.intelligence.publishing_strategy import BundlePlanner, PublishingStrategy


def row(niche, score, level="HIGH", revenue=100.0, competition=50):
    return {
        "niche": niche,
        "portfolio_score": score,
        "confidence_level": level,
        "estimated_monthly_revenue": revenue,
        "competition_score": competition,
    }


ROWS = [
    row("dinosaurs", 70, "MEDIUM", 600),
    row("animals", 80, "HIGH", 640),
    row("farm animals", 50, "LOW", 300),
    row("diwali", 60, "LOW", 200),
    row("space", 55, "HIGH", 400),
]


def test_launch_order_follows_portfolio_score():
    plan = PublishingStrategy().plan(ROWS)
    names = [item["niche"] for item in plan["launch_order"]]
    assert names == ["animals", "dinosaurs", "diwali", "space", "farm animals"] or names[0] == "animals", "wrong order: " + str(names)
    assert [i["order"] for i in plan["launch_order"]] == [1, 2, 3, 4, 5], "order numbers are wrong"
    scores = [i["portfolio_score"] for i in plan["launch_order"]]
    assert scores == sorted(scores, reverse=True), "scores are not in descending order"
    print("[PASS] launch order follows the portfolio score")


def test_low_confidence_means_test_small():
    plan = PublishingStrategy().plan(ROWS)
    actions = {i["niche"]: i["action"] for i in plan["launch_order"]}
    assert actions["diwali"] == "test small" and actions["farm animals"] == "test small", "LOW confidence was not told to test small"
    assert actions["animals"] == "build" and actions["dinosaurs"] == "build", "HIGH or MEDIUM confidence was held back"
    print("[PASS] low-confidence niches are told to test small")


def test_seasonal_and_high_competition_are_called_out():
    rows = [row("diwali", 60, "HIGH", 100, competition=90), row("animals", 50, "HIGH", 100, competition=40)]
    plan = PublishingStrategy().plan(rows)
    by = {i["niche"]: " ".join(i["reasons"]) for i in plan["launch_order"]}
    assert "seasonal" in by["diwali"], "a festival niche was not flagged as seasonal"
    assert "competition" in by["diwali"], "a high-competition niche was not flagged"
    assert "seasonal" not in by["animals"] and "competition" not in by["animals"], "a plain niche was flagged by mistake"
    print("[PASS] seasonal and high-competition niches are flagged, plain ones are not")


def test_error_and_bad_rows_are_skipped():
    rows = [row("animals", 80), {"niche": "broken", "error": "boom", "portfolio_score": 0},
            {"niche": "", "portfolio_score": 5}, {"portfolio_score": 9}, "text", None,
            {"niche": "space", "portfolio_score": "high"}]
    plan = PublishingStrategy().plan(rows)
    assert [i["niche"] for i in plan["launch_order"]] == ["animals"], "bad rows were not skipped"
    print("[PASS] error rows and bad rows are skipped")


def test_marketplace_choice_comes_from_input_and_carries_a_caveat():
    plan = PublishingStrategy().plan(ROWS, {"best_marketplace": "etsy"})
    assert plan["first_marketplace"] == "etsy", "marketplace was not taken from the input"
    assert any("royalty" in n for n in plan["notes"]), "the royalty-only caveat is missing"
    none_plan = PublishingStrategy().plan(ROWS, None)
    assert none_plan["first_marketplace"] is None and none_plan["notes"] == [], "marketplace invented without input"
    print("[PASS] marketplace comes from the input and carries a caveat")


def test_bundles_group_related_niches_and_sum_revenue():
    result = BundlePlanner().suggest(ROWS)
    animals = [b for b in result["bundles"] if b["group"] == "animals"][0]
    assert animals["niches"] == ["animals", "dinosaurs", "farm animals"], "bundle members or order wrong: " + str(animals["niches"])
    assert animals["combined_monthly_revenue_estimate"] == 1540.0, "revenue sum wrong"
    assert animals["weakest_confidence"] == "LOW", "weakest confidence was not reported"
    assert animals["seasonal"] is False, "animals bundle marked seasonal"
    print("[PASS] related niches are grouped, revenue is summed, weakest confidence is reported")


def test_single_niche_groups_do_not_make_a_bundle():
    result = BundlePlanner().suggest(ROWS)
    groups = [b["group"] for b in result["bundles"]]
    assert "festivals" not in groups, "one festival niche was bundled with nothing"
    assert "fantasy and play" not in groups, "one niche made a bundle"
    print("[PASS] a group with a single niche makes no bundle")


def test_bundle_size_limit_and_ungrouped_niches():
    many = [row("animals", 90), row("dinosaurs", 80), row("farm animals", 70), row("ocean animals", 60),
            row("lion", 50)]
    result = BundlePlanner().suggest(many, max_per_bundle=2)
    assert result["bundles"][0]["niches"] == ["animals", "dinosaurs"], "size limit not applied"
    assert result["ungrouped"] == ["lion"], "an unknown niche was not listed as ungrouped"
    print("[PASS] bundle size limit works and unknown niches are listed")


def test_niche_names_match_ignoring_case_and_festival_bundles_are_seasonal():
    rows = [row("Diwali", 60, "HIGH", 100), row("HOLI", 55, "HIGH", 100)]
    result = BundlePlanner().suggest(rows)
    assert result["bundles"] and result["bundles"][0]["group"] == "festivals", "case-different names were not grouped"
    assert result["bundles"][0]["seasonal"] is True, "a festival bundle was not marked seasonal"
    print("[PASS] niche names match ignoring case and festival bundles are marked seasonal")


def test_garbage_input_never_crashes_and_always_carries_the_disclaimer():
    for bad in (None, [], "x", 5, {}, [None], [{}]):
        plan = PublishingStrategy().plan(bad, "not a dict")
        bundles = BundlePlanner().suggest(bad)
        assert plan["launch_order"] == [] and bundles["bundles"] == [], "garbage produced output"
        assert plan["disclaimer"] and bundles["disclaimer"], "disclaimer missing"
    print("[PASS] garbage input never crashes and the disclaimer is always there")


def run_all():
    tests = [
        test_launch_order_follows_portfolio_score,
        test_low_confidence_means_test_small,
        test_seasonal_and_high_competition_are_called_out,
        test_error_and_bad_rows_are_skipped,
        test_marketplace_choice_comes_from_input_and_carries_a_caveat,
        test_bundles_group_related_niches_and_sum_revenue,
        test_single_niche_groups_do_not_make_a_bundle,
        test_bundle_size_limit_and_ungrouped_niches,
        test_niche_names_match_ignoring_case_and_festival_bundles_are_seasonal,
        test_garbage_input_never_crashes_and_always_carries_the_disclaimer,
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
        print(str(failed) + "/" + str(len(tests)) + " publishing strategy tests FAILED")
    else:
        print("All " + str(len(tests)) + " publishing strategy tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
