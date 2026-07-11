"""
==========================================================
AI Publishing OS V7
Knowledge Agent
==========================================================
"""

from agents.data.knowledge import KnowledgeEngine


class KnowledgeAgent:

    VERSION = "7.0.0"

    def __init__(self):
        self.engine = KnowledgeEngine()

    def get_niche(self, niche_id: str):
        """
        Return JSON niche if available.
        Otherwise fallback to Python source.
        """
        niche = self.engine.database_niche(niche_id)

        if niche:
            return niche

        return self.engine.niche(niche_id)

    def search(self, keyword: str):
        return self.engine.search(keyword)

    def statistics(self):
        return self.engine.statistics()