"""
==========================================================
AI Publishing OS V5
Action Provider
==========================================================
"""


class ActionProvider:

    DEFAULT = [
        "standing",
        "walking",
        "running",
        "playing",
        "smiling"
    ]

    ACTIONS = {

        "dinosaurs": [
            "roaring",
            "walking",
            "running",
            "eating leaves",
            "sleeping",
            "playing"
        ],

        "farm animals": [
            "grazing",
            "running",
            "jumping",
            "sleeping",
            "playing"
        ],

        "jungle animals": [
            "climbing",
            "running",
            "swinging",
            "sleeping"
        ],

        "vehicles": [
            "driving",
            "working",
            "moving",
            "parking"
        ],

        "princess": [
            "waving",
            "dancing",
            "walking",
            "reading"
        ]
    }

    def get(self, niche):

        return self.ACTIONS.get(
            niche.lower(),
            self.DEFAULT
        )