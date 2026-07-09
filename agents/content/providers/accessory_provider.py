"""
==========================================================
AI Publishing OS V5
Accessory Provider
==========================================================
"""


class AccessoryProvider:

    DEFAULT = [
        "bow",
        "hat",
        "scarf"
    ]

    ACCESSORIES = {

        "dinosaurs": [
            "explorer hat",
            "backpack",
            "bandana",
            "adventure cap"
        ],

        "farm animals": [
            "bell",
            "straw hat",
            "scarf",
            "flower crown"
        ],

        "jungle animals": [
            "leaf crown",
            "jungle backpack",
            "vine necklace"
        ],

        "ocean animals": [
            "pirate hat",
            "pearl necklace",
            "starfish crown"
        ],

        "vehicles": [
            "warning light",
            "construction helmet",
            "tool belt"
        ],

        "princess": [
            "crown",
            "magic necklace",
            "royal cape",
            "tiara"
        ]
    }

    def get(self, niche):

        return self.ACCESSORIES.get(
            niche.lower(),
            self.DEFAULT
        )