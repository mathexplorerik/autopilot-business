"""
==========================================================
AI KDP AUTOPILOT V9
Relationship Engine
==========================================================
"""
import random
from agents.engines.relationship_engine.matrix import RELATIONSHIP_MATRIX
from agents.engines.relationship_engine.matcher import Matcher
from agents.engines.relationship_engine.compatibility import Compatibility
from agents.data.world.locations import LOCATIONS
from agents.data.world.backgrounds import BACKGROUNDS
from agents.data.world.props import PROPS
from agents.engines.action_matcher import ActionMatcher
from agents.engines.relationship_engine.scorer import Scorer


class RelationshipEngine:
    """
    Central decision engine.
    Future responsibilities:
    - Action Selection
    - locations Selection
    - Background Matching
    - Pose Matching
    - Expression Matching
    - Prop Matching
    - Accessory Matching
    """

    def __init__(self):
        self.matcher = Matcher()
        self.compatibility = Compatibility()
        self.scorer = Scorer()

    def get_relationship(self, category):
        data = RELATIONSHIP_MATRIX.get(category)
        if not data:
            data = RELATIONSHIP_MATRIX["daily_life"]
        return data

    def get_locations(self, category):
        return LOCATIONS.get(category, LOCATIONS.get("daily_life", []))

    def get_poses(self, category):
        return self.get_relationship(category).get("poses", [])

    def get_expressions(self, category):
        return self.get_relationship(category).get("expressions", [])

    def get_backgrounds(self, category):
        return BACKGROUNDS.get(category, BACKGROUNDS.get("daily_life", []))

    def get_props(self, category):
        return PROPS.get(category, PROPS.get("daily_life", []))

    def best_match(self, candidates, keywords=None):

        if not candidates:
            return None

        if not keywords:
            return random.choice(candidates)

        best = None
        best_score = -1

        for item in candidates:
            score = self.scorer.score(item, keywords)

            if score > best_score:
                best_score = score
                best = item

        return best

    def build(self, category, action=None):

        relationship = self.get_relationship(category)
        match = ActionMatcher.detect(action) if action else None

        locations = random.choice(self.get_locations(category))

        if match and match.get("backgrounds"):
            background = self.best_match(match["backgrounds"], match["keywords"])
        else:
            candidates = self.get_backgrounds(category)
            valid = [bg for bg in candidates if self.compatibility.is_valid(action or "", bg)]
            background = random.choice(valid) if valid else random.choice(candidates)

        prop_keywords = match.get("keywords") if match else None
        prop = self.best_match(self.get_props(category), prop_keywords)

        pose = random.choice(relationship.get("poses", []))
        expression = random.choice(relationship.get("expressions", []))

        return {
            "locations": locations,
            "background": background,
            "prop": prop,
            "pose": pose,
            "expression": expression,
        }