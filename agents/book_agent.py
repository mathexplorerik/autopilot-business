"""
==========================================================
AI Publishing OS V8
Book Agent
==========================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from agents.engines.book_engine import BookEngine


class BookAgent:
    """
    AI Publishing OS

    Main entry point for book generation.

    Responsibilities
    ----------------
    • Configure generation
    • Generate books
    • Save blueprints
    • Export JSON
    • Statistics
    • Health
    """

    VERSION = "8.0.0"

    def __init__(self):

        self.engine = BookEngine()

        self.output_dir = Path("output/books")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.reset()

    # --------------------------------------------------

    def reset(self):

        self.book = None

        self.created_at = None

        self.keyword = ""

        self.book_type = ""

        self.age_group = ""

    # --------------------------------------------------

    def configure(
        self,
        keyword: str,
        book_type: str,
        age_group: str,
    ):

        self.keyword = keyword.strip()

        self.book_type = book_type.strip()

        self.age_group = age_group.strip()

    # --------------------------------------------------

    def create_book(
        self,
        keyword: str,
        book_type: str = "coloring_books",
        age_group: str = "kids",
        season: str = None,
    ) -> Dict:
        """
        Generate a complete book blueprint.
        """

        self.season = season

        self.configure(
            keyword,
            book_type,
            age_group,
        )

        self.created_at = datetime.now()

        self.book = self.engine.build(
            keyword=self.keyword,
            book_type=self.book_type,
            age_group=self.age_group,
            season=self.season,
        )

        return self.book
        # --------------------------------------------------

    def preview(self) -> Optional[Dict]:
        """
        Return current generated book.
        """

        return self.book

    # --------------------------------------------------

    def validate(self) -> bool:
        """
        Basic validation.
        """

        if self.book is None:
            return False

        required = [
            "title",
            "subtitle",
            "keyword",
            "theme",
            "scenes",
            "quality",
        ]

        for field in required:

            if field not in self.book:
                return False

        return True

    # --------------------------------------------------

    def export_json(self) -> str:
        """
        Export current book as JSON string.
        """

        if self.book is None:
            return ""

        return json.dumps(
            self.book,
            indent=4,
            ensure_ascii=False,
        )

    # --------------------------------------------------

    def save(
        self,
        filename: Optional[str] = None,
    ) -> Path:
        """
        Save blueprint to disk.
        """

        if self.book is None:
            raise RuntimeError(
                "No book has been generated."
            )

        if filename is None:

            filename = (
                self.keyword
                .replace(" ", "_")
                .lower()
            )

        path = self.output_dir / f"{filename}.json"

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.book,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return path

    # --------------------------------------------------

    def save_blueprint(
        self,
        filename: Optional[str] = None,
    ) -> Path:
        """
        Alias for save().
        """

        return self.save(filename)
        # --------------------------------------------------

    def statistics(self) -> Dict:
        """
        Agent statistics.
        """

        if self.book is None:

            return {
                "generated": False,
                "version": self.VERSION,
            }

        return {

            "generated": True,

            "version": self.VERSION,

            "keyword": self.keyword,

            "book_type": self.book_type,

            "age_group": self.age_group,

            "total_pages": self.book.get(
                "total_pages",
                0,
            ),

            "total_scenes": len(
                self.book.get(
                    "scenes",
                    [],
                )
            ),

            "quality_valid": self.book.get(
                "quality",
                {},
            ).get(
                "valid",
                False,
            ),
        }

    # --------------------------------------------------

    def summary(self) -> Dict:
        """
        Book summary.
        """

        if self.book is None:

            return {}

        return {

            "title": self.book.get(
                "title"
            ),

            "subtitle": self.book.get(
                "subtitle"
            ),

            "keyword": self.keyword,

            "theme": self.book.get(
                "theme"
            ),

            "pages": self.book.get(
                "total_pages",
                0,
            ),

            "recommendation": self.book.get(
                "trend",
                {},
            ).get(
                "recommendation",
                "Unknown",
            ),
        }

    # --------------------------------------------------

    def health(self) -> Dict:
        """
        Agent health status.
        """

        return {

            "healthy": self.book is not None,

            "engine": "BookEngine",

            "version": self.VERSION,

            "created_at":
                self.created_at.isoformat()
                if self.created_at
                else None,
        }

    # --------------------------------------------------

    def version(self) -> str:
        """
        Agent version.
        """

        return self.VERSION
        # --------------------------------------------------

    def load(
        self,
        filename: str,
    ) -> Dict:
        """
        Load a previously saved book blueprint.
        """

        path = self.output_dir / filename

        if not path.exists():

            raise FileNotFoundError(
                f"{path} not found."
            )

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            self.book = json.load(file)

        return self.book

    # --------------------------------------------------

    def reload(self):
        """
        Reload current book from disk.
        """

        if self.book is None:

            return None

        filename = (
            self.keyword
            .replace(" ", "_")
            .lower()
        ) + ".json"

        return self.load(filename)

    # --------------------------------------------------

    def exists(
        self,
        filename: str,
    ) -> bool:
        """
        Check whether a saved blueprint exists.
        """

        path = self.output_dir / filename

        return path.exists()

    # --------------------------------------------------

    def delete(
        self,
        filename: str,
    ) -> bool:
        """
        Delete a saved blueprint.
        """

        path = self.output_dir / filename

        if not path.exists():

            return False

        path.unlink()

        return True

    # --------------------------------------------------

    def clear(self):
        """
        Clear current agent state.
        """

        self.reset()

    # --------------------------------------------------

    def created_time(self):
        """
        Return creation timestamp.
        """

        return self.created_at

    # --------------------------------------------------

    def output_directory(self) -> Path:
        """
        Return output directory.
        """

        return self.output_dir

    # --------------------------------------------------

    def current_book(self):
        """
        Return current book object.
        """

        return self.book
        # --------------------------------------------------

    def __len__(self):
        """
        Return total pages in the current book.
        """

        if self.book is None:
            return 0

        return self.book.get(
            "total_pages",
            0,
        )

    # --------------------------------------------------

    def __bool__(self):
        """
        True if a book has been generated.
        """

        return self.book is not None

    # --------------------------------------------------

    def __getitem__(self, key):
        """
        Dictionary-style access.
        """

        if self.book is None:
            raise KeyError("No active book.")

        return self.book[key]

    # --------------------------------------------------

    def __contains__(self, key):
        """
        Support:
            "title" in agent
        """

        if self.book is None:
            return False

        return key in self.book

    # --------------------------------------------------

    def __repr__(self):

        pages = 0

        if self.book:

            pages = self.book.get(
                "total_pages",
                0,
            )

        return (
            f"<BookAgent "
            f"version={self.VERSION} "
            f"keyword='{self.keyword}' "
            f"pages={pages}>"
        )

    # --------------------------------------------------

    def __str__(self):

        if self.book is None:

            return "BookAgent(No Book)"

        return (
            f"BookAgent("
            f"title='{self.book.get('title')}', "
            f"pages={self.book.get('total_pages', 0)})"
        )