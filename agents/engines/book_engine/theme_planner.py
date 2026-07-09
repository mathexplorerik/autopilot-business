class ThemePlanner:
    """
    Plans the overall theme for the book.
    """

    def __init__(self):

        self.default_themes = {
            "animals": "Cute Animal Adventures",
            "dinosaurs": "Prehistoric World",
            "space": "Space Exploration",
            "farm": "Fun on the Farm",
            "ocean": "Ocean Life",
            "jungle": "Jungle Safari",
            "robots": "Robot World",
            "construction": "Construction Site",
            "princess": "Royal Kingdom",
            "unicorn": "Magical Unicorn Land",
            "dragons": "Dragon Fantasy"
        }

    def plan(self, keyword: str) -> dict:

        key = keyword.strip().lower()

        theme = self.default_themes.get(
            key,
            f"{keyword} Adventure"
        )

        return {
            "keyword": keyword,
            "theme": theme
        }