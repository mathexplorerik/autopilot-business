import os
import random
from agents.engines.prompt_engine import PromptEngine


class PromptAgent:

    def generate(self, report):

        print("\n✍️ Prompt Agent Running...\n")

        animals = [
            "baby elephant",
            "lion cub",
            "baby tiger",
            "giraffe",
            "zebra",
            "panda",
            "koala",
            "monkey",
            "fox",
            "rabbit",
            "bear cub",
            "penguin",
            "owl",
            "deer",
            "hippo",
            "rhino",
            "crocodile",
            "turtle",
            "dolphin",
            "whale",
            "octopus",
            "seal",
            "cat",
            "puppy",
            "duck",
            "chicken",
            "horse",
            "cow",
            "goat",
            "sheep",
            "camel",
            "kangaroo",
            "parrot",
            "peacock",
            "hedgehog",
            "squirrel",
            "bee",
            "butterfly",
            "snail",
            "frog"
        ]

        actions = [
            "smiling",
            "waving",
            "holding a balloon",
            "holding flowers",
            "playing with a butterfly",
            "playing with a ball",
            "wearing a party hat",
            "eating leaves",
            "eating bamboo",
            "sleeping",
            "jumping",
            "running",
            "sitting",
            "standing",
            "drinking water",
            "reading a book",
            "flying a kite",
            "wearing a bow tie",
            "wearing a cute hat",
            "playing in the grass"
        ]

        prompts = []

        for animal in animals[:report["pages"]]:

            action = random.choice(actions)

            prompt = (
                f"Cute {animal} {action}, "
                "kids coloring book page, "
                "simple black and white line art, "
                "thick bold outlines, "
                "no shading, "
                "no gray, "
                "white background, "
                "centered composition, "
                "printable coloring page"
            )

            prompts.append(prompt)

        os.makedirs("output/prompts", exist_ok=True)

        with open("output/prompts/prompts.txt", "w", encoding="utf-8") as f:
            for prompt in prompts:
                f.write(prompt + "\n")

        print("Prompts saved to output/prompts/prompts.txt ✅")

        return prompts