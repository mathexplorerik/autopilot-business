"""
==========================================================
Quality Checker (V12.6+)
==========================================================
Validates the generated book against its ACTUAL
generated_pages - the real, final content that ships in
the PDF/prompts/SEO - not just blueprint field presence.

BUG FIX: the old version only checked that title/subtitle/
theme/pages/scenes were non-empty. It never inspected
semantic content (duplicate prompts, season/habitat
conflicts, scene/background redundancy, complexity/content
mismatch) - the exact things tests/qa_common.py already
catches for the test suite. This ports that detection logic
into production so "Ready for Publishing" actually means
something. Also fixed alongside the double-generation bug in
book_engine.py, which previously fed this checker a
throwaway preview instead of the real shipped pages.
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
_CONFLICTING_ENVIRONMENT_GROUPS = [
    {"snow", "snowy", "frost", "frosty", "frozen", "icy", "blizzard", "sleet"},
    {"savanna", "desert", "grassland", "acacia", "jungle", "sahara", "cactus", "dune"},
]
from agents.safety.content_safety import check_book

_COMPLEXITY_PHRASE_HINTS = {
    "simple": ["2-3 large elements", "2-3 elements"],
    "pro": ["highly detailed", "many interesting objects"],
}


def _head_noun(text):
    if not text:
        return ""
    t = text.lower()
    for p in _PREPOSITIONS:
        if p in t:
            t = t.split(p)[0]
    words = t.split()
    return words[-1] if words else ""


def _significant_words(text):
    if not text:
        return set()
    words = text.lower().replace(",", " ").split()
    return {w for w in words if w not in _STOPWORDS and len(w) > 3}


def _significant_overlap(a, b, min_shared=2):
    overlap = _significant_words(a) & _significant_words(b)
    return overlap if len(overlap) >= min_shared else set()


def _environment_conflicts(*texts):
    combined = " ".join((t or "").lower() for t in texts)
    hits = [{w for w in group if w in combined} for group in _CONFLICTING_ENVIRONMENT_GROUPS]
    conflicts = []
    for i in range(len(hits)):
        for j in range(i + 1, len(hits)):
            if hits[i] and hits[j]:
                conflicts.append((hits[i], hits[j]))
    return conflicts


def _complexity_content_mismatch(complexity, prompt_text):
    text_lower = (prompt_text or "").lower()
    expected = _COMPLEXITY_PHRASE_HINTS.get(complexity)
    if not expected:
        return ""
    if any(phrase in text_lower for phrase in expected):
        return ""
    other_hits = [
        (level, phrase)
        for level, phrases in _COMPLEXITY_PHRASE_HINTS.items()
        if level != complexity
        for phrase in phrases
        if phrase in text_lower
    ]
    if other_hits:
        level, phrase = other_hits[0]
        return f"complexity='{complexity}' but text contains '{phrase}' (belongs to '{level}')"
    return ""


class QualityChecker:
    """
    Validates the generated book blueprint AND its actual
    generated_pages content (semantic checks, not just
    field-presence checks).
    """

    def __init__(self):
        pass

    def _validate_structure(self, blueprint: dict, issues: list):
        if not blueprint.get("title"):
            issues.append("Missing title")
        if not blueprint.get("subtitle"):
            issues.append("Missing subtitle")
        if not blueprint.get("theme"):
            issues.append("Missing theme")
        if blueprint.get("total_pages", 0) <= 0:
            issues.append("Invalid page count")

    def _validate_pages(self, pages: list, issues: list):
        if not pages:
            issues.append("No scenes generated")
            return

        seen_prompts = set()
        for page_data in pages:
            page_num = page_data.get("page", "?")
            scene = page_data.get("scene") or ""
            background = page_data.get("background") or ""
            complexity = page_data.get("complexity") or ""
            prompt = page_data.get("positive") or ""

            if prompt:
                if prompt in seen_prompts:
                    issues.append(f"Page {page_num}: duplicate prompt")
                seen_prompts.add(prompt)

            if scene and background:
                if _head_noun(scene) == _head_noun(background):
                    issues.append(
                        f"Page {page_num}: scene/background redundancy "
                        f"('{scene}' / '{background}')"
                    )
                else:
                    overlap = _significant_overlap(scene, background)
                    if overlap:
                        issues.append(
                            f"Page {page_num}: scene/background overlap {sorted(overlap)} "
                            f"('{scene}' / '{background}')"
                        )

            for group_a, group_b in _environment_conflicts(scene, background):
                issues.append(
                    f"Page {page_num}: environment conflict {sorted(group_a)} vs {sorted(group_b)}"
                )

            mismatch = _complexity_content_mismatch(complexity, prompt)
            if mismatch:
                issues.append(f"Page {page_num}: {mismatch}")

    def validate(self, blueprint: dict) -> dict:
        issues = []

        self._validate_structure(blueprint, issues)

        pages = blueprint.get("generated_pages") or blueprint.get("scenes") or []
        self._validate_pages(pages, issues)

        safety = check_book(blueprint)
        if not safety["safe"]:
            for issue in safety["issues"]:
                matched = ", ".join(f"{phrase} ({cat})" for phrase, cat in issue["matches"])
                issues.append(f"CONTENT SAFETY: {issue['field']} flagged - {matched}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }
