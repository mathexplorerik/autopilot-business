"""
=========================================
Heuristic Market Data Source (V14)
=========================================
The current, default implementation of
BaseMarketDataSource: delegates to the existing
JSON-backed analyzers (agents/data/knowledge/
database/trends/*.json). No behavior change from
before this refactor - this class only wraps the
already-tested analyzers behind the new interface.

Replace/extend this with a LiveMarketDataSource
(real APIs) later, without touching TrendEngine.
"""


from .base_market_data_source import BaseMarketDataSource


class HeuristicMarketDataSource(BaseMarketDataSource):

    def __init__(self):
        from agents.engines.trend_engine.demand_analyzer import DemandAnalyzer
        from agents.engines.trend_engine.competition_analyzer import CompetitionAnalyzer
        from agents.engines.trend_engine.profit_analyzer import ProfitAnalyzer
        from agents.engines.trend_engine.evergreen_analyzer import EvergreenAnalyzer
        from agents.engines.trend_engine.seasonal_analyzer import SeasonalAnalyzer
        from agents.engines.trend_engine.marketplace_analyzer import MarketplaceAnalyzer

        # ✅ Lazy imports — circular import avoid karo
        from agents.engines.trend_engine.demand_analyzer import DemandAnalyzer
        from agents.engines.trend_engine.competition_analyzer import CompetitionAnalyzer
        from agents.engines.trend_engine.profit_analyzer import ProfitAnalyzer
        from agents.engines.trend_engine.evergreen_analyzer import EvergreenAnalyzer
        from agents.engines.trend_engine.seasonal_analyzer import SeasonalAnalyzer
        from agents.engines.trend_engine.marketplace_analyzer import MarketplaceAnalyzer

        self._demand = DemandAnalyzer()
        self._competition = CompetitionAnalyzer()
        self._profit = ProfitAnalyzer()
        self._evergreen = EvergreenAnalyzer()
        self._seasonal = SeasonalAnalyzer()
        self._marketplace = MarketplaceAnalyzer()

    def demand(self, niche: str) -> int:
        return self._demand.analyze(niche)

    def competition(self, niche: str) -> int:
        return self._competition.analyze(niche)

    def profit(self, niche: str) -> int:
        return self._profit.analyze(niche)

    def evergreen(self, niche: str) -> int:
        return self._evergreen.analyze(niche)

    def seasonal(self, niche: str) -> int:
        return self._seasonal.analyze(niche)

    def marketplace(self, book_type: str) -> int:
        return self._marketplace.analyze(book_type)
