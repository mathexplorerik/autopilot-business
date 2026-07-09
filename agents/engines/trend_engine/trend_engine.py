from .demand_analyzer import DemandAnalyzer
from .competition_analyzer import CompetitionAnalyzer
from .profit_analyzer import ProfitAnalyzer
from .evergreen_analyzer import EvergreenAnalyzer
from .seasonal_analyzer import SeasonalAnalyzer
from .marketplace_analyzer import MarketplaceAnalyzer
from .opportunity_analyzer import OpportunityAnalyzer
from .recommendation_engine import RecommendationEngine


class TrendEngine:

    def __init__(self):

        self.demand = DemandAnalyzer()
        self.competition = CompetitionAnalyzer()
        self.profit = ProfitAnalyzer()
        self.evergreen = EvergreenAnalyzer()
        self.seasonal = SeasonalAnalyzer()
        self.marketplace = MarketplaceAnalyzer()
        self.opportunity = OpportunityAnalyzer()
        self.recommendation = RecommendationEngine()

    def analyze(
        self,
        keyword: str,
        book_type: str = "",
        age_group: str = "",
    ):

        report = {}

        report["keyword"] = keyword
        report["book_type"] = book_type
        report["age_group"] = age_group

        report["demand"] = self.demand.analyze(keyword)

        report["competition"] = self.competition.analyze(keyword)

        report["profit"] = self.profit.analyze(keyword)

        report["evergreen"] = self.evergreen.analyze(keyword)

        report["seasonal"] = self.seasonal.analyze(keyword)

        report["marketplace"] = self.marketplace.analyze(book_type)

        report["opportunity"] = self.opportunity.analyze(report)

        report["recommendation"] = self.recommendation.analyze(
            report["opportunity"]
        )

        return report