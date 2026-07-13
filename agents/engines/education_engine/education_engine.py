"""
=========================================
Education Engine
=========================================
Generates prompts for educational coloring
book pages: alphabet, numbers, colors, shapes.
"""

from agents.data.education.alphabet_data import ALPHABET_DATA
from agents.data.education.numbers_data import NUMBERS_DATA
from agents.data.education.colors_data import COLORS_DATA
from agents.data.education.shapes_data import SHAPES_DATA

MODE_DATA = {
    "alphabet": ALPHABET_DATA,
    "numbers": NUMBERS_DATA,
    "colors": COLORS_DATA,
    "shapes": SHAPES_DATA,
}


class EducationEngine:

    DEFAULT_NEGATIVE = (
        "color fills, shading, gradients, gray areas, "
        "realistic, photo, watermark, text errors, "
        "blurry, low quality, extra limbs, deformed"
    )

    def get_page_count(self, education_mode):
        data = MODE_DATA.get(education_mode, [])
        return len(data)

    def build(self, education_mode, page_number, age_group="kids"):
        data = MODE_DATA.get(education_mode)
        if not data:
            raise ValueError("Unknown education_mode: " + str(education_mode))

        index = (page_number - 1) % len(data)
        entry = data[index]

        if education_mode == "alphabet":
            positive = self._build_alphabet_prompt(entry)
            label = "Letter " + entry["letter"]
        elif education_mode == "numbers":
            positive = self._build_numbers_prompt(entry)
            label = "Number " + str(entry["number"])
        elif education_mode == "colors":
            positive = self._build_colors_prompt(entry)
            label = "Color " + entry["color"]
        elif education_mode == "shapes":
            positive = self._build_shapes_prompt(entry)
            label = "Shape " + entry["shape"]
        else:
            raise ValueError("Unknown education_mode: " + str(education_mode))

        return {
            "positive": positive,
            "negative": self.DEFAULT_NEGATIVE,
            "education_mode": education_mode,
            "label": label,
            "entry": entry,
            "page": page_number,
            "age_group": age_group,
        }

    def _build_alphabet_prompt(self, entry):
        letter = entry["letter"]
        word = entry["word"]
        obj = entry["object"]
        parts = [
            "Large bold letter " + letter,
            letter + " is for " + word,
            obj + " next to the letter",
            "kids alphabet learning coloring book page",
            "clean vector-style black and white line art",
            "bold thick black outlines",
            "high contrast clean linework",
            "large traceable letter",
            "single main object",
            "centered composition",
            "large open coloring spaces",
            "simple uncluttered composition",
            "easy to color",
            "print-ready",
            "no shading",
            "no gray",
            "no gradients",
            "no color",
            "simple design",
            "moderate detail",
        ]
        return self._clean(", ".join(parts))

    def _build_numbers_prompt(self, entry):
        number = entry["number"]
        word = entry["word"]
        phrase = entry["count_phrase"]
        parts = [
            "Large bold number " + str(number),
            str(number) + " is for " + word,
            phrase + " arranged playfully on the page",
            "kids counting learning coloring book page",
            "clean vector-style black and white line art",
            "bold thick black outlines",
            "high contrast clean linework",
            "large traceable number",
            "objects clearly countable and separated",
            "centered composition",
            "large open coloring spaces",
            "simple uncluttered composition",
            "easy to color",
            "print-ready",
            "no shading",
            "no gray",
            "no gradients",
            "no color",
            "simple design",
            "moderate detail",
        ]
        return self._clean(", ".join(parts))

    def _build_colors_prompt(self, entry):
        color = entry["color"]
        obj = entry["object"]
        parts = [
            "Color learning page for " + color,
            obj,
            "the word " + color + " written in large bold letters",
            "kids color learning coloring book page",
            "clean vector-style black and white line art",
            "bold thick black outlines",
            "high contrast clean linework",
            "single main object",
            "centered composition",
            "large open coloring spaces",
            "simple uncluttered composition",
            "easy to color",
            "print-ready",
            "no shading",
            "no gray",
            "no gradients",
            "no color",
            "simple design",
            "moderate detail",
        ]
        return self._clean(", ".join(parts))

    def _build_shapes_prompt(self, entry):
        shape = entry["shape"]
        obj = entry["object"]
        parts = [
            "Shape learning page for " + shape,
            obj + " shaped like a " + shape.lower(),
            "large outline of the " + shape.lower() + " shape itself alongside the object",
            "kids shape learning coloring book page",
            "clean vector-style black and white line art",
            "bold thick black outlines",
            "high contrast clean linework",
            "single main object",
            "centered composition",
            "large open coloring spaces",
            "simple uncluttered composition",
            "easy to color",
            "print-ready",
            "no shading",
            "no gray",
            "no gradients",
            "no color",
            "simple design",
            "moderate detail",
        ]
        return self._clean(", ".join(parts))

    def _clean(self, text):
        cleaned = []
        seen = set()
        for part in text.split(", "):
            part = part.strip()
            if not part:
                continue
            key = part.lower()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(part)
        return ", ".join(cleaned)
