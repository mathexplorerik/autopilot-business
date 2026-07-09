class TitleGenerator:
    """
    Generates a book title.
    """

    def __init__(self):
        pass

    def generate(
        self,
        keyword: str,
        book_type: str,
    ) -> str:

        keyword = keyword.strip().title()

        book_type = (
            book_type
            .replace("_", " ")
            .title()
        )

        return f"{keyword} {book_type}"