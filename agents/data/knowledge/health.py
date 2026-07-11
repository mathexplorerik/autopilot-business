"""
==========================================================
AI Publishing OS V7
Knowledge Health Check
==========================================================
"""

from knowledge import KnowledgeEngine


class KnowledgeHealth:

    def __init__(self):
        self.engine = KnowledgeEngine()

    def check(self):

        return {
            "version": self.engine.version(),
            "python_niches": len(self.engine.niches()),
            "json_niches": len(self.engine.database_niches()),
            "categories": len(self.engine.categories()),
        }

    def print_report(self):

        report = self.check()

        print("\n")
        print("=" * 50)
        print("Knowledge Health Report")
        print("=" * 50)

        for key, value in report.items():
            print(f"{key:<20}: {value}")

        print("=" * 50)