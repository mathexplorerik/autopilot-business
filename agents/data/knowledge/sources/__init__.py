"""
==========================================================
AI Publishing OS V7
Knowledge Sources
==========================================================
"""

from .niches import (
    NICHES,
    get_all,
    get_by_id,
)

from .animals import (
    get_categories,
    get_subjects,
)

__all__ = [
    "NICHES",
    "get_all",
    "get_by_id",
    "get_categories",
    "get_subjects",
]