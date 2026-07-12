"""
=========================================
Story Mode Quality Test (V11 QA)
=========================================
Verifies story_mode=True end-to-end for
multiple subjects across a full 40-page book:

- Story beats follow the expected fixed sequence
- Chapters progress in order (no jumps backward)
- Complexity progresses simple -> pro
- Scene/background are not redundant
- Pose/expression match the beat (spot-check)
- No crashes, no exact-duplicate prompts
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.engines.animal_engine import AnimalEngine
from agents.engines.story_engine.story_planner import StoryPlanner, BEATS

SUBJECTS = ["lion", "rabbit", "panda", "penguin", "elephant", "tiger", "giraffe", "zebra", "fox", "owl"]

EXPECTED_BEAT_ORDER = [b["beat"] for b in BEATS]

CHAPTER_ORDER = ["Introduction", "Exploration", "Activities", "Adventure", "Wrap-up"]

COMPLEXITY_ORDER = ["simple", "intermediate", "advanced", "pro"]


def run_story_test(subject, total_pages=40):
    engine = AnimalEngine()
    issues = []

    prompts = set()
    seen_beats = []
    seen_chapters = []
    seen_complexity = []
    redundant_scene_bg = 0

    for page in range(1, total_pages + 1):
        try:
            r = engine.build(subject, page_number=page, total_pages=total_pages, story_mode=True)
        except Exception as e:
            issues.append(f"[{subject}] page {page}: CRASH - {type(e).__name__}: {e}")
            continue

        prompt = r.get("positive", "")
        if not prompt:
            issues.append(f"[{subject}] page {page}: EMPTY PROMPT")
            continue

        if prompt in prompts:
            issues.append(f"[{subject}] page {page}: DUPLICATE PROMPT")
        prompts.add(prompt)

        seen_beats.append(r.get("story_beat"))
        seen_chapters.append(r.get("chapter"))
        seen_complexity.append(r.get("complexity"))

        scene = (r.get("scene") or "")
        background = (r.get("background") or "")
        if scene and background and (scene.lower() in background.lower() or background.lower() in scene.lower()):
            redundant_scene_bg += 1
            issues.append(f"[{subject}] page {page}: scene/background redundant ('{scene}' / '{background}')")

    # --- Beat order check ---
    if seen_beats != EXPECTED_BEAT_ORDER[:len(seen_beats)]:
        for i, (expected, actual) in enumerate(zip(EXPECTED_BEAT_ORDER, seen_beats), start=1):
            if expected != actual:
                issues.append(f"[{subject}] page {i}: expected beat '{expected}', got '{actual}'")

    # --- Chapter monotonic progression check ---
    last_index = -1
    for page, chapter in enumerate(seen_chapters, start=1):
        idx = CHAPTER_ORDER.index(chapter) if chapter in CHAPTER_ORDER else -1
        if idx < last_index:
            issues.append(f"[{subject}] page {page}: chapter went backward ('{chapter}' after chapter index {last_index})")
        last_index = max(last_index, idx)

    # --- Complexity monotonic progression check ---
    last_complexity_idx = -1
    for page, complexity in enumerate(seen_complexity, start=1):
        idx = COMPLEXITY_ORDER.index(complexity) if complexity in COMPLEXITY_ORDER else -1
        if idx < last_complexity_idx:
            issues.append(f"[{subject}] page {page}: complexity went backward ('{complexity}')")
        last_complexity_idx = max(last_complexity_idx, idx)

    return {
        "subject": subject,
        "total_pages": total_pages,
        "unique_prompts": len(prompts),
        "redundant_scene_bg": redundant_scene_bg,
        "issues": issues,
    }


def main():
    all_issues = []
    print("=" * 70)
    print("STORY MODE QUALITY TEST (V11 QA)")
    print("=" * 70)

    for subject in SUBJECTS:
        result = run_story_test(subject)
        status = "PASS" if not result["issues"] else "FAIL"
        print(
            f"[{status}] {subject:10} | unique={result['unique_prompts']}/{result['total_pages']} "
            f"| redundant_scene_bg={result['redundant_scene_bg']} | issues={len(result['issues'])}"
        )
        all_issues.extend(result["issues"])

    print("=" * 70)
    if all_issues:
        print(f"\nTOTAL ISSUES FOUND: {len(all_issues)}\n")
        for issue in all_issues:
            print(" -", issue)
    else:
        print("\nAll subjects passed story mode QA with zero issues.")

    print()
    print("--- SAMPLE: full 40-page beat/pose/expression trace for first subject ---")
    engine = AnimalEngine()
    for page in range(1, 41):
        r = engine.build(SUBJECTS[0], page_number=page, total_pages=40, story_mode=True)
        print(
            f"Page {page:2} [{r['chapter']:12}] beat={r['story_beat']:16} "
            f"complexity={r['complexity']:12} pose={r['pose']:15} expr={r['expression']:10} action={r['action']}"
        )


if __name__ == "__main__":
    main()
