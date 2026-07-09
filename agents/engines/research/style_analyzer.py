"""
==========================================================
AI KDP AUTOPILOT V5
Style Analyzer
==========================================================
"""


class StyleAnalyzer:

    STYLES = {

        "kids": {
            "line_weight": "bold thick outlines",
            "coloring_style": "large coloring spaces",
            "detail_level": "simple"
        },

        "teens": {
            "line_weight": "medium outlines",
            "coloring_style": "moderate details",
            "detail_level": "medium"
        },

        "adults": {
            "line_weight": "fine outlines",
            "coloring_style": "highly detailed",
            "detail_level": "complex"
        }
    }

    def analyze(self, age_group: str):

        return self.STYLES.get(
            age_group,
            self.STYLES["kids"]
        )