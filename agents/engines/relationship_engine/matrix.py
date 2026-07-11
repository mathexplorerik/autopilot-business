"""
==========================================================
AI KDP AUTOPILOT V9
Relationship Matrix
==========================================================
Central compatibility rules for the generation engine.
"""

RELATIONSHIP_MATRIX = {

    "movement": {
        "poses": ["walking", "running", "jumping", "standing"],
        "expressions": ["happy", "excited"],
        "locations": ["running across an open meadow", "racing along a sandy path", "moving through tall grass"]
    },
    "play": {
        "poses": ["running", "jumping", "dancing"],
        "expressions": ["playful", "happy", "excited"],
        "locations": ["playing in a sunny backyard", "having fun at a playground", "playing near a colorful park"]
    },
    "adventure": {
        "poses": ["walking", "climbing", "standing"],
        "expressions": ["curious", "brave", "excited"],
        "locations": ["exploring a mysterious forest", "discovering a hidden cave", "venturing across rocky hills"]
    },
    "nature": {
        "poses": ["walking", "sitting", "resting"],
        "expressions": ["calm", "curious"],
        "locations": ["resting in a peaceful garden", "sitting beside a quiet pond", "wandering through a flower field"]
    },
    "creative": {
        "poses": ["sitting", "standing"],
        "expressions": ["happy", "thoughtful"],
        "locations": ["painting under a shady tree", "crafting at a small wooden table", "drawing in a cozy corner"]
    },
    "daily_life": {
        "poses": ["standing", "walking", "sitting"],
        "expressions": ["happy", "calm"],
        "locations": ["relaxing at home", "enjoying a quiet afternoon", "spending time in a cozy room"]
    },
    "learning": {
        "poses": ["sitting", "standing"],
        "expressions": ["curious", "thoughtful"],
        "locations": ["studying at a little desk", "reading in a quiet library corner", "learning in a bright classroom"]
    },
    "celebration": {
        "poses": ["jumping", "dancing", "standing"],
        "expressions": ["excited", "happy", "proud"],
        "locations": ["celebrating at a birthday party", "enjoying a festive gathering", "having fun at a party table"]
    },
    "sports": {
        "poses": ["running", "jumping"],
        "expressions": ["excited", "proud"],
        "locations": ["playing on a sports field", "competing at a sunny stadium", "training on an open field"]
    },
    "fantasy": {
        "poses": ["walking", "flying", "standing"],
        "expressions": ["surprised", "curious", "excited"],
        "locations": ["flying above a magical kingdom", "wandering through an enchanted forest", "standing before a sparkling castle"]
    }
    
}