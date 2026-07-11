from pathlib import Path
import json


class BaseAnalyzer:
    """
    Base class for all Trend Engine analyzers.
    """

    DEFAULT_SCORE = 50

    def __init__(self):
        self.database_root = (
            Path("agents/data/knowledge")
            / "database"
            / "trends"
        )

    def load_json(self, filename: str) -> dict:

        file_path = self.database_root / filename

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def normalize(self, value: str) -> str:

        if value is None:
            return ""

        return value.strip().lower()

    def clamp_score(
        self,
        score: int,
        minimum: int = 0,
        maximum: int = 100,
    ) -> int:

        return max(minimum, min(score, maximum))

    def fallback_score(self) -> int:

        return self.DEFAULT_SCORE