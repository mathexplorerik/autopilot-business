"""
=========================================
Story Beat Actions
=========================================
Generic, animal-agnostic action templates for
each story beat. {subject} is filled in at
runtime by the engine. These take priority over
subject-specific and generic category actions
when story_mode is on, since they match the
narrative moment precisely.
"""

STORY_BEAT_ACTIONS = {
    "wake_up": [
        "waking up with a big yawn",
        "opening its eyes slowly",
        "stretching after waking up",
    ],
    "stretch": [
        "stretching its legs",
        "having a big morning stretch",
    ],
    "morning_routine": [
        "washing up in the morning",
        "brushing its teeth",
        "getting washed and clean",
    ],
    "eat_breakfast": [
        "eating a healthy breakfast",
        "enjoying breakfast",
        "drinking a morning drink",
    ],
    "get_ready": [
        "getting ready for the day",
        "packing a small bag",
        "putting on a hat before heading out",
    ],
    "leave_home": [
        "leaving home for the day",
        "walking out the front door",
        "heading outside",
    ],
    "morning_walk": [
        "taking a morning walk",
        "walking along a quiet path",
    ],
    "say_hello": [
        "waving hello to a friend",
        "greeting a neighbor",
    ],
    "walk_to_park": [
        "walking toward the park",
        "strolling down a path",
    ],
    "discover_nature": [
        "discovering pretty flowers",
        "looking closely at a leaf",
        "noticing a small plant",
    ],
    "meet_friend": [
        "meeting a friend",
        "saying hi to a new friend",
    ],
    "learn_something": [
        "learning something new",
        "watching closely and learning",
    ],
    "watch_animals": [
        "watching birds fly by",
        "watching butterflies",
    ],
    "cross_path": [
        "crossing a small bridge",
        "stepping across a stream",
    ],
    "collect_things": [
        "collecting pretty leaves",
        "gathering small pebbles",
    ],
    "rest_outdoors": [
        "resting under a tree",
        "taking a break outside",
    ],
    "play_sports": [
        "playing a fun game of ball",
        "running around and playing sports",
    ],
    "paint_picture": [
        "painting a colorful picture",
        "drawing with crayons",
    ],
    "celebrate": [
        "celebrating a happy moment",
        "having a small celebration",
    ],
    "play_game": [
        "playing a fun game",
        "playing together with friends",
    ],
    "music_time": [
        "singing a happy song",
        "dancing to music",
    ],
    "help_friend": [
        "helping a friend",
        "sharing with a friend",
    ],
    "dance_party": [
        "dancing happily",
        "having a little dance",
    ],
    "build_something": [
        "building something fun",
        "making a small craft",
    ],
    "start_adventure": [
        "starting a new adventure",
        "setting off to explore",
    ],
    "find_treasure": [
        "finding a hidden treasure",
        "discovering something special",
    ],
    "cross_river": [
        "crossing a gentle river",
        "wading across a stream",
    ],
    "climb_high": [
        "climbing up a small hill",
        "climbing to a higher spot",
    ],
    "discover_cave": [
        "discovering a hidden cave",
        "peeking into a small cave",
    ],
    "magic_moment": [
        "experiencing a magical moment",
        "seeing something sparkle and shine",
    ],
    "solve_mystery": [
        "solving a fun little mystery",
        "following mysterious footprints",
    ],
    "return_journey": [
        "starting the journey back",
        "heading back from the adventure",
    ],
    "head_home": [
        "walking home",
        "heading back home",
    ],
    "share_stories": [
        "sharing stories about the day",
        "telling a friend about the day",
    ],
    "family_time": [
        "spending time with family",
        "sitting together with family",
    ],
    "eat_dinner": [
        "eating a cozy dinner",
        "enjoying dinner",
    ],
    "relax": [
        "relaxing after a long day",
        "taking it easy in the evening",
    ],
    "bath_time": [
        "taking a warm bath",
        "washing up before bed",
    ],
    "bedtime_story": [
        "listening to a bedtime story",
        "enjoying a story before bed",
    ],
    "goodnight": [
        "sleeping peacefully",
        "drifting off to sleep",
        "saying goodnight",
    ],
}
