"""
=========================================
Open Library Market Data Source
=========================================
Implements BaseMarketDataSource using the free, public Open
Library Search API (https://openlibrary.org/search.json) - no
API key or payment required.

HONESTY NOTE: same philosophy as GoogleBooksMarketDataSource -
Open Library only gives a real signal for COMPETITION (how
many books already exist for this niche, via numFound). It has
no signal for demand/profit/evergreen/seasonal/marketplace-fit,
so those are honestly deferred to the fallback source rather
than fabricated.

Requires outbound network access. Never raises for a failed
network call - always falls back to the heuristic source, since
TrendEngine expects a plain int back from every method.
"""

import urllib.request
import urllib.parse
import json

from .base_market_data_source import BaseMarketDataSource
from .heuristic_market_data_source import HeuristicMarketDataSource


class OpenLibraryMarketDataSource(BaseMarketDataSource):

    API_URL = "https://openlibrary.org/search.json"
    TIMEOUT_SECONDS = 8
    COMPETITION_CEILING = 5000

    def __init__(self, fallback: BaseMarketDataSource = None):
        self.fallback = fallback or HeuristicMarketDataSource()
        self._cache = {}

    def _fetch(self, niche: str) -> dict:
        if niche in self._cache:
            return self._cache[niche]

        query = f"{niche} coloring book"
        params = urllib.parse.urlencode({"q": query, "limit": 20})
        url = f"{self.API_URL}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "autopilot-business-research/1.0"})

        with urllib.request.urlopen(req, timeout=self.TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))

        self._cache[niche] = data
        return data

    def _competition_result(self, niche: str):
        from .source_value import SourceValue

        try:
            data = self._fetch(niche)
            num_found = data.get("numFound", 0)
            value = min(
                100,
                round((num_found / self.COMPETITION_CEILING) * 100),
            )
            return SourceValue(
                value=value,
                source="open_library",
                mode="real",
            )
        except Exception:
            return SourceValue(
                value=self.fallback.competition(niche),
                source=self.fallback.source_name,
                mode="fallback",
            )

    def competition(self, niche: str) -> int:
        return self._competition_result(niche).value

    def value_with_provenance(self, field: str, key: str):
        from .source_value import SourceValue

        if field == "competition":
            return self._competition_result(key)

        allowed = {
            "demand",
            "profit",
            "evergreen",
            "seasonal",
            "marketplace",
        }
        if field not in allowed:
            raise ValueError(f"Unknown market-data field: {field}")

        value = getattr(self.fallback, field)(key)
        return SourceValue(
            value=value,
            source=self.fallback.source_name,
            mode="fallback",
        )

    def demand(self, niche: str) -> int:
        return self.fallback.demand(niche)

    def profit(self, niche: str) -> int:
        return self.fallback.profit(niche)

    def evergreen(self, niche: str) -> int:
        return self.fallback.evergreen(niche)

    def seasonal(self, niche: str) -> int:
        return self.fallback.seasonal(niche)

    def marketplace(self, book_type: str) -> int:
        return self.fallback.marketplace(book_type)

    @property
    def source_name(self) -> str:
        return "OpenLibraryMarketDataSource"
