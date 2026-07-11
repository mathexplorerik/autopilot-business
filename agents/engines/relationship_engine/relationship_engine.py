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
    

    def build(self, category, action=None):

        import random
        
        relationship = self.get_relationship(category)

        locations= random.choice(self.get_locations(category))
        background = random.choice(self.get_backgrounds(category))
        pose = random.choice(relationship.get("poses", []))
        expression = random.choice(relationship.get("expressions", []))

        return {
        "locations": locations,
        "background": background,
        "pose": pose,
        "expression": expression,
    }