"""
master.py argument tests (V16)
Bad arguments must produce a clear error and exit code 2: a --pages that is
not a whole number or is out of range, unknown flags, a flag with no value,
and stray words (such as an unquoted two-word niche). Valid commands must
parse exactly as before.
"""

import contextlib
import io
import os
import subprocess
import sys
from unittest import mock

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

import master


def parse(args):
    with contextlib.redirect_stdout(io.StringIO()):
        return master.MasterCommand().parse(args)


def rejected(args):
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            master.MasterCommand().parse(args)
    except SystemExit as e:
        return e.code, out.getvalue()
    return None, out.getvalue()


def expect_rejected(args, fragment):
    code, text = rejected(args)
    assert code == 2, str(args) + " was not rejected with exit code 2 (got " + repr(code) + ")"
    assert fragment in text, str(args) + " error does not mention '" + fragment + "': " + text


def base(**changes):
    config = {"niche": "", "season": None, "pages": None, "age": "kids",
              "command": "book", "book_type": "coloring_books", "provider": "manual"}
    config.update(changes)
    return config


def test_valid_arguments_still_parse_as_before():
    cases = [
        (["lion", "--story", "--season", "christmas"],
         base(niche="lion", book_type="story", season="christmas")),
        (["--dashboard"], base(command="dashboard")),
        (["--portfolio", "--season", "christmas"], base(command="portfolio", season="christmas")),
        (["animals", "--bundle"], base(niche="animals", command="bundle")),
        (["lion", "--tracing"], base(niche="lion", command="tracing")),
        (["lion", "--pages", "30", "--age", "toddler", "--provider", "stability"],
         base(niche="lion", pages=30, age="toddler", provider="stability")),
        (["jungle animals"], base(niche="jungle animals")),
    ]
    for args, expected in cases:
        got = parse(args)
        assert got == expected, str(args) + " parsed as " + str(got) + ", expected " + str(expected)
    print("[PASS] valid commands parse exactly as before")


def test_pages_that_is_not_a_number_is_a_clear_error():
    for bad in ("abc", "3.5", "", "twenty"):
        expect_rejected(["lion", "--pages", bad], "whole number")
    print("[PASS] a --pages that is not a whole number is a clear error")


def test_pages_out_of_range_is_a_clear_error():
    for bad in ("0", "-5", "301", "99999"):
        expect_rejected(["lion", "--pages", bad], "between")
    assert parse(["lion", "--pages", "1"])["pages"] == 1, "1 page should be allowed"
    assert parse(["lion", "--pages", "300"])["pages"] == 300, "300 pages should be allowed"
    print("[PASS] --pages outside 1-300 is a clear error, 1 and 300 are allowed")


def test_flag_without_a_value_is_an_error():
    for args in (["lion", "--season"], ["lion", "--pages"], ["lion", "--age"], ["lion", "--provider"],
                 ["lion", "--season", "--story"]):
        expect_rejected(args, "needs a value")
    print("[PASS] a flag with no value (or another flag in its place) is an error")


def test_unknown_option_is_an_error():
    for args in (["lion", "--seasn", "christmas"], ["lion", "--help"], ["lion", "--ask"]):
        expect_rejected(args, "unknown option")
    print("[PASS] an unknown option is an error, not silently skipped")


def test_stray_word_is_an_error_and_mentions_quotes():
    expect_rejected(["jungle", "animals"], "unexpected argument 'animals'")
    expect_rejected(["lion", "--story", "extra"], "unexpected argument 'extra'")
    code, text = rejected(["jungle", "animals"])
    assert "quotes" in text, "the error does not tell the user to use quotes"
    print("[PASS] a stray word is an error and the message suggests quotes")


def test_quoted_two_word_niche_works():
    assert parse(["jungle animals", "--story"])["niche"] == "jungle animals", "a quoted niche was not kept whole"
    print("[PASS] a quoted two-word niche still works")


def test_error_happens_before_anything_is_built():
    cmd = master.MasterCommand()

    def must_not_run(*args, **kwargs):
        raise AssertionError("a book was built from a bad command")

    out = io.StringIO()
    try:
        with mock.patch.object(cmd, "_run_book", must_not_run), contextlib.redirect_stdout(out):
            cmd.run(["lion", "--pages", "abc"])
    except SystemExit as e:
        assert e.code == 2, "wrong exit code " + repr(e.code)
    else:
        raise AssertionError("run() did not stop on a bad command")
    print("[PASS] a bad command stops before any book is built")


def test_real_process_prints_an_error_not_a_traceback():
    for args, fragment in ((["lion", "--pages", "abc"], "whole number"),
                           (["jungle", "animals"], "unexpected argument")):
        result = subprocess.run([sys.executable, "master.py"] + args, cwd=REPO_ROOT,
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == 2, str(args) + " exited with " + str(result.returncode)
        assert "Traceback" not in result.stdout + result.stderr, str(args) + " printed a traceback"
        assert fragment in result.stdout, str(args) + " did not print its error"
    print("[PASS] a real run exits with code 2 and prints an error, not a traceback")


def run_all():
    tests = [
        test_valid_arguments_still_parse_as_before,
        test_pages_that_is_not_a_number_is_a_clear_error,
        test_pages_out_of_range_is_a_clear_error,
        test_flag_without_a_value_is_an_error,
        test_unknown_option_is_an_error,
        test_stray_word_is_an_error_and_mentions_quotes,
        test_quoted_two_word_niche_works,
        test_error_happens_before_anything_is_built,
        test_real_process_prints_an_error_not_a_traceback,
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
        print(str(failed) + "/" + str(len(tests)) + " master argument tests FAILED")
    else:
        print("All " + str(len(tests)) + " master argument tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
