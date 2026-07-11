"""
==========================================================
AI KDP AUTOPILOT V10
Relationship Scorer
==========================================================
"""


class Scorer:

    def score(self, item):

        if not item:
            return 0

        score = 100

        text = item.lower()

        # Very long text gets a small penalty
        if len(text.split()) > 6:
            score -= 10

        # Prefer simple, kid-friendly words
        preferred = [
            "forest",
            "garden",
            "river",
            "flower",
            "tree",
            "meadow",
            "park",
        ]

        if any(word in text for word in preferred):
            score += 10

        return score