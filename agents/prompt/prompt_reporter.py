"""
==========================================================
AI Publishing OS V6
Prompt Reporter
==========================================================
"""

from collections import Counter
from statistics import mean


class PromptReporter:
    """
    Generate analytics for prompt batches.

    Responsibilities
    ----------------
    ✓ Batch Statistics
    ✓ Complexity Distribution
    ✓ Subject Distribution
    ✓ Quality Scores
    ✓ Diversity Scores
    """

    def report(self, prompts):

        if not prompts:

            return {
                "total": 0
            }

        complexities = Counter()

        subjects = Counter()

        prompt_scores = []

        scene_scores = []

        diversity_scores = []

        for prompt in prompts:

            complexities[prompt["complexity"]] += 1

            subjects[prompt["subject"]] += 1

            metadata = prompt.get("metadata", {})

            prompt_scores.append(
                metadata.get("prompt_score", 100)
            )

            scene_scores.append(
                metadata.get("scene_score", 100)
            )

            diversity_scores.append(
                metadata.get("diversity_score", 100)
            )

        report = {

            "total": len(prompts),

            "complexity": dict(complexities),

            "subjects": dict(subjects),

            "average_prompt_score": round(
                mean(prompt_scores), 2
            ),

            "average_scene_score": round(
                mean(scene_scores), 2
            ),

            "average_diversity_score": round(
                mean(diversity_scores), 2
            ),

            "top_subjects": subjects.most_common(10)

        }

        self.print(report)

        return report

    def print(self, report):

        print("\n")
        print("=" * 65)

        print("📊 Prompt AI Report")

        print("=" * 65)

        print(f"Total Prompts        : {report['total']}")

        print(
            f"Prompt Score Avg    : {report['average_prompt_score']}"
        )

        print(
            f"Scene Score Avg     : {report['average_scene_score']}"
        )

        print(
            f"Diversity Avg       : {report['average_diversity_score']}"
        )

        print("\nComplexity")

        for name, count in report["complexity"].items():

            print(f"  {name:<18} {count}")

        print("\nTop Subjects")

        for name, count in report["top_subjects"]:

            print(f"  {name:<20} {count}")

        print("=" * 65)