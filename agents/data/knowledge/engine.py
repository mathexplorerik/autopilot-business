"""
==========================================================
AI Publishing OS V7
Knowledge Engine
==========================================================
"""

from .loader import KnowledgeLoader
from .sources import (
    get_all,
    get_by_id,
    get_categories,
    get_subjects,
)


class KnowledgeEngine:
    """
    Central knowledge engine.
    """

    VERSION = "7.0.0"

    def __init__(self):
        self.loader = KnowledgeLoader()

    # --------------------------------------------------

    def version(self):
        return self.VERSION

    # --------------------------------------------------

    def source_exists(self, filename: str):
        return self.loader.exists(filename)

    # --------------------------------------------------

    def get_source_path(self, filename: str):
        return self.loader.source_path(filename)

    # --------------------------------------------------

    def get_cache_path(self, filename: str):
        return self.loader.cache_path(filename)

    # --------------------------------------------------

    def get_database_path(self, filename: str):
        return self.loader.database_path(filename)

    # --------------------------------------------------

    def info(self):

        return {
            "version": self.VERSION,
            "sources": str(self.loader.sources),
            "cache": str(self.loader.cache),
            "database": str(self.loader.database),
        }

    # --------------------------------------------------

    def niches(self):
        return get_all()

    # --------------------------------------------------

    def niche(self, niche_id: str):
        return get_by_id(niche_id)

    # --------------------------------------------------

    def categories(self):
        return get_categories()

    # --------------------------------------------------

    def subjects(self, category: str):
        return get_subjects(category)

    # --------------------------------------------------

    def search(self, keyword: str):

        keyword = keyword.lower().strip()

        results = []

        for niche in self.niches():

            if (
                keyword in niche.id.lower()
                or keyword in niche.name.lower()
                or keyword in niche.category.lower()
                or keyword in niche.description.lower()
            ):
                results.append(niche)

        return results

    # --------------------------------------------------

    def statistics(self):

        return {
            "total_niches": len(self.niches()),
            "total_categories": len(self.categories()),
        }

    # --------------------------------------------------

    def database_niches(self):
        return self.loader.available_niches()

    # --------------------------------------------------

    def database_niche(self, niche_id: str):
        return self.loader.load_niche(niche_id)