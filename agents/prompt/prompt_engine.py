"""
==========================================================
AI Publishing OS V6
Prompt Engine
AI Orchestrator
==========================================================
"""

from agents.scene import SceneEngine

from agents.prompt import (
    PromptBuilder,
    PromptFormatter,
    PromptScorer,
    PromptReporter,
    PromptSaver,
    PromptTemplates,
)

from agents.checkers.duplicate_engine import DuplicateEngine


class PromptEngine:
    """
    AI Prompt Orchestrator

    Responsibilities
    ----------------
    ✓ Coordinate AI modules
    ✓ Generate prompt
    ✓ Score prompt
    ✓ Format output
    ✓ Save batch
    ✓ Report statistics

    Does NOT
    ----------
    ✗ Build scene
    ✗ Store content
    ✗ Validate research
    """

    VERSION = "V6"

    def __init__(self):

        # AI Engines

        self.scene_engine = SceneEngine()

        # Prompt Modules

        self.builder = PromptBuilder()

        self.formatter = PromptFormatter()

        self.scorer = PromptScorer()

        self.templates = PromptTemplates()

        self.reporter = PromptReporter()

        self.saver = PromptSaver()

        # Duplicate

        self.duplicate = DuplicateEngine()

        def build_batch(
            self,
            niche: str,
            pages: int,
            style: str,
            line_weight: str,
            age_style: str,
            marketplace: str = "amazon",
            product: str = "coloring",
        ):
            """
            Generate a complete prompt batch.
            """

            prompts = []

            for page in range(1, pages + 1):

                prompt = self.build_prompt(
                    niche=niche,
                    page=page,
                    total_pages=pages,
                    style=style,
                    line_weight=line_weight,
                    age_style=age_style,
                    marketplace=marketplace,
                    product=product,
                )

                 # -----------------------------
                 # Duplicate Check
                 # -----------------------------

                duplicate = self.duplicate.validate(
                prompt=prompt["positive"],
                subject=prompt["subject"],
                )

                if not duplicate["valid"]:
                    continue

                self.duplicate.add(
                    prompt=prompt["positive"],
                    subject=prompt["subject"],
                )

                prompts.append(prompt)

            # -----------------------------
            # Report
            # -----------------------------

            report = self.reporter.report(prompts)

            return {

                "prompts": prompts,

                "report": report,

                "total": len(prompts),

                "version": self.VERSION,

            }   
        def save_batch(
            self,
            prompts,
            niche,
            age_group,
            season=""
        ):
            """
            Save prompt batch.
            """

            return self.saver.save(
            prompts=prompts,
            niche=niche,
            age_group=age_group,
            season=season,
        )