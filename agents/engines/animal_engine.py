import random


class AnimalEngine:

    def build(
        self,
        subject,
        age_group,
        page_number,
        total_pages,
        season=None,
    ):

        positive = (
            f"{subject}, cute cartoon animal, kids coloring book page, "
            "bold clean outlines, black and white line art, "
            "simple background, centered composition, "
            "no shading, printable, white background"
        )

        negative = (
            "color, grayscale, realistic, photo, text, watermark, "
            "logo, blurry, low quality, extra limbs"
        )

        return {
            "positive": positive,
            "negative": negative,
            "complexity": self.get_complexity(page_number, total_pages),
        }

    def get_complexity(self, page, total):

        ratio = page / total

        if ratio <= 0.25:
            return "simple"

        elif ratio <= 0.50:
            return "intermediate"

        elif ratio <= 0.75:
            return "advanced"

        return "pro"