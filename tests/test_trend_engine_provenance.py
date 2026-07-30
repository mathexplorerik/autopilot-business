"""
TrendEngine provenance integration tests.

Verifies that provenance metadata is exposed while the
existing integer score contract remains backward compatible.
"""

import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from agents.engines.trend_engine.trend_engine import TrendEngine
from agents.engines.intelligence.data_sources.open_library_market_data_source import (
    OpenLibraryMarketDataSource,
)
from agents.engines.intelligence.data_sources.heuristic_market_data_source import (
    HeuristicMarketDataSource,
)


def test_open_library_provenance():
    source = OpenLibraryMarketDataSource()
    source._fetch = lambda niche: {"numFound": 2500}

    result = TrendEngine(source).analyze(
        "lion",
        book_type="coloring_books",
        age_group="kids",
    )

    assert result["competition"] == 50
    assert result["provenance"]["competition"] == {
        "value": 50,
        "source": "open_library",
        "mode": "real",
    }

    # Unsupported Open Library fields must honestly report fallback.
    assert result["provenance"]["profit"]["mode"] == "fallback"

    # Existing score contract stays unchanged.
    for field in (
        "demand",
        "competition",
        "profit",
        "evergreen",
        "seasonal",
        "marketplace",
        "opportunity",
    ):
        assert isinstance(result[field], int), field

    print("[PASS] TrendEngine exposes Open Library provenance")


def test_heuristic_provenance():
    result = TrendEngine(
        HeuristicMarketDataSource()
    ).analyze(
        "lion",
        book_type="coloring_books",
        age_group="kids",
    )

    for field in (
        "demand",
        "competition",
        "profit",
        "evergreen",
        "seasonal",
        "marketplace",
    ):
        meta = result["provenance"][field]
        assert meta["value"] == result[field]
        assert meta["mode"] == "heuristic"

    print("[PASS] TrendEngine exposes heuristic provenance")


def run_all():
    test_open_library_provenance()
    test_heuristic_provenance()

    print("\nAll 2 TrendEngine provenance tests PASSED")
    return True


if __name__ == "__main__":
    run_all()
