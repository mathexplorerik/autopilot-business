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
✔ Cover
✔ Title
✔ Subtitle
✔ Description
✔ Keywords
✔ Categories
"""

        with open("output/publish/metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        with open("output/publish/upload_checklist.txt", "w", encoding="utf-8") as f:
            f.write(checklist)

        print("✅ Publish files created.")

        return metadata