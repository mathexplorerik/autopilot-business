import os
import json
from datetime import datetime

class BookAgent:
    def create(self, report):
        """main.py ke liye — research se basic book banao"""
        print("\n📖 Book Agent Running...\n")

        # Basic book report se
        book = {
            "niche":       report["niche"],
            "pages":       report["pages"],
            "target_age":  report["target_age"],
            "difficulty":  report["difficulty"],
            "age_group":   report.get("age_group", "kids"),
            "subjects":    report.get("subjects", []),
            "keywords":    report.get("keywords", []),
            "kdp_category": report.get("kdp_category", ""),
            "title":       f"{report['niche'].title()} Coloring Book for Kids",
            "subtitle":    f"Fun, Easy and Relaxing Coloring Pages for Ages {report['target_age']}",
            "created_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version":     "v3"
        }

        self._save(book)
        self._print_summary(book)
        return book

    def build(self, report, seo):
        """SEO data ke saath complete book banao"""
        print("\n📖 Book Agent Running...\n")

        book = {
            "niche":        report["niche"],
            "pages":        report["pages"],
            "target_age":   report["target_age"],
            "difficulty":   report["difficulty"],
            "age_group":    report.get("age_group", "kids"),
            "subjects":     report.get("subjects", []),
            "kdp_category": report.get("kdp_category", ""),
            "title":        seo["title"],
            "subtitle":     seo["subtitle"],
            "description":  seo["description"],
            "keywords":     seo["keywords"],
            "prompts_file": "output/prompts/prompts.txt",
            "seo_file":     "output/seo/seo.txt",
            "created_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version":      "v3"
        }

        self._save(book)
        self._print_summary(book)
        return book

    def _save(self, book):
        """Book JSON save karo"""
        os.makedirs("output/books", exist_ok=True)

        # Dynamic filename
        safe_title = book["niche"].replace(" ", "_").lower()
        path = f"output/books/{safe_title}_book.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(book, f, indent=4, ensure_ascii=False)

        print(f"  ✅ Saved : {path}")
        book["json_path"] = path

    def _print_summary(self, book):
        """Summary print karo"""
        print(f"  📚 Title      : {book['title']}")
        print(f"  📄 Pages      : {book['pages']}")
        print(f"  👶 Age Group  : {book['target_age']}")
        print(f"  🎯 Difficulty : {book['difficulty']}")
        print(f"  🏷️  Category  : {book.get('kdp_category', 'N/A')}")
        print(f"  ✅ Book Ready!")