"""
master.py --ask tests (V16)
Checks the confirm-before-run flow with a fake terminal and fake input:
yes runs, no or empty cancels, no terminal never runs, errors never run,
and ordinary commands are unaffected.
"""

import contextlib
import io
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import master


class FakeStdin:
    def __init__(self, tty):
        self._tty = tty

    def isatty(self):
        return self._tty


def ask(words, tty=True, answer="y"):
    cmd = master.MasterCommand()
    out = io.StringIO()
    asked = {"n": 0}

    def fake_input(prompt=""):
        asked["n"] += 1
        return answer

    with mock.patch.object(sys, "stdin", FakeStdin(tty)), \
            mock.patch("builtins.input", fake_input), \
            contextlib.redirect_stdout(out):
        result = cmd._ask_to_args(words)
    return result, out.getvalue(), asked["n"]


def test_yes_returns_the_arguments():
    result, text, asked = ask(["lion", "story", "book"], answer="y")
    assert result == ["lion", "--story"], "wrong arguments: " + str(result)
    assert asked == 1, "the user was not asked exactly once"
    assert "python3 master.py lion --story" in text, "the command was not shown"
    print("[PASS] yes returns the arguments after showing the command")


def test_answer_is_case_insensitive_and_strict():
    assert ask(["lion", "book"], answer="YES")[0] == ["lion"], "YES was not accepted"
    assert ask(["lion", "book"], answer=" y ")[0] == ["lion"], "' y ' was not accepted"
    for answer in ("n", "", "no", "yep", "ok"):
        assert ask(["lion", "book"], answer=answer)[0] is None, answer + " should cancel"
    print("[PASS] y and yes run, anything else (including empty) cancels")


def test_cancel_says_so():
    result, text, asked = ask(["lion", "book"], answer="n")
    assert result is None and "Cancelled" in text, "cancel was not reported"
    print("[PASS] cancelling is reported and nothing runs")


def test_no_terminal_never_runs_and_never_asks():
    result, text, asked = ask(["lion", "story", "book"], tty=False)
    assert result is None, "it ran without a terminal"
    assert asked == 0, "it tried to ask without a terminal"
    assert "Not running" in text and "python3 master.py lion --story" in text, "no-terminal message or command missing"
    print("[PASS] without a terminal it shows the command and does not run or ask")


def test_errors_never_run_and_never_ask():
    result, text, asked = ask(["make", "a", "book"])
    assert result is None and asked == 0, "an invalid request ran or asked"
    assert "no niche" in text, "the error was not shown"
    print("[PASS] an invalid request shows its error and never runs")


def test_warnings_are_shown_before_the_question():
    result, text, asked = ask(["50", "page", "dinosaurs", "book"], answer="n")
    assert "pages=50 will be ignored" in text, "the ignored-pages warning was not shown"
    print("[PASS] warnings are shown before the question")


def test_run_with_ask_does_not_build_a_book_when_nothing_is_confirmed():
    cmd = master.MasterCommand()

    def must_not_run(*args, **kwargs):
        raise AssertionError("a book was built without confirmation")

    out = io.StringIO()
    with mock.patch.object(sys, "stdin", FakeStdin(False)), \
            mock.patch.object(cmd, "_run_book", must_not_run), \
            contextlib.redirect_stdout(out):
        value = cmd.run(["--ask", "lion", "story", "book"])
    assert value is None, "run() returned something for an unconfirmed request"
    print("[PASS] run() with --ask builds nothing when nothing is confirmed")


def test_confirmed_request_reaches_the_book_builder():
    cmd = master.MasterCommand()
    seen = {}

    def fake_build(config):
        seen["config"] = config
        return "built"

    out = io.StringIO()
    with mock.patch.object(sys, "stdin", FakeStdin(True)), \
            mock.patch("builtins.input", lambda prompt="": "y"), \
            mock.patch.object(cmd, "_run_book", fake_build), \
            contextlib.redirect_stdout(out):
        value = cmd.run(["--ask", "lion", "story", "book", "for", "christmas"])
    assert value == "built", "the confirmed request did not reach the builder"
    config = seen["config"]
    assert config["niche"] == "lion" and config["book_type"] == "story" and config["season"] == "christmas", (
        "the builder got the wrong config: " + str(config)
    )
    print("[PASS] a confirmed request reaches the builder with the right settings")


def test_ordinary_commands_are_unaffected():
    cmd = master.MasterCommand()
    out = io.StringIO()
    with mock.patch.object(cmd, "_run_book", lambda config: "ran " + config["niche"]), \
            contextlib.redirect_stdout(out):
        value = cmd.run(["lion"])
    assert value == "ran lion", "a normal command no longer reaches the builder"
    print("[PASS] ordinary commands still work as before")


def run_all():
    tests = [
        test_yes_returns_the_arguments,
        test_answer_is_case_insensitive_and_strict,
        test_cancel_says_so,
        test_no_terminal_never_runs_and_never_asks,
        test_errors_never_run_and_never_ask,
        test_warnings_are_shown_before_the_question,
        test_run_with_ask_does_not_build_a_book_when_nothing_is_confirmed,
        test_confirmed_request_reaches_the_book_builder,
        test_ordinary_commands_are_unaffected,
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
        print(str(failed) + "/" + str(len(tests)) + " master --ask tests FAILED")
    else:
        print("All " + str(len(tests)) + " master --ask tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
