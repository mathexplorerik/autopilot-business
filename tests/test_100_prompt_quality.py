"""
=========================================
100 Prompt Quality Test
=========================================
Runs the AnimalEngine 100 times across
various subjects and checks for:
- Crashes
- Duplicate exact prompts
- Missing fields
- Grammar sanity (a/an)
- Average prompt length
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.engines.animal_engine import AnimalEngine

SUBJECTS = [
    "lion", "elephant", "tiger", "giraffe", "zebra",
    "fox", "owl", "deer", "bear", "squirrel",
    "hedgehog", "wolf", "horse", "sheep", "cow",
    "duck", "turtle", "dolphin", "frog", "koala",
    "kangaroo", "penguin", "panda", "monkey", "rabbit",
]


def run_test(total=100):
    engine = AnimalEngine()

    results = []
    errors = []
    seen_prompts = set()
    duplicate_count = 0

    for i in range(total):
        subject = SUBJECTS[i % len(SUBJECTS)]

        try:
            result = engine.build(subject)
            prompt = result.get("positive", "")

            if not prompt:
                errors.append(f"[{i}] {subject}: EMPTY PROMPT")
                continue

            if prompt in seen_prompts:
                duplicate_count += 1
            else:
                seen_prompts.add(prompt)

            results.append({
                "subject": subject,
                "prompt": prompt,
                "length": len(prompt),
            })

        except Exception as e:
            errors.append(f"[{i}] {subject}: CRASH - {type(e).__name__}: {e}")

    # ===== Report =====
    print("=" * 60)
    print(f"TOTAL RUNS       : {total}")
    print(f"SUCCESSFUL       : {len(results)}")
    print(f"CRASHES/ERRORS   : {len(errors)}")
    print(f"DUPLICATE PROMPTS: {duplicate_count}")

    if results:
        avg_len = sum(r["length"] for r in results) / len(results)
        min_len = min(r["length"] for r in results)
        max_len = max(r["length"] for r in results)
        print(f"AVG PROMPT LENGTH: {avg_len:.0f} chars")
        print(f"MIN / MAX LENGTH : {min_len} / {max_len} chars")

    print("=" * 60)

    if errors:
        print("\n--- ERRORS ---")
        for e in errors:
            print(e)

    # Grammar sanity check: look for "a a" or "a e" style mistakes
    grammar_issues = []
    bad_patterns = [" a a", " a e", " a i", " a o", " a u", " an b", " an c", " an d"]

    for r in results:
        lower_prompt = r["prompt"].lower()
        for pattern in bad_patterns:
            if pattern in lower_prompt:
                grammar_issues.append(f"{r['subject']}: possible grammar issue near '{pattern.strip()}'")

    if grammar_issues:
        print("\n--- POSSIBLE GRAMMAR ISSUES ---")
        for g in grammar_issues:
            print(g)
    else:
        print("\nNo obvious grammar issues detected.")

    print("\n--- SAMPLE PROMPTS (first 5) ---")
    for r in results[:5]:
        print(f"\n[{r['subject']}]")
        print(r["prompt"])

    return {
        "total": total,
        "success": len(results),
        "errors": len(errors),
        "duplicates": duplicate_count,
    }


if __name__ == "__main__":
    run_test(100)