from agents.engines.trend_engine import TrendEngine


class TrendAgent:

    def __init__(self):
        self.engine = TrendEngine()

    def analyze(
        self,
        keyword: str,
        book_type: str = "",
        age_group: str = "",
    ):

        return self.engine.analyze(
            keyword=keyword,
            book_type=book_type,
            age_group=age_group,
        )