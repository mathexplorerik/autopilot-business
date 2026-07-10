"""
AI Publishing OS V8
Prompt Engine
"""

from __future__ import annotations
from typing import Dict, List

from agents.prompt.prompt_builder import PromptBuilder
from agents.prompt.prompt_formatter import PromptFormatter
from agents.prompt.prompt_scorer import PromptScorer
from agents.prompt.prompt_reporter import PromptReporter
from agents.prompt.prompt_templates import PromptTemplates

class PromptEngineV8:

    VERSION = "8.0.0"

    def __init__(self):

        self.builder = PromptBuilder()

        self.formatter = PromptFormatter()

        self.scorer = PromptScorer()

        self.reporter = PromptReporter()

        self.templates = PromptTemplates()

    # --------------------------------------------------

    def build(
        self,
        scene: Dict,
        style: str = "coloring_book",
        line_weight: str = "bold",
        marketplace: str = "amazon",
        product: str = "coloring_book",
    ) -> Dict:

        template = self.templates.get(
            marketplace=marketplace,
            product=product,
        )

        return self.builder.build(
            scene=scene,
            style=style,
            line_weight=line_weight,
            age_style=scene["age_group"],
            complexity=scene["complexity"],
            template=template,
        )
    
    # --------------------------------------------------

    def score(
        self,
        prompt: Dict,
    ) -> Dict:

        result = self.scorer.score(
            {
                "positive": prompt["positive"],
            }
        )

        prompt["score"] = result["score"]

        prompt["grade"] = self.scorer.grade(
            result["score"]
        )

        return prompt
    
    # --------------------------------------------------

    def metadata(
        self,
        prompt: Dict,
        marketplace: str = "amazon",
        product: str = "coloring_book",
    ) -> Dict:

        prompt["metadata"] = self.formatter.format_metadata(
            prompt_score=prompt["score"],
            marketplace=marketplace,
            product_type=product,
        )

        return prompt
    
    
    # --------------------------------------------------

    def format(
        self,
        page: int,
        keyword: str,
        subject: str,
        prompt: Dict,
    ) -> Dict:

        return self.formatter.format(

            page=page,

            subject=subject,

            niche=keyword,

            positive=prompt["positive"],

            negative=prompt["negative"],

            complexity=prompt["complexity"],

            label=prompt["complexity"].upper(),

            metadata=prompt["metadata"],
        )
    
    # --------------------------------------------------

    def build_final(
        self,
        page: int,
        keyword: str,
        subject: str,
        scene: Dict,
        style: str = "coloring_book",
        line_weight: str = "bold",
        marketplace: str = "amazon",
        product: str = "coloring_book",
    ) -> Dict:

        prompt = self.build(
            scene=scene,
            style=style,
            line_weight=line_weight,
            marketplace=marketplace,
            product=product,
        )

        prompt["complexity"] = scene["complexity"]

        prompt = self.score(prompt)

        prompt = self.metadata(
            prompt,
            marketplace,
            product,
        )

        return self.format(
            page=page,
            keyword=keyword,
            subject=subject,
            prompt=prompt,
        )
    
    # --------------------------------------------------

    def health(self) -> Dict:
        """
        Engine health information.
        """

        return {

            "healthy": True,

            "engine": "PromptEngineV8",

            "version": self.VERSION,

            "builder": self.builder.__class__.__name__,

            "formatter": self.formatter.__class__.__name__,

            "scorer": self.scorer.__class__.__name__,

            "reporter": self.reporter.__class__.__name__,
        }
    
    # --------------------------------------------------

    def statistics(
        self,
        prompts: List[Dict],
    ) -> Dict:
        """
        Prompt statistics.
        """

        if not prompts:

            return {
                "total": 0,
                "average_score": 0,
                "highest_score": 0,
                "lowest_score": 0,
            }

        scores = [
            p["metadata"]["prompt_score"]
            for p in prompts
        ]

        return {

            "total": len(prompts),

            "average_score": round(
                sum(scores) / len(scores),
                2,
            ),

            "highest_score": max(scores),

            "lowest_score": min(scores),
        }