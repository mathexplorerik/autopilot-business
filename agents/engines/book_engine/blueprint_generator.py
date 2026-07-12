class BlueprintGenerator:
    """
    Builds the final book blueprint.

    Produces a rich, self-describing blueprint object that
    downstream modules (Character Memory, Theme Consistency,
    Educational Modes) can build on without needing to
    re-derive book structure.
    """

    def __init__(self):
        pass

    def _build_chapter_allocation(self, book_type, total_pages):
        """
        Returns the chapter breakdown for story books,
        scaled to total_pages. Empty for niche books
        (no chapters apply).
        """
        if book_type != "story":
            return []

        base_chapters = [
            ("Introduction", 1, 8),
            ("Exploration", 9, 16),
            ("Activities", 17, 24),
            ("Adventure", 25, 32),
            ("Wrap-up", 33, 40),
        ]
        base_total = 40

        chapters = []
        for name, start, end in base_chapters:
            scaled_start = max(1, round((start - 1) / base_total * total_pages) + 1)
            scaled_end = max(scaled_start, round(end / base_total * total_pages))
            chapters.append({
                "name": name,
                "pages": [scaled_start, scaled_end],
            })

        return chapters

    def generate(
        self,
        title: str,
        subtitle: str,
        keyword: str,
        theme: str,
        pages: int,
        scenes: list,
        book_type: str = "niche",
        target_age: str = "kids",
        character_profile: dict = None,
    ) -> dict:

        chapters = self._build_chapter_allocation(book_type, pages)

        difficulty_curve = (
            "simple -> intermediate -> advanced -> pro"
            if book_type == "story"
            else "varies by page position"
        )

        return {
            "title": title,
            "subtitle": subtitle,
            "keyword": keyword,
            "book_type": book_type,
            "theme": theme,
            "target_age": target_age,
            "total_pages": pages,
            "difficulty_curve": difficulty_curve,
            "chapters": chapters,

            # Reserved for future milestones (V12.2+)
            "character_profile": character_profile or {},
            "recurring_elements": [],
            "learning_objective": None,

            "scenes": scenes,
        }
