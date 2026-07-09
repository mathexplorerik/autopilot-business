"""
==========================================================
AI Publishing OS V6
Prompt Scorer
==========================================================
"""

from typing import Dict


class PromptScorer:
    """
    Evaluate prompt quality.

    Responsibilities
    ----------------
    ✓ Prompt Quality
    ✓ Diversity
    ✓ Printability
    ✓ AI Compatibility

    Does NOT
    ----------
    ✗ Modify Prompt
    ✗ Save
    ✗ Validate
    """

    def score(
        self,
        prompt: Dict
    ) -> Dict:

        positive = prompt.get("positive", "").lower()

        score = 100

        report = []

        # ------------------------------------
        # Subject
        # ------------------------------------

        if len(positive) < 80:

            score -= 10

            report.append(
                "Prompt too short"
            )

        # ------------------------------------
        # Background
        # ------------------------------------

        if "background" not in positive:

            score -= 3

            report.append(
                "Background missing"
            )

        # ------------------------------------
        # Printable
        # ------------------------------------

        if "printable" not in positive:

            score -= 2

            report.append(
                "Printable keyword missing"
            )

        # ------------------------------------
        # White Background
        # ------------------------------------

        if "white background" not in positive:

            score -= 2

            report.append(
                "White background missing"
            )

        # ------------------------------------
        # Line Art
        # ------------------------------------

        if "line art" not in positive:

            score -= 5

            report.append(
                "Line art missing"
            )

        # ------------------------------------
        # Coloring Page
        # ------------------------------------

        if "coloring book" not in positive:

            score -= 5

            report.append(
                "Coloring book keyword missing"
            )

        score = max(score, 0)

        return {

            "score": score,

            "grade": self.grade(score),

            "issues": report

        }

    def grade(
        self,
        score: int
    ) -> str:

        if score >= 95:
            return "A+"

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        return "D"

    def should_regenerate(
        self,
        score: int,
        minimum: int = 90
    ) -> bool:

        return score < minimum