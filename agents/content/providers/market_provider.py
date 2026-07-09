"""
==========================================================
AI Publishing OS V5
Market Provider
==========================================================
"""


class MarketProvider:

    DEFAULT = {

        "price_min": 5.99,
        "price_max": 8.99,

        "evergreen": True,

        "seasonal": False,

        "recommended_products": [
            "Coloring Book"
        ]

    }

    DATA = {

        "dinosaurs": {

            "price_min": 6.99,

            "price_max": 8.99,

            "evergreen": True,

            "seasonal": False,

            "recommended_products": [

                "Coloring Book",

                "Tracing Book",

                "Activity Book",

                "Dot-to-Dot"

            ]

        }

    }

    def get(self, niche):

        return self.DATA.get(

            niche.lower(),

            self.DEFAULT

        )