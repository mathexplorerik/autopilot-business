"""
Dashboard CLI test (V16)
Runs master.py --dashboard for real and checks the plan it writes: every
niche is planned, the ordering and the test-small rule are consistent, the
dashboard top 5 still matches, bundles are sane and the disclaimers are there.
Old output files are deleted first so a stale file can never make it pass.

It checks the plan is well-formed and consistent. It cannot tell whether the
numbers are good, because they come from heuristic scores.
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

from agents.data.subjects import SUBJECTS

STRATEGY = os.path.join(REPO_ROOT, "output", "business_dashboard", "strategy.json")
DASHBOARD = os.path.join(REPO_ROOT, "output", "business_dashboard", "dashboard.json")
LEVELS = ("LOW", "MEDIUM", "HIGH")
ACTIONS = ("build", "test small")

_cache = {}


def _num(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def run_dashboard():
    for path in (STRATEGY, DASHBOARD):
        if os.path.exists(path):
            os.remove(path)
    return subprocess.run(
        [sys.executable, "master.py", "--dashboard"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )


def outputs():
    if "data" not in _cache:
        for path, name in ((STRATEGY, "strategy.json"), (DASHBOARD, "dashboard.json")):
            assert os.path.exists(path), name + " was not written by this run"
        with open(STRATEGY, encoding="utf-8") as f:
            strategy = json.load(f)
        with open(DASHBOARD, encoding="utf-8") as f:
            dashboard = json.load(f)
        _cache["data"] = (strategy, dashboard)
    return _cache["data"]


def test_run_succeeds(result):
    assert result.returncode == 0, (
        "master.py --dashboard exited with code " + str(result.returncode) + "\n" + result.stderr[-1500:]
    )
    print("[PASS] master.py --dashboard exits with code 0")


def test_output_shows_plan_and_log(result):
    assert "Launch plan" in result.stdout, "the launch plan was not printed"
    assert "Log saved" in result.stdout, "the run log was not reported"
    print("[PASS] the launch plan is printed and the run log is saved")


def test_every_niche_is_planned():
    strategy, _ = outputs()
    planned = [item["niche"] for item in strategy["strategy"]["launch_order"]]
    assert len(planned) == len(SUBJECTS), (
        str(len(planned)) + " niches planned but " + str(len(SUBJECTS)) + " exist - a niche failed or was dropped"
    )
    assert len(set(planned)) == len(planned), "a niche appears twice in the launch order"
    print("[PASS] all " + str(len(planned)) + " niches are planned exactly once")


def test_launch_order_is_consistent():
    strategy, _ = outputs()
    items = strategy["strategy"]["launch_order"]
    assert [i["order"] for i in items] == list(range(1, len(items) + 1)), "order numbers are not 1..N"
    scores = [i["portfolio_score"] for i in items]
    assert scores == sorted(scores, reverse=True), "scores are not in descending order"
    for i in items:
        assert i["action"] in ACTIONS, i["niche"] + " has an unknown action " + repr(i["action"])
        assert i["confidence"] in LEVELS, i["niche"] + " has an unknown confidence " + repr(i["confidence"])
        assert i["reasons"], i["niche"] + " has no reasons"
        assert (i["action"] == "test small") == (i["confidence"] == "LOW"), (
            i["niche"] + ": action " + i["action"] + " does not match confidence " + i["confidence"]
        )
    print("[PASS] order, scores, actions and reasons are consistent")


def test_dashboard_top5_is_unchanged_and_matches():
    strategy, dashboard = outputs()
    top = dashboard.get("top_niches")
    assert isinstance(top, list), "dashboard.json has no top_niches list"
    assert len(top) == 5, "dashboard shows " + str(len(top)) + " top niches, expected 5"
    first = strategy["strategy"]["launch_order"][0]["niche"]
    assert top[0]["niche"] == first, "dashboard top niche " + top[0]["niche"] + " differs from launch order first " + first
    print("[PASS] the dashboard still shows 5 niches and agrees with the launch order")


def test_bundles_are_valid():
    strategy, _ = outputs()
    planned = {i["niche"] for i in strategy["strategy"]["launch_order"]}
    for b in strategy["bundles"]["bundles"]:
        assert len(b["niches"]) >= 2, "bundle " + b["group"] + " has fewer than 2 niches"
        assert set(b["niches"]) <= planned, "bundle " + b["group"] + " has a niche that is not planned"
        assert _num(b["combined_monthly_revenue_estimate"]) and b["combined_monthly_revenue_estimate"] >= 0, (
            "bundle " + b["group"] + " has a bad revenue estimate"
        )
        assert b["weakest_confidence"] in LEVELS, "bundle " + b["group"] + " has a bad confidence"
    print("[PASS] every bundle has 2 or more planned niches and sane numbers")


def test_disclaimers_are_present():
    strategy, _ = outputs()
    assert strategy["strategy"].get("disclaimer"), "strategy has no disclaimer"
    assert strategy["bundles"].get("disclaimer"), "bundles have no disclaimer"
    print("[PASS] both outputs carry the not-market-research disclaimer")


def run_all():
    try:
        result = run_dashboard()
    except subprocess.TimeoutExpired:
        print("[FAIL] master.py --dashboard did not finish within 180 seconds")
        return False

    tests = [
        ("test_run_succeeds", lambda: test_run_succeeds(result)),
        ("test_output_shows_plan_and_log", lambda: test_output_shows_plan_and_log(result)),
        ("test_every_niche_is_planned", test_every_niche_is_planned),
        ("test_launch_order_is_consistent", test_launch_order_is_consistent),
        ("test_dashboard_top5_is_unchanged_and_matches", test_dashboard_top5_is_unchanged_and_matches),
        ("test_bundles_are_valid", test_bundles_are_valid),
        ("test_disclaimers_are_present", test_disclaimers_are_present),
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            failed += 1
            print("[FAIL] " + name + ": " + str(e))
        except Exception as e:
            failed += 1
            print("[ERROR] " + name + ": " + type(e).__name__ + ": " + str(e))
    print()
    if failed:
        print(str(failed) + "/" + str(len(tests)) + " dashboard CLI tests FAILED")
    else:
        print("All " + str(len(tests)) + " dashboard CLI tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
