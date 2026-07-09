"""
==========================================================
AI KDP AUTOPILOT V5
Niche Analyzer
==========================================================
"""

from data.resolver import NicheResolver
from agents.data.subjects import get_subjects


class NicheAnalyzer:

    def __init__(self):
        self.resolver = NicheResolver()

    def analyze(self, niche: str):

        resolved = self.resolver.resolve(niche)

        resolved_niche = resolved["niche"]

        subjects = resolved.get("subjects", [])

        if not subjects:
            subjects = get_subjects(resolved_niche)

        return {
            "input_niche": niche,
            "resolved_niche": resolved_niche,
            "subjects": subjects,
            "subject_count": len(subjects),
            "confidence": resolved.get("confidence", 100),
            "match_type": resolved.get("match_type", "exact")
        }