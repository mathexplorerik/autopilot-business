"""
==========================================================
AI KDP AUTOPILOT V5
Audience Analyzer
==========================================================
"""

from agents.data.subjects import get_age_group


class AudienceAnalyzer:

    AGE_RULES = {
        "toddler": {
            "target_age": "2-4 Years",
            "difficulty": "very_easy",
            "pages": 30
        },
        "kids": {
            "target_age": "4-8 Years",
            "difficulty": "easy",
            "pages": 40
        },
        "teens": {
            "target_age": "9-15 Years",
            "difficulty": "advanced",
            "pages": 50
        },
        "adults": {
            "target_age": "16+ Years",
            "difficulty": "pro",
            "pages": 60
        }
    }

    def analyze(self, niche: str):

        age_group = get_age_group(niche)

        profile = self.AGE_RULES.get(
            age_group,
            self.AGE_RULES["kids"]
        )

        return {
            "age_group": age_group,
            "target_age": profile["target_age"],
            "difficulty": profile["difficulty"],
            "recommended_pages": profile["pages"]
        }