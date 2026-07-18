"""
=========================================
Bestseller Intelligence (V13)
=========================================
Flags whether a niche matches known bestseller PATTERNS
(high demand, high evergreen, manageable competition) and
suggests title/listing conventions common to bestselling
kids' coloring books.

IMPORTANT: this does not scrape or verify real-time Amazon
bestseller rankings (no live market-data source is wired
into this pipeline). It is a pattern-matcher against the
trend scores this system already computes, not a live
bestseller-list lookup - framed honestly as such.
"""


class BestsellerIntelligence:

    DEMAND_THRESHOLD = 80
    EVERGREEN_THRESHOLD = 75
    COMPETITION_CEILING = 85

    TITLE_CONVENTIONS = [
        "Include the target age range explicitly (e.g. 'Ages 4-8')",
        "State the page count in the title or subtitle (e.g. '40 Pages')",
        "Use concrete, searchable subject nouns rather than vague themes",
        "Keep the title under ~200 characters (KDP display truncates longer titles)",
        "Mention 'Coloring Book' or 'Activity Book' explicitly for category matching",
    ]

    def analyze(self, demand_score: float, competition_score: float, evergreen_score: float) -> dict:
        demand_score = max(0, min(100, demand_score if demand_score is not None else 0))
        competition_score = max(0, min(100, competition_score if competition_score is not None else 100))
        evergreen_score = max(0, min(100, evergreen_score if evergreen_score is not None else 0))

        is_match = (
            demand_score >= self.DEMAND_THRESHOLD
            and evergreen_score >= self.EVERGREEN_THRESHOLD
            and competition_score <= self.COMPETITION_CEILING
        )

        reasons = []
        if demand_score < self.DEMAND_THRESHOLD:
            reasons.append(f"demand {demand_score:.0f} is below the {self.DEMAND_THRESHOLD} bestseller-pattern threshold")
        if evergreen_score < self.EVERGREEN_THRESHOLD:
            reasons.append(f"evergreen score {evergreen_score:.0f} is below the {self.EVERGREEN_THRESHOLD} threshold")
        if competition_score > self.COMPETITION_CEILING:
            reasons.append(f"competition {competition_score:.0f} is above the {self.COMPETITION_CEILING} ceiling (too crowded)")

        return {
            "bestseller_pattern_match": is_match,
            "reasons": reasons if not is_match else ["meets demand, evergreen, and competition thresholds"],
            "title_conventions": self.TITLE_CONVENTIONS,
            "disclaimer": (
                "Pattern-match against this system's own trend scores - "
                "not a live Amazon bestseller-list lookup."
            ),
        }
