"""
==========================================================
AI Publishing OS V7
Niche Schema
==========================================================
"""

REQUIRED_FIELDS = (
    "id",
    "name",
    "category",
    "audience",
    "marketplace",
    "recommended_pages",
    "difficulty",
    "evergreen",
    "seasonal",
    "keywords",
)


class NicheSchema:

    @staticmethod
    def validate(data: dict):

        if not isinstance(data, dict):
            return False

        for field in REQUIRED_FIELDS:

            if field not in data:
                return False

        if not isinstance(data["keywords"], list):
            return False

        if not isinstance(data["recommended_pages"], int):
            return False

        if not isinstance(data["evergreen"], bool):
            return False

        if not isinstance(data["seasonal"], bool):
            return False

        return True