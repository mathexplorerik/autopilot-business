"""
=========================================
Keyword Intelligence Engine
=========================================
Generates a ranked list of long-tail keyword
opportunities for a niche, combining:

- Base niche demand/competition (from TrendEngine)
- Proven KDP/Etsy search-pattern modifiers
  (agents/data/keywords/keyword_modifiers.py)

Each keyword gets a popularity estimate, a
competition estimate, and an opportunity score
(popularity - competition, weighted), so the
list can be sorted best-opportunity-first.
"""

from agents.data.keywords.keyword_modifiers import KEYWORD_MODIFIERS


class KeywordIntelligence:

    def _clamp(self, value, lo=0, hi=100):
        return max(lo, min(hi, value))

    def analyze(self, niche: str, base_demand: int = 50, base_competition: int = 50):
        """
        Returns a ranked list of keyword opportunities for the niche.

        base_demand / base_competition should come from
        TrendEngine.analyze() (demand / competition scores)
        so keyword scores are grounded in real niche-level data.
        """
        niche = niche.strip().lower()
        results = []

        for mod in KEYWORD_MODIFIERS:
            keyword = mod["pattern"].format(niche=niche)

            popularity = self._clamp(
                round((base_demand * 0.5) + (mod["popularity"] * 0.5))
            )
            competition = self._clamp(
                round(base_competition + mod["competition_delta"])
            )
            opportunity = self._clamp(
                round((popularity * 0.6) + ((100 - competition) * 0.4))
            )

            results.append({
                "keyword": keyword,
                "popularity": popularity,
                "competition": competition,
                "opportunity": opportunity,
            })

        results.sort(key=lambda r: r["opportunity"], reverse=True)
        return results

    def top_keywords(self, niche: str, base_demand: int = 50, base_competition: int = 50, limit: int = 5):
        return self.analyze(niche, base_demand, base_competition)[:limit]
