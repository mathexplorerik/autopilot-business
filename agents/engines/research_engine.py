"""
==========================================================
AI Publishing OS V5
Research Engine
==========================================================
"""

from agents.models.research_report import ResearchReport

from agents.engines.research.niche_analyzer import NicheAnalyzer
from agents.engines.research.audience_analyzer import AudienceAnalyzer
from agents.engines.research.theme_analyzer import ThemeAnalyzer
from agents.engines.research.style_analyzer import StyleAnalyzer
from agents.engines.research.market_analyzer import MarketAnalyzer
from agents.engines.research.seo_analyzer import SEOAnalyzer


class ResearchEngine:

    def __init__(self):

        self.niche = NicheAnalyzer()
        self.audience = AudienceAnalyzer()
        self.theme = ThemeAnalyzer()
        self.style = StyleAnalyzer()
        self.market = MarketAnalyzer()
        self.seo = SEOAnalyzer()

    def analyze(self, niche: str, season: str = ""):

        # -----------------------------
        # Run All AI Analyzers
        # -----------------------------

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

        # -----------------------------
        # Build Research Report
        # -----------------------------

        report = ResearchReport(

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

            metadata={

                "market": market_data,

                "seo": seo_data,

                "style": style_data,

                "theme": theme_data,

                "confidence": niche_data["confidence"],

                "match_type": niche_data["match_type"]

            }

        )

        return report