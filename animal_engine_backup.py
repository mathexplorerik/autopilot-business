import random
from agents.data.animals.scenes import SCENES
from agents.data.animals.backgrounds import BACKGROUNDS
from agents.data.animals.actions import ACTIONS
from agents.data.animals.poses import POSES
from agents.data.animals.expressions import EXPRESSIONS
from agents.data.animals.props import PROPS
from agents.data.animals.accessories import ACCESSORIES
from agents.data.animals.scene_categories import ANIMAL_SCENE_CATEGORY

class AnimalEngine:

    def __init__(self):
        self._used_combos = set()

    def build(self, subject, age_group="kids", page_number=1, total_pages=40, season=None):

        # ✅ Scene
        category   = self._get_category(subject, season)
        scene      = self._pick(SCENES, category, "in a beautiful garden")

        # ✅ Background
        background = self._pick(BACKGROUNDS, category, "white background")

        # ✅ Action
        action_category, action = self._pick_action()

        # ✅ Pose
        pose = self._pick_pose(action_category)

        # ✅ Expression
        expression = self._pick_expression(action_category)

        # ✅ Props
        props = self._pick_prop(category)

        # ✅ Accessories
        accessories = []
        if self._random.random() < 0.40:
            accessories = self._pick_list(ACCESSORIES, category, 1)
            
        # ✅ Complexity
        complexity = self._get_complexity(page_number, total_pages)

        # ✅ Age style
        age_styles = {
            "toddler": "very simple, extra thick lines, minimal details",
            "kids":    "simple design, thick outlines, large coloring spaces",
            "teens":   "detailed design, medium lines, intricate patterns"
        }
        age_detail = age_styles.get(age_group, age_styles["kids"])

        # ✅ Complexity detail
        complexity_details = {
            "simple":       "2-3 elements only, extra large spaces, very easy",
            "intermediate": "4-5 elements, large spaces, easy to color",
            "advanced":     "6-8 elements, medium spaces, some details",
            "pro":          "9-12 elements, intricate details, complex scene"
        }
        complexity_detail = complexity_details.get(complexity, "simple")

        # ✅ Props + Accessories string
        props_str = f", {', '.join(props)}" if props else ""
        acc_str   = f", {', '.join(accessories)}" if accessories else ""

        # ✅ Build positive prompt
        positive = (
            f"Cute {expression} {subject} {action} {scene} {background}, "
            f"{pose}{props_str}{acc_str}, "
            f"kids coloring book page, "
            f"bold clean outlines, black and white line art, "
            f"no shading, white background, "
            f"centered composition, printable, "
            f"{age_detail}, "
            f"{complexity_detail}"
        )

        # ✅ Negative prompt
        negative = (
            "color fills, shading, gradients, gray areas, "
            "realistic, photo, watermark, text, signature, "
            "blurry, low quality, extra limbs, deformed"
        )


        return {
            "positive":    positive,
            "negative":    negative,
            "complexity":  complexity,
            "scene":       scene,
            "background":  background,
            "action":      action,
            "pose":        pose,
            "expression":  expression,
            "props":       props,
            "accessories": accessories,
            "subject":     subject,
            "age_group":   age_group
        }

    def _get_category(self, subject, season=None):
        """Subject ka category lo"""
        if season:
            season_map = {
                "christmas": "winter",
                "halloween": "spooky",
                "easter":    "spring",
                "diwali":    "festival",
                "holi":      "festival",
                "eid":       "festival"
            }
            if season.lower() in season_map:
                return season_map[season.lower()]

        return ANIMAL_SCENE_CATEGORY.get(subject.lower(), "nature")

    def _pick(self, data_dict, category, fallback=""):
        """Category se random item lo"""
        if category in data_dict:
            return random.choice(data_dict[category])
        if "nature" in data_dict:
            return random.choice(data_dict["nature"])
        if "default" in data_dict:
            return random.choice(data_dict["default"])
        return fallback

    def _pick_list(self, data_dict, category, count=1):
        """Category se random list lo"""
        items = []
        if category in data_dict:
            pool = data_dict[category]
        elif "default" in data_dict:
            pool = data_dict["default"]
        else:
            return []

        count = min(count, len(pool))
        return random.sample(pool, count)

    def _get_complexity(self, page, total):
        """Page number se complexity decide karo"""
        ratio = page / total
        if ratio <= 0.25:
            return "simple"
        elif ratio <= 0.50:
            return "intermediate"
        elif ratio <= 0.75:
            return "advanced"
        return "pro"
    
        def _pick_action(self):
            category = self._random.choice(list(ACTIONS.keys()))
            action = self._random.choice(ACTIONS[category])
            return category, action

    def _pick_pose(self, action_category):
        pose_groups = self.ACTION_TO_POSE.get(
            action_category,
            ["standing"],
        )

        pose_group = self._random.choice(pose_groups)

        pose_pool = POSES.get(
            pose_group,
            POSES["standing"],
        )

        return self._random.choice(pose_pool)

    def _pick_expression(self, action_category):
        expression_groups = self.ACTION_TO_EXPRESSION.get(
            action_category,
            ["happy"],
        )

        expression_group = self._random.choice(
            expression_groups
        )

        expression_pool = EXPRESSIONS.get(
            expression_group,
            EXPRESSIONS["happy"],
        )

        return self._random.choice(expression_pool)

    def _pick_prop(self, category):
        props = self._pick_list(PROPS, category, 1)

        if props:
            return props

        props = self._pick_list(PROPS, "default", 1)

        if props:
            return props

        return ["small flower"]