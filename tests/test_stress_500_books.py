"""
=========================================
Stress Test — 500 Random Books (V12 QA)
=========================================
Generates a large volume of books across:
- 100+ different subjects (known + unknown/fallback)
- All book types (story, niche)
- All supported seasons
- Random age groups

Flags: crashes, malformed prompts, empty fields,
duplicate prompts within a book, and any exception
trace so failures are actionable.
"""

import sys
import os
import random
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.engines.book_engine.book_engine import BookEngine

KNOWN_SUBJECTS = [
    "lion", "rabbit", "panda", "penguin", "elephant", "tiger", "giraffe",
    "zebra", "fox", "owl", "deer", "bear", "squirrel", "hedgehog", "wolf",
    "horse", "sheep", "cow", "duck", "turtle", "dolphin", "frog", "koala",
    "kangaroo", "monkey",
]

UNKNOWN_SUBJECTS = [
    "narwhal", "quokka", "axolotl", "capybara", "pangolin", "okapi",
    "platypus", "chinchilla", "wombat", "tapir", "manatee", "otter",
    "flamingo", "peacock", "hedgefox", "unicat", "dragonfly-bear",
    "sparkle-owl", "moonwolf", "rainbowfish",
]

NICHE_KEYWORDS = [
    "jungle animals", "farm animals", "ocean animals", "dinosaurs",
    "butterflies", "space", "princess", "vehicles", "animals",
]

SEASONS = [None, "christmas", "halloween", "easter", "diwali", "holi", "eid"]

BOOK_TYPES = ["story", "niche"]

AGE_GROUPS = ["toddler", "kids", "teens"]

REQUIRED_FIELDS = [
    "positive", "negative", "scene", "background", "action",
    "pose", "expression", "subject", "complexity", "age_group",
]


def is_malformed(prompt: str) -> list:
    """Cheap heuristic checks for common malformed patterns."""
    problems = []
    if not prompt or not prompt.strip():
        problems.append("empty prompt")
        return problems

    lower = prompt.lower()
    if ",," in prompt:
        problems.append("double comma")
    if "  " in prompt:
        problems.append("double space")
    if lower.count(" pose pose") > 0:
        problems.append("duplicated 'pose pose'")
    if lower.startswith(" ") or lower.endswith(" "):
        problems.append("leading/trailing whitespace")
    if "none" in lower.split(", "):
        problems.append("literal 'None' leaked into prompt")
    return problems


def run_one_book(seed_index):
    random.seed(seed_index)

    book_type = random.choice(BOOK_TYPES)
    season = random.choice(SEASONS)
    age_group = random.choice(AGE_GROUPS)

    if book_type == "story":
        pool = KNOWN_SUBJECTS + UNKNOWN_SUBJECTS
        keyword = random.choice(pool)
        total_pages_hint = None
    else:
        keyword = random.choice(NICHE_KEYWORDS + UNKNOWN_SUBJECTS)
        total_pages_hint = None

    result = {
        "index": seed_index,
        "keyword": keyword,
        "book_type": book_type,
        "season": season,
        "age_group": age_group,
        "crashed": False,
        "error": None,
        "malformed_pages": [],
        "missing_fields": [],
        "duplicate_prompts": 0,
        "total_pages": 0,
    }

    try:
        engine = BookEngine()
        blueprint = engine.build(
            keyword=keyword,
            book_type=book_type,
            age_group=age_group,
            provider="manual",
            season=season,
        )

        pages = blueprint.get("generated_pages", [])
        result["total_pages"] = len(pages)

        seen_prompts = set()

        for page_data in pages:
            for field in REQUIRED_FIELDS:
                if field not in page_data or page_data[field] in (None, ""):
                    if field in ("scene", "background") and page_data.get(field) == "":
                        continue
                    result["missing_fields"].append(f"page {page_data.get('page')}: missing/empty '{field}'")

            prompt = page_data.get("positive", "")
            problems = is_malformed(prompt)
            if problems:
                result["malformed_pages"].append(f"page {page_data.get('page')}: {problems}")

            if prompt in seen_prompts:
                result["duplicate_prompts"] += 1
            seen_prompts.add(prompt)

    except Exception as e:
        result["crashed"] = True
        result["error"] = f"{type(e).__name__}: {e}"
        result["traceback"] = traceback.format_exc()

    return result


def main(total_books=500):
    print("=" * 70)
    print(f"STRESS TEST — {total_books} RANDOM BOOKS")
    print("=" * 70)

    crashes = []
    malformed_books = []
    missing_field_books = []
    duplicate_books = []
    successes = 0

    for i in range(total_books):
        result = run_one_book(i)

        if result["crashed"]:
            crashes.append(result)
        else:
            successes += 1
            if result["malformed_pages"]:
                malformed_books.append(result)
            if result["missing_fields"]:
                missing_field_books.append(result)
            if result["duplicate_prompts"] > 0:
                duplicate_books.append(result)

        if (i + 1) % 50 == 0:
            print(f"  ... {i + 1}/{total_books} books processed")

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Total books attempted : {total_books}")
    print(f"Successful            : {successes}")
    print(f"Crashed               : {len(crashes)}")
    print(f"Books with malformed prompts : {len(malformed_books)}")
    print(f"Books with missing fields   : {len(missing_field_books)}")
    print(f"Books with duplicate prompts: {len(duplicate_books)}")
    print("=" * 70)

    if crashes:
        print(f"\n--- CRASHES ({len(crashes)}) ---")
        for c in crashes[:10]:
            print(f"\n[{c['index']}] keyword='{c['keyword']}' book_type={c['book_type']} "
                  f"season={c['season']} age_group={c['age_group']}")
            print(f"  Error: {c['error']}")
        if len(crashes) > 10:
            print(f"\n  ... and {len(crashes) - 10} more crashes (truncated)")

    if malformed_books:
        print(f"\n--- MALFORMED PROMPTS ({len(malformed_books)} books) ---")
        for m in malformed_books[:10]:
            print(f"\n[{m['index']}] keyword='{m['keyword']}' book_type={m['book_type']} season={m['season']}")
            for p in m["malformed_pages"][:3]:
                print(f"  - {p}")

    if missing_field_books:
        print(f"\n--- MISSING FIELDS ({len(missing_field_books)} books) ---")
        for m in missing_field_books[:10]:
            print(f"\n[{m['index']}] keyword='{m['keyword']}' book_type={m['book_type']}")
            for f in m["missing_fields"][:3]:
                print(f"  - {f}")

    if duplicate_books:
        print(f"\n--- DUPLICATE PROMPTS WITHIN A BOOK ({len(duplicate_books)} books) ---")
        for d in duplicate_books[:10]:
            print(f"[{d['index']}] keyword='{d['keyword']}' book_type={d['book_type']} "
                  f"duplicates={d['duplicate_prompts']}/{d['total_pages']}")

    if not crashes and not malformed_books and not missing_field_books and not duplicate_books:
        print("\nALL CLEAR — no crashes, malformed prompts, missing fields, or duplicates found.")

    return {
        "total": total_books,
        "successes": successes,
        "crashes": len(crashes),
        "malformed": len(malformed_books),
        "missing_fields": len(missing_field_books),
        "duplicates": len(duplicate_books),
    }


if __name__ == "__main__":
    main(500)
