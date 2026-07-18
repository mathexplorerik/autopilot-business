"""
=========================================
Pricing Intelligence (V13)
=========================================
Suggests a price point for a book based on page count,
demand/competition scores (from trend_engine), and
marketplace - using KDP-style pricing psychology (charm
pricing) and print-cost-aware minimum pricing so a
suggestion is never below break-even for print marketplaces.

This gives a starting number for a human to review, not a
final, unsupervised pricing decision - real-world market
conditions should always be sanity-checked by a person
before publishing.
"""


class PricingIntelligence:

    MARKETPLACE_CONFIG = {
        "amazon": {"fixed_cost": 0.85, "cost_per_page": 0.012, "royalty_rate": 0.60, "is_print": True},
        "etsy": {"fixed_cost": 0.0, "cost_per_page": 0.0, "royalty_rate": 0.935, "is_print": False},
        "gumroad": {"fixed_cost": 0.0, "cost_per_page": 0.0, "royalty_rate": 0.91, "is_print": False},
    }

    DEFAULT_MARKETPLACE = "amazon"

    def _get_config(self, marketplace: str) -> dict:
        return self.MARKETPLACE_CONFIG.get(
            (marketplace or "").lower(), self.MARKETPLACE_CONFIG[self.DEFAULT_MARKETPLACE]
        )

    def estimate_print_cost(self, pages: int, marketplace: str = "amazon") -> float:
        config = self._get_config(marketplace)
        pages = max(0, pages or 0)
        if not config["is_print"]:
            return 0.0
        return round(config["fixed_cost"] + config["cost_per_page"] * pages, 2)

    def _base_price_by_pages(self, pages: int) -> float:
        pages = max(0, pages or 0)
        if pages <= 0:
            return 4.99
        if pages <= 30:
            return 5.99
        if pages <= 50:
            return 7.99
        return 9.99

    def _apply_charm_pricing(self, price: float) -> float:
        price = max(price, 0.99)
        whole = int(price)
        return round(whole + 0.99, 2)

    def _positioning_label(self, opportunity: float) -> str:
        if opportunity > 30:
            return "premium (low competition, high demand)"
        if opportunity >= 0:
            return "standard"
        if opportunity > -30:
            return "value (competitive market)"
        return "budget (high competition)"

    def suggest_price(
        self,
        pages: int,
        demand_score: float = 50,
        competition_score: float = 50,
        marketplace: str = "amazon",
    ) -> dict:
        marketplace_key = (marketplace or self.DEFAULT_MARKETPLACE).lower()
        if marketplace_key not in self.MARKETPLACE_CONFIG:
            marketplace_key = self.DEFAULT_MARKETPLACE

        demand_score = max(0, min(100, demand_score if demand_score is not None else 50))
        competition_score = max(0, min(100, competition_score if competition_score is not None else 50))
        opportunity = demand_score - competition_score

        base = self._base_price_by_pages(pages)
        adjustment = (opportunity / 100) * 2.0
        suggested = self._apply_charm_pricing(base + adjustment)

        print_cost = self.estimate_print_cost(pages, marketplace_key)

        if print_cost > 0:
            min_viable = self._apply_charm_pricing(print_cost + 1.50)
            if suggested < min_viable:
                suggested = min_viable

        config = self._get_config(marketplace_key)
        if config["is_print"]:
            estimated_royalty = round((suggested - print_cost) * config["royalty_rate"], 2)
        else:
            estimated_royalty = round(suggested * config["royalty_rate"], 2)
        estimated_royalty = max(0.0, estimated_royalty)

        return {
            "suggested_price": suggested,
            "price_range": (round(suggested - 1, 2), round(suggested + 1, 2)),
            "print_cost": print_cost,
            "estimated_royalty_per_sale": estimated_royalty,
            "marketplace": marketplace_key,
            "positioning": self._positioning_label(opportunity),
        }
