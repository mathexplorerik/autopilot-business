import random
from agents.data.categories import get_engine
from agents.engines.animal_engine import AnimalEngine

class PromptEngine:
    def __init__(self):
        self.actions = [
            "smiling", "running", "jumping", "holding balloons",
            "wearing a party hat", "playing football", "reading a book",
            "sleeping", "painting", "camping", "flying a kite",
            "playing in the rain", "drinking water", "playing guitar",
            "playing piano", "gardening", "watering flowers",
            "baking cookies", "making pizza", "playing with a puppy",
            "playing with kittens", "riding a bicycle", "riding a scooter",
            "ice skating", "building a snowman", "surfing", "swimming",
            "fishing", "having a picnic", "exploring the jungle",
            "exploring space", "being an astronaut", "being a firefighter",
            "being a police officer", "being a doctor", "being a chef",
            "being a pirate", "being a superhero", "celebrating a birthday",
            "opening presents", "playing with butterflies", "playing with birds",
            "looking at stars", "walking in the forest", "walking on the beach",
            "playing in autumn leaves", "decorating a Christmas tree",
            "collecting flowers", "feeding ducks", "building a sandcastle"
        ]
        self.backgrounds = [
            "at the park", "at the beach", "in the jungle", "in the forest",
            "in space", "on a farm", "at school", "at home",
            "in the mountains", "near a rainbow", "in a flower garden",
            "at the zoo", "at a birthday party", "during winter",
            "during summer", "near a waterfall", "under the stars",
            "near a castle", "in a magical garden", "at the playground"
        ]
        self.expressions = [
            "happy", "excited", "sleepy", "surprised", "curious",
            "laughing", "shy", "brave", "proud", "silly",
            "cheerful", "amazed"
        ]
        self.props = [
            "holding an ice cream cone", "carrying a teddy bear",
            "holding a bunch of flowers", "wearing a cape",
            "carrying a backpack", "holding a magnifying glass",
            "carrying a lunchbox", "holding a trophy",
            "wearing sunglasses", "carrying a watering can",
            "holding a paintbrush", "wearing a crown",
            "carrying a lantern", "holding a map", "wearing a scarf"
        ]
        self.angles = [
            "full body view", "close-up portrait", "side view",
            "front view", "action pose", "sitting pose", "standing pose"
        ]
        self.seasonal = {
            "christmas": [
                "decorating a Christmas tree", "opening Christmas presents",
                "making a snowman", "hanging stockings",
                "baking Christmas cookies", "riding a sleigh"
            ],
            "halloween": [
                "trick or treating", "carving a pumpkin",
                "wearing a Halloween costume", "exploring a haunted house",
                "collecting candy"
            ],
            "easter": [
                "hunting Easter eggs", "decorating Easter eggs",
                "meeting the Easter bunny", "planting spring flowers"
            ],
            "summer": [
                "building a sandcastle", "having a water fight",
                "eating watermelon", "flying a kite", "having a picnic"
            ],
            "winter": [
                "building a snowman", "ice skating",
                "drinking hot chocolate", "making snow angels"
            ]
        }
        self.niche_styles = {
            "dinosaurs": {
                "style": "bold thick lines, prehistoric style illustration",
                "backgrounds": [
                    "in a prehistoric jungle", "near a volcano",
                    "in a swamp", "near a waterfall", "in a rocky canyon",
                    "under a meteor shower", "in a dense forest"
                ],
                "line_weight": "extra thick bold outlines"
            },
            "butterflies": {
                "style": "delicate fine lines, nature illustration style",
                "backgrounds": [
                    "in a flower garden", "near a pond",
                    "in a meadow", "on a sunny day",
                    "near colorful flowers", "in a butterfly sanctuary"
                ],
                "line_weight": "thin delicate outlines"
            },
            "ocean animals": {
                "style": "flowing curved lines, underwater illustration",
                "backgrounds": [
                    "underwater near coral reef", "in the deep ocean",
                    "near a shipwreck", "in a tropical lagoon",
                    "near sea rocks", "in crystal clear water"
                ],
                "line_weight": "smooth flowing outlines"
            },
            "jungle animals": {
                "style": "bold expressive lines, safari illustration",
                "backgrounds": [
                    "in the African savanna", "near a watering hole",
                    "in a dense jungle", "on a rocky hill",
                    "near a river", "under a big tree"
                ],
                "line_weight": "thick bold outlines"
            },
            "farm animals": {
                "style": "cute rounded lines, countryside illustration",
                "backgrounds": [
                    "on a sunny farm", "near a red barn",
                    "in a green meadow", "near a fence",
                    "in a haystack", "near a farmhouse"
                ],
                "line_weight": "medium rounded outlines"
            },
            "space": {
                "style": "geometric clean lines, space illustration",
                "backgrounds": [
                    "in outer space", "on the moon",
                    "near a planet", "in a space station",
                    "near a black hole", "in a galaxy"
                ],
                "line_weight": "clean sharp outlines"
            },
            "default": {
                "style": "cute cartoon line art",
                "backgrounds": [],
                "line_weight": "thick bold outlines"
            }
        }

        # ✅ 4 Levels — Simple / Intermediate / Advanced / Pro
        self.complexity_levels = {
            "simple": {
                "details": "very simple design, 2-3 main elements only, big cute character",
                "spaces": "extra large coloring spaces, very easy to color",
                "lines": "extra thick lines, suitable for toddlers age 2-4",
                "label": "🟢 SIMPLE"
            },
            "intermediate": {
                "details": "moderate detail, 4-5 elements, cute character with simple background",
                "spaces": "large coloring spaces, easy to color",
                "lines": "thick lines, suitable for kids age 4-8",
                "label": "🔵 INTERMEDIATE"
            },
            "advanced": {
                "details": "detailed design, 6-8 elements, character with scene and props",
                "spaces": "medium coloring spaces, some fine details",
                "lines": "medium lines, suitable for kids age 8-12",
                "label": "🟠 ADVANCED"
            },
            "pro": {
                "details": "highly detailed, 9-12 elements, complex scene with patterns and textures",
                "spaces": "small detailed coloring spaces, intricate patterns",
                "lines": "fine detailed lines, suitable for teens and adults",
                "label": "🔴 PRO"
            }
        }

        self.age_styles = {
            "toddler": "very simple shapes, extra thick lines, minimal details",
            "kids":    "simple design, thick outlines, large spaces to color",
            "teens":   "detailed design, medium outlines, intricate patterns"
        }

        self.negative_prompt = (
            "no color fills, no shading, no gradients, "
            "no gray areas, no crosshatching, no texture fills, "
            "no background patterns, no watermark, no text, "
            "no signature, no blur, no shadows, "
            "no photorealistic style, no 3D rendering"
        )

        self._used = set()

    def _get_complexity(self, page_number, total_pages):
        """4 levels — equal distribution"""
        ratio = page_number / total_pages
        if ratio <= 0.25:
            return "simple"
        elif ratio <= 0.50:
            return "intermediate"
        elif ratio <= 0.75:
            return "advanced"
        else:
            return "pro"

    def _get_niche_data(self, niche):
        niche_lower = niche.lower() if niche else "default"
        for key in self.niche_styles:
            if key in niche_lower:
                return self.niche_styles[key]
        return self.niche_styles["default"]

    def build_prompt(self, subject, age_group="kids", season=None, niche=None, page_number=1, total_pages=40):
        niche_data  = self._get_niche_data(niche or subject)
        style       = niche_data["style"]
        line_weight = niche_data["line_weight"]

        if niche_data["backgrounds"]:
            background = random.choice(niche_data["backgrounds"])
        else:
            background = random.choice(self.backgrounds)

        complexity_key = self._get_complexity(page_number, total_pages)
        complexity     = self.complexity_levels[complexity_key]
        age_detail     = self.age_styles.get(age_group, self.age_styles["kids"])

        max_attempts = 10
        for _ in range(max_attempts):
            action     = random.choice(self.actions)
            expression = random.choice(self.expressions)
            prop       = random.choice(self.props)
            angle      = random.choice(self.angles)

            if season and season.lower() in self.seasonal:
                action = random.choice(self.seasonal[season.lower()])

            combo = f"{subject}_{action}_{background}_{prop}"
            if combo not in self._used:
                self._used.add(combo)
                break

        positive = (
            f"Cute {expression} {subject} {action} {background}, "
            f"{prop}, {angle}, "
            f"kids coloring book page, "
            f"{style}, "
            f"{line_weight}, "
            f"{complexity['details']}, "
            f"{complexity['spaces']}, "
            f"{age_detail}, "
            f"white background, "
            f"centered composition, "
            f"printable coloring page"
        )

        return {
            "positive":   positive,
            "negative":   self.negative_prompt,
            "complexity": complexity_key,
            "label":      complexity["label"],
            "page":       page_number,
            "subject":    subject
        }

    def build_batch(self, subject, count=40, age_group="kids", season=None, niche=None):
        self._used.clear()
        prompts = []

        print(f"\n  📊 Level Distribution:")
        print(f"     🟢 Simple       : Page 1-{count//4}")
        print(f"     🔵 Intermediate : Page {count//4+1}-{count//2}")
        print(f"     🟠 Advanced     : Page {count//2+1}-{(count*3)//4}")
        print(f"     🔴 Pro          : Page {(count*3)//4+1}-{count}\n")

        for i in range(1, count + 1):
            prompt = self.build_prompt(
                subject=subject,
                age_group=age_group,
                season=season,
                niche=niche,
                page_number=i,
                total_pages=count
            )
            prompts.append(prompt)
            print(f"  ✅ Page {i:02}/{count} {prompt['label']} : {subject}")

        return prompts

    def stats(self):
        total = len(self.actions) * len(self.backgrounds) * len(self.props)
        print(f"\n📊 Prompt Engine V3 Stats:")
        print(f"   Actions       : {len(self.actions)}")
        print(f"   Backgrounds   : {len(self.backgrounds)}")
        print(f"   Expressions   : {len(self.expressions)}")
        print(f"   Props         : {len(self.props)}")
        print(f"   Angles        : {len(self.angles)}")
        print(f"   Seasonal      : {len(self.seasonal)} themes")
        print(f"   Niche styles  : {len(self.niche_styles)} niches")
        print(f"   Levels        : Simple / Intermediate / Advanced / Pro")
        print(f"   Unique combos : {total:,}")
        print(f"   Used so far   : {len(self._used)}")

    def random_action(self):
        return random.choice(self.actions)