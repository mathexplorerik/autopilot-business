class SubtitleGenerator:
    """
    Generates a subtitle for the book.
    """

    def __init__(self):
        pass

    def generate(
        self,
        keyword: str,
        age_group: str,
    ) -> str:

        keyword = keyword.strip().title()

        if age_group:
            return (
                f"A Fun {keyword} Activity Book "
                f"for Kids Ages {age_group}"
            )

        return f"A Fun {keyword} Book for Kids"