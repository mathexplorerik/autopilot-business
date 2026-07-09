"""
==========================================================
AI Publishing OS V5
Prop Provider
==========================================================
"""


class PropProvider:

    DEFAULT = [
        "flower",
        "ball",
        "tree",
        "rock",
        "cloud"
    ]

    PROPS = {

        "dinosaurs": [
            "dinosaur egg",
            "large leaf",
            "rock",
            "tree stump",
            "bones"
        ],

        "farm animals": [
            "hay bale",
            "bucket",
            "apple",
            "wooden fence",
            "water trough"
        ],

        "jungle animals": [
            "banana",
            "vine",
            "log",
            "flower",
            "rock"
        ],

        "ocean animals": [
            "starfish",
            "shell",
            "seaweed",
            "coral",
            "treasure chest"
        ],

        "vehicles": [
            "traffic cone",
            "road sign",
            "tool box",
            "fuel can",
            "barrel"
        ],

        "princess": [
            "crown",
            "magic wand",
            "flower basket",
            "storybook",
            "heart"
        ]
    }

    def get(self, niche):

        return self.PROPS.get(
            niche.lower(),
            self.DEFAULT
        )