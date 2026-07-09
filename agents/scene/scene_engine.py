"""
==========================================================
AI Publishing OS V6
Scene Engine
==========================================================
"""

from agents.scene.scene_planner import ScenePlanner
from agents.scene.rules_engine import RulesEngine
from agents.scene.diversity_engine import DiversityEngine
from agents.content.content_provider import ContentProvider


class SceneEngine:

    def __init__(self):

        self.planner = ScenePlanner()
        self.rules = RulesEngine()
        self.diversity = DiversityEngine()
        self.content = ContentProvider()

    def build(
        self,
        niche,
        page,
        total_pages
    ):

        plan = self.planner.plan(
            page,
            total_pages
        )

        scene = self.content.build_scene(niche)

        scene["plan"] = plan

        validation = self.rules.validate(scene)

        if validation["valid"]:

            self.rules.remember(scene)

        scene["validation"] = validation

        return scene

    def report(self, scenes):

        return self.diversity.score(scenes)

    def reset(self):

        self.rules.reset()