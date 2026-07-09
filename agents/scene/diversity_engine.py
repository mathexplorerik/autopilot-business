"""
==========================================================
AI Publishing OS V6
Diversity Engine
==========================================================
"""

from collections import Counter


class DiversityEngine:

    def score(self, scenes):

        if not scenes:
            return {
                "score": 100,
                "details": {}
            }

        metrics = {
            "subjects": Counter(),
            "actions": Counter(),
            "backgrounds": Counter(),
            "props": Counter(),
            "accessories": Counter()
        }

        for scene in scenes:

            metrics["subjects"][scene.get("subject")] += 1
            metrics["actions"][scene.get("action")] += 1
            metrics["backgrounds"][scene.get("background")] += 1

            for prop in scene.get("props", []):
                metrics["props"][prop] += 1

            for accessory in scene.get("accessories", []):
                metrics["accessories"][accessory] += 1

        penalties = 0

        for counter in metrics.values():
            for count in counter.values():
                if count > 1:
                    penalties += (count - 1)

        score = max(0, 100 - penalties)

        return {
            "score": score,
            "details": {
                key: dict(value)
                for key, value in metrics.items()
            }
        }

    def needs_regeneration(self, score, minimum=85):

        return score < minimum