"""
==========================================================
AI Publishing OS V7
Style Schema
==========================================================
"""

from .base_schema import BaseSchema


class StyleSchema(BaseSchema):

    REQUIRED_FIELDS = (
        "id",
        "name",
        "line_weight",
        "complexity",
    )