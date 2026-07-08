"""
==========================================================
AI KDP AUTOPILOT V4
Similarity Checker
==========================================================
"""

from difflib import SequenceMatcher


class SimilarityChecker:

    def __init__(self, threshold=0.90):
        self.threshold = threshold
        self.prompts = []

    def similarity(self, a: str, b: str) -> float:
        """
        Returns similarity score (0.0 - 1.0)
        """
        return SequenceMatcher(
            None,
            a.lower().strip(),
            b.lower().strip()
        ).ratio()

    def check(self, prompt: str):

        for old_prompt in self.prompts:

            score = self.similarity(
                prompt,
                old_prompt
            )

            if score >= self.threshold:

                return {
                    "valid": False,
                    "score": score,
                    "matched": old_prompt
                }

        return {
            "valid": True,
            "score": 0,
            "matched": None
        }

    def add(self, prompt: str):
        self.prompts.append(prompt)

    def total(self):
        return len(self.prompts)

    def reset(self):
        self.prompts.clear()