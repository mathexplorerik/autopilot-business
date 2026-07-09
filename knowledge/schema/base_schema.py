"""
==========================================================
AI Publishing OS V7
Base Schema
==========================================================
"""


class BaseSchema:

    REQUIRED_FIELDS = ()

    @classmethod
    def validate(cls, data: dict):

        if not isinstance(data, dict):
            return False

        for field in cls.REQUIRED_FIELDS:

            if field not in data:
                return False

            value = data[field]

            if isinstance(value, str) and not value.strip():
                return False

        return True