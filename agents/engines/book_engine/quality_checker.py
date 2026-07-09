class QualityChecker:
    """
    Validates the generated book blueprint.
    """

    def __init__(self):
        pass

    def validate(self, blueprint: dict) -> dict:

        issues = []

        if not blueprint.get("title"):
            issues.append("Missing title")

        if not blueprint.get("subtitle"):
            issues.append("Missing subtitle")

        if not blueprint.get("theme"):
            issues.append("Missing theme")

        if blueprint.get("total_pages", 0) <= 0:
            issues.append("Invalid page count")

        if not blueprint.get("scenes"):
            issues.append("No scenes generated")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }