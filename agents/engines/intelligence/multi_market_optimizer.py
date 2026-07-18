"""
=========================================
Multi-Market Optimizer (V13)
=========================================
Given a single book's page count and trend scores, computes
suggested pricing/revenue side-by-side across every
supported marketplace.
"""

from agents.engines.intelligence.revenue_predictor import RevenuePredictor
from agents.engines.intelligence.pricing_intelligence import PricingIntelligence


class MultiMarketOptimizer:

    def __init__(self):
        self.revenue = RevenuePredictor()
        self.marketplaces = list(PricingIntelligence.MARKETPLACE_CONFIG.keys())

    def compare(
        self,
        pages: int,
        demand_score: float = 50,
        competition_score: float = 50,
    ) -> dict:
        results = {}
        for marketplace in self.marketplaces:
            prediction = self.revenue.predict(
                pages=pages,
                demand_score=demand_score,
                competition_score=competition_score,
                marketplace=marketplace,
            )
            results[marketplace] = {
                "suggested_price": prediction["pricing"]["suggested_price"],
                "estimated_monthly_revenue_mid": prediction["estimated_monthly_revenue"]["mid"],
                "estimated_monthly_revenue_range": (
                    prediction["estimated_monthly_revenue"]["low"],
                    prediction["estimated_monthly_revenue"]["high"],
                ),
            }

        best_marketplace = max(
            results, key=lambda m: results[m]["estimated_monthly_revenue_mid"]
        )

        return {
            "by_marketplace": results,
            "recommended_marketplace": best_marketplace,
            "disclaimer": (
                "Based on heuristic pricing/revenue estimates - actual "
                "marketplace performance depends on each platform's own "
                "audience, fees, and discoverability, not modeled in full here."
            ),
        }
