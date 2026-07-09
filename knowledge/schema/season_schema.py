"""
==========================================================
AI Publishing OS V7
Season Schema
==========================================================
"""

from .base_schema import BaseSchema


class SeasonSchema(BaseSchema):

    REQUIRED_FIELDS = (
        "id",
        "name",
    )