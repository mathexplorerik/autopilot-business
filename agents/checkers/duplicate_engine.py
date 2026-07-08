"""
==========================================================
AI KDP AUTOPILOT V4
Duplicate Detection Engine V2
==========================================================
"""

from agents.checkers.duplicate_checker import DuplicateChecker
from agents.checkers.combination_checker import CombinationChecker
from agents.checkers.similarity_checker import SimilarityChecker
from agents.checkers.diversity_checker import DiversityChecker


class DuplicateEngine:

    def __init__(self):

        self.duplicate = DuplicateChecker()
        self.combination = CombinationChecker()
        self.similarity = SimilarityChecker()
        self.diversity = DiversityChecker()

    def validate(
        self,
        prompt="",
        subject="",
        action="",
        pose="",
        background=""
    ):

        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # Exact duplicate
        if self.duplicate.is_duplicate(prompt):
            result["valid"] = False
            result["errors"].append("Exact duplicate prompt")

        # Similarity
        sim = self.similarity.check(prompt)

        if not sim["valid"]:
            result["valid"] = False
            result["errors"].append(
                f"Similar prompt ({sim['score']:.0%})"
            )

        # Combination
        combo = self.combination.check(
            subject,
            action,
            pose,
            background
        )

        result["errors"].extend(combo["errors"])
        result["warnings"].extend(combo["warnings"])

        if combo["errors"]:
            result["valid"] = False

        return result

    def add(
        self,
        prompt="",
        subject="",
        action="",
        pose="",
        background=""
    ):

        self.duplicate.add_prompt(prompt)

        self.similarity.add(prompt)

        self.combination.add(
            subject,
            action,
            pose,
            background
        )

        self.diversity.add(
            subject,
            action,
            pose,
            background
        )

    def report(self):
        return self.diversity.analyze()

    def reset(self):

        self.duplicate.reset()
        self.similarity.reset()
        self.diversity.reset()