"""
==========================================================
AI KDP AUTOPILOT V4
Diversity Checker
==========================================================
"""

from collections import Counter


class DiversityChecker:

    def __init__(self):
        self.subjects = Counter()
        self.actions = Counter()
        self.poses = Counter()
        self.backgrounds = Counter()

    def add(
        self,
        subject="",
        action="",
        pose="",
        background=""
    ):
        if subject:
            self.subjects[subject.lower()] += 1

        if action:
            self.actions[action.lower()] += 1

        if pose:
            self.poses[pose.lower()] += 1

        if background:
            self.backgrounds[background.lower()] += 1

    def analyze(self):

        warnings = []

        for name, counter in [
            ("Subjects", self.subjects),
            ("Actions", self.actions),
            ("Poses", self.poses),
            ("Backgrounds", self.backgrounds),
        ]:

            if not counter:
                continue

            total = sum(counter.values())

            for item, count in counter.items():

                percentage = count / total

                if percentage > 0.35:
                    warnings.append(
                        f"{name}: '{item}' appears {count} times ({percentage:.0%})"
                    )

        return {
            "valid": len(warnings) == 0,
            "warnings": warnings,
            "stats": {
                "subjects": dict(self.subjects),
                "actions": dict(self.actions),
                "poses": dict(self.poses),
                "backgrounds": dict(self.backgrounds),
            }
        }

    def reset(self):
        self.subjects.clear()
        self.actions.clear()
        self.poses.clear()
        self.backgrounds.clear()