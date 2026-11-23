"""
Page count consistency test (V16)
The number of pages must be the same everywhere it is shown: prompts,
metadata.json, the PDF, the listing title, the analytics file. The gate
did not notice before that --pages 20 left "40" in the title.
It runs master.py for real and deletes old outputs first.
"""

import glob
import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = [
    "output/publish/metadata.json",
    "output/seo/seo.json",
    "output/analytics/stats.json",
    "output/prompts/prompts.txt",
]


def run(args):
    for path in FILES:
        full = os.path.join(REPO_ROOT, path)
        if os.path.exists(full):
            os.remove(full)
    return subprocess.run([sys.executable, "master.py"] + args, cwd=REPO_ROOT,
                          capture_output=True, text=True, timeout=240)


def load(path):
    with open(os.path.join(REPO_ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def pdf_pages(stdout):
    m = re.search(r"Pages\s*:\s*(\d+) \(title \+ (\d+) content\)", stdout)
    assert m, "the PDF page line was not found in the output"
    return int(m.group(2))


def check(args, expected):
    result = run(args)
    assert result.returncode == 0, str(args) + " exited with " + str(result.returncode) + "\n" + result.stderr[-800:]
    out = result.stdout
    problems = []

    pdf = pdf_pages(out)
    if pdf != expected:
        problems.append("PDF has " + str(pdf) + " content pages")

    meta = load("output/publish/metadata.json")["pages"]
    if meta != expected:
        problems.append("metadata.json says " + str(meta))

    seo = load("output/seo/seo.json")
    if seo.get("metadata", {}).get("pages") != expected:
        problems.append("seo.json says " + str(seo.get("metadata", {}).get("pages")))
    title_numbers = re.findall(r"\b(\d{1,3}) (?:Fun|unique)", seo.get("title", "") + " " + seo.get("description", ""))
    if any(int(n) != expected for n in title_numbers):
        problems.append("the listing text says " + str(title_numbers))

    stats = load("output/analytics/stats.json")["pages"]
    if stats != expected:
        problems.append("analytics says " + str(stats))

    with open(os.path.join(REPO_ROOT, "output/prompts/prompts.txt"), encoding="utf-8") as f:
        prompt_count = len([line for line in f.read().splitlines() if line.strip()])
    if prompt_count != expected:
        problems.append("prompts.txt has " + str(prompt_count) + " lines")

    assert not problems, "expected " + str(expected) + " pages everywhere: " + "; ".join(problems)


def test_default_story_book_is_40_everywhere():
    check(["lion", "--story"], 40)
    print("[PASS] a default story book shows 40 pages everywhere")


def test_requested_pages_are_the_same_everywhere():
    check(["lion", "--story", "--pages", "20"], 20)
    print("[PASS] --pages 20 shows 20 pages everywhere (PDF, metadata, SEO, analytics, prompts)")


def test_out_of_range_pages_fall_back_to_the_default_everywhere():
    check(["lion", "--story", "--pages", "99"], 40)
    print("[PASS] --pages 99 is ignored and 40 pages show everywhere")


def run_all():
    tests = [
        test_default_story_book_is_40_everywhere,
        test_requested_pages_are_the_same_everywhere,
        test_out_of_range_pages_fall_back_to_the_default_everywhere,
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
        print(str(failed) + "/" + str(len(tests)) + " page count tests FAILED")
    else:
        print("All " + str(len(tests)) + " page count tests PASSED")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)
