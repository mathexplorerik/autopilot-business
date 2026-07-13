"""
=========================================
QA Common Helpers
=========================================
Shared text-analysis helpers used by every QA
test file under tests/. Centralized here so a
fix to one detector can't drift out of sync
between test files.
"""

_PREPOSITIONS = (
    " under ", " through ", " with ", " near ", " beside ",
    " peeking", " surrounded by", " in ",
)

_STOPWORDS = {
    "a", "an", "the", "at", "in", "on", "of", "to", "and", "with",
    "under", "through", "near", "beside", "surrounded", "by", "its",
    "from", "this", "that", "some", "into", "onto",
}


def head_noun(text):
    if not text:
        return ""
    t = text.lower()
    for p in _PREPOSITIONS:
        if p in t:
            t = t.split(p)[0]
    words = t.split()
    return words[-1] if words else ""


def significant_words(text):
    if not text:
        return set()
    words = text.lower().replace(",", " ").split()
    return {w for w in words if w not in _STOPWORDS and len(w) > 3}


def shared_word_overlap(text_a, text_b):
    return significant_words(text_a) & significant_words(text_b)


CONFLICTING_ENVIRONMENT_GROUPS = [
    {"snow", "snowy", "frost", "frosty", "frozen", "icy", "blizzard", "sleet"},
    {"savanna", "desert", "grassland", "acacia", "jungle", "sahara", "cactus", "dune"},
]


def environment_conflicts(*texts):
    combined = " ".join((t or "").lower() for t in texts)
    hits = []
    for group in CONFLICTING_ENVIRONMENT_GROUPS:
        found = {w for w in group if w in combined}
        hits.append(found)

    conflicts = []
    for i in range(len(hits)):
        for j in range(i + 1, len(hits)):
            if hits[i] and hits[j]:
                conflicts.append((hits[i], hits[j]))
    return conflicts


COMPLEXITY_PHRASE_HINTS = {
    "simple": ["2-3 large elements", "2-3 elements"],
    "pro": ["highly detailed", "many interesting objects"],
}


def complexity_content_mismatch(complexity, prompt_text):
    text_lower = (prompt_text or "").lower()
    expected = COMPLEXITY_PHRASE_HINTS.get(complexity)

    if expected:
        if not any(phrase in text_lower for phrase in expected):
            other_hits = [
                (level, phrase)
                for level, phrases in COMPLEXITY_PHRASE_HINTS.items()
                if level != complexity
                for phrase in phrases
                if phrase in text_lower
            ]
            if other_hits:
                level, phrase = other_hits[0]
                return f"complexity='{complexity}' but text contains '{phrase}' (belongs to '{level}')"
    return ""


def prop_accessory_duplicate(props, accessories):
    props_set = {p.lower() for p in (props or [])}
    accessories_set = {a.lower() for a in (accessories or [])}
    return props_set & accessories_set


JARRING_TRANSITIONS = {
    ("sleepy", "excited"), ("sleepy", "brave"), ("sleepy", "surprised"),
    ("excited", "sleepy"), ("brave", "sleepy"), ("surprised", "sleepy"),
}

def emotional_jump(prev_expression, current_expression):
    if not prev_expression or not current_expression:
        return False
    pair = (prev_expression.lower(), current_expression.lower())
    return pair in JARRING_TRANSITIONS
