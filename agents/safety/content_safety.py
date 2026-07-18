"""
=========================================
Content Safety Checker
=========================================
Final brand-safety gate for a kids' publishing business:
scans every generated prompt (and SEO/title/subtitle text)
for words that should never appear in children's content,
BEFORE it reaches image generation or KDP publishing.
"""

import re

BLOCKED_TERMS = {
    "violence": [
        "kill", "kills", "killing", "killed",
        "murder", "murders", "murdering", "murdered",
        "blood", "bloody", "bloodied",
        "gore", "gory",
        "gun", "guns", "firearm",
        "knife", "knives", "stabbing", "stabbed",
        "weapon", "weapons",
        "torture", "torturing", "tortured",
        "suicide",
        "corpse", "corpses", "dead body", "dead bodies",
    ],
    "adult_content": [
        "nude", "nudity", "naked",
        "sex", "sexual", "porn", "pornographic", "erotic", "fetish",
    ],
    "drugs_alcohol": [
        "cocaine", "heroin", "marijuana",
        "alcohol", "cigarette", "cigarettes",
        "beer bottle", "vodka", "drunk",
    ],
    "hate_speech": [
        "nazi", "hate crime",
    ],
    "self_harm": [
        "self-harm", "self harm", "cutting", "overdose",
    ],
}

SAFE_COMPOUND_EXCEPTIONS = [
    "killer whale", "killer whales",
]

_WORD_TO_CATEGORY = {
    word.lower(): category
    for category, words in BLOCKED_TERMS.items()
    for word in words
}


def _find_matches(text: str) -> list:
    if not text:
        return []

    text_lower = text.lower()

    for exception in SAFE_COMPOUND_EXCEPTIONS:
        text_lower = text_lower.replace(exception, "")

    matches = []
    for phrase, category in _WORD_TO_CATEGORY.items():
        pattern = r"\b" + re.escape(phrase) + r"\b"
        if re.search(pattern, text_lower):
            matches.append((phrase, category))

    return matches


def check_text(text: str) -> dict:
    matches = _find_matches(text)
    return {
        "safe": len(matches) == 0,
        "matches": matches,
    }


def check_book(book: dict) -> dict:
    issues = []

    for field in ("title", "subtitle", "description"):
        value = book.get(field)
        if value:
            result = check_text(value)
            if not result["safe"]:
                issues.append({"field": field, "matches": result["matches"]})

    for page_data in book.get("generated_pages") or []:
        page_num = page_data.get("page", "?")
        prompt = page_data.get("positive", "")
        result = check_text(prompt)
        if not result["safe"]:
            issues.append({"field": f"page {page_num} positive", "matches": result["matches"]})

    return {
        "safe": len(issues) == 0,
        "issues": issues,
    }
