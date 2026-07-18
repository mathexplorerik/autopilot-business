"""
=========================================
Competitor Intelligence (V13)
=========================================
Provides competitive-positioning guidance based on the
competition_score already computed by trend_engine, plus
concrete differentiation suggestions. This is NOT a live
competitor scraper - it turns a single competition number
into actionable strategy, honestly framed as heuristic
guidance rather than real competitor analysis.
"""


class CompetitorIntelligence:

    LOW_COMPETITION = 40
    HIGH_COMPETITION = 75

    def _tier(self, competition_score: float) -> str:
        if competition_score < self.LOW_COMPETITION:
            return "low"
        if competition_score < self.HIGH_COMPETITION:
            return "moderate"
        return "high"

    def _strategy_for_tier(self, tier: str) -> dict:
        strategies = {
            "low": {
                "positioning": "First-mover advantage - focus on volume and broad keyword coverage.",
                "differentiation": [
                    "Cover the niche broadly before competitors catch up",
                    "Use straightforward, high-search-volume titles",
                ],
            },
            "moderate": {
                "positioning": "Differentiate on a specific angle rather than competing head-on.",
                "differentiation": [
                    "Target a specific sub-theme or age range competitors haven't covered",
                    "Improve on common weak points: better cover art, clearer age-appropriateness, larger print size",
                    "Bundle with a companion product (e.g. matching activity pages)",
                ],
            },
            "high": {
                "positioning": "Avoid head-to-head competition - find an underserved angle or skip this niche.",
                "differentiation": [
                    "Look for an unaddressed sub-niche within this category",
                    "Consider a different age group or format (tracing vs coloring) within the same theme",
                    "If proceeding anyway, budget for stronger SEO/marketing to compete for visibility",
                ],
            },
        }
        return strategies[tier]

    def analyze(self, competition_score: float) -> dict:
        competition_score = max(0, min(100, competition_score if competition_score is not None else 50))
        tier = self._tier(competition_score)
        strategy = self._strategy_for_tier(tier)

        return {
            "competition_score": competition_score,
            "competition_tier": tier,
            "positioning": strategy["positioning"],
            "differentiation_suggestions": strategy["differentiation"],
            "disclaimer": (
                "Heuristic guidance based on this system's competition score - "
                "not a live scrape of actual competitor listings."
            ),
        }
