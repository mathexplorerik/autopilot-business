"""
==========================================================
AI Publishing OS V5
Content Provider
==========================================================
"""

from agents.content.providers.subject_provider import SubjectProvider
from agents.content.providers.action_provider import ActionProvider
from agents.content.providers.background_provider import BackgroundProvider
from agents.content.providers.prop_provider import PropProvider
from agents.content.providers.accessory_provider import AccessoryProvider
from agents.content.providers.scene_provider import SceneProvider


class ContentProvider:

    def __init__(self):

        self.subjects = SubjectProvider()
        self.actions = ActionProvider()
        self.backgrounds = BackgroundProvider()
        self.props = PropProvider()
        self.accessories = AccessoryProvider()
        self.scenes = SceneProvider()

    def get_subjects(self, niche):

        return self.subjects.get(niche)

    def get_actions(self, niche):

        return self.actions.get(niche)

    def get_backgrounds(self, niche):

        return self.backgrounds.get(niche)

    def get_props(self, niche):

        return self.props.get(niche)

    def get_accessories(self, niche):

        return self.accessories.get(niche)

    def build_scene(self, niche):

        return self.scenes.build(niche)