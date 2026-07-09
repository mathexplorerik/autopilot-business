"""
==========================================================
AI Publishing OS V5
Background Provider
==========================================================
"""


class BackgroundProvider:

    DEFAULT = [
        "white background",
        "simple nature background",
        "grass field",
        "park",
        "trees"
    ]

    BACKGROUNDS = {

        "dinosaurs": [
            "prehistoric jungle",
            "volcano",
            "rocky mountains",
            "fern forest",
            "dinosaur valley"
        ],

        "farm animals": [
            "barn",
            "farm field",
            "wooden fence",
            "hay field",
            "windmill"
        ],

        "jungle animals": [
            "rainforest",
            "waterfall",
            "large trees",
            "river",
            "vines"
        ],

        "ocean animals": [
            "coral reef",
            "underwater plants",
            "sea floor",
            "ocean cave",
            "bubbles"
        ],

        "vehicles": [
            "city road",
            "construction site",
            "garage",
            "highway",
            "parking area"
        ],

        "princess": [
            "castle",
            "royal garden",
            "palace",
            "flower field",
            "magic forest"
        ]
    }

    def get(self, niche):

        return self.BACKGROUNDS.get(
            niche.lower(),
            self.DEFAULT
        )