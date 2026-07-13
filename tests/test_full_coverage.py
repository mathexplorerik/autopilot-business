"""
=========================================
Full Coverage QA Test
=========================================
Runs the qa_common semantic checks (environment
conflicts, scene/background overlap, complexity
content) across EVERY subject in SUBJECT_HABITATS
x EVERY season - not just the 10-subject spot
check in test_semantic_consistency.py /
test_story_mode_quality.py.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))

from agents.engines.animal_engine import AnimalEngine
from agents.data.animals.subject_habitats import SUBJECT_HABITATS
from qa_common import (
    head_noun,
    significant_overlap,
    environment_conflicts,
    complexity_content_mismatch,
)

ALL_SUBJECTS = sorted(SUBJECT_HABITATS.keys())
ALL_SEASONS = ["christmas", "halloween", "easter", "diwali", "holi", "eid"]


def run_full_check(subject, season=None, total_pages=40):
    engine = AnimalEngine()
    issues = []

    for page in range(1, total_pages + 1):
        try:
            r = engine.build(
                subject, page_number=page, total_pages=total_pages,
                story_mode=True, season=season,
            )
        except Exception as e:
            issues.append(f"[{subject}/{season}] page {page}: CRASH - {type(e).__name__}: {e}")
            continue

        scene = r.get("scene") or ""
        background = r.get("background") or ""
        prompt = r.get("positive") or ""

        if head_noun(scene) and head_noun(scene) == head_noun(background):
            issues.append(f"[{subject}/{season}] page {page}: same head noun '{scene}' / '{background}'")
        else:
            overlap = significant_overlap(scene, background)
            if overlap:
                issues.append(f"[{subject}/{season}] page {page}: overlap {sorted(overlap)} '{scene}' / '{background}'")

        for group_a, group_b in environment_conflicts(scene, background):
            issues.append(
                f"[{subject}/{season}] page {page}: environment conflict {sorted(group_a)} vs {sorted(group_b)} "
                f"in scene='{scene}' background='{background}'"
            )

        mismatch = complexity_content_mismatch(r.get("complexity", ""), prompt)
        if mismatch:
            issues.append(f"[{subject}/{season}] page {page}: {mismatch}")

    return issues


def main():
    print("=" * 70)
    print(f"FULL COVERAGE QA TEST - {len(ALL_SUBJECTS)} subjects x (no season + {len(ALL_SEASONS)} seasons)")
    print("=" * 70)

    all_issues = []
    total_runs = 0

    print("\n--- No season ---")
    for subject in ALL_SUBJECTS:
        issues = run_full_check(subject, season=None)
        total_runs += 1
        status = "PASS" if not issues else "FAIL"
        print(f"[{status}] {subject:15}| issues={len(issues)}")
        all_issues.extend(issues)

    for season in ALL_SEASONS:
        print(f"\n--- season={season} ---")
        for subject in ALL_SUBJECTS:
            issues = run_full_check(subject, season=season)
            total_runs += 1
            status = "PASS" if not issues else "FAIL"
            print(f"[{status}] {subject:15}({season:10})| issues={len(issues)}")
            all_issues.extend(issues)

    print("=" * 70)
    print(f"Total subject x season combinations tested: {total_runs}")
    if all_issues:
        print(f"\nTOTAL ISSUES FOUND: {len(all_issues)}\n")
        for issue in all_issues[:100]:
            print(" -", issue)
        if len(all_issues) > 100:
            print(f"  ... and {len(all_issues) - 100} more")
    else:
        print("\nALL CLEAR across every subject and every season.")


if __name__ == "__main__":
    main()
