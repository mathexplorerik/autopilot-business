"""
=========================================
ResearchResult (V14 Canonical Data Model)
=========================================
Every research plugin (local JSON, Google Books,
Open Library, future real-time APIs) must return
data shaped like THIS, regardless of its source.
Downstream code (normalizer, SmartResearchEngine,
intelligence modules) only ever depends on this
shape - never on any single plugin's raw format.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ResearchResult:
    niche: str
    source: str  # which plugin produced this (e.g. "local", "google_books")

    title_examples: List[str] = field(default_factory=list)
    estimated_listing_count: Optional[int] = None
    average_rating: Optional[float] = None
    review_count_estimate: Optional[int] = None

    related_keywords: List[str] = field(default_factory=list)
    related_categories: List[str] = field(default_factory=list)

    raw: dict = field(default_factory=dict)  # original untouched plugin payload, for debugging

    def is_empty(self) -> bool:
        return (
            not self.title_examples
            and self.estimated_listing_count is None
            and not self.related_keywords
        )
