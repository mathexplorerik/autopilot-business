"""
=========================================
Base Research Plugin (V14)
=========================================
Abstract interface every data-source plugin
must implement. PluginManager and
SmartResearchEngine only depend on this
interface - never on a specific plugin's
internals.
"""

from abc import ABC, abstractmethod

from .research_result import ResearchResult


class BaseResearchPlugin(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique plugin identifier, e.g. 'local', 'google_books'."""
        raise NotImplementedError

    @abstractmethod
    def fetch(self, niche: str) -> ResearchResult:
        """
        Fetch data for the given niche and return it as a
        ResearchResult. Must NEVER raise for a "no data found"
        case - return an empty ResearchResult instead. Should
        raise only for genuine failures (network error, etc.),
        which PluginManager will catch and log.
        """
        raise NotImplementedError

    def is_available(self) -> bool:
        """
        Optional health check - e.g. an API-key-based plugin
        can return False if no key is configured, so
        PluginManager can skip it cleanly instead of failing.
        Defaults to True (always available).
        """
        return True
