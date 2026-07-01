import os


class SEOAgent:

    def generate(self, report):

        print("\n🔎 SEO Agent Running...\n")

        niche = report["niche"]

        seo = {
            "title": f"{niche} Coloring Book for Kids",
            "subtitle": "Fun, Easy and Relaxing Coloring Pages",
            "description": f"Enjoy 40 beautiful {niche.lower()} coloring pages designed for kids. Thick outlines, easy illustrations and hours of creative fun.",
            "keywords": [
                niche.lower(),
                f"{niche.lower()} coloring book",
                "kids coloring book",
                "easy coloring pages",
                "activity book",
                "gift for kids",
                "black and white line art"
            ]
        }

        os.makedirs("output/seo", exist_ok=True)

        with open("output/seo/seo.txt", "w", encoding="utf-8") as f:
            f.write(f"TITLE:\n{seo['title']}\n\n")
            f.write(f"SUBTITLE:\n{seo['subtitle']}\n\n")
            f.write(f"DESCRIPTION:\n{seo['description']}\n\n")
            f.write("KEYWORDS:\n")

            for keyword in seo["keywords"]:
                f.write(f"- {keyword}\n")

        print("SEO saved to output/seo/seo.txt ✅")

        return seo