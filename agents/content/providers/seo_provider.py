"""
==========================================================
AI Publishing OS V5
SEO Provider
==========================================================
"""


class SEOProvider:

    def get(self, niche):

        niche = niche.lower().strip()

        return {

            "amazon": {
                "title_template": f"{niche.title()} Coloring Book for Kids",
                "backend_keywords": [
                    niche,
                    "coloring book",
                    "kids",
                    "activity"
                ]
            },

            "etsy": {
                "tags": [
                    niche,
                    "printable",
                    "digital download",
                    "kids activity"
                ]
            },

            "gumroad": {
                "description_template":
                    f"{niche.title()} printable bundle"
            },

            "pinterest": {
                "keywords": [
                    f"{niche} printable",
                    f"{niche} coloring pages"
                ]
            }

        }