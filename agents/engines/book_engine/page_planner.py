class PagePlanner:
    """
    Plans the number of pages for a book.
    """

    def __init__(self):

        self.default_pages = {
            "coloring_books": 50,
            "activity_books": 60,
            "maze_books": 40,
            "trace_books": 45,
            "dot_to_dot": 40,
            "word_search": 80,
            "cut_and_paste": 35
        }

    def plan(
        self,
        book_type: str,
        age_group: str = ""
    ) -> dict:

        book_type = book_type.strip().lower()

        pages = self.default_pages.get(
            book_type,
            50
        )

        return {
            "book_type": book_type,
            "age_group": age_group,
            "pages": pages
        }