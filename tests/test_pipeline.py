"""
=========================================
Pipeline / CLI Integration Test (V13 QA)
=========================================
Actually runs master.py end-to-end (subprocess,
real CLI invocation) instead of only testing the
underlying engines directly. This is the layer
that caught real bugs earlier (character memory
using wrong subject, season accessory not fixed
per-book, target_age showing "kids" instead of a
range, blueprint missing "niche" key) that engine-
level tests completely missed.
"""

import sys
import os
import re
import json
import subprocess
import glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_master(args, timeout=180):
    cmd = [sys.executable, "master.py"] + args
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result


def test_story_book_runs_successfully():
    result = run_master(["lion", "--story", "--season", "christmas"])
    assert result.returncode == 0, (
        f"master.py exited with code {result.returncode}\nSTDERR:\n{result.stderr[-2000:]}"
    )
    print("[PASS] master.py story+season run completed with exit code 0")
    return result


def test_pdf_was_created(stdout_text):
    match = re.search(r"PDF Created\s*:\s*(\S+\.pdf)", stdout_text)
    assert match, "Could not find 'PDF Created' line in master.py output"
    pdf_path = os.path.join(REPO_ROOT, match.group(1))
    assert os.path.exists(pdf_path), f"PDF file does not exist at {pdf_path}"
    assert os.path.getsize(pdf_path) > 1000, f"PDF file is suspiciously small: {os.path.getsize(pdf_path)} bytes"
    print(f"[PASS] PDF created and non-trivial size: {pdf_path}")


def test_character_consistency_in_prompts():
    prompts_path = os.path.join(REPO_ROOT, "output/prompts/prompts.txt")
    assert os.path.exists(prompts_path), "prompts.txt was not generated"

    with open(prompts_path) as f:
        lines = [l.strip() for l in f if l.strip()]

    assert len(lines) >= 10, f"Expected at least 10 prompt lines, got {len(lines)}"

    wearing_phrases = []
    for line in lines:
        m = re.search(r"wearing ([^,]+(?:, [^,]+)?)", line)
        if m:
            wearing_phrases.append(m.group(1))

    assert wearing_phrases, "No 'wearing' phrase found in any prompt (character memory may be missing)"

    first = wearing_phrases[0]
    inconsistent = [p for p in wearing_phrases if p != first]
    assert not inconsistent, (
        f"Character/season accessories are NOT consistent across the book. "
        f"First page: '{first}', but found {len(inconsistent)} different variant(s), "
        f"e.g. '{inconsistent[0]}'"
    )
    print(f"[PASS] character/season accessories consistent across all {len(lines)} pages: '{first}'")


def test_analytics_status_is_valid():
    stats_path = os.path.join(REPO_ROOT, "output/analytics/stats.json")
    assert os.path.exists(stats_path), "stats.json was not generated"

    with open(stats_path) as f:
        stats = json.load(f)

    status = stats.get("status")
    assert status in ("Ready for Publishing", "Needs Review"), (
        f"Unexpected/invalid status value: '{status}'"
    )
    print(f"[PASS] analytics status is a valid, real value: '{status}'")


def test_niche_book_runs_successfully():
    result = run_master(["jungle animals"])
    assert result.returncode == 0, (
        f"master.py niche-mode exited with code {result.returncode}\nSTDERR:\n{result.stderr[-2000:]}"
    )
    print("[PASS] master.py niche-mode run completed with exit code 0")


def run_all():
    tests_run = []

    try:
        result = test_story_book_runs_successfully()
        tests_run.append(True)

        test_pdf_was_created(result.stdout)
        tests_run.append(True)

        test_character_consistency_in_prompts()
        tests_run.append(True)

        test_analytics_status_is_valid()
        tests_run.append(True)

        test_niche_book_runs_successfully()
        tests_run.append(True)

    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except subprocess.TimeoutExpired:
        print("[FAIL] master.py did not complete within the timeout")
        return False
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return False

    print(f"\nAll {len(tests_run)} pipeline checks PASSED")
    return True


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
