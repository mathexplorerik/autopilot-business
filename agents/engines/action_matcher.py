"""
====================================================
Action Matcher Engine
AI KDP Autopilot V9
====================================================
"""

class ActionMatcher:

    RULES = {

        "river": {
            "keywords": [
                "river",
                "lake",
                "pond",
                "waterfall",
                "stream",
            ],
            "backgrounds": [
                "riverbank",
                "smooth rocks",
                "water plants",
                "small trees",
            ],
            "props": [
                "leaf boat",
                "bucket",
                "water lilies",
            ],
        },

        "forest": {
            "keywords": [
                "forest",
                "tree",
                "woods",
                "bamboo",
            ],
            "backgrounds": [
                "tall trees",
                "forest plants",
                "tree stumps",
            ],
            "props": [
                "acorns",
                "pinecones",
                "mushrooms",
            ],
        },

        "garden": {
            "keywords": [
                "garden",
                "flower",
                "flowers",
            ],
            "backgrounds": [
                "flower beds",
                "garden bushes",
                "colorful plants",
            ],
            "props": [
                "watering can",
                "flower pot",
                "garden shovel",
            ],
        },

    }

    @classmethod
    def detect(cls, action):

        action = action.lower()

        for name, rule in cls.RULES.items():

            if any(word in action for word in rule["keywords"]):
                return rule

        return None