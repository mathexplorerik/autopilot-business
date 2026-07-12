"""
=========================================
Character Profile Generator
=========================================
Decides a fixed character identity for story
books, so that pages share consistent visual
elements (accessory, companion, etc.) instead
of picking a new one randomly every page.

Only used when book_type == "story". Niche
books have no single character, so profile
stays empty ({}).
"""

import random

from agents.data.animals.subject_props import SUBJECT_PROPS
from agents.data.animals.subject_wearables import SUBJECT_WEARABLES


COMPANIONS = {
    "lion": "a little monkey friend",
    "elephant": "a small bird friend",
    "tiger": "a curious rabbit friend",
    "giraffe": "a playful zebra friend",
    "zebra": "a gentle giraffe friend",
    "fox": "a cheerful squirrel friend",
    "owl": "a friendly hedgehog friend",
    "deer": "a small bird friend",
    "bear": "a little fox friend",
    "squirrel": "a friendly owl friend",
    "hedgehog": "a gentle deer friend",
    "wolf": "a curious fox friend",
    "horse": "a small sheep friend",
    "sheep": "a friendly horse friend",
    "cow": "a playful duck friend",
    "duck": "a gentle frog friend",
    "turtle": "a cheerful crab friend",
    "dolphin": "a playful turtle friend",
    "frog": "a small duck friend",
    "koala": "a curious kangaroo friend",
    "kangaroo": "a gentle koala friend",
    "penguin": "a small seal friend",
    "panda": "a playful rabbit friend",
    "monkey": "a cheerful parrot friend",
    "rabbit": "a gentle butterfly friend",
}

PERSONALITIES = [
    "curious and gentle",
    "brave and kind",
    "playful and cheerful",
    "calm and thoughtful",
    "adventurous and friendly",
]

FAVORITE_ACTIVITIES = [
    "painting", "exploring nature", "playing games",
    "singing songs", "collecting things", "helping friends",
]

HOME_ENVIRONMENTS = {
    "lion": ["a cozy den on the savanna", "a shady den near the grassland"],
    "elephant": ["a peaceful spot near the waterhole", "a shady grove on the savanna"],
    "tiger": ["a den hidden in the jungle", "a quiet spot by the riverbank"],
    "giraffe": ["a spot beneath a tall acacia tree", "a peaceful savanna clearing"],
    "zebra": ["a spot on the open grassland", "a shady patch near the waterhole"],
    "fox": ["a cozy den in the forest", "a burrow beneath a tree"],
    "owl": ["a warm nest in a tall tree", "a hollow in an old oak"],
    "deer": ["a quiet clearing in the woods", "a soft nook by the stream"],
    "bear": ["a den by the forest stream", "a cozy cave in the woods"],
    "squirrel": ["a nest high in a tree", "a cozy tree hollow"],
    "hedgehog": ["a burrow beneath the hedges", "a leafy nest in the garden"],
    "wolf": ["a den in the quiet woodland", "a rocky den on the hillside"],
    "horse": ["a cozy stable in the pasture", "a shady spot by the fence"],
    "sheep": ["a soft spot in the pasture", "a cozy corner of the barn"],
    "cow": ["a peaceful barnyard", "a shady spot in the pasture"],
    "duck": ["a nest by the pond", "a cozy spot near the lily pads"],
    "turtle": ["a quiet spot by the shore", "a sandy nook near the water"],
    "dolphin": ["a favorite spot in the calm sea", "a cove near the coral reef"],
    "frog": ["a lily pad on the pond", "a mossy spot by the marsh"],
    "koala": ["a cozy perch in the eucalyptus tree", "a shady branch in the grove"],
    "kangaroo": ["a warm spot on the outback plain", "a shady patch of scrubland"],
    "penguin": ["a cozy spot on the ice", "a sheltered nook by the glacier"],
    "panda": ["a peaceful spot in the bamboo grove", "a cozy nook in the bamboo forest"],
    "monkey": ["a nest high in the jungle canopy", "a cozy perch among the vines"],
    "rabbit": ["a cozy burrow in the garden", "a soft nook by the flower patch"],
}


class CharacterProfileGenerator:
    """
    Generates a fixed character profile for a
    story book, to be reused consistently across
    all pages.
    """

    def generate(self, subject: str, age_group: str = "kids") -> dict:
        subject_key = subject.lower()

        wearables = SUBJECT_WEARABLES.get(subject_key, [])
        signature_item = random.choice(wearables) if wearables else None

        companion = COMPANIONS.get(subject_key, "a cheerful animal friend")
        personality = random.choice(PERSONALITIES)
        favorite_activity = random.choice(FAVORITE_ACTIVITIES)
        home_options = HOME_ENVIRONMENTS.get(subject_key, ["a cozy home nearby"])
        home_environment = random.choice(home_options)

        return {
            "species": subject_key,
            "age_style": age_group,
            "personality": personality,
            "accessories": [signature_item] if signature_item else [],
            "signature_item": signature_item,
            "companion": companion,
            "favorite_activity": favorite_activity,
            "home_environment": home_environment,
        }
