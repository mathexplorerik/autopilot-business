"""
==========================================================
AI Publishing OS V6
Rules Engine
==========================================================
"""


class RulesEngine:

    def __init__(self):

        self.used = {
            "subjects": set(),
            "actions": set(),
            "backgrounds": set(),
            "props": set(),
            "accessories": set(),
        }

    def validate(self, scene: dict):

        errors = []

        if scene["subject"] in self.used["subjects"]:
            errors.append("Duplicate subject")

        if scene["action"] in self.used["actions"]:
            errors.append("Duplicate action")

        if scene["background"] in self.used["backgrounds"]:
            errors.append("Duplicate background")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def remember(self, scene: dict):

        self.used["subjects"].add(scene["subject"])
        self.used["actions"].add(scene["action"])
        self.used["backgrounds"].add(scene["background"])

        if "props" in scene:
            for p in scene["props"]:
                self.used["props"].add(p)

        if "accessories" in scene:
            for a in scene["accessories"]:
                self.used["accessories"].add(a)

    def reset(self):

        for key in self.used:
            self.used[key].clear()