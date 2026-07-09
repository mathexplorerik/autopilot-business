from .base_analyzer import BaseAnalyzer


class ProfitAnalyzer(BaseAnalyzer):

    def __init__(self):
        super().__init__()
        self.data = self.load_json("profit.json")

    def analyze(self, keyword: str) -> int:

        keyword = self.normalize(keyword)

        score = self.data.get(
            keyword,
            self.fallback_score()
        )

        return self.clamp_score(score)