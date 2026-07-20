"""
=========================================
Multi-Market Optimizer (V13)
=========================================
Compares pricing/royalty across all supported
marketplaces (Amazon, Etsy, Gumroad) for the
same book, and recommends where to launch
first based on real per-sale profitability -
not just list price.
"""


class MultiMarketOptimizer:

    def __init__(self, pricing_intelligence, revenue_predictor):
        self.pricing_intelligence = pricing_intelligence
        self.revenue_predictor = revenue_predictor

    def compare_marketplaces(
        self,
        pages: int,
        demand_score: float = 50,
        competition_score: float = 50,
        opportunity_score: float = 50,
    ) -> dict:
        marketplaces = list(self.pricing_intelligence.MARKETPLACE_CONFIG.keys())
        results = []

        for marketplace in marketplaces:
            pricing = self.pricing_intelligence.suggest_price(
                pages=pages,
                demand_score=demand_score,
                competition_score=competition_score,
                marketplace=marketplace,
            )

            revenue = self.revenue_predictor.predict(
                demand_score=demand_score,
                opportunity_score=opportunity_score,
                suggested_price=pricing["suggested_price"],
                royalty_per_sale=pricing["estimated_royalty_per_sale"],
            )

            results.append({
                "marketplace": marketplace,
                "suggested_price": pricing["suggested_price"],
                "estimated_royalty_per_sale": pricing["estimated_royalty_per_sale"],
                "print_cost": pricing["print_cost"],
                "estimated_monthly_units": revenue["estimated_monthly_units"],
                "estimated_monthly_revenue": revenue["estimated_monthly_revenue"],
            })

        results.sort(key=lambda r: r["estimated_monthly_revenue"], reverse=True)

        return {
            "marketplace_comparison": results,
            "best_marketplace": results[0]["marketplace"] if results else None,
            "recommendation": (
                "Launch on " + results[0]["marketplace"] + " first - highest estimated monthly revenue ($" + str(results[0]["estimated_monthly_revenue"]) + ")"
                if results else "No marketplace data available"
            ),
        }
