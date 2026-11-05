"""
Run log tests (V16)
The log must receive what is printed (without colour codes), the screen must
still get it, old logs must be pruned, and a log that cannot be created
must never stop a run.
"""

import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.utils import run_log


def _isolated(fn):
    real_out, real_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
    try:
        return fn()
    finally:
        run_log.stop_run_log()
        sys.stdout, sys.stderr = real_out, real_err


def test_log_gets_text_without_colour_and_screen_still_gets_it():
    with tempfile.TemporaryDirectory() as tmp:
        def work():
            path = run_log.start_run_log(log_dir=tmp, argv=["master.py", "lion"])
            print("\033[91mred line\033[0m")
            screen = sys.stdout._stream.getvalue()
            run_log.stop_run_log()
            return path, screen
        path, screen = _isolated(work)
        with open(path, encoding="utf-8") as f:
            text = f.read()
    assert "red line" in text, "the printed line is not in the log"
    assert "\033" not in text, "colour codes were left in the log"
    assert "master.py lion" in text, "the command line is not in the log header"
    assert "red line" in screen, "the screen no longer gets the output"
    print("[PASS] log gets the text without colour codes and the screen still gets it")


def test_stderr_is_logged_too():
    with tempfile.TemporaryDirectory() as tmp:
        def work():
            path = run_log.start_run_log(log_dir=tmp)
            print("something broke", file=sys.stderr)
            run_log.stop_run_log()
            return path
        path = _isolated(work)
        with open(path, encoding="utf-8") as f:
            assert "something broke" in f.read(), "stderr was not logged"
    print("[PASS] error output is logged too")


def test_old_logs_are_pruned():
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(1, 6):
            open(os.path.join(tmp, "run_000" + str(i) + ".log"), "w").close()
        open(os.path.join(tmp, "notes.txt"), "w").close()
        def work():
            run_log.start_run_log(log_dir=tmp, keep=3)
            run_log.stop_run_log()
        _isolated(work)
        left = sorted(os.listdir(tmp))
    logs = [n for n in left if n.endswith(".log")]
    assert len(logs) == 3, "expected 3 logs to be kept, found " + str(logs)
    assert "run_0001.log" not in logs and "run_0003.log" not in logs, "the oldest logs were not removed"
    assert "notes.txt" in left, "a file that is not a run log was deleted"
    print("[PASS] only the newest logs are kept and other files are left alone")


def test_starting_twice_does_not_double_wrap():
    with tempfile.TemporaryDirectory() as tmp:
        def work():
            first = run_log.start_run_log(log_dir=tmp)
            second = run_log.start_run_log(log_dir=tmp)
            inner = type(sys.stdout._stream).__name__
            run_log.stop_run_log()
            return first, second, inner
        first, second, inner = _isolated(work)
    assert first == second, "second start returned a different log"
    assert inner != "_Tee", "stdout was wrapped twice"
    print("[PASS] starting twice does not double-wrap the output")


def test_unusable_log_dir_does_not_crash_or_change_output():
    with tempfile.TemporaryDirectory() as tmp:
        blocker = os.path.join(tmp, "not_a_folder")
        open(blocker, "w").close()
        def work():
            before = sys.stdout
            path = run_log.start_run_log(log_dir=blocker)
            return path, sys.stdout is before
        path, unchanged = _isolated(work)
    assert path is None, "a log was reported although the folder could not be created"
    assert unchanged, "output was wrapped even though there is no log"
    print("[PASS] an unusable log folder is skipped without crashing the run")


def test_stop_restores_the_streams():
    with tempfile.TemporaryDirectory() as tmp:
        def work():
            before = sys.stdout
            run_log.start_run_log(log_dir=tmp)
            run_log.stop_run_log()
            return sys.stdout is before
        assert _isolated(work), "stop did not restore stdout"
    print("[PASS] stopping restores the original streams")


def run_all():
    tests = [
        test_log_gets_text_without_colour_and_screen_still_gets_it,
        test_stderr_is_logged_too,
        test_old_logs_are_pruned,
        test_starting_twice_does_not_double_wrap,
        test_unusable_log_dir_does_not_crash_or_change_output,
        test_stop_restores_the_streams,
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
        print(str(failed) + "/" + str(len(tests)) + " run log tests FAILED")
    else:
        print("All " + str(len(tests)) + " run log tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
