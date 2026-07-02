import os
import json


class PublishAgent:

    def generate(self, book, seo):

        print("\n📦 Publish Agent Running...\n")

        os.makedirs("output/publish", exist_ok=True)

        metadata = {
            "title": seo["title"],
            "subtitle": seo["subtitle"],
            "description": seo["description"],
            "keywords": seo["keywords"],
            "pages": book["pages"],
            "language": "English",
            "trim_size": "8.5 x 11"
        }

        checklist = """
KDP Upload Checklist

✔ Interior PDF
✔ Cover PDF
✔ Title
✔ Subtitle
✔ Description
✔ Keywords
✔ Categories
✔ Pricing
✔ Preview Before Publish
"""

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