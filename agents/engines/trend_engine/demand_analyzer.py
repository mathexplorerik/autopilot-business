import json
from pathlib import Path


class DemandAnalyzer:

    DEFAULT_SCORE = 50

    def __init__(self):

        data_file = (
            Path("agents/data/knowledge")
            / "database"
            / "trends"
            / "evergreen.json"
        )

        with open(data_file, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def normalize(self, keyword: str) -> str:

        return keyword.strip().lower()

    def analyze(self, keyword: str) -> int:

        keyword = self.normalize(keyword)

        return self._data.get(keyword, self.DEFAULT_SCORE)