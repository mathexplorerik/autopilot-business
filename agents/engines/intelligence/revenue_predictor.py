"""
=========================================
Revenue Predictor (V13)
=========================================
Estimates monthly sales volume and revenue for
a niche/book, combining demand, opportunity, and
pricing data already computed elsewhere. This is
a heuristic estimate for planning purposes, not
a guarantee - explicitly framed as such.
"""


class RevenuePredictor:

    # Baseline monthly unit sales at demand=100, opportunity=100,
    # scaled down by how far actual scores are from that ceiling.
    MAX_MONTHLY_UNITS_CEILING = 150

    def _estimate_monthly_units(self, demand_score, opportunity_score):
        demand_score = max(0, min(100, demand_score if demand_score is not None else 50))
        opportunity_score = max(0, min(100, opportunity_score if opportunity_score is not None else 50))

        # Weighted blend: demand drives search volume, opportunity
        # drives how much of that volume converts to a sale for THIS book.
        blended = (demand_score * 0.6) + (opportunity_score * 0.4)
        units = round((blended / 100) * self.MAX_MONTHLY_UNITS_CEILING)
        return max(1, units)

    def predict(self, demand_score=50, opportunity_score=50, suggested_price=6.99, royalty_per_sale=None):
        # Clamp/default here (not just inside _estimate_monthly_units) so
        # the confidence-band check below never sees a raw None and
        # crashes with "'>=' not supported between NoneType and int".
        demand_score = max(0, min(100, demand_score if demand_score is not None else 50))
        opportunity_score = max(0, min(100, opportunity_score if opportunity_score is not None else 50))

        estimated_units = self._estimate_monthly_units(demand_score, opportunity_score)

        if royalty_per_sale is None:
            # Fallback heuristic if no real print-cost data is passed in:
            # rough KDP royalty is often ~35-40% of list price for print books.
            royalty_per_sale = round(suggested_price * 0.35, 2)

        estimated_monthly_revenue = round(estimated_units * royalty_per_sale, 2)
        estimated_annual_revenue = round(estimated_monthly_revenue * 12, 2)

        # Simple confidence band based on how extreme the inputs are
        if demand_score >= 80 and opportunity_score >= 70:
            confidence = "Medium-High"
        elif demand_score <= 30 or opportunity_score <= 30:
            confidence = "Low"
        else:
            confidence = "Medium"

        return {
            "estimated_monthly_units": estimated_units,
            "royalty_per_sale": royalty_per_sale,
            "estimated_monthly_revenue": estimated_monthly_revenue,
            "estimated_annual_revenue": estimated_annual_revenue,
            "confidence": confidence,
            "disclaimer": (
                "Heuristic estimate based on demand/opportunity scoring - "
                "actual sales depend on execution, marketing, and market conditions."
            ),
        }
