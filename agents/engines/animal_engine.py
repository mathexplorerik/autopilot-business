from data.animals.scenes import SCENES


class AnimalEngine:
    """
    Animal Engine V2 Foundation

    Responsibilities:
    - Select Scene
    - Select Background
    - Select Action
    - Select Pose
    - Select Expression
    - Select Props
    - Select Accessories
    - Build Prompt
    """

    def __init__(self):

        self.scene = None
        self.background = None
        self.action = None
        self.pose = None
        self.expression = None

        self.props = []
        self.accessories = []

    def build(
        self,
        subject,
        age_group,
        page_number,
        total_pages,
        season=None,
    ):

        self.scene = self.select_scene(subject, season)
        print(f"[AnimalEngine] Selected Scene: {self.scene}")
        self.background = self.select_background(subject)
        self.action = self.select_action(subject)
        self.pose = self.select_pose(subject)
        self.expression = self.select_expression(subject)
        self.props = self.select_props(subject)
        self.accessories = self.select_accessories(subject)

        positive = (
            f"{subject}, cute cartoon animal, kids coloring book page, "
            "bold clean outlines, black and white line art, "
            "simple background, centered composition, "
            "no shading, printable, white background"
        )

        negative = (
            "color, grayscale, realistic, photo, text, watermark, "
            "logo, blurry, low quality, extra limbs"
        )

        return {
            "positive": positive,
            "negative": negative,
            "complexity": self.get_complexity(page_number, total_pages),
        }
    def get_scene_category(self, subject, season=None):
        """
        Returns the scene category.
        Temporary version.
        """

        return "nature"

    def select_scene(self, subject, season=None):
        """
        Select one scene from the selected category.
        """

        category = self.get_scene_category(subject, season)

        return SCENES[category][0]
    
    def select_background(self, subject):
        return None

    def select_action(self, subject):
        return None

    def select_pose(self, subject):
        return None

    def select_expression(self, subject):
        return None

    def select_props(self, subject):
        return []

    def select_accessories(self, subject):
        return []

    def get_complexity(self, page, total):

        ratio = page / total

        if ratio <= 0.25:
            return "simple"

        elif ratio <= 0.50:
            return "intermediate"

        elif ratio <= 0.75:
            return "advanced"

        return "pro"