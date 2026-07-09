import os
import json
from datetime import datetime


class BookAgent:

    VERSION = "v5"

    def create(self, report):
        """
        Create book from ResearchReport
        """

        print("\n📖 Book Agent Running...\n")

        # -------- Support object OR dict --------

        if hasattr(report, "resolved_niche"):

            niche = report.resolved_niche
            pages = report.pages
            age_group = report.age_group
            target_age = report.target_age
            difficulty = report.difficulty
            subjects = report.subjects
            keywords = report.keywords

            title = f"{niche.title()} Coloring Book for Kids"

            subtitle = (
                f"Fun, Easy and Printable Coloring Pages "
                f"for Ages {target_age}"
            )

        else:

            niche = report["niche"]
            pages = report["pages"]
            age_group = report.get("age_group", "kids")
            target_age = report["target_age"]
            difficulty = report["difficulty"]
            subjects = report.get("subjects", [])
            keywords = report.get("keywords", [])

            title = f"{niche.title()} Coloring Book for Kids"

            subtitle = (
                f"Fun, Easy Coloring Pages "
                f"for Ages {target_age}"
            )

        # -------- Build Book --------

        book = {

            "version": self.VERSION,

            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "niche": niche,

            "title": title,

            "subtitle": subtitle,

            "pages": pages,

            "age_group": age_group,

            "target_age": target_age,

            "difficulty": difficulty,

            "subjects": subjects,

            "keywords": keywords,

            "platforms": [
                "Amazon KDP",
                "Etsy",
                "Gumroad",
                "Payhip"
            ],

            "status": "draft"

        }

        self._save(book)

        self._summary(book)

        return book

    # -------------------------------------

    def _save(self, book):

        os.makedirs("output/books", exist_ok=True)

        filename = (
            book["niche"]
            .replace(" ", "_")
            .lower()
        )

        path = f"output/books/{filename}_book.json"

        with open(path, "w", encoding="utf-8") as f:

            json.dump(
                book,
                f,
                indent=4,
                ensure_ascii=False
            )

        book["json_path"] = path

        print(f"  💾 Saved : {path}")

    # -------------------------------------

    def _summary(self, book):

        print("────────────────────────────────")

        print(f"📚 Title       : {book['title']}")
        print(f"📄 Pages       : {book['pages']}")
        print(f"👶 Target Age  : {book['target_age']}")
        print(f"🎯 Difficulty  : {book['difficulty']}")
        print(f"📦 Platforms   : {', '.join(book['platforms'])}")

        print("────────────────────────────────")

        print("✅ Book Ready")