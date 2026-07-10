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

    ACTION_TO_POSE = {
        "movement":    ["walking", "running", "jumping", "standing"],
        "play":        ["running", "jumping", "dancing"],
        "adventure":   ["walking", "climbing", "standing"],
        "nature":      ["walking", "sitting", "resting"],
        "creative":    ["sitting", "standing"],
        "daily_life":  ["standing", "walking", "sitting"],
        "learning":    ["sitting", "standing"],
        "celebration": ["jumping", "dancing", "standing"],
        "sports":      ["running", "jumping"],
        "fantasy":     ["walking", "flying", "standing"],
    }

    ACTION_TO_EXPRESSION = {
        "movement":    ["happy", "excited"],
        "play":        ["playful", "silly", "excited"],
        "adventure":   ["curious", "brave", "excited"],
        "nature":      ["calm", "curious", "thoughtful"],
        "creative":    ["happy", "thoughtful", "proud"],
        "daily_life":  ["happy", "calm"],
        "learning":    ["curious", "thoughtful", "proud"],
        "celebration": ["excited", "happy", "proud"],
        "sports":      ["excited", "proud"],
        "fantasy":     ["surprised", "curious", "excited"],
    }

    def __init__(self):
        self._used_combos = set()

    def build(self, subject, age_group="kids", page_number=1, total_pages=40, season=None):

        # ✅ Category
        category = self._get_category(subject, season)

        # ✅ Scene
        scene = self._pick(SCENES, category, "in a beautiful garden")

        # ✅ Background
        background = self._pick(BACKGROUNDS, category, "white background")

        # ✅ Action
        action = self._pick(ACTIONS, category, "playing happily")

        # ✅ Action category
        action_cat = self._get_action_category(action)

        # ✅ Pose — action se match karo
        pose_options = self.ACTION_TO_POSE.get(action_cat, ["standing pose"])
        pose = random.choice(pose_options)

        # ✅ Expression — action se match karo
        expr_options = self.ACTION_TO_EXPRESSION.get(action_cat, ["happy"])
        expression = random.choice(expr_options)

        # ✅ Props
        props = self._pick_list(PROPS, category, count=1)

        # ✅ Accessories
        accessories = self._pick_list(ACCESSORIES, category, count=1)

        # ✅ Complexity
        complexity = self._get_complexity(page_number, total_pages)

        # ✅ Build positive prompt
        positive = self._build_positive_prompt(
            subject=subject,
            scene=scene,
            background=background,
            action=action,
            pose=pose,
            expression=expression,
            props=props,
            accessories=accessories,
            age_group=age_group,
            complexity=complexity
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

    def _build_positive_prompt(self, subject, scene, background, action, pose, expression, props, accessories, age_group, complexity):

        age_styles = {
            "toddler": "very simple, extra thick outlines, minimal details",
            "kids":    "simple design, thick outlines, large coloring spaces",
            "teens":   "detailed design, clean outlines, intricate details",
        }

        complexity_styles = {
            "simple":       "2-3 large elements, huge coloring spaces",
            "intermediate": "4-5 elements, balanced composition",
            "advanced":     "6-8 detailed elements",
            "pro":          "highly detailed coloring page with many interesting objects",
        }

        parts = [
            f"Cute {expression} {subject}",
            action,
            scene,
            background,
            pose,
        ]

        if props:
            parts.append(", ".join(props))

        if accessories:
            parts.append(", ".join(accessories))

        parts.extend([
            "kids coloring book page",
            "black and white line art",
            "bold clean outlines",
            "no shading",
            "no gray",
            "white background",
            "centered composition",
            "print ready",
            age_styles.get(age_group, age_styles["kids"]),
            complexity_styles.get(complexity, complexity_styles["simple"]),
        ])

        return ", ".join(parts)

    def _get_category(self, subject, season=None):
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

    def _get_action_category(self, action):
        action_lower = action.lower()
        if any(w in action_lower for w in ["walk", "run", "jump", "climb"]):
            return "movement"
        if any(w in action_lower for w in ["play", "dance", "swing"]):
            return "play"
        if any(w in action_lower for w in ["explore", "discover", "adventure"]):
            return "adventure"
        if any(w in action_lower for w in ["garden", "flower", "plant", "nature"]):
            return "nature"
        if any(w in action_lower for w in ["paint", "draw", "craft", "create"]):
            return "creative"
        if any(w in action_lower for w in ["eat", "cook", "sleep", "read"]):
            return "daily_life"
        if any(w in action_lower for w in ["learn", "study", "school"]):
            return "learning"
        if any(w in action_lower for w in ["celebrat", "birthday", "party"]):
            return "celebration"
        if any(w in action_lower for w in ["sport", "football", "swim"]):
            return "sports"
        return "daily_life"

    def _pick(self, data_dict, category, fallback=""):
        if category in data_dict:
            return random.choice(data_dict[category])
        if "nature" in data_dict:
            return random.choice(data_dict["nature"])
        if "default" in data_dict:
            return random.choice(data_dict["default"])
        return fallback

    def _pick_list(self, data_dict, category, count=1):
        if category in data_dict:
            pool = data_dict[category]
        elif "default" in data_dict:
            pool = data_dict["default"]
        else:
            return []
        count = min(count, len(pool))
        return random.sample(pool, count)

    def _get_complexity(self, page, total):
        ratio = page / total
        if ratio <= 0.25:   return "simple"
        elif ratio <= 0.50: return "intermediate"
        elif ratio <= 0.75: return "advanced"
        return "pro"