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
