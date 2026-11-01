"""
Publish agent tests (V16)
The upload checklist used to be fixed text with every item ticked,
whatever the book looked like. These tests check it now follows the
real readiness verdict and never ticks anything it has not checked.
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.publish_agent import PublishAgent

BOOK = {"title": "Lion Book", "pages": 40}
SEO = {
    "title": "Lion Coloring Book for Kids",
    "subtitle": "Fun for ages 4-8",
    "description": "Lion pages.",
    "keywords": ["lion coloring book"],
    "categories": ["Children's Books"],
}
NOT_READY = {
    "verdict": "NOT READY",
    "ready": False,
    "blockers": ["none of the 40 pages has a real image (all placeholders)", "cover file is missing or empty"],
    "warnings": ["no SEO score was calculated"],
}
READY = {"verdict": "READY", "ready": True, "blockers": [], "warnings": []}


def _run(readiness, price=None):
    with tempfile.TemporaryDirectory() as tmp:
        old = os.getcwd()
        os.chdir(tmp)
        try:
            PublishAgent().generate(BOOK, SEO, readiness=readiness, price=price)
            with open("output/publish/upload_checklist.txt", encoding="utf-8") as f:
                checklist = f.read()
            with open("output/publish/metadata.json", encoding="utf-8") as f:
                meta = json.load(f)
        finally:
            os.chdir(old)
    return checklist, meta


def test_blocked_book_lists_every_blocker_and_ticks_nothing():
    checklist, _ = _run(NOT_READY)
    assert "NOT READY" in checklist, "checklist did not say NOT READY"
    assert "none of the 40 pages has a real image" in checklist, "image blocker missing"
    assert "cover file is missing" in checklist, "cover blocker missing"
    assert "\u2714" not in checklist, "checklist ticked something for a blocked book"
    print("[PASS] a blocked book lists its blockers and ticks nothing")


def test_unchecked_book_never_claims_anything():
    checklist, _ = _run(None)
    assert "NOT CHECKED" in checklist, "unchecked book was not labelled NOT CHECKED"
    assert "\u2714" not in checklist and "READY" not in checklist.replace("NOT CHECKED", ""), "an unchecked book claimed readiness"
    print("[PASS] when readiness was not run, the checklist says so")


def test_ready_book_has_no_blockers_listed():
    checklist, _ = _run(READY)
    assert "NOT READY" not in checklist, "a ready book was labelled NOT READY"
    assert "\u2718" not in checklist, "a ready book shows a blocker mark"
    print("[PASS] a ready book shows no blockers")


def test_metadata_has_price_categories_and_old_fields():
    _, meta = _run(READY, price=8.99)
    for key in ("title", "subtitle", "description", "keywords", "pages", "language", "trim_size"):
        assert key in meta, "metadata lost the original field " + key
    assert meta["price"] == 8.99, "price was not saved"
    assert meta["categories"] == ["Children's Books"], "categories were not saved"
    print("[PASS] metadata keeps its old fields and now has price and categories")


def run_all():
    tests = [
        test_blocked_book_lists_every_blocker_and_ticks_nothing,
        test_unchecked_book_never_claims_anything,
        test_ready_book_has_no_blockers_listed,
        test_metadata_has_price_categories_and_old_fields,
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
        print(str(failed) + "/" + str(len(tests)) + " publish agent tests FAILED")
    else:
        print("All " + str(len(tests)) + " publish agent tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
