"""
=========================================
Semantic Consistency Test (V12 QA)
=========================================
Season is expressed via accessories (a wearable/
held festive item), never via scene/background
weather text - see animal_engine.py. This file's
season checks reflect that design.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))

from agents.engines.book_engine.book_engine import BookEngine
from agents.engines.book_engine.character_profile_generator import COMPANIONS, HOME_ENVIRONMENTS
from qa_common import (
    head_noun,
    shared_word_overlap,
    environment_conflicts,
    complexity_content_mismatch,
)

SUBJECTS = ["lion", "rabbit", "panda", "penguin", "elephant", "tiger", "giraffe", "zebra", "fox", "owl"]

INCOMPATIBLE_POSE_ACTION = {
    "lying down": ["running", "jumping", "climbing", "dancing"],
    "sitting": ["running", "jumping", "climbing"],
    "sleeping": ["running", "jumping", "dancing", "playing"],
}

# Keywords expected in ACCESSORIES (not scene/background) when a season
# is active - matches SEASON_ACCESSORIES in animal_engine.py.
SEASON_ACCESSORY_KEYWORDS = {
    "christmas": ["santa", "scarf", "ornament"],
    "halloween": ["pumpkin", "witch", "bat"],
    "easter": ["flower crown", "bow", "egg"],
    "diwali": ["diya", "fairy lights", "rangoli"],
    "holi": ["powder", "water gun", "bandana"],
    "eid": ["lantern", "bunting", "crescent"],
}


def check_pose_action(action, pose, issues, subject, page):
    action_l = action.lower()
    pose_l = pose.lower()
    for bad_pose_word, bad_actions in INCOMPATIBLE_POSE_ACTION.items():
        if bad_pose_word in pose_l:
            for bad_action_word in bad_actions:
                if bad_action_word in action_l:
                    issues.append(
                        f"[{subject}] page {page}: pose/action mismatch - "
                        f"pose='{pose}' action='{action}'"
                    )
                    return


def check_scene_background(scene, background, issues, subject, page):
    if not scene or not background:
        return
    if head_noun(scene) == head_noun(background):
        issues.append(
            f"[{subject}] page {page}: scene/background same head noun - "
            f"'{scene}' / '{background}'"
        )
        return
    overlap = shared_word_overlap(scene, background)
    if overlap:
        issues.append(
            f"[{subject}] page {page}: scene/background share word(s) {sorted(overlap)} - "
            f"'{scene}' / '{background}'"
        )


def check_season_scene(scene, background, season, issues, subject, page):
    """
    By design, season is expressed as an ACCESSORY (see
    check_season_accessory below) and must NEVER leak into scene/
    background weather text. This is a regression guard: if the
    environment-conflict detector ever finds season-climate words
    mixed with habitat words again, that means season logic drifted
    back toward directly modifying scene/background.
    """
    if not season:
        return
    for group_a, group_b in environment_conflicts(scene, background):
        issues.append(
            f"[{subject}] page {page}: season/habitat environment conflict - "
            f"found {sorted(group_a)} AND {sorted(group_b)} in scene='{scene}' background='{background}'"
        )


def check_season_accessory(accessories, season, issues, subject, page):
    if not season:
        return
    keywords = SEASON_ACCESSORY_KEYWORDS.get(season.lower())
    if not keywords:
        return
    text = " ".join(accessories or []).lower()
    if not any(kw in text for kw in keywords):
        issues.append(
            f"[{subject}] page {page}: season='{season}' set but no season-themed "
            f"accessory found in {accessories}"
        )


def check_companion_species(subject, companion, issues):
    if not companion:
        return
    expected = COMPANIONS.get(subject.lower())
    if expected and companion != expected:
        issues.append(
            f"[{subject}]: companion mismatch - expected '{expected}', got '{companion}'"
        )


def check_home_species(subject, home, issues):
    if not home:
        return
    expected_options = HOME_ENVIRONMENTS.get(subject.lower(), [])
    if expected_options and home not in expected_options:
        issues.append(
            f"[{subject}]: home_environment mismatch - '{home}' not in expected set for species"
        )


def check_complexity_content(complexity, page_data, issues, subject, page):
    props = page_data.get("props") or []
    accessories = page_data.get("accessories") or []
    total_items = len(props) + len(accessories)

    if complexity == "pro" and total_items == 0:
        issues.append(
            f"[{subject}] page {page}: complexity='pro' but zero props/accessories present"
        )

    mismatch = complexity_content_mismatch(complexity, page_data.get("positive", ""))
    if mismatch:
        issues.append(f"[{subject}] page {page}: {mismatch}")


def run_semantic_test(subject, season=None):
    engine = BookEngine()
    b = engine.build(
        keyword=subject,
        book_type="story",
        age_group="kids",
        provider="manual",
        season=season,
    )

    issues = []
    character_profile = b.get("character_profile", {})

    check_companion_species(subject, character_profile.get("companion"), issues)
    check_home_species(subject, character_profile.get("home_environment"), issues)

    for page_data in b["generated_pages"]:
        page = page_data["page"]

        check_pose_action(page_data["action"], page_data["pose"], issues, subject, page)
        check_scene_background(page_data["scene"], page_data["background"], issues, subject, page)
        check_season_scene(page_data["scene"], page_data["background"], season, issues, subject, page)
        check_season_accessory(page_data.get("accessories"), season, issues, subject, page)
        check_complexity_content(page_data["complexity"], page_data, issues, subject, page)

    return issues


def main():
    print("=" * 70)
    print("SEMANTIC CONSISTENCY TEST (V12 QA)")
    print("=" * 70)

    all_issues = []

    for subject in SUBJECTS:
        issues = run_semantic_test(subject)
        status = "PASS" if not issues else "FAIL"
        print(f"[{status}] {subject:10} | issues={len(issues)}")
        all_issues.extend(issues)

    print()
    print("--- Season-specific check (christmas) ---")
    season_issues = run_semantic_test("lion", season="christmas")
    status = "PASS" if not season_issues else "FAIL"
    print(f"[{status}] lion (christmas) | issues={len(season_issues)}")
    all_issues.extend(season_issues)

    print("=" * 70)
    if all_issues:
        print(f"\nTOTAL ISSUES FOUND: {len(all_issues)}\n")
        for issue in all_issues:
            print(" -", issue)
    else:
        print("\nAll semantic consistency checks passed.")


if __name__ == "__main__":
    main()
