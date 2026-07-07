import os
import json
import requests
from datetime import datetime

class SEOAgent:

    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL      = "gemma3"

    def generate(self, book):
        print("\n🔎 SEO Agent Running...\n")

        niche      = book.get("niche", "animals")
        age        = book.get("target_age", "4-8 Years")
        pages      = book.get("pages", 40)
        difficulty = book.get("difficulty", "Easy")
        category   = book.get("kdp_category", "Children's Books")

        # ✅ AI se generate karo
        print("  🤖 Generating with AI...")
        ai_seo = self._generate_with_ai(niche, age, pages)

        if not ai_seo:
            print("  ⚠️  AI failed — using smart templates")
            ai_seo = self._smart_template(niche, age, pages)

        # ✅ Keywords — 7 KDP backend keywords
        keywords = self._generate_keywords(niche, age)

        # ✅ Categories
        categories = self._get_categories(niche)

        seo = {
            "title":       ai_seo.get("title",       f"{niche.title()} Coloring Book for Kids"),
            "subtitle":    ai_seo.get("subtitle",     f"Fun, Easy Coloring Pages for Ages {age}"),
            "description": ai_seo.get("description",  self._default_description(niche, age, pages)),
            "keywords":    keywords,
            "categories":  categories,
            "kdp_category": category,
            "metadata": {
                "niche":      niche,
                "age":        age,
                "pages":      pages,
                "difficulty": difficulty,
                "generated":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

        self._save(seo)
        self._print_summary(seo)
        return seo

    def _generate_with_ai(self, niche, age, pages):
        """Ollama Gemma3 se SEO generate karo"""
        prompt = f"""You are an Amazon KDP SEO expert. Generate SEO content for a kids coloring book.

Niche: {niche}
Age: {age}
Pages: {pages}

Generate ONLY a JSON object with these exact fields:
{{
  "title": "compelling Amazon KDP title with main keyword (max 200 chars)",
  "subtitle": "benefit-focused subtitle (max 200 chars)",
  "description": "Amazon book description with emotional hook, benefits, and call to action (max 4000 chars)"
}}

Rules:
- Title must contain main keyword naturally
- Subtitle must show clear benefit
- Description: start with hook, list 5 benefits, end with CTA
- Target age: {age}
- NO markdown, NO extra text, ONLY JSON"""

        try:
            response = requests.post(
                self.OLLAMA_URL,
                json={
                    "model": self.MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                text = response.json().get("response", "")
                # JSON extract karo
                start = text.find("{")
                end   = text.rfind("}") + 1
                if start != -1 and end > start:
                    return json.loads(text[start:end])

        except Exception as e:
            print(f"  ⚠️  AI error: {e}")

        return None

    def _smart_template(self, niche, age, pages):
        """Smart template fallback"""
        niche_title = niche.title()
        return {
            "title": f"{niche_title} Coloring Book for Kids Ages {age}: {pages} Fun & Adorable {niche_title} Coloring Pages for Children",
            "subtitle": f"Perfect Gift for Boys & Girls | Hours of Creative Fun | Stress Relief Activity Book",
            "description": self._default_description(niche, age, pages)
        }

    def _default_description(self, niche, age, pages):
        niche_title = niche.title()
        return f"""🎨 Introducing the MOST ADORABLE {niche_title} Coloring Book for Kids!

Is this the perfect gift you've been looking for? YES! This amazing {niche_title} coloring book is specially designed for children ages {age} who LOVE {niche_title}!

✅ WHAT'S INSIDE:
- {pages} unique and adorable {niche_title} illustrations
- Large, easy-to-color designs perfect for little hands
- Thick black outlines for easy coloring
- Single-sided pages to prevent bleed-through
- Progressive difficulty from simple to detailed

🌟 BENEFITS FOR YOUR CHILD:
- Develops creativity and imagination
- Improves hand-eye coordination
- Builds focus and concentration
- Screen-free entertainment for hours
- Perfect for home, school, or travel

🎁 PERFECT GIFT FOR:
- Birthdays, Christmas, Easter
- Rainy day activities
- Classroom rewards
- Road trips and holidays

👆 Click ADD TO CART now and give your child the gift of creativity!"""

    def _generate_keywords(self, niche, age):
        """7 KDP backend keywords generate karo"""
        niche_lower = niche.lower()
        age_clean   = age.replace(" ", "").lower()

        keywords = [
            f"{niche_lower} coloring book for kids",
            f"{niche_lower} coloring pages children",
            f"kids coloring book ages {age_clean}",
            f"{niche_lower} activity book children",
            f"coloring book {niche_lower} gift kids",
            f"{niche_lower} coloring book boys girls",
            f"fun {niche_lower} coloring pages toddlers"
        ]

        return keywords[:7]

    def _get_categories(self, niche):
        """Best KDP categories suggest karo"""
        niche_lower = niche.lower()

        category_map = {
            "animals":   ["Children's Books > Arts, Music & Photography > Drawing", "Children's Books > Activities, Crafts & Games > Activity Books"],
            "dinosaurs": ["Children's Books > Science, Nature & How It Works > Zoology", "Children's Books > Activities, Crafts & Games > Activity Books"],
            "diwali":    ["Children's Books > Holidays & Celebrations > Other Holidays", "Children's Books > Arts, Music & Photography > Drawing"],
            "christmas": ["Children's Books > Holidays & Celebrations > Christmas & Advent", "Children's Books > Activities, Crafts & Games > Activity Books"],
            "eid":       ["Children's Books > Holidays & Celebrations > Other Holidays", "Children's Books > Arts, Music & Photography > Drawing"],
        }

        for key in category_map:
            if key in niche_lower:
                return category_map[key]

        return [
            "Children's Books > Arts, Music & Photography > Drawing",
            "Children's Books > Activities, Crafts & Games > Activity Books"
        ]

    def _save(self, seo):
        """Sab files save karo"""
        os.makedirs("output/seo", exist_ok=True)

        # ✅ TXT — KDP upload ke liye
        txt_path = "output/seo/seo.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("="*50 + "\n")
            f.write("KDP SEO CONTENT\n")
            f.write("="*50 + "\n\n")
            f.write(f"TITLE:\n{seo['title']}\n\n")
            f.write(f"SUBTITLE:\n{seo['subtitle']}\n\n")
            f.write(f"DESCRIPTION:\n{seo['description']}\n\n")
            f.write("7 BACKEND KEYWORDS:\n")
            for i, kw in enumerate(seo['keywords'], 1):
                f.write(f"{i}. {kw}\n")
            f.write(f"\nCATEGORIES:\n")
            for cat in seo['categories']:
                f.write(f"• {cat}\n")

        # ✅ JSON — system ke liye
        json_path = "output/seo/seo.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(seo, f, indent=2, ensure_ascii=False)

        # ✅ KDP Ready file
        kdp_path = "output/seo/kdp_ready.txt"
        with open(kdp_path, "w", encoding="utf-8") as f:
            f.write("KDP UPLOAD CHECKLIST\n")
            f.write("="*50 + "\n\n")
            f.write(f"📚 TITLE (copy-paste):\n{seo['title']}\n\n")
            f.write(f"📖 SUBTITLE (copy-paste):\n{seo['subtitle']}\n\n")
            f.write(f"📝 DESCRIPTION (copy-paste):\n{seo['description']}\n\n")
            f.write("🔑 7 KEYWORDS (copy-paste one by one):\n")
            for kw in seo['keywords']:
                f.write(f"{kw}\n")
            f.write(f"\n📂 CATEGORIES:\n")
            for cat in seo['categories']:
                f.write(f"{cat}\n")

        print(f"  📄 TXT      : {txt_path}")
        print(f"  📄 JSON     : {json_path}")
        print(f"  📄 KDP File : {kdp_path}")

    def _print_summary(self, seo):
        print(f"\n  {'='*40}")
        print(f"  📚 Title    : {seo['title'][:50]}...")
        print(f"  📖 Subtitle : {seo['subtitle'][:50]}...")
        print(f"  🔑 Keywords : {len(seo['keywords'])} generated")
        print(f"  📂 Category : {seo['categories'][0][:40]}...")
        print(f"  ✅ SEO Complete!")