SUBJECTS = {
    # ✅ Metadata add kiya har niche ke liye
    "farm animals": {
        "subjects": [
            "cow", "horse", "pig", "sheep", "goat",
            "chicken", "duck", "rabbit", "donkey", "turkey"
        ],
        "age_group": "kids",
        "kdp_category": "Children's Books > Animals",
        "keywords": ["farm animals coloring book", "kids coloring pages", "animal coloring book"],
        "difficulty": "easy"
    },
    "dinosaurs": {
        "subjects": [
            "T-Rex", "Triceratops", "Stegosaurus", "Brachiosaurus",
            "Velociraptor", "Ankylosaurus", "Parasaurolophus",
            "Spinosaurus", "Pterodactyl", "Diplodocus"
        ],
        "age_group": "kids",
        "kdp_category": "Children's Books > Dinosaurs",
        "keywords": ["dinosaur coloring book", "dino coloring pages", "kids dinosaur book"],
        "difficulty": "medium"
    },
    "butterflies": {
        "subjects": [
            "butterfly", "caterpillar", "monarch butterfly",
            "swallowtail butterfly", "blue butterfly", "garden butterfly"
        ],
        "age_group": "toddler",
        "kdp_category": "Children's Books > Nature",
        "keywords": ["butterfly coloring book", "nature coloring pages", "kids butterfly book"],
        "difficulty": "easy"
    },
    "ocean animals": {
        "subjects": [
            "dolphin", "whale", "octopus", "sea turtle",
            "seal", "starfish", "crab", "seahorse", "jellyfish", "shark"
        ],
        "age_group": "kids",
        "kdp_category": "Children's Books > Ocean",
        "keywords": ["ocean animals coloring book", "sea creatures coloring", "underwater coloring book"],
        "difficulty": "medium"
    },
    "jungle animals": {
        "subjects": [
            "lion", "tiger", "elephant", "giraffe", "zebra",
            "monkey", "hippo", "rhino", "cheetah", "gorilla"
        ],
        "age_group": "kids",
        "kdp_category": "Children's Books > Jungle",
        "keywords": ["jungle animals coloring book", "safari coloring pages", "wild animals coloring"],
        "difficulty": "medium"
    },

    # ✅ Naye niches add kiye — future expansion
    "space": {
        "subjects": [
            "astronaut", "rocket", "alien", "planet Saturn",
            "moon rover", "space station", "shooting star",
            "UFO", "telescope", "comet"
        ],
        "age_group": "kids",
        "kdp_category": "Children's Books > Space",
        "keywords": ["space coloring book", "astronaut coloring pages", "galaxy coloring book"],
        "difficulty": "medium"
    },
    "princess": {
        "subjects": [
            "princess", "fairy", "mermaid", "unicorn",
            "castle", "magic wand", "crown", "dragon",
            "enchanted forest", "fairy godmother"
        ],
        "age_group": "toddler",
        "kdp_category": "Children's Books > Fantasy",
        "keywords": ["princess coloring book", "fairy tale coloring", "unicorn coloring book"],
        "difficulty": "easy"
    },
    "vehicles": {
        "subjects": [
            "fire truck", "police car", "ambulance", "school bus",
            "monster truck", "racing car", "helicopter",
            "submarine", "tractor", "bulldozer"
        ],
        "age_group": "toddler",
        "kdp_category": "Children's Books > Vehicles",
        "keywords": ["vehicles coloring book", "trucks coloring pages", "cars coloring book"],
        "difficulty": "easy"
    }
}

# ✅ Helper functions
def get_subjects(niche: str) -> list:
    """Niche ke subjects lo"""
    return SUBJECTS.get(niche, {}).get("subjects", [])

def get_keywords(niche: str) -> list:
    """KDP keywords lo"""
    return SUBJECTS.get(niche, {}).get("keywords", [])

def get_age_group(niche: str) -> str:
    """Age group lo"""
    return SUBJECTS.get(niche, {}).get("age_group", "kids")

def get_kdp_category(niche: str) -> str:
    """KDP category lo"""
    return SUBJECTS.get(niche, {}).get("kdp_category", "")

def list_niches() -> list:
    """Saare available niches dikhaao"""
    return list(SUBJECTS.keys())

def niche_stats() -> None:
    """Har niche ki info print karo"""
    print("\n📚 Available Niches:\n")
    for niche, data in SUBJECTS.items():
        print(f"  🎨 {niche.title()}")
        print(f"     Age    : {data['age_group']}")
        print(f"     Animals: {len(data['subjects'])}")
        print(f"     Level  : {data['difficulty']}\n")