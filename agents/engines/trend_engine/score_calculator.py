class ScoreCalculator:
    """
    Common score calculation utilities for Trend Engine.
    """

    @staticmethod
    def clamp(score: float, minimum: int = 0, maximum: int = 100) -> int:
        """
        Keep score between minimum and maximum.
        """
        return max(minimum, min(round(score), maximum))

    @staticmethod
    def weighted_average(scores: dict, weights: dict) -> int:
        """
        Calculate weighted average score.

        Example:
            scores = {
                "demand": 90,
                "profit": 80
            }

            weights = {
                "demand": 0.6,
                "profit": 0.4
            }
        """

        total = 0.0

        for key, weight in weights.items():
            total += scores.get(key, 0) * weight

        return ScoreCalculator.clamp(total)

    @staticmethod
    def invert(score: int) -> int:
        """
        Convert high competition to low opportunity.

        Example:
            Competition = 80
            Returns = 20
        """
        return 100 - score

    @staticmethod
    def average(values: list[int]) -> int:
        """
        Simple average.
        """
        if not values:
            return 0

        return ScoreCalculator.clamp(sum(values) / len(values))

    @staticmethod
    def percentage(value: float, total: float) -> int:
        """
        Convert value into percentage.
        """
        if total <= 0:
            return 0

        return ScoreCalculator.clamp((value / total) * 100)

    @staticmethod
    def confidence(scores: list[int]) -> int:
        """
        Estimate confidence based on score consistency.
        """

        if not scores:
            return 0

        spread = max(scores) - min(scores)

        confidence = 100 - spread

        return ScoreCalculator.clamp(confidence)