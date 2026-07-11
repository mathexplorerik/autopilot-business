import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.engines.animal_engine import AnimalEngine

engine = AnimalEngine()

animals = [
    "lion",
    "penguin",
    "panda",
    "monkey",
    "rabbit",
]

TOTAL = 20

print("=" * 80)
print("PROMPT QUALITY TEST")
print("=" * 80)

for animal in animals:

    print(f"\n{'=' * 30}")
    print(animal.upper())
    print(f"{'=' * 30}")

    for i in range(TOTAL):

        result = engine.build(animal)

        print(f"\n{i + 1}.")
        print(result["positive"])