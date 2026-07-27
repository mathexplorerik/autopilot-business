"""
=========================================
Base Market Data Source (V14)
=========================================
Abstract interface for market-data providers.
TrendEngine depends on this interface, not on
any specific implementation, so a real-API
provider (Google Trends, Amazon scraping, a
keyword-research API, etc.) can be swapped in
later without changing TrendEngine or anything
downstream of it.
"""

from abc import ABC, abstractmethod


class BaseMarketDataSource(ABC):

    @abstractmethod
    def demand(self, niche: str) -> int:
        """Return a 0-100 demand score for the niche."""
        raise NotImplementedError

    @abstractmethod
    def competition(self, niche: str) -> int:
        """Return a 0-100 competition score for the niche."""
        raise NotImplementedError

    @abstractmethod
    def profit(self, niche: str) -> int:
        """Return a 0-100 profit-potential score for the niche."""
        raise NotImplementedError

    @abstractmethod
    def evergreen(self, niche: str) -> int:
        """Return a 0-100 evergreen (timelessness) score for the niche."""
        raise NotImplementedError

    @abstractmethod
    def seasonal(self, niche: str) -> int:
        """Return a 0-100 seasonal-relevance score for the niche."""
        raise NotImplementedError

    @abstractmethod
    def marketplace(self, book_type: str) -> int:
        """Return a 0-100 marketplace-fit score for the book type."""
        raise NotImplementedError

    @property
    def source_name(self) -> str:
        return self.__class__.__name__

    def value_with_provenance(self, field: str, key: str):
        """
        Return a SourceValue for an existing score method without
        changing the legacy int-returning API.

        Concrete real-data sources may override this method to mark
        individual fields as real or fallback.
        """
        from .source_value import SourceValue

        allowed = {
            "demand",
            "competition",
            "profit",
            "evergreen",
            "seasonal",
            "marketplace",
        }
        if field not in allowed:
            raise ValueError(f"Unknown market-data field: {field}")

        value = getattr(self, field)(key)

        return SourceValue(
            value=value,
            source=self.source_name,
            mode="heuristic",
        )
