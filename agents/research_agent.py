"""
==========================================================
AI Publishing OS V5
Research Agent
==========================================================
"""

from agents.engines.research_engine import ResearchEngine


class ResearchAgent:

    def __init__(self):

        self.engine = ResearchEngine()

    def research(self, niche: str, season: str = ""):

        print("\n🔍 Research Agent Running...\n")

        report = self.engine.analyze(
            niche=niche,
            season=season
        )

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
        print(f"Competition    : {report.competition}")

        print("\nResearch Complete ✅")

        return report