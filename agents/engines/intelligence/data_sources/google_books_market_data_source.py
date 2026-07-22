"""
=========================================
Google Books Market Data Source
=========================================
Implements BaseMarketDataSource using the free, public Google
Books API (https://www.googleapis.com/books/v1/volumes) - no
API key or payment required for basic search.

HONESTY NOTE: Google Books genuinely only gives us a real
signal for COMPETITION (how many books already exist for this
niche). It has no signal for profit/evergreen/seasonal/
marketplace-fit - rather than fabricate those from Google
Books data (which would look like real data but wouldn't be),
this class falls back to HeuristicMarketDataSource for every
field Google Books can't actually measure.

Requires outbound network access. If a request fails (no
internet, rate limited, timeout), demand()/competition() fall
back to the heuristic source too - this class NEVER raises
for a missing/failed network call, since TrendEngine expects
a plain int back from every method.
"""

import urllib.request
import urllib.parse
import json

from .base_market_data_source import BaseMarketDataSource
from .heuristic_market_data_source import HeuristicMarketDataSource


class GoogleBooksMarketDataSource(BaseMarketDataSource):

    API_URL = "https://www.googleapis.com/books/v1/volumes"
    TIMEOUT_SECONDS = 8
    COMPETITION_CEILING = 20000

    def __init__(self, fallback: BaseMarketDataSource = None):
        self.fallback = fallback or HeuristicMarketDataSource()
        self._cache = {}

    def _fetch(self, niche: str) -> dict:
        if niche in self._cache:
            return self._cache[niche]

        query = f"{niche} coloring book"
        params = urllib.parse.urlencode({"q": query, "maxResults": 20, "printType": "books"})
        url = f"{self.API_URL}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "autopilot-business-research/1.0"})

        with urllib.request.urlopen(req, timeout=self.TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))

        self._cache[niche] = data
        return data

    def competition(self, niche: str) -> int:
        try:
            data = self._fetch(niche)
            total_items = data.get("totalItems", 0)
            return min(100, round((total_items / self.COMPETITION_CEILING) * 100))
        except Exception:
            return self.fallback.competition(niche)

    def demand(self, niche: str) -> int:
        try:
            data = self._fetch(niche)
            items = data.get("items", [])
            rating_counts = [
                item.get("volumeInfo", {}).get("ratingsCount", 0)
                for item in items
                if item.get("volumeInfo", {}).get("ratingsCount")
            ]
            if not rating_counts:
                return self.fallback.demand(niche)
            avg_rating_count = sum(rating_counts) / len(rating_counts)
            return min(100, round((avg_rating_count / 500) * 100))
        except Exception:
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
        return "GoogleBooksMarketDataSource"
