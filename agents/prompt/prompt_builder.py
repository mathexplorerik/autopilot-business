"""
==========================================================
AI Publishing OS V6
Prompt Builder
==========================================================
"""

from typing import Dict


class PromptBuilder:
    """
    Builds AI prompts from structured scene data.

    Responsibilities:
    -----------------
    ✓ Build Positive Prompt
    ✓ Build Negative Prompt

    Does NOT:
    ----------
    ✗ Validate
    ✗ Save
    ✗ Report
    ✗ Check Duplicates
    ✗ Generate Scene
    """

    DEFAULT_NEGATIVE = (
        "color, grayscale, shading, gradient, shadow, blur, "
        "watermark, logo, signature, text, caption, frame, "
        "photorealistic, realistic skin, painting, oil painting, "
        "3d render, low quality, low resolution"
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

        positive = template.format(

            subject=scene.get("subject", ""),

            action=scene.get("action", ""),

            expression=scene.get("expression", ""),

            background=scene.get("background", ""),

            props=", ".join(scene.get("props", [])),

            accessories=", ".join(
                scene.get("accessories", [])
            ),

            style=style,

            line_weight=line_weight,

            age_style=age_style,

            complexity=complexity,
        )

        return {
            "positive": " ".join(
                positive.split()
            ).strip(),

            "negative": self.DEFAULT_NEGATIVE,
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

    def build_negative(self) -> str:

        return self.DEFAULT_NEGATIVE