"""
Command parser tests (V16)
Checks the request is turned into the right master.py arguments, that
ignored flags carry a warning, and that bad input is rejected without
crashing or letting text from the request become a flag.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.command_parser import CommandParser

ALLOWED_FLAGS = {"--story", "--season", "--pages", "--age", "--provider", "--bundle", "--dashboard", "--portfolio"}


def parse(text):
    return CommandParser().parse(text)


def any_has(items, fragment):
    return any(fragment in item for item in items)


def test_story_book_with_season():
    r = parse("make a story book about lion with christmas")
    assert r["ok"], str(r["errors"])
    assert r["argv"] == ["lion", "--story", "--season", "christmas"], "wrong argv: " + str(r["argv"])
    assert r["command_line"] == "python3 master.py lion --story --season christmas", "wrong command line"
    print("[PASS] story book with a season becomes the right master.py command")


def test_pages_and_age_are_passed_and_warned():
    r = parse("50 page dinosaurs book for ages 4-6")
    assert r["argv"] == ["dinosaurs", "--pages", "50"], "wrong argv: " + str(r["argv"])
    assert r["age"] == "kids" and not any_has(r["warnings"], "age="), "kids is the default and must not warn"
    assert any_has(r["warnings"], "pages=50 will be ignored"), "no warning that pages is ignored"
    r2 = parse("20 pages animals book for toddlers")
    assert r2["argv"] == ["animals", "--pages", "20", "--age", "toddler"], "wrong argv: " + str(r2["argv"])
    assert any_has(r2["warnings"], "age=toddler will be ignored"), "no warning that age is ignored"
    print("[PASS] pages and age are passed on and each ignored flag carries a warning")


def test_age_groups_from_numbers():
    cases = [("lion book ages 2-3", "toddler"), ("lion book ages 4-6", "kids"), ("lion book ages 9-12", "teens"),
             ("lion book ages 16", "adults"), ("6 years old lion book", "kids")]
    for text, expected in cases:
        r = parse(text)
        assert r["age"] == expected, text + " gave " + str(r["age"]) + ", expected " + expected
        assert r["niche"] == "lion", text + " lost the niche: " + str(r["niche"])
    print("[PASS] ages are mapped to toddler / kids / teens / adults")


def test_pages_written_either_way():
    assert parse("pages 25 lion book")["pages"] == 25, "'pages 25' was not read"
    assert parse("lion book 300 pages")["pages"] == 300 and parse("lion book 300 pages")["ok"], "300 pages is allowed"
    print("[PASS] pages are read from '25 pages' and 'pages 25'")


def test_bad_page_counts_are_errors():
    for text in ("0 pages lion book", "lion book 301 pages", "5000 pages lion book", "12345 pages lion"):
        r = parse(text)
        assert not r["ok"] and r["argv"] == [], text + " was accepted"
        assert any_has(r["errors"], "pages must be between"), text + " has no pages error"
    print("[PASS] page counts outside 1-300 are errors and produce no command")


def test_provider_phrases():
    r = parse("lion story book using stability")
    assert r["argv"] == ["lion", "--story", "--provider", "stability"], "wrong argv: " + str(r["argv"])
    assert any_has(r["warnings"], "API key"), "a real provider has no key warning"
    assert parse("lion book with openai")["provider"] == "openai", "'with openai' was not read"
    r_manual = parse("lion book using manual")
    assert r_manual["provider"] == "manual" and not any_has(r_manual["warnings"], "API key"), "manual must not warn about a key"
    print("[PASS] provider is read and a real provider warns about the key")


def test_dashboard_and_portfolio():
    assert parse("dashboard")["argv"] == ["--dashboard"], "plain dashboard wrong"
    r = parse("show me the business dashboard for christmas")
    assert r["argv"] == ["--dashboard", "--season", "christmas"], "wrong argv: " + str(r["argv"])
    assert r["niche"] is None, "a dashboard request got a niche"
    assert parse("portfolio")["argv"] == ["--portfolio"], "plain portfolio wrong"
    print("[PASS] dashboard and portfolio requests need no niche")


def test_bundle_request_warns():
    r = parse("bundle of dinosaurs books")
    assert r["argv"] == ["dinosaurs", "--bundle"], "wrong argv: " + str(r["argv"])
    assert any_has(r["warnings"], "bundle is unverified"), "no bundle warning"
    print("[PASS] a bundle request works and carries its unverified warning")


def test_season_words_and_niche_names():
    assert parse("diwali coloring book")["argv"] == ["diwali"], "a season-only request should use it as the niche"
    assert parse("bakra eid book")["niche"] == "bakra eid", "a known two-word niche was split"
    r = parse("eid lion book")
    assert r["niche"] == "lion" and r["season"] == "eid", "season and niche not separated: " + str(r["niche"]) + "/" + str(r["season"])
    print("[PASS] seasons and niche names are told apart")


def test_known_and_unknown_niche_notes():
    assert any_has(parse("dinosaurs book")["notes"], "is a known niche"), "a known niche was not noted"
    assert any_has(parse("lion book")["notes"], "not one of the known niches"), "an unknown niche was not noted"
    print("[PASS] known and unknown niches are told apart")


def test_hinglish_request():
    r = parse("lion ki story book banao")
    assert r["argv"] == ["lion", "--story"], "wrong argv: " + str(r["argv"])
    print("[PASS] a short Hinglish request is understood")


def test_bad_input_is_rejected_without_crashing():
    for bad in (None, "", "   ", 42, ["lion"], {}):
        r = parse(bad)
        assert not r["ok"] and r["errors"] and r["argv"] == [], "bad input " + repr(bad) + " was accepted"
    r = parse("make a book")
    assert not r["ok"] and any_has(r["errors"], "no niche"), "a request with no niche was accepted"
    print("[PASS] empty, wrong-type and niche-less requests are rejected")


def test_request_text_cannot_become_a_flag():
    r = parse("; rm -rf / --pages 5")
    assert not r["argv"][0].startswith("-"), "the niche slot starts with a dash"
    for item in r["argv"]:
        if item.startswith("--"):
            assert item in ALLOWED_FLAGS, "unexpected flag " + item
    assert "'rm rf'" in r["command_line"], "the niche was not quoted for the shell"
    print("[PASS] text in the request cannot add flags and the command line is quoted")


def test_very_long_text_is_cut_and_rejected_safely():
    r = parse("lion " * 1000)
    assert not r["ok"], "a 100-word niche was accepted"
    assert any_has(r["notes"], "longer than"), "the cut was not mentioned"
    print("[PASS] very long text is cut, noted and rejected without crashing")


def run_all():
    tests = [
        test_story_book_with_season,
        test_pages_and_age_are_passed_and_warned,
        test_age_groups_from_numbers,
        test_pages_written_either_way,
        test_bad_page_counts_are_errors,
        test_provider_phrases,
        test_dashboard_and_portfolio,
        test_bundle_request_warns,
        test_season_words_and_niche_names,
        test_known_and_unknown_niche_notes,
        test_hinglish_request,
        test_bad_input_is_rejected_without_crashing,
        test_request_text_cannot_become_a_flag,
        test_very_long_text_is_cut_and_rejected_safely,
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
        print(str(failed) + "/" + str(len(tests)) + " command parser tests FAILED")
    else:
        print("All " + str(len(tests)) + " command parser tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
