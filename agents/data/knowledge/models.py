"""
==========================================================
AI Publishing OS V7
Knowledge Models
==========================================================
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class KnowledgeRecord:
    """
    Base knowledge record.
    """

    id: str
    name: str
    category: str
    description: str = ""
    tags: tuple[str, ...] = ()
    source: str = ""
    active: bool = True


@dataclass(slots=True)
class NicheRecord(KnowledgeRecord):
    """
    Publishing niche.
    """

    audience: str = ""
    marketplace: str = "Amazon KDP"


@dataclass(slots=True)
class StyleRecord(KnowledgeRecord):
    """
    Drawing / illustration style.
    """

    line_weight: str = ""
    complexity: str = "medium"


@dataclass(slots=True)
class SeasonRecord(KnowledgeRecord):
    """
    Seasonal publishing record.
    """

    month: Optional[int] = None


@dataclass(slots=True)
class MarketplaceRecord(KnowledgeRecord):
    """
    Marketplace metadata.
    """

    url: str = ""
    currency: str = "USD"