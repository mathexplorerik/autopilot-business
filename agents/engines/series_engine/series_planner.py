"""
=========================================
Series Planner (V13 - Series Management)
=========================================
Defines and tracks a book series: a shared
character/subject and theme across multiple
books, with consistent branding and reading
order. Builds on the existing CharacterProfileGenerator
so the SAME character (name, accessory, companion,
home) persists across every book in the series -
not just within a single book.
"""

from agents.engines.book_engine.character_profile_generator import CharacterProfileGenerator


class SeriesPlanner:

    def __init__(self):
        self.character_profile_generator = CharacterProfileGenerator()

    def create_series(self, series_name: str, subject: str, age_group: str = "kids", planned_books: int = 3) -> dict:
        """
        Defines a new series: locks in ONE character profile
        that every book in the series will reuse, so the same
        character (accessory, companion, home) appears
        consistently across the whole series.
        """
        character_profile = self.character_profile_generator.generate(
            subject=subject,
            age_group=age_group,
        )

        return {
            "series_name": series_name,
            "subject": subject,
            "age_group": age_group,
            "planned_books": planned_books,
            "character_profile": character_profile,
            "books": [],
        }

    def add_book_to_series(self, series: dict, book_title: str, book_type: str = "story", season: str = None) -> dict:
        """
        Registers a new book entry within a series (does not
        generate the book itself - that's BookEngine's job).
        Returns the updated series dict with book metadata,
        including its position/order in the series.
        """
        book_number = len(series["books"]) + 1

        book_entry = {
            "book_number": book_number,
            "title": book_title,
            "book_type": book_type,
            "season": season,
            "series_label": f"Book {book_number} of {series['planned_books']}: {series['series_name']}",
        }

        series["books"].append(book_entry)
        return series

    def get_series_summary(self, series: dict) -> dict:
        return {
            "series_name": series["series_name"],
            "subject": series["subject"],
            "total_books_planned": series["planned_books"],
            "books_created": len(series["books"]),
            "books_remaining": max(0, series["planned_books"] - len(series["books"])),
            "reading_order": [b["title"] for b in series["books"]],
            "character_signature": series["character_profile"].get("signature_item"),
            "character_companion": series["character_profile"].get("companion"),
        }

    def get_cross_promotion_text(self, series: dict, current_book_number: int) -> str:
        """
        Generates "Also in this series..." text for back-cover/
        marketing use, listing the OTHER books in the series.
        """
        other_books = [
            b["title"] for b in series["books"]
            if b["book_number"] != current_book_number
        ]

        if not other_books:
            return f"Look out for more books in the {series['series_name']} series!"

        listed = ", ".join(other_books)
        return f"Also in the {series['series_name']} series: {listed}"
