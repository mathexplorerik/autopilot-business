import random


class PromptEngine:

    def build_prompt(self, subject, action):

        return (
            f"Cute {subject} {action}, "
            "kids coloring book page, "
            "simple black and white line art, "
            "thick bold outlines, "
            "large open spaces, "
            "no shading, "
            "no gray, "
            "white background, "
            "centered composition, "
            "printable coloring page"
        )

    def random_action(self):

        actions = [
            "smiling",
            "running",
            "jumping",
            "holding balloons",
            "wearing a party hat",
            "playing football",
            "reading a book",
            "sleeping",
            "eating leaves",
            "playing with butterflies",
            "painting",
            "camping",
            "flying a kite",
            "playing in the rain",
            "drinking water"
        ]

        return random.choice(actions)