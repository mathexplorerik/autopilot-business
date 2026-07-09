"""
==========================================================
AI Publishing OS V5
Scene Provider
==========================================================
"""

import random

from agents.content.providers.subject_provider import SubjectProvider
from agents.content.providers.action_provider import ActionProvider
from agents.content.providers.background_provider import BackgroundProvider
from agents.content.providers.prop_provider import PropProvider
from agents.content.providers.accessory_provider import AccessoryProvider


class SceneProvider:

    def __init__(self):

        self.subjects = SubjectProvider()
        self.actions = ActionProvider()
        self.backgrounds = BackgroundProvider()
        self.props = PropProvider()
        self.accessories = AccessoryProvider()

    def build(self, niche):

        subjects = self.subjects.get(niche)

        return {

            "subject": random.choice(subjects),

            "action": random.choice(
                self.actions.get(niche)
            ),

            "background": random.choice(
                self.backgrounds.get(niche)
            ),

            "prop": random.choice(
                self.props.get(niche)
            ),

            "accessory": random.choice(
                self.accessories.get(niche)
            )

        }