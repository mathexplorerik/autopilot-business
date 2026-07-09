"""
Trend Engine Package

This package provides trend analysis for publishing opportunities.
"""

from .base_analyzer import BaseAnalyzer
from .score_calculator import ScoreCalculator

from .demand_analyzer import DemandAnalyzer
from .competition_analyzer import CompetitionAnalyzer
from .profit_analyzer import ProfitAnalyzer
from .evergreen_analyzer import EvergreenAnalyzer
from .seasonal_analyzer import SeasonalAnalyzer
from .marketplace_analyzer import MarketplaceAnalyzer

from .opportunity_analyzer import OpportunityAnalyzer
from .recommendation_engine import RecommendationEngine

from .trend_engine import TrendEngine


__all__ = [
    "BaseAnalyzer",
    "ScoreCalculator",

    "DemandAnalyzer",
    "CompetitionAnalyzer",
    "ProfitAnalyzer",
    "EvergreenAnalyzer",
    "SeasonalAnalyzer",
    "MarketplaceAnalyzer",

    "OpportunityAnalyzer",
    "RecommendationEngine",

    "TrendEngine",
]