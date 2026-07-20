from .opportunity_analyzer import OpportunityAnalyzer
from .recommendation_engine import RecommendationEngine
from agents.engines.intelligence.data_sources.heuristic_market_data_source import HeuristicMarketDataSource


class TrendEngine:

    def __init__(self, data_source=None):
        # data_source defaults to the current heuristic/JSON-backed
        # implementation. Pass a different BaseMarketDataSource
        # subclass here later (e.g. a real-API-backed one) without
        # changing anything below this line.
        self.data_source = data_source or HeuristicMarketDataSource()
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
        report["demand"] = self.data_source.demand(keyword)
        report["competition"] = self.data_source.competition(keyword)
        report["profit"] = self.data_source.profit(keyword)
        report["evergreen"] = self.data_source.evergreen(keyword)
        report["seasonal"] = self.data_source.seasonal(keyword)
        report["marketplace"] = self.data_source.marketplace(book_type)
        report["opportunity"] = self.opportunity.analyze(report)
        report["recommendation"] = self.recommendation.analyze(
            report["opportunity"]
        )
        return report
