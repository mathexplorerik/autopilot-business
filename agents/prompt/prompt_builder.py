"""
==========================================================
AI Publishing OS V6
Prompt Builder
==========================================================
"""

from typing import Dict


class SafeDict(dict):
    """
    Prevent KeyError for missing template variables.
    """

    def __missing__(self, key):
        return ""


class PromptBuilder:
    """
    Builds AI prompts from structured scene data.

    Responsibilities
    ----------------
    ✓ Build Positive Prompt
    ✓ Build Negative Prompt

    Does NOT
    --------
    ✗ Generate Scenes
    ✗ Validate Data
    ✗ Save Files
    ✗ Report Progress
    """

    DEFAULT_NEGATIVE = (
        "color, grayscale, shading, gradient, shadow, blur, "
        "watermark, logo, signature, text, caption, frame, "
        "photorealistic, realistic skin, painting, oil painting, "
        "3d render, low quality, low resolution"
    )

    def _clean(self, text: str) -> str:
        """
        Clean generated prompt.
        """

        return (
            " ".join(text.split())
            .replace(" ,", ",")
            .replace(" .", ".")
            .replace(" ,.", ".")
            .strip()
        )

    def build(
        self,
        scene: Dict,
        style: str,
        line_weight: str,
        age_style: str,
        complexity: str,
        template: str,
    ) -> Dict:

        data = SafeDict(
            {
                **scene,

                "props": ", ".join(scene.get("props", [])),
                "accessories": ", ".join(scene.get("accessories", [])),

                "style": style,
                "line_weight": line_weight,
                "age_style": age_style,
                "complexity": complexity,
            }
        )

        positive = template.format_map(data)

        extra_parts = []

        for key in [
            "camera",
            "lighting",
            "composition",
            "framing",
            "view",
            "weather",
            "season",
            "time_of_day",
            "mood",
            "emotion",
            "color_palette",
        ]:
            value = scene.get(key)

            if value:
                extra_parts.append(str(value))

        if extra_parts:
            positive += ", " + ", ".join(extra_parts)

        positive = self._clean(positive)

        return {
            "positive": positive,
            "negative": self.build_negative(scene),
        }

    def build_positive(
        self,
        scene: Dict,
        style: str,
        line_weight: str,
        age_style: str,
        complexity: str,
        template: str,
    ) -> str:

        return self.build(
            scene,
            style,
            line_weight,
            age_style,
            complexity,
            template,
        )["positive"]

    def build_negative(self, scene: Dict = None) -> str:
        """
        Build dynamic negative prompt.
        """

        negative = [self.DEFAULT_NEGATIVE]

        if scene:
            extra_negative = scene.get("negative", [])

            if isinstance(extra_negative, list):
                negative.extend(extra_negative)

            elif isinstance(extra_negative, str):
                negative.append(extra_negative)

        return ", ".join(filter(None, negative))