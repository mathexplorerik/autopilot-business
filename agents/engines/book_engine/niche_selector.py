from agents.trend_agent import TrendAgent


class NicheSelector:
    """
    Selects the best niche using Trend Engine.
    """

    def __init__(self):

        self.trend_agent = TrendAgent()

    def select(
        self,
        keyword: str,
        book_type: str,
        age_group: str,
    ):

        trend_report = self.trend_agent.analyze(
            keyword=keyword,
            book_type=book_type,
            age_group=age_group,
        )

        return {
            "keyword": keyword,
            "trend_report": trend_report,
        }