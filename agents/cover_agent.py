import os
import json


class CoverAgent:

    def generate(self, book):

        print("\n🖼️ Cover Agent Running...\n")

        cover = {

            "title": book["title"],

            "subtitle": book["subtitle"],

            "size": "8.5 x 11 inches",

            "dpi": 300,

            "prompt":
            f"""
Professional kids coloring book cover.

Title:
{book['title']}

Subtitle:
{book['subtitle']}

Cute cartoon animals.
Colorful.
Bold typography.
Clean layout.
White background.
Bright colors.
Best selling Amazon KDP style.
Professional design.
"""
        }

        os.makedirs("output/covers", exist_ok=True)

        with open("output/covers/cover.json", "w") as f:
            json.dump(cover, f, indent=4)

        with open("output/covers/cover_prompt.txt", "w") as f:
            f.write(cover["prompt"])

        print("✅ Cover files created.")

        return cover