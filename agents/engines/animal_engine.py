import random
from agents.data.animals.scenes import SCENES
from agents.data.animals.backgrounds import BACKGROUNDS
from agents.data.animals.actions import ACTIONS
from agents.data.animals.poses import POSES
from agents.data.animals.expressions import EXPRESSIONS
from agents.data.animals.props import PROPS
from agents.data.animals.accessories import ACCESSORIES
from agents.data.animals.scene_categories import ANIMAL_SCENE_CATEGORY
from agents.engines.relationship_engine.matrix import RELATIONSHIP_MATRIX
from agents.data.animals.action_index import ACTION_INDEX
from agents.engines.action_matcher import ActionMatcher
from agents.engines.grammar_engine import with_article
from agents.engines.relationship_engine.relationship_engine import RelationshipEngine
from agents.prompt.validator import PromptValidator
from agents.data.animals.scene_categories import ANIMAL_SCENE_CATEGORY
from agents.data.world.habitats import HABITATS
from agents.data.animals.subject_habitats import SUBJECT_HABITATS
from agents.data.animals.subject_actions import SUBJECT_ACTIONS
from agents.data.animals.subject_props import SUBJECT_PROPS
from agents.data.animals.subject_locations import SUBJECT_LOCATIONS

class AnimalEngine:


    def __init__(self):
        self._used_combos = set()
        self.relationship = RelationshipEngine()
        self.validator = PromptValidator()

    def build(self, subject, age_group="kids", page_number=1, total_pages=40, season=None):
        complexity = self._get_complexity(page_number, total_pages)
        accessories = []

        # ✅ Category
        category = self._get_category(subject, season)

        # ✅ Background
        background = self._pick(BACKGROUNDS, category, "white background")

        # ✅ Subject-specific actions
        if subject.lower() in SUBJECT_ACTIONS:
            action = random.choice(SUBJECT_ACTIONS[subject.lower()])
        else:
            action = self._pick(ACTIONS, category, "playing happily")
        
        # ✅ Action category
        action_cat = ACTION_INDEX.get(action, "daily_life")
        relationship = RELATIONSHIP_MATRIX.get(action_cat, {})

        # ✅ Relationship Engine decides everything

        decision = self.relationship.build(
        category=action_cat,
        action=action,
    )
        
        scene      = decision.get("locations", "in a garden")
        background = decision.get("background", "white background")
        prop       = decision.get("prop", "")
        pose       = decision.get("pose", "standing pose")
        expression = decision.get("expression", "happy")

        # ✅ Subject-specific locations
        if subject.lower() in SUBJECT_LOCATIONS:
            scene = random.choice(SUBJECT_LOCATIONS[subject.lower()])

        # ✅ Subject-specific props
        if subject.lower() in SUBJECT_PROPS:
            prop = random.choice(SUBJECT_PROPS[subject.lower()])

        # ✅ Habitat — agar subject ka known habitat hai, to usse background override karo
        habitat_key = SUBJECT_HABITATS.get(subject.lower())
        if habitat_key and habitat_key in HABITATS:
            background = random.choice(HABITATS[habitat_key])

        positive = self._build_positive_prompt(
            subject=subject,
            scene=scene,
            background=background,
            action=action,
            pose=pose,
            expression=expression,
            props=[prop] if prop else [],
            accessories=[],
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
            "props": [prop] if prop else [],
            "accessories": accessories,
            "subject":     subject,
            "age_group":   age_group
        }
    

    def _format_subject(self, subject, age_group):

            if age_group == "toddler":
                return f"Adorable baby {subject}"

            elif age_group == "kids":
                return f"Cute baby {subject}"

            elif age_group == "teens":
                return f"Young {subject}"

            return subject
    

    def _build_positive_prompt(self, subject, scene, background, action, pose, expression, props, accessories, age_group, complexity):
        subject = self._format_subject(subject, age_group)

        age_styles = {
            "toddler": "very simple design, minimal details",
            "kids":    "simple design, moderate detail",
            "teens":   "detailed design, intricate details",
        }

        complexity_styles = {
            "simple":       "2-3 large elements",
            "intermediate": "4-5 elements, balanced composition",
            "advanced":     "6-8 detailed elements",
            "pro":          "highly detailed coloring page with many interesting objects",
        }

        parts = [

            subject,
            action,
        ]    


        if scene:
            parts.append(f"at {with_article(scene)}")


        if background:
            parts.append(f"surrounded by {background}")

        if pose:
            parts.append(f"in a {pose} pose")

        if expression:
            parts.append(f"with {with_article(expression)} facial expression")
        

        if props:
            parts.append("holding " + ", ".join(props))

        if accessories:
            parts.append("wearing " + ", ".join(accessories))

        parts.extend([

            "professional children's coloring book illustration",

            "clean vector-style black and white line art",

            "bold thick black outlines",

            "high contrast clean linework",

            "single character",

            "full body visible",

            "centered composition",

            "large open coloring spaces",

            "simple uncluttered composition",

            "easy to color",

            "print-ready",

            "no shading",

            "no gray",

            "no gradients",

            "no color",
                
            age_styles.get(age_group, age_styles["kids"]),
            complexity_styles.get(complexity, complexity_styles["simple"]),
        ])
        
        parts = self.validator.validate(parts)
        return self._clean_prompt(parts)
    
    def _clean_prompt(self, parts):

        cleaned = []
        seen = set()

        for part in parts:

            if not part:
                continue

            part = part.strip()

            if not part:
                continue

            key = part.lower()

            if key in seen:
                continue

            seen.add(key)
            cleaned.append(part)

        return ", ".join(cleaned)


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

    
    def _pick(self, data_dict, category, fallback=""):

        if category in data_dict:
            pool = data_dict[category]
        elif "nature" in data_dict:
            pool = data_dict["nature"]
        elif "default" in data_dict:
            pool = data_dict["default"]
        else:
            return fallback

        available = [
            item for item in pool
            if item not in self._used_combos
        ]

        if not available:
            self._used_combos.clear()
            available = pool

        choice = random.choice(available)

        self._used_combos.add(choice)

        return choice
    
    
    def _pick_list(self, data_dict, category, count=1):

        
        if category in data_dict:
            pool = data_dict[category]
        elif "default" in data_dict:
            pool = data_dict["default"]
        else:
            return []

        available = [
            item for item in pool
            if item not in self._used_combos
        ]

        if len(available) < count:
            self._used_combos.clear()
            available = pool

        count = min(count, len(available))

        selected = random.sample(available, count)

        self._used_combos.update(selected)

        return selected
    
    def _get_complexity(self, page, total):
        ratio = page / total
        if ratio <= 0.25:   return "simple"
        elif ratio <= 0.50: return "intermediate"
        elif ratio <= 0.75: return "advanced"
        return "pro"