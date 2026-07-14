from agents.engines.research.audience_analyzer import AudienceAnalyzer


class SubtitleGenerator:
    """
    Generates a subtitle for the book.
    """

    def __init__(self):
        self.audience_analyzer = AudienceAnalyzer()

    def _resolve_target_age(self, age_group):
        rules = self.audience_analyzer.AGE_RULES
        if age_group in rules:
            return rules[age_group]["target_age"]
        return age_group

    def generate(
        self,
        keyword: str,
        age_group: str,
    ) -> str:
        keyword = keyword.strip().title()
        if age_group:
            target_age = self._resolve_target_age(age_group)
            return (
                f"A Fun {keyword} Activity Book "
                f"for Kids Ages {target_age}"
            )
        return f"A Fun {keyword} Book for Kids"
