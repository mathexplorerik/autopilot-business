from .opportunity_analyzer import OpportunityAnalyzer
from .recommendation_engine import RecommendationEngine
from .confidence_scorer import ConfidenceScorer
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
        self.confidence = ConfidenceScorer()

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
        field_keys = {
            "demand": keyword,
            "competition": keyword,
            "profit": keyword,
            "evergreen": keyword,
            "seasonal": keyword,
            "marketplace": book_type,
        }

        provenance = {}

        for field, key in field_keys.items():
            if hasattr(self.data_source, "value_with_provenance"):
                result = self.data_source.value_with_provenance(field, key)
                report[field] = result.value
                provenance[field] = result.as_dict()
            else:
                # Backward compatibility for older/custom data sources.
                report[field] = getattr(self.data_source, field)(key)

        if provenance:
            report["provenance"] = provenance
            report["confidence"] = self.confidence.analyze(provenance)

        report["opportunity"] = self.opportunity.analyze(report)
        report["recommendation"] = self.recommendation.analyze(
            report["opportunity"]
        )
        return report
