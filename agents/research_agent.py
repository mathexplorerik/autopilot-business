"""
==========================================================
AI Publishing OS V7
Research Agent
==========================================================

Coordinates research workflow and integrates the
V7 Knowledge Engine without breaking the existing
Research Engine pipeline.
"""

from agents.engines.research_engine import ResearchEngine
from agents.knowledge_agent import KnowledgeAgent


class ResearchAgent:

    VERSION = "7.0.0"

    def __init__(self):

        self.engine = ResearchEngine()
        self.knowledge = KnowledgeAgent()

    # --------------------------------------------------

    def research(
        self,
        niche: str,
        season: str = ""
    ):

        print("\n🔍 Research Agent Running...\n")

        report = self.engine.analyze(
            niche=niche,
            season=season
        )

        self._print_summary(report)

        return report

    # --------------------------------------------------

    def get_niche(
        self,
        niche_id: str
    ):

        """
        Return niche information from the
        V7 Knowledge Engine.
        """

        return self.knowledge.get_niche(niche_id)

    # --------------------------------------------------

    def search_niches(
        self,
        keyword: str
    ):

        return self.knowledge.search(keyword)

    # --------------------------------------------------

    def statistics(self):

        return self.knowledge.statistics()

    # --------------------------------------------------

    def health(self):

        return {
            "version": self.VERSION,
            "knowledge": self.statistics(),
        }

    # --------------------------------------------------

    def _print_summary(self, report):

        print("────────────────────────────────────")
        print("📚 Research Summary")
        print("────────────────────────────────────")

        print(f"Resolved Niche : {report.resolved_niche}")
        print(f"Age Group      : {report.age_group}")
        print(f"Target Age     : {report.target_age}")
        print(f"Pages          : {report.pages}")
        print(f"Difficulty     : {report.difficulty}")
        print(f"Theme          : {report.theme}")
        print(f"Style          : {report.style}")
        print(f"Subjects       : {len(report.subjects)}")
        print(f"Demand Score   : {report.demand_score}/100")
        print(f"Competition    : {report.competition_score}/100")
        print(f"Profit Score   : {report.profit_score}/100")
        print(f"Evergreen      : {report.evergreen_score}/100")
        print(f"Opportunity    : {report.opportunity_score}/100")
        print(f"Recommendation : {report.recommendation}")
        print(f"Suggested Price: ${report.suggested_price}")

        competitor = report.metadata.get("competitor") or {}
        if competitor:
            print(f"Competition Tier: {competitor.get('competition_tier', 'unknown')}")
            print(f"Positioning    : {competitor.get('positioning', 'n/a')}")

        keyword_intel = report.metadata.get("keyword_intelligence") or []
        if keyword_intel:
            top_keyword = keyword_intel[0]
            print(f"Top Keyword    : {top_keyword.get('keyword')} (opportunity={top_keyword.get('opportunity')})")

        print("\nResearch Complete ✅")