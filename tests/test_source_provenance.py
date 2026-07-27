"""
Deterministic tests for market-data source provenance.

No live network dependency.
"""

import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from agents.engines.intelligence.data_sources.google_books_market_data_source import (
    GoogleBooksMarketDataSource,
)
from agents.engines.intelligence.data_sources.open_library_market_data_source import (
    OpenLibraryMarketDataSource,
)


def test_google_books_real_competition():
    source = GoogleBooksMarketDataSource()
    source._fetch = lambda niche: {
        "totalItems": 10000,
        "items": [],
    }

    result = source.value_with_provenance("competition", "lion")

    assert result.value == 50
    assert result.source == "google_books"
    assert result.mode == "real"
    assert isinstance(source.competition("lion"), int)

    print("[PASS] Google Books competition real provenance")


def test_google_books_real_demand():
    source = GoogleBooksMarketDataSource()
    source._fetch = lambda niche: {
        "totalItems": 1000,
        "items": [
            {"volumeInfo": {"ratingsCount": 250}},
            {"volumeInfo": {"ratingsCount": 500}},
        ],
    }

    result = source.value_with_provenance("demand", "lion")

    assert result.value == 75
    assert result.source == "google_books"
    assert result.mode == "real"
    assert isinstance(source.demand("lion"), int)

    print("[PASS] Google Books demand real provenance")


def test_google_books_missing_ratings_fallback():
    source = GoogleBooksMarketDataSource()
    source._fetch = lambda niche: {
        "totalItems": 1000,
        "items": [{"volumeInfo": {}}],
    }

    result = source.value_with_provenance("demand", "lion")

    assert result.mode == "fallback"
    assert result.source == source.fallback.source_name

    print("[PASS] Google Books missing ratings fallback provenance")


def test_google_books_api_failure_fallback():
    source = GoogleBooksMarketDataSource()

    def fail(_):
        raise TimeoutError("simulated API timeout")

    source._fetch = fail

    competition = source.value_with_provenance("competition", "lion")
    demand = source.value_with_provenance("demand", "lion")

    assert competition.mode == "fallback"
    assert demand.mode == "fallback"
    assert competition.source == source.fallback.source_name
    assert demand.source == source.fallback.source_name

    print("[PASS] Google Books API failure fallback provenance")


def test_open_library_real_competition():
    source = OpenLibraryMarketDataSource()
    source._fetch = lambda niche: {"numFound": 2500}

    result = source.value_with_provenance("competition", "lion")

    assert result.value == 50
    assert result.source == "open_library"
    assert result.mode == "real"
    assert isinstance(source.competition("lion"), int)

    print("[PASS] Open Library competition real provenance")


def test_open_library_api_failure_fallback():
    source = OpenLibraryMarketDataSource()

    def fail(_):
        raise TimeoutError("simulated API timeout")

    source._fetch = fail

    result = source.value_with_provenance("competition", "lion")

    assert result.mode == "fallback"
    assert result.source == source.fallback.source_name
    assert isinstance(source.competition("lion"), int)

    print("[PASS] Open Library API failure fallback provenance")


def run_all():
    tests = [
        test_google_books_real_competition,
        test_google_books_real_demand,
        test_google_books_missing_ratings_fallback,
        test_google_books_api_failure_fallback,
        test_open_library_real_competition,
        test_open_library_api_failure_fallback,
    ]

    for test in tests:
        test()

    print(f"\nAll {len(tests)} source provenance tests PASSED")
    return True


if __name__ == "__main__":
    run_all()
