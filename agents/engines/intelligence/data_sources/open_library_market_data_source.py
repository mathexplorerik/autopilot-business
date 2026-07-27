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

    def competition(self, niche: str) -> int:
        try:
            data = self._fetch(niche)
            num_found = data.get("numFound", 0)
            return min(100, round((num_found / self.COMPETITION_CEILING) * 100))
        except Exception:
            return self.fallback.competition(niche)

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
