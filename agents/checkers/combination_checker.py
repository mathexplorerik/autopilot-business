"""
==========================================================
AI KDP AUTOPILOT V4
Combination Checker
==========================================================
"""

from collections import defaultdict


class CombinationChecker:

    def __init__(self):

        self.subject_action = set()
        self.subject_pose = set()
        self.subject_background = set()

        self.action_count = defaultdict(int)
        self.pose_count = defaultdict(int)
        self.background_count = defaultdict(int)

    def check(
        self,
        subject="",
        action="",
        pose="",
        background=""
    ):

        errors = []
        warnings = []

        key1 = (
            subject.lower(),
            action.lower()
        )

        key2 = (
            subject.lower(),
            pose.lower()
        )

        key3 = (
            subject.lower(),
            background.lower()
        )

        if key1 in self.subject_action:
            errors.append("Duplicate subject + action")

        if key2 in self.subject_pose:
            errors.append("Duplicate subject + pose")

        if key3 in self.subject_background:
            warnings.append("Repeated background")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def add(
        self,
        subject="",
        action="",
        pose="",
        background=""
    ):

        self.subject_action.add(
            (
                subject.lower(),
                action.lower()
            )
        )

        self.subject_pose.add(
            (
                subject.lower(),
                pose.lower()
            )
        )

        self.subject_background.add(
            (
                subject.lower(),
                background.lower()
            )
        )

        self.action_count[action.lower()] += 1
        self.pose_count[pose.lower()] += 1
        self.background_count[background.lower()] += 1