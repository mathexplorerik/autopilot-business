"""
=========================================
Portfolio Planner (V13)
=========================================
Analyzes multiple niches at once and ranks them
by combined opportunity + revenue potential, so
a publisher can decide WHICH books to make next,
not just how to make one book well.
"""


class PortfolioPlanner:

    def __init__(self, research_engine):
        self.research_engine = research_engine

    def _score_niche(self, report):
        """
        Combined ranking score: opportunity is the primary
        driver (how easy to succeed), revenue potential is
        the secondary driver (how much it is worth succeeding).
        """
        opportunity = report.opportunity_score or 0
        revenue = report.metadata.get("revenue", {})
        monthly_revenue = revenue.get("estimated_monthly_revenue", 0)

        # Normalize monthly_revenue into a 0-100-ish scale for blending
        # (very rough: $1000/month treated as a strong ceiling for this heuristic)
        revenue_scaled = min(100, (monthly_revenue / 1000) * 100)

        return round((opportunity * 0.6) + (revenue_scaled * 0.4), 1)

    def analyze_portfolio(self, niches: list, season: str = "") -> dict:
        """
        Runs full research on every niche, ranks them, and
        returns a portfolio recommendation.
        """
        results = []

        for niche in niches:
            try:
                report = self.research_engine.analyze(niche, season=season)
            except Exception as e:
                results.append({
                    "niche": niche,
                    "error": f"{type(e).__name__}: {e}",
                    "portfolio_score": 0,
                })
                continue

            revenue = report.metadata.get("revenue", {})

            results.append({
                "niche": niche,
                "resolved_niche": report.resolved_niche,
                "opportunity_score": report.opportunity_score,
                "demand_score": report.demand_score,
                "competition_score": report.competition_score,
                "suggested_price": report.suggested_price,
                "estimated_monthly_revenue": revenue.get("estimated_monthly_revenue", 0),
                "recommendation": report.recommendation,
                "portfolio_score": self._score_niche(report),
            })

        results.sort(key=lambda r: r["portfolio_score"], reverse=True)

        total_estimated_monthly_revenue = sum(
            r.get("estimated_monthly_revenue", 0) for r in results if "error" not in r
        )

        return {
            "ranked_niches": results,
            "top_pick": results[0] if results else None,
            "total_estimated_monthly_revenue_if_all_built": round(total_estimated_monthly_revenue, 2),
            "niches_analyzed": len(niches),
            "niches_with_errors": sum(1 for r in results if "error" in r),
        }

    def top_n(self, niches: list, n: int = 5, season: str = "") -> list:
        portfolio = self.analyze_portfolio(niches, season=season)
        return portfolio["ranked_niches"][:n]
