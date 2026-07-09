"""
==========================================================
AI Publishing OS V6
Prompt Agent — Thin Wrapper
==========================================================
"""
from agents.prompt.prompt_engine import PromptEngine


class PromptAgent:
    """
    V6 — Thin wrapper around PromptEngine.

    ✓ Receive Research Report
    ✓ Call PromptEngine
    ✓ Return Prompt Batch
    """

    def __init__(self):
        self.engine = PromptEngine()

    def generate(self, report, season=None):
        print("\n✍️  Prompt Agent V6 Running...\n")

        # ✅ ResearchReport object ya dict
        if hasattr(report, 'resolved_niche'):
            niche     = report.resolved_niche.lower()
            pages     = report.pages
            age_group = report.age_group
            season    = season or getattr(report, 'season', None) or ""
        else:
            niche     = report.get("niche", "animals").lower()
            pages     = report.get("pages", 40)
            age_group = report.get("age_group", "kids")
            season    = season or ""

        # ✅ Build batch
        batch = self.engine.build_batch(
            niche=niche,
            pages=pages,
            style="cute cartoon line art",
            line_weight="bold clean outlines",
            age_style=age_group,
            marketplace="amazon",
            product="coloring"
        )

        # ✅ Save
        self.engine.save_batch(
            prompts=batch["prompts"],
            niche=niche,
            age_group=age_group,
            season=season
        )

        print(f"\n  ✅ V6 Complete : {batch['total']} prompts")
        return [p["positive"] for p in batch["prompts"]]