"""
=========================================
Story Mode Quality Test (V11 QA)
=========================================
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))

from agents.engines.animal_engine import AnimalEngine
from agents.engines.story_engine.story_planner import StoryPlanner, BEATS
from qa_common import (
    head_noun,
    shared_word_overlap,
    environment_conflicts,
    complexity_content_mismatch,
    emotional_jump,
    average_emotional_flow_score,
)

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
    prev_expression = None
    seen_expressions = []

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

        scene_head = head_noun(scene)
        bg_head = head_noun(background)

        if scene and background and scene_head and scene_head == bg_head:
            redundant_scene_bg += 1
            issues.append(f"[{subject}] page {page}: scene/background same head noun '{scene_head}' ('{scene}' / '{background}')")
        else:
            overlap = shared_word_overlap(scene, background)
            if overlap:
                redundant_scene_bg += 1
                issues.append(f"[{subject}] page {page}: scene/background share word(s) {sorted(overlap)} ('{scene}' / '{background}')")

        for group_a, group_b in environment_conflicts(scene, background):
            issues.append(
                f"[{subject}] page {page}: environment conflict - found {sorted(group_a)} AND "
                f"{sorted(group_b)} in scene='{scene}' background='{background}'"
            )

        mismatch = complexity_content_mismatch(r.get("complexity", ""), prompt)
        if mismatch:
            issues.append(f"[{subject}] page {page}: {mismatch}")

        current_expression = r.get("expression")
        seen_expressions.append(current_expression)
        if emotional_jump(prev_expression, current_expression):
            issues.append(
                f"[{subject}] page {page}: jarring emotional jump '{prev_expression}' -> '{current_expression}'"
            )
        prev_expression = current_expression

    if seen_beats != EXPECTED_BEAT_ORDER[:len(seen_beats)]:
        for i, (expected, actual) in enumerate(zip(EXPECTED_BEAT_ORDER, seen_beats), start=1):
            if expected != actual:
                issues.append(f"[{subject}] page {i}: expected beat '{expected}', got '{actual}'")

    last_index = -1
    for page, chapter in enumerate(seen_chapters, start=1):
        idx = CHAPTER_ORDER.index(chapter) if chapter in CHAPTER_ORDER else -1
        if idx < last_index:
            issues.append(f"[{subject}] page {page}: chapter went backward ('{chapter}' after chapter index {last_index})")
        last_index = max(last_index, idx)

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
        "emotional_flow_score": average_emotional_flow_score(seen_expressions),
    }


def run_story_test_with_season(subject, season, total_pages=40):
    engine = AnimalEngine()
    issues = []

    for page in range(1, total_pages + 1):
        try:
            r = engine.build(subject, page_number=page, total_pages=total_pages, story_mode=True, season=season)
        except Exception as e:
            issues.append(f"[{subject}/{season}] page {page}: CRASH - {type(e).__name__}: {e}")
            continue

        scene = (r.get("scene") or "")
        background = (r.get("background") or "")

        for group_a, group_b in environment_conflicts(scene, background):
            issues.append(
                f"[{subject}/{season}] page {page}: environment conflict - found {sorted(group_a)} AND "
                f"{sorted(group_b)} in scene='{scene}' background='{background}'"
            )

    return issues


def main():
    all_issues = []
    print("=" * 70)
    print("STORY MODE QUALITY TEST (V11 QA)")
    print("=" * 70)

    flow_scores = []
    for subject in SUBJECTS:
        result = run_story_test(subject)
        status = "PASS" if not result["issues"] else "FAIL"
        flow_scores.append(result["emotional_flow_score"])
        print(
            f"[{status}] {subject:10} | unique={result['unique_prompts']}/{result['total_pages']} "
            f"| redundant_scene_bg={result['redundant_scene_bg']} | issues={len(result['issues'])} "
            f"| emotional_flow={result['emotional_flow_score']:.1f}%"
        )
        all_issues.extend(result["issues"])

    if flow_scores:
        avg_flow = sum(flow_scores) / len(flow_scores)
        print()
        print(f"Average Emotional Flow Score: {avg_flow:.1f}%")

    print()
    print("--- Season/habitat conflict check (christmas, first 3 subjects) ---")
    for subject in SUBJECTS[:3]:
        season_issues = run_story_test_with_season(subject, "christmas")
        status = "PASS" if not season_issues else "FAIL"
        print(f"[{status}] {subject:10} (christmas) | issues={len(season_issues)}")
        all_issues.extend(season_issues)

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
