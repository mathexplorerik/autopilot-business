from agents.data.animals.actions import ACTIONS

LOCATION_WORDS = {
    "forest",
    "garden",
    "river",
    "lake",
    "pond",
    "beach",
    "mountain",
    "meadow",
    "field",
    "jungle",
    "desert",
    "farm",
    "village",
    "tree",
    "flowers",
    "flower",
    "bamboo",
    "waterfall",
    "cave",
    "snow",
    "park",
    "island",
}

print("=" * 60)
print("ACTION DATA ANALYSIS")
print("=" * 60)

total = 0
mixed = 0

for category, actions in ACTIONS.items():

    print(f"\n[{category.upper()}]")

    for action in actions:

        total += 1

        text = action.lower()

        found = [w for w in LOCATION_WORDS if w in text]

        if found:

            mixed += 1

            print(f"⚠ {action}")
            print(f"   Location words: {found}")

print("\n" + "=" * 60)
print("Total Actions :", total)
print("Mixed Entries :", mixed)
print("=" * 60)