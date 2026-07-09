"""
==========================================================
AI Publishing OS V5
Subject Provider
==========================================================
"""

from agents.data.subjects import SUBJECTS, get_subjects


class SubjectProvider:

    def __init__(self):
        self.subjects = SUBJECTS

    def get(self, niche: str):

        niche = niche.lower().strip()

        # Exact match
        subjects = get_subjects(niche)

        if subjects:
            return subjects

        # Partial match
        for key in self.subjects:

            if key in niche or niche in key:

                return get_subjects(key)

        # Fallback
        return [niche]

    def count(self, niche: str):

        return len(self.get(niche))

    def exists(self, niche: str):

        return len(self.get(niche)) > 0

    def all_niches(self):

        return sorted(self.subjects.keys())