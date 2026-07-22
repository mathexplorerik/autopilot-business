"""
=========================================
Local/Offline Research Plugin (V14)
=========================================
Wraps the existing static JSON-backed data
(agents/data/knowledge/database/trends/*.json)
behind the new BaseResearchPlugin interface.
Always available (no network/API key needed),
serves as the reliable default/fallback plugin.
"""

from agents.engines.trend_engine.demand_analyzer import DemandAnalyzer
from agents.engines.trend_engine.evergreen_analyzer import EvergreenAnalyzer
from agents.data.subjects import get_keywords, list_niches

from ..base_plugin import BaseResearchPlugin
from ..research_result import ResearchResult


class LocalPlugin(BaseResearchPlugin):

    def __init__(self):
        self._demand = DemandAnalyzer()
        self._evergreen = EvergreenAnalyzer()
        self._known_niches = set(list_niches())

    @property
    def name(self) -> str:
        return "local"

    def is_available(self) -> bool:
        return True  # local data is always available, no network needed

    def fetch(self, niche: str) -> ResearchResult:
        niche_key = niche.strip().lower()
        is_known = niche_key in self._known_niches

        if not is_known:
            # Genuinely no local data for this niche - return an
            # honest empty result rather than a disguised guess.
            return ResearchResult(niche=niche, source=self.name, raw={"known": False})

        demand_score = self._demand.analyze(niche_key)
        evergreen_score = self._evergreen.analyze(niche_key)
        keywords = get_keywords(niche_key)

        estimated_listing_count = round(demand_score * 3.5)

        return ResearchResult(
            niche=niche,
            source=self.name,
            title_examples=[f"{niche.title()} Coloring Book for Kids"],
            estimated_listing_count=estimated_listing_count,
            related_keywords=keywords,
            raw={"demand_score": demand_score, "evergreen_score": evergreen_score, "known": True},
        )
