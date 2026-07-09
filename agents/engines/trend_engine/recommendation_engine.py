class RecommendationEngine:

    def __init__(self):

        self.rules = [
            (90, "Highly Recommended"),
            (80, "Recommended"),
            (70, "Good Opportunity"),
            (60, "Moderate Opportunity"),
            (50, "Low Opportunity"),
            (0, "Avoid")
        ]

    def analyze(self, opportunity_score: int) -> str:

        for minimum_score, recommendation in self.rules:

            if opportunity_score >= minimum_score:
                return recommendation

        return "Unknown"