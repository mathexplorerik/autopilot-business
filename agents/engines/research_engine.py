"""
==========================================================
AI Publishing OS V7
Research Engine
==========================================================
"""

from agents.models.research_report import ResearchReport
from agents.knowledge_agent import KnowledgeAgent

from agents.engines.research.niche_analyzer import NicheAnalyzer
from agents.engines.research.audience_analyzer import AudienceAnalyzer
from agents.engines.research.theme_analyzer import ThemeAnalyzer
from agents.engines.research.style_analyzer import StyleAnalyzer
from agents.engines.research.market_analyzer import MarketAnalyzer
from agents.engines.research.seo_analyzer import SEOAnalyzer
from agents.engines.trend_engine.trend_engine import TrendEngine
from agents.engines.intelligence.keyword_intelligence import KeywordIntelligence


class ResearchEngine:

    VERSION = "7.0.0"

    def __init__(self):

        self.knowledge = KnowledgeAgent()

        self.niche = NicheAnalyzer()
        self.audience = AudienceAnalyzer()
        self.theme = ThemeAnalyzer()
        self.style = StyleAnalyzer()
        self.market = MarketAnalyzer()
        self.seo = SEOAnalyzer()
        self.trend = TrendEngine()
        self.keyword_intelligence = KeywordIntelligence()

    # --------------------------------------------------

    def analyze(
        self,
        niche: str,
        season: str = ""
    ):

        # ----------------------------------------
        # Knowledge Lookup (V7)
        # ----------------------------------------

        knowledge = self.knowledge.get_niche(niche)

        # ----------------------------------------
        # Existing AI Pipeline
        # ----------------------------------------

        niche_data = self.niche.analyze(niche)

        audience_data = self.audience.analyze(
            niche_data["resolved_niche"]
        )

        theme_data = self.theme.analyze(
            niche_data["resolved_niche"]
        )

        style_data = self.style.analyze(
            audience_data["age_group"]
        )

        market_data = self.market.analyze(
            niche_data["resolved_niche"]
        )

        seo_data = self.seo.analyze(
            niche_data["resolved_niche"]
        )
        trend_data = self.trend.analyze(
            niche_data["resolved_niche"],
            book_type="coloring_books",
            age_group=audience_data["age_group"],
        )

        # ----------------------------------------
        # Build Report
        # ----------------------------------------

        return ResearchReport(

            niche=niche,

            resolved_niche=niche_data["resolved_niche"],

            age_group=audience_data["age_group"],

            target_age=audience_data["target_age"],

            pages=audience_data["recommended_pages"],

            difficulty=audience_data["difficulty"],

            theme=theme_data["theme"],

            style=theme_data["style"],

            season=season,

            subjects=niche_data["subjects"],

            keywords=seo_data["keywords"],

            backend_keywords=seo_data["backend_keywords"],

            category="",

            competition=market_data["competition"],
            demand_score=trend_data["demand"],
            competition_score=trend_data["competition"],
            profit_score=trend_data["profit"],
            evergreen_score=trend_data["evergreen"],
            seasonal_score=trend_data["seasonal"],
            marketplace_score=trend_data["marketplace"],
            opportunity_score=trend_data["opportunity"],
            recommendation=trend_data["recommendation"],

            metadata={

                "knowledge": knowledge,

                "market": market_data,

                "seo": seo_data,

                "style": style_data,

                "theme": theme_data,

                "confidence": niche_data["confidence"],

                "match_type": niche_data["match_type"],

                "engine_version": self.VERSION

            }

        )

    # --------------------------------------------------

    def statistics(self):

        return self.knowledge.statistics()

    # --------------------------------------------------

    def search(self, keyword: str):

        return self.knowledge.search(keyword)