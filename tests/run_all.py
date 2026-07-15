"""
=========================================
Autopilot QA Suite — Master Runner
=========================================
Runs every QA test module and produces a single
consolidated pass/fail report. Intended to be run
before every release as a quality gate.
"""

import sys
import os
import io
import contextlib
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))


def run_module_main(module_name, entry_point="main", entry_kwargs=None):
    """
    Imports a test module fresh and runs its designated
    entry-point function, capturing stdout so we can inspect
    pass/fail signals without spamming the console.
    """
    import importlib

    if module_name in sys.modules:
        del sys.modules[module_name]

    module = importlib.import_module(module_name)
    func = getattr(module, entry_point)

    buffer = io.StringIO()
    start = time.time()
    with contextlib.redirect_stdout(buffer):
        func(**(entry_kwargs or {}))
    elapsed = time.time() - start

    output = buffer.getvalue()
    return output, elapsed


def evaluate(output, fail_markers=("[FAIL]", "TOTAL ISSUES FOUND", "CRASHES/ERRORS   : ")):
    """
    A run is considered FAIL if any fail marker appears
    with a nonzero count, or any [FAIL] tag is present.
    """
    if "[FAIL]" in output:
        return False

    if "CRASHES/ERRORS   : 0" in output:
        pass
    elif "CRASHES/ERRORS   :" in output:
        return False

    if "TOTAL ISSUES FOUND:" in output:
        return False

    if "Crashed               : 0" in output:
        pass
    elif "Crashed               :" in output:
        return False

    if "Books with malformed prompts : 0" not in output and "Books with malformed prompts :" in output:
        return False

    if "Books with missing fields   : 0" not in output and "Books with missing fields   :" in output:
        return False

    if "Books with duplicate prompts: 0" not in output and "Books with duplicate prompts:" in output:
        return False

    return True


SUITES = [
    ("Semantic",   "test_semantic_consistency", "main", None),
    ("Story",      "test_story_mode_quality", "main", None),
    ("Regression", "test_100_prompt_quality", "run_test", {"total": 100}),
    ("Negative",   "test_negative_cases", "run_all", None),
    ("Stress",     "test_stress_500_books", "main", {"total_books": 500}),
]


def main():
    print("=" * 45)
    print("AUTOPILOT QA SUITE")
    print("=" * 45)
    print()

    results = []

    for label, module_name, entry_point, entry_kwargs in SUITES:
        try:
            output, elapsed = run_module_main(module_name, entry_point, entry_kwargs)
            passed = evaluate(output)
        except Exception as e:
            passed = False
            elapsed = 0.0
            output = f"CRASH while running suite: {type(e).__name__}: {e}"

        results.append((label, passed, elapsed, output))
        status = "PASS" if passed else "FAIL"
        print(f"{label:20} {status}   ({elapsed:.1f}s)")

    print()
    total = len(results)
    passed_count = sum(1 for _, p, _, _ in results if p)

    print(f"TOTAL: {passed_count}/{total} PASS")
    print()

    if passed_count == total:
        print("BUILD STATUS: RELEASE READY \u2705")
    else:
        print("BUILD STATUS: NOT READY \u274c")
        print()
        print("--- Failing suite details ---")
        for label, p, _, output in results:
            if not p:
                print(f"\n### {label} ###")
                print(output[-2000:])

    print("=" * 45)

    return passed_count == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
