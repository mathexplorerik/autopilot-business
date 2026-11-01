import os
import json


class PublishAgent:

    def generate(self, book, seo, readiness=None, price=None):

        print("\n📦 Publish Agent Running...\n")

        os.makedirs("output/publish", exist_ok=True)

        metadata = {
            "title": seo["title"],
            "subtitle": seo["subtitle"],
            "description": seo["description"],
            "keywords": seo["keywords"],
            "categories": seo.get("categories", []),
            "price": price,
            "pages": book.get("pages") or book.get("total_pages", 40),
            "language": "English",
            "trim_size": "8.5 x 11"
        }

        checklist = self._checklist(readiness)

        # JSON
        with open("output/publish/metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        # Individual Files
        with open("output/publish/title.txt", "w", encoding="utf-8") as f:
            f.write(seo["title"])

        with open("output/publish/subtitle.txt", "w", encoding="utf-8") as f:
            f.write(seo["subtitle"])

        with open("output/publish/description.txt", "w", encoding="utf-8") as f:
            f.write(seo["description"])

        with open("output/publish/keywords.txt", "w", encoding="utf-8") as f:
            f.write(", ".join(seo["keywords"]))

        with open("output/publish/upload_checklist.txt", "w", encoding="utf-8") as f:
            f.write(checklist)

        print("✅ Publish files created.")

        return metadata

    def _checklist(self, readiness):
        """The checklist only states what the readiness check found. It never ticks anything on its own."""
        if not isinstance(readiness, dict):
            return (
                "KDP upload readiness: NOT CHECKED\n\n"
                "The readiness check was not run for this book, so nothing is confirmed.\n"
            )

        blockers = readiness.get("blockers") or []
        warnings = readiness.get("warnings") or []

        lines = ["KDP upload readiness: " + str(readiness.get("verdict", "NOT CHECKED")), ""]
        lines.append("Blocking problems (fix before uploading):" if blockers else "Blocking problems: none")
        for item in blockers:
            lines.append("  ✘ " + str(item))
        lines.append("")
        lines.append("Warnings:" if warnings else "Warnings: none")
        for item in warnings:
            lines.append("  ! " + str(item))
        lines.append("")
        lines.append("Always open the book in the KDP previewer and check it before you publish.")
        return "\n".join(lines) + "\n"
