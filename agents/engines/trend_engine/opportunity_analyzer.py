class OpportunityAnalyzer:

    def __init__(self):

        self.weights = {
            "demand": 0.30,
            "profit": 0.20,
            "evergreen": 0.20,
            "marketplace": 0.15,
            "competition": 0.15
        }

    def analyze(self, report: dict) -> int:

        demand = report.get("demand", 0)
        profit = report.get("profit", 0)
        evergreen = report.get("evergreen", 0)
        marketplace = report.get("marketplace", 0)
        competition = report.get("competition", 0)

        opportunity = (
            demand * self.weights["demand"]
            + profit * self.weights["profit"]
            + evergreen * self.weights["evergreen"]
            + marketplace * self.weights["marketplace"]
            + (100 - competition) * self.weights["competition"]
        )

        return round(opportunity)