"""
=========================================
Business Dashboard (V13)
=========================================
Aggregates every saved book blueprint under output/books/
into a single portfolio-level summary. Degrades gracefully:
missing directory, empty directory, or corrupted JSON files
are excluded (and counted) rather than crashing the report.
"""

import json
from pathlib import Path


class BusinessDashboard:

    def __init__(self, books_dir: str = "output/books"):
        self.books_dir = Path(books_dir)

    def _load_books(self) -> tuple:
        if not self.books_dir.exists():
            return [], 0

        books = []
        corrupted = 0
        for path in self.books_dir.glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    books.append(json.load(f))
            except (json.JSONDecodeError, OSError):
                corrupted += 1

        return books, corrupted

    def generate(self) -> dict:
        books, corrupted_count = self._load_books()

        if not books:
            return {
                "total_books": 0,
                "corrupted_files_skipped": corrupted_count,
                "quality_pass_rate": None,
                "niches": [],
                "note": "No readable book blueprints found under " + str(self.books_dir),
            }

        total = len(books)
        valid_count = sum(1 for b in books if (b.get("quality") or {}).get("valid"))
        niches = sorted({b.get("niche") or b.get("keyword", "unknown") for b in books})

        revenue_estimates = [
            b["metadata"]["revenue_prediction"]["estimated_monthly_revenue"]["mid"]
            for b in books
            if isinstance(b.get("metadata"), dict)
            and isinstance(b["metadata"].get("revenue_prediction"), dict)
        ]

        return {
            "total_books": total,
            "corrupted_files_skipped": corrupted_count,
            "quality_pass_rate": round(valid_count / total, 2),
            "books_needing_review": total - valid_count,
            "niches": niches,
            "total_estimated_monthly_revenue_mid": (
                round(sum(revenue_estimates), 2) if revenue_estimates else None
            ),
            "books_with_revenue_data": len(revenue_estimates),
        }
