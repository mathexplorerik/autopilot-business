"""
==========================================================
AI KDP AUTOPILOT V5
Theme Analyzer
==========================================================
"""


class ThemeAnalyzer:

    THEMES = {

        "dinosaurs": {
            "theme": "Prehistoric Adventure",
            "style": "Cute Cartoon",
            "scene": "Volcanoes, jungles, rocks"
        },

        "farm animals": {
            "theme": "Happy Farm",
            "style": "Cute Farm Cartoon",
            "scene": "Barns, fences, grass"
        },

        "jungle animals": {
            "theme": "Wild Jungle",
            "style": "Cute Safari",
            "scene": "Trees, vines, rivers"
        },

        "ocean animals": {
            "theme": "Underwater Adventure",
            "style": "Cute Ocean",
            "scene": "Corals, fish, bubbles"
        },

        "space": {
            "theme": "Space Adventure",
            "style": "Cute Space",
            "scene": "Planets, stars, rockets"
        },

        "princess": {
            "theme": "Royal Kingdom",
            "style": "Fantasy Cartoon",
            "scene": "Castle, flowers, magic"
        },

        "vehicles": {
            "theme": "Transportation",
            "style": "Bold Cartoon",
            "scene": "Roads, city, construction"
        }
    }

    def analyze(self, niche: str):

        data = self.THEMES.get(
            niche.lower(),
            {
                "theme": niche.title(),
                "style": "Cute Cartoon",
                "scene": "Simple White Background"
            }
        )

        return data