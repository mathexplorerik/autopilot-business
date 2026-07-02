import random

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

        # ✅ NEW: Expressions
        self.expressions = [
            "happy", "excited", "sleepy", "surprised",
            "curious", "laughing", "shy", "brave",
            "proud", "silly", "cheerful", "amazed"
        ]

        # ✅ NEW: Props
        self.props = [
            "holding an ice cream cone",
            "carrying a teddy bear",
            "holding a bunch of flowers",
            "wearing a cape",
            "carrying a backpack",
            "holding a magnifying glass",
            "carrying a lunchbox",
            "holding a trophy",
            "wearing sunglasses",
            "carrying a watering can",
            "holding a paintbrush",
            "wearing a crown",
            "carrying a lantern",
            "holding a map",
            "wearing a scarf"
        ]

        # ✅ NEW: Seasonal themes
        self.seasonal = {
            "christmas":  [
                "decorating a Christmas tree",
                "opening Christmas presents",
                "making a snowman",
                "hanging stockings",
                "baking Christmas cookies",
                "riding a sleigh"
            ],
            "halloween":  [
                "trick or treating",
                "carving a pumpkin",
                "wearing a Halloween costume",
                "exploring a haunted house",
                "collecting candy"
            ],
            "easter":     [
                "hunting Easter eggs",
                "decorating Easter eggs",
                "meeting the Easter bunny",
                "planting spring flowers"
            ],
            "summer":     [
                "building a sandcastle",
                "having a water fight",
                "eating watermelon",
                "flying a kite",
                "having a picnic"
            ],
            "winter":     [
                "building a snowman",
                "ice skating",
                "drinking hot chocolate",
                "making snow angels"
            ]
        }

        # ✅ NEW: Camera angles
        self.angles = [
            "full body view",
            "close-up portrait",
            "side view",
            "front view",
            "action pose",
            "sitting pose",
            "standing pose"
        ]

        # ✅ NEW: Style variations
        self.styles = [
            "simple black and white line art",
            "cute cartoon line art",
            "bold outline illustration",
            "minimalist line drawing"
        ]

        # ✅ Age-based complexity
        self.age_styles = {
            "toddler": "very simple shapes, extra thick lines, minimal details",
            "kids":    "simple design, thick outlines, large spaces to color",
            "teens":   "detailed design, medium outlines, intricate patterns"
        }

        # ✅ Duplicate tracker
        self._used = set()

    def build_prompt(self, subject, age_group="kids", season=None):
        max_attempts = 10

        for _ in range(max_attempts):
            action     = random.choice(self.actions)
            background = random.choice(self.backgrounds)
            expression = random.choice(self.expressions)
            prop       = random.choice(self.props)
            angle      = random.choice(self.angles)

            # Seasonal override
            if season and season.lower() in self.seasonal:
                action = random.choice(self.seasonal[season.lower()])

            combo = f"{subject}_{action}_{background}_{prop}"

            if combo not in self._used:
                self._used.add(combo)
                break

        style      = random.choice(self.styles)
        age_detail = self.age_styles.get(age_group, self.age_styles["kids"])

        return (
            f"Cute {expression} {subject} {action} {background}, "
            f"{prop}, "
            f"{angle}, "
            f"kids coloring book page, "
            f"{style}, "
            f"thick bold outlines, "
            f"large open spaces, "
            f"{age_detail}, "
            f"no shading, "
            f"white background, "
            f"centered composition, "
            f"printable coloring page"
        )

    def build_batch(self, subject, count=30, age_group="kids", season=None):
        self._used.clear()
        prompts = []
        for i in range(count):
            prompt = self.build_prompt(subject, age_group, season)
            prompts.append(prompt)
            print(f"  ✅ Prompt {i+1:02}/{count}: {subject} — done")
        return prompts

    def random_action(self):
        return random.choice(self.actions)

    def stats(self):
        total = len(self.actions) * len(self.backgrounds) * len(self.props)
        print(f"\n📊 Prompt Engine Stats:")
        print(f"   Actions     : {len(self.actions)}")
        print(f"   Backgrounds : {len(self.backgrounds)}")
        print(f"   Expressions : {len(self.expressions)}")
        print(f"   Props       : {len(self.props)}")
        print(f"   Angles      : {len(self.angles)}")
        print(f"   Seasonal    : {len(self.seasonal)} themes")
        print(f"   Unique combos: {total:,}")
        print(f"   Used so far : {len(self._used)}")
        return total