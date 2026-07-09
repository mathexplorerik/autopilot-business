"""
==========================================================
AI Publishing OS V6
Prompt Formatter
==========================================================
"""

from datetime import datetime
from typing import Dict


class PromptFormatter:
    """
    Responsible ONLY for formatting prompt output.

    Responsibilities
    ----------------
    ✓ Standard Prompt Format
    ✓ Metadata Formatting
    ✓ Export-ready Structure

    Does NOT
    ----------
    ✗ Generate Prompt
    ✗ Save Files
    ✗ Validate
    ✗ Score
    """

    VERSION = "V6"

    def format(
        self,
        page: int,
        subject: str,
        niche: str,
        positive: str,
        negative: str,
        complexity: str,
        label: str,
        metadata: Dict | None = None
    ) -> Dict:

        return {

            "page": page,

            "subject": subject,

            "niche": niche,

            "positive": positive,

            "negative": negative,

            "complexity": complexity,

            "label": label,

            "metadata": metadata or {},

            "version": self.VERSION,

            "generated_at": datetime.now().isoformat()

        }

    def format_metadata(
        self,
        scene_score: float = 100,
        prompt_score: float = 100,
        diversity_score: float = 100,
        marketplace: str = "Amazon KDP",
        generator: str = "Gemini",
        product_type: str = "Coloring Book"
    ) -> Dict:

        return {

            "scene_score": scene_score,

            "prompt_score": prompt_score,

            "diversity_score": diversity_score,

            "marketplace": marketplace,

            "generator": generator,

            "product_type": product_type

        }

    def summary(self, prompt: Dict) -> str:

        return (
            f"[Page {prompt['page']:02}] "
            f"{prompt['subject']} | "
            f"{prompt['complexity']} | "
            f"{prompt['label']}"
        )