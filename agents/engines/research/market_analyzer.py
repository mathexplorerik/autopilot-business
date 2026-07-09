"""
==========================================================
AI Publishing OS
Market Analyzer V1
==========================================================
"""


class MarketAnalyzer:

    MARKET_RULES = {

        "dinosaurs": {
            "competition": "Medium",
            "demand": "High",
            "evergreen": True,
            "seasonal": False,
            "price": 6.99,
            "products": [
                "Coloring Book",
                "Tracing Book",
                "Activity Book",
                "Dot-to-Dot"
            ]
        },

        "farm animals": {
            "competition": "Low",
            "demand": "High",
            "evergreen": True,
            "seasonal": False,
            "price": 6.99,
            "products": [
                "Coloring Book",
                "Activity Book",
                "Flash Cards"
            ]
        }

    }

    DEFAULT = {
        "competition": "Unknown",
        "demand": "Medium",
        "evergreen": True,
        "seasonal": False,
        "price": 6.99,
        "products": [
            "Coloring Book"
        ]
    }

    def analyze(self, niche: str):

        return self.MARKET_RULES.get(
            niche.lower(),
            self.DEFAULT
        )