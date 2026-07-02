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

        # ✅ Pro: Style variations
        self.styles = [
            "simple black and white line art",
            "cute cartoon line art",
            "bold outline illustration",
            "minimalist line drawing"
        ]

        # ✅ Pro: Age-based complexity
        self.age_styles = {
            "toddler": "very simple shapes, extra thick lines, minimal details",
            "kids":    "simple design, thick outlines, large spaces to color",
            "teens":   "detailed design, medium outlines, intricate patterns"
        }

        # ✅ Pro: Track used combinations
        self._used = set()

    def build_prompt(self, subject, age_group="kids"):
        max_attempts = 10
        for _ in range(max_attempts):
            action = random.choice(self.actions)
            background = random.choice(self.backgrounds)
            combo = f"{subject}_{action}_{background}"

            # Duplicate avoid karo
            if combo not in self._used:
                self._used.add(combo)
                break

        style = random.choice(self.styles)
        age_detail = self.age_styles.get(age_group, self.age_styles["kids"])

        return (
            f"Cute {subject} {action} {background}, "
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

    def build_batch(self, subject, count=30, age_group="kids"):
        """Ek baar mein saare prompts banao"""
        self._used.clear()
        prompts = []
        for i in range(count):
            prompt = self.build_prompt(subject, age_group)
            prompts.append(prompt)
            print(f"✅ Prompt {i+1:02}: {prompt[:60]}...")
        return prompts

    def random_action(self):
        return random.choice(self.actions)

    def stats(self):
        """Kitne unique combinations possible hain"""
        total = len(self.actions) * len(self.backgrounds)
        print(f"📊 Total unique combinations: {total}")
        print(f"📋 Used so far: {len(self._used)}")
        return total