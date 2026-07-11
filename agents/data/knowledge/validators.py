"""
==========================================================
AI Publishing OS V7
Knowledge Validators
==========================================================
"""


class KnowledgeValidator:
    """
    Validate knowledge records before they are used.

    Responsibilities
    ----------------
    ✓ Required fields
    ✓ Empty values
    ✓ Future schema validation
    """

    REQUIRED_FIELDS = (
        "id",
        "name",
        "category",
    )

    def validate_dict(self, record: dict) -> bool:

        if not isinstance(record, dict):
            return False

        for field in self.REQUIRED_FIELDS:

            value = record.get(field)

            if value is None:
                return False

            if isinstance(value, str) and not value.strip():
                return False

        return True

    def validate_records(self, records) -> bool:

        if not isinstance(records, list):
            return False

        return all(
            self.validate_dict(record)
            for record in records
        )