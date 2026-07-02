import os
import json
from datetime import datetime

class CoverAgent:

    def create(self, book):
        """main.py ke liye"""
        return self.generate(book)

    def generate(self, book):
        print("\n🖼️  Cover Agent Running...\n")

        title    = book.get("title", "Coloring Book")
        subtitle = book.get("subtitle", "Fun Coloring Pages for Kids")
        niche    = book.get("niche", "animals")
        age      = book.get("target_age", "4-8 Years")

        # ✅ Main cover prompt
        cover_prompt = (
            f"Professional kids coloring book cover, "
            f"title '{title}', "
            f"cute cartoon {niche} characters, "
            f"bright vivid colors, bold typography, "
            f"clean layout, white background, "
            f"Amazon KDP style, bestseller design, "
            f"target age {age}, "
            f"high quality illustration, "
            f"no text overlap, centered composition"
        )

        # ✅ Negative prompt
        negative_prompt = (
            "no blurry images, no watermark, no adult content, "
            "no dark themes, no violence, no scary elements, "
            "no copyright characters, no text errors"
        )

        # ✅ Back cover prompt
        back_prompt = (
            f"Back cover of kids coloring book, "
            f"simple design, white background, "
            f"small cute {niche} illustration, "
            f"space for book description, "
            f"barcode placeholder at bottom right, "
            f"Amazon KDP back cover style"
        )

        # ✅ Spine prompt
        spine_prompt = (
            f"Book spine design, "
            f"title '{title}', "
            f"vertical text, "
            f"colorful background, "
            f"Amazon KDP spine style"
        )

        cover = {
            "title":           title,
            "subtitle":        subtitle,
            "niche":           niche,
            "size":            "8.5 x 11 inches",
            "full_wrap_size":  "17.5 x 11.25 inches",
            "dpi":             300,
            "color_mode":      "RGB",
            "created_at":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompts": {
                "front":    cover_prompt,
                "back":     back_prompt,
                "spine":    spine_prompt,
                "negative": negative_prompt
            },
            "kdp_specs": {
                "bleed":        "0.125 inch all sides",
                "safe_zone":    "0.25 inch from edges",
                "spine_width":  "calculated by KDP",
                "format":       "PDF or JPG",
                "color_profile": "sRGB"
            }
        }

        # ✅ Save files
        os.makedirs("output/covers", exist_ok=True)

        # JSON
        json_path = "output/covers/cover.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(cover, f, indent=4, ensure_ascii=False)

        # Front prompt
        front_path = "output/covers/cover_prompt_front.txt"
        with open(front_path, "w", encoding="utf-8") as f:
            f.write(f"=== FRONT COVER ===\n")
            f.write(f"POSITIVE:\n{cover_prompt}\n\n")
            f.write(f"NEGATIVE:\n{negative_prompt}\n")

        # Back prompt
        back_path = "output/covers/cover_prompt_back.txt"
        with open(back_path, "w", encoding="utf-8") as f:
            f.write(f"=== BACK COVER ===\n")
            f.write(f"POSITIVE:\n{back_prompt}\n\n")
            f.write(f"NEGATIVE:\n{negative_prompt}\n")

        # KDP specs
        specs_path = "output/covers/kdp_specs.txt"
        with open(specs_path, "w", encoding="utf-8") as f:
            f.write("KDP COVER SPECIFICATIONS\n")
            f.write("="*40 + "\n\n")
            for key, val in cover["kdp_specs"].items():
                f.write(f"{key:15} : {val}\n")

        # ✅ Print summary
        print(f"  📚 Title      : {title}")
        print(f"  📖 Subtitle   : {subtitle}")
        print(f"  📐 Size       : {cover['size']}")
        print(f"  🖨️  DPI        : {cover['dpi']}")
        print(f"  🎨 Prompts    : Front + Back + Spine ready")
        print(f"  📄 JSON       : {json_path}")
        print(f"  📄 Front      : {front_path}")
        print(f"  📄 Back       : {back_path}")
        print(f"  📄 KDP Specs  : {specs_path}")
        print(f"  ✅ Cover Ready!")

        return cover
