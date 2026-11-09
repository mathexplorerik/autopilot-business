"""
master.py choice tests (V16)
--season and --provider must be one of the values the engine really knows.
Anything else is a clear error with exit code 2, before any book is built.
The command parser keeps its own copies of these lists, so a test checks
they still match the engine's lists.
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
from agents.command_parser import CommandParser
from agents.data.animals.season_accessories import SEASON_ACCESSORIES
from agents.image_engine.provider_manager import ProviderManager


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


def test_known_values_are_accepted_in_any_case():
    for season in SEASON_ACCESSORIES:
        assert parse(["lion", "--season", season])["season"] == season, season + " was rejected"
    assert parse(["lion", "--season", "Christmas"])["season"] == "christmas", "Christmas was not lower-cased"
    for provider in ProviderManager().providers():
        assert parse(["lion", "--provider", provider])["provider"] == provider, provider + " was rejected"
    assert parse(["lion", "--provider", "STABILITY"])["provider"] == "stability", "STABILITY was not lower-cased"
    print("[PASS] every known season and provider is accepted, in any letter case")


def test_unknown_season_is_a_clear_error():
    for args in (["lion", "--season", "chrismas"], ["--dashboard", "--season", "chrismas"],
                 ["--portfolio", "--season", "summer"]):
        code, text = rejected(args)
        assert code == 2, str(args) + " was not rejected (exit " + repr(code) + ")"
        assert "unknown season" in text and "christmas" in text, str(args) + " error does not list the known seasons: " + text
    print("[PASS] an unknown season is a clear error that lists the known seasons")


def test_unknown_provider_is_a_clear_error():
    for bad in ("foo", "stabilty", "dalle"):
        code, text = rejected(["lion", "--provider", bad])
        assert code == 2, bad + " was not rejected (exit " + repr(code) + ")"
        assert "unknown provider" in text and "manual" in text, bad + " error does not list the known providers: " + text
    print("[PASS] an unknown provider is a clear error that lists the known providers")


def test_bad_choice_stops_before_anything_is_built():
    cmd = master.MasterCommand()

    def must_not_run(*args, **kwargs):
        raise AssertionError("a book was built from a bad command")

    for args in (["lion", "--season", "chrismas"], ["lion", "--provider", "foo"]):
        try:
            with mock.patch.object(cmd, "_run_book", must_not_run), contextlib.redirect_stdout(io.StringIO()):
                cmd.run(args)
        except SystemExit as e:
            assert e.code == 2, "wrong exit code " + repr(e.code)
        else:
            raise AssertionError(str(args) + " did not stop")
    print("[PASS] a bad season or provider stops before any book is built")


def test_parser_lists_match_the_engine_lists():
    assert set(CommandParser.SEASONS) == set(SEASON_ACCESSORIES), (
        "CommandParser.SEASONS " + str(sorted(CommandParser.SEASONS)) + " differs from the engine " + str(sorted(SEASON_ACCESSORIES))
    )
    assert set(CommandParser.PROVIDERS) == set(ProviderManager().providers()), (
        "CommandParser.PROVIDERS " + str(sorted(CommandParser.PROVIDERS)) + " differs from the engine " + str(ProviderManager().providers())
    )
    print("[PASS] the command parser's season and provider lists match the engine's")


def test_real_process_prints_an_error_not_a_traceback():
    for args, fragment in ((["lion", "--provider", "foo"], "unknown provider"),
                           (["lion", "--season", "chrismas"], "unknown season")):
        result = subprocess.run([sys.executable, "master.py"] + args, cwd=REPO_ROOT,
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == 2, str(args) + " exited with " + str(result.returncode)
        assert "Traceback" not in result.stdout + result.stderr, str(args) + " printed a traceback"
        assert fragment in result.stdout, str(args) + " did not print its error"
    print("[PASS] a real run exits with code 2 and prints an error, not a traceback")


def run_all():
    tests = [
        test_known_values_are_accepted_in_any_case,
        test_unknown_season_is_a_clear_error,
        test_unknown_provider_is_a_clear_error,
        test_bad_choice_stops_before_anything_is_built,
        test_parser_lists_match_the_engine_lists,
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
        print(str(failed) + "/" + str(len(tests)) + " master choice tests FAILED")
    else:
        print("All " + str(len(tests)) + " master choice tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
