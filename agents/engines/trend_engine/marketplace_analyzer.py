from .base_analyzer import BaseAnalyzer


class MarketplaceAnalyzer(BaseAnalyzer):

    def __init__(self):
        super().__init__()
        self.data = self.load_json("marketplace.json")

    def analyze(self, book_type: str) -> int:

        book_type = self.normalize(book_type)

        score = self.data.get(
            book_type,
            self.fallback_score()
        )

        return self.clamp_score(score)