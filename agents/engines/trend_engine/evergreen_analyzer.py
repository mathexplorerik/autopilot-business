from .base_analyzer import BaseAnalyzer


class EvergreenAnalyzer(BaseAnalyzer):

    def __init__(self):
        super().__init__()
        self.data = self.load_json("evergreen.json")

    def analyze(self, keyword: str) -> int:

        keyword = self.normalize(keyword)

        score = self.data.get(
            keyword,
            self.fallback_score()
        )

        return self.clamp_score(score)