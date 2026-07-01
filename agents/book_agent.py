import os
import json


class BookAgent:

    def build(self, report, seo):

        print("\n📖 Book Agent Running...\n")

        book = {
            "title": seo["title"],
            "subtitle": seo["subtitle"],
            "description": seo["description"],
            "keywords": seo["keywords"],
            "niche": report["niche"],
            "pages": report["pages"],
            "target_age": report["target_age"],
            "difficulty": report["difficulty"],
            "prompts_file": "output/prompts/prompts.txt",
            "seo_file": "output/seo/seo.txt"
        }

        os.makedirs("output/books", exist_ok=True)

        with open("output/books/book.json", "w", encoding="utf-8") as f:
            json.dump(book, f, indent=4)

        print("Book data saved to output/books/book.json ✅")

        return book