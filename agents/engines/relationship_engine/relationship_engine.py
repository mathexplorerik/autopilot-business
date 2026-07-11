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

    def get_relationship(self, category):

        data = RELATIONSHIP_MATRIX.get(category)

        if not data:
            data = RELATIONSHIP_MATRIX["daily_life"]

        return data

    def get_locations(self, category):
        return LOCATIONS.get(category, [])

    def get_poses(self, category):
        return self.get_relationship(category).get("poses", [])

    def get_expressions(self, category):
        return self.get_relationship(category).get("expressions", [])
    
    def get_backgrounds(self, category):
        return BACKGROUNDS.get(category, [])
    
    def get_props(self, category):
        return PROPS.get(category, [])
    
    def best_match(self, candidates, keywords):

        if not candidates:
            return None

        best = None
        best_score = -1

        for item in candidates:

            score = self.scorer.score(item, keywords)

        if score > best_score:
            best_score = score
            best = item

        return best
    

    def build(self, category, action=None):

        import random
        
        relationship = self.get_relationship(category)
        match = ActionMatcher.detect(action) if action else None

        locations= random.choice(self.get_locations(category))

        if match and match.get("backgrounds"):
            print("Using ActionMatcher backgrounds")
            background = random.choice(match["backgrounds"],match["keywords"])
        else:
            background = random.choice(self.get_backgrounds(category))

        prop = random.choice(self.get_props(category))
        pose = random.choice(relationship.get("poses", []))
        expression = random.choice(relationship.get("expressions", []))
        

        return {
        "locations": locations,
        "background": background,
        "prop": prop,
        "pose": pose,
        "expression": expression,
    }