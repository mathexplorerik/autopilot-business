"""
=========================================
Multi-Market Optimizer (V13)
=========================================
Given a book's page count and trend scores (demand,
competition, opportunity), computes suggested pricing and
estimated revenue side-by-side across every supported
marketplace, so a publisher can compare Amazon vs Etsy vs
Gumroad at a glance.
"""

from agents.engines.intelligence.pricing_intelligence import PricingIntelligence
from agents.engines.intelligence.revenue_predictor import RevenuePredictor


class MultiMarketOptimizer:

    def __init__(self):
        self.pricing = PricingIntelligence()
        self.revenue = RevenuePredictor()
        self.marketplaces = list(PricingIntelligence.MARKETPLACE_CONFIG.keys())

    def compare(
        self,
        pages: int,
        demand_score: float = 50,
        competition_score: float = 50,
        opportunity_score: float = None,
    ) -> dict:
        demand_score = max(0, min(100, demand_score if demand_score is not None else 50))
        competition_score = max(0, min(100, competition_score if competition_score is not None else 50))
        if opportunity_score is None:
            opportunity_score = max(0, min(100, demand_score - competition_score))

        results = {}
        for marketplace in self.marketplaces:
            pricing = self.pricing.suggest_price(
                pages=pages,
                demand_score=demand_score,
                competition_score=competition_score,
                marketplace=marketplace,
            )

            prediction = self.revenue.predict(
                demand_score=demand_score,
                opportunity_score=opportunity_score,
                suggested_price=pricing["suggested_price"],
                royalty_per_sale=pricing["estimated_royalty_per_sale"],
            )

            results[marketplace] = {
                "suggested_price": pricing["suggested_price"],
                "royalty_per_sale": prediction["royalty_per_sale"],
                "estimated_monthly_units": prediction["estimated_monthly_units"],
                "estimated_monthly_revenue": prediction["estimated_monthly_revenue"],
                "estimated_annual_revenue": prediction["estimated_annual_revenue"],
                "confidence": prediction["confidence"],
            }

        best_marketplace = max(
            results, key=lambda m: results[m]["estimated_monthly_revenue"]
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
