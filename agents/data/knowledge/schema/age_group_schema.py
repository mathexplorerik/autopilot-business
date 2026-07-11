"""
==========================================================
AI Publishing OS V7
Age Group Schema
==========================================================
"""

from .base_schema import BaseSchema


class AgeGroupSchema(BaseSchema):

    REQUIRED_FIELDS = (
        "id",
        "name",
        "recommended_pages",
        "complexity",
    )