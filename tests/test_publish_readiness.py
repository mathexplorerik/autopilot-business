"""
Publish readiness tests (V16)
Checks the verdict is READY only for a complete book, that each
specific problem blocks it with a clear reason, and that bad input
never crashes.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.publish_readiness import PublishReadiness

GOOD_SEO = {
    "title": "Lion Coloring Book for Kids Ages 4-8: 40 Fun Lion Coloring Pages",
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
    "categories": ["Children's Books > Arts, Music and Photography"],
    "score": {"score": 100},
}


def _make_files(tmp):
    pdf = os.path.join(tmp, "book.pdf")
    cover = os.path.join(tmp, "cover.png")
    for path in (pdf, cover):
        with open(path, "wb") as f:
            f.write(b"not empty")
    return pdf, cover


def _assess(tmp, **changes):
    pdf, cover = _make_files(tmp)
    args = {
        "seo": dict(GOOD_SEO),
        "price": 8.99,
        "total_pages": 40,
        "images_found": 40,
        "cover_path": cover,
        "interior_pdf_path": pdf,
    }
    args.update(changes)
    return PublishReadiness().assess(**args)


def test_complete_book_is_ready(tmp):
    r = _assess(tmp)
    assert r["ready"] and r["verdict"] == "READY", "complete book was blocked: " + str(r["blockers"])
    assert r["blockers"] == [], "a ready book should have no blockers"
    print("[PASS] a complete book is READY")


def test_all_placeholders_block(tmp):
    r = _assess(tmp, images_found=0)
    assert not r["ready"], "a book with zero real images was called ready"
    assert any("none of the 40" in b for b in r["blockers"]), "blocker did not say all pages are placeholders"
    print("[PASS] all-placeholder PDF blocks with a clear reason")


def test_some_placeholders_block(tmp):
    r = _assess(tmp, images_found=30)
    assert not r["ready"], "a book with 10 placeholder pages was called ready"
    assert any("10 of 40" in b for b in r["blockers"]), "blocker did not give the 10 of 40 count"
    print("[PASS] partial placeholders block and give the count")


def test_unknown_image_count_blocks(tmp):
    r = _assess(tmp, images_found=None)
    assert not r["ready"], "an unknown image count was treated as fine"
    print("[PASS] unknown image count blocks")


def test_missing_cover_blocks(tmp):
    r = _assess(tmp, cover_path=None)
    assert not r["ready"] and any("cover" in b for b in r["blockers"]), "missing cover did not block"
    r2 = _assess(tmp, cover_path=os.path.join(tmp, "does_not_exist.png"))
    assert not r2["ready"], "a cover path that does not exist did not block"
    print("[PASS] missing cover blocks")


def test_missing_interior_pdf_blocks(tmp):
    r = _assess(tmp, interior_pdf_path=os.path.join(tmp, "nope.pdf"))
    assert not r["ready"] and any("interior PDF" in b for b in r["blockers"]), "missing PDF did not block"
    print("[PASS] missing interior PDF blocks")


def test_bad_prices_block(tmp):
    for bad in (None, 0, -1, True, "8.99"):
        r = _assess(tmp, price=bad)
        assert not r["ready"], "price " + repr(bad) + " was accepted"
    print("[PASS] missing, zero, negative, boolean and text prices all block")


def test_unsafe_listing_text_blocks(tmp):
    seo = dict(GOOD_SEO)
    seo["description"] = "A lion with a knife. " * 20
    r = _assess(tmp, seo=seo)
    assert not r["ready"], "unsafe listing text was accepted"
    assert any("content safety" in b for b in r["blockers"]), "blocker did not mention content safety"
    print("[PASS] unsafe listing text blocks")


def test_missing_listing_fields_and_categories_block(tmp):
    for field in ("title", "subtitle", "description"):
        seo = dict(GOOD_SEO)
        seo[field] = ""
        assert not _assess(tmp, seo=seo)["ready"], field + " missing did not block"
    seo = dict(GOOD_SEO)
    seo["categories"] = []
    assert not _assess(tmp, seo=seo)["ready"], "empty categories did not block"
    seo = dict(GOOD_SEO)
    seo["keywords"] = []
    assert not _assess(tmp, seo=seo)["ready"], "no keywords did not block"
    print("[PASS] missing title, subtitle, description, categories and keywords all block")


def test_low_seo_score_and_odd_keyword_count_only_warn(tmp):
    seo = dict(GOOD_SEO)
    seo["score"] = {"score": 60}
    r = _assess(tmp, seo=seo)
    assert r["ready"] and r["warnings"], "a low SEO score should warn but not block"
    seo = dict(GOOD_SEO)
    seo["keywords"] = GOOD_SEO["keywords"][:4]
    r2 = _assess(tmp, seo=seo)
    assert r2["ready"] and r2["warnings"], "4 keywords should warn but not block"
    print("[PASS] low SEO score and unusual keyword count warn without blocking")


def test_garbage_input_never_crashes(tmp):
    r = PublishReadiness().assess(None, None, "x", "y", None, None)
    assert not r["ready"], "all-None input was called ready"
    r2 = PublishReadiness().assess("text", [], {}, 3.5, 7, 42)
    assert not r2["ready"], "nonsense input was called ready"
    print("[PASS] garbage input never crashes and is never READY")


def run_all():
    tests = [
        test_complete_book_is_ready,
        test_all_placeholders_block,
        test_some_placeholders_block,
        test_unknown_image_count_blocks,
        test_missing_cover_blocks,
        test_missing_interior_pdf_blocks,
        test_bad_prices_block,
        test_unsafe_listing_text_blocks,
        test_missing_listing_fields_and_categories_block,
        test_low_seo_score_and_odd_keyword_count_only_warn,
        test_garbage_input_never_crashes,
    ]
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for test in tests:
            try:
                test(tmp)
            except AssertionError as e:
                failed += 1
                print("[FAIL] " + test.__name__ + ": " + str(e))
            except Exception as e:
                failed += 1
                print("[ERROR] " + test.__name__ + ": " + type(e).__name__ + ": " + str(e))
    print()
    if failed:
        print(str(failed) + "/" + str(len(tests)) + " publish readiness tests FAILED")
    else:
        print("All " + str(len(tests)) + " publish readiness tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
