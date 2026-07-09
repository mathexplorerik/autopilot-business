"""
==========================================================
AI Publishing OS V7
Marketplace Schema
==========================================================
"""

from .base_schema import BaseSchema


class MarketplaceSchema(BaseSchema):

    REQUIRED_FIELDS = (
        "id",
        "name",
        "currency",
    )