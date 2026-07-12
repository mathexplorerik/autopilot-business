"""
=========================================
Story Beat Poses
=========================================
Beat-specific poses that override the generic
category-level RELATIONSHIP_MATRIX pose pool
when story_mode is on.
"""

STORY_BEAT_POSES = {
    "wake_up": ["lying down", "sitting up sleepily"],
    "stretch": ["stretching", "standing"],
    "morning_routine": ["standing", "sitting"],
    "eat_breakfast": ["sitting"],
    "get_ready": ["standing"],
    "leave_home": ["walking", "standing"],
    "morning_walk": ["walking"],
    "say_hello": ["standing", "waving pose"],

    "walk_to_park": ["walking"],
    "discover_nature": ["crouching", "sitting"],
    "meet_friend": ["standing", "waving pose"],
    "learn_something": ["sitting", "standing"],
    "watch_animals": ["sitting", "standing"],
    "cross_path": ["walking", "standing"],
    "collect_things": ["crouching", "sitting"],
    "rest_outdoors": ["sitting", "resting"],

    "play_sports": ["running", "jumping"],
    "paint_picture": ["sitting"],
    "celebrate": ["jumping", "standing"],
    "play_game": ["running", "jumping", "sitting"],
    "music_time": ["dancing", "standing"],
    "help_friend": ["standing", "sitting"],
    "dance_party": ["dancing"],
    "build_something": ["sitting", "standing"],

    "start_adventure": ["walking", "standing"],
    "find_treasure": ["crouching", "standing"],
    "cross_river": ["walking", "standing"],
    "climb_high": ["climbing", "standing"],
    "discover_cave": ["standing", "crouching"],
    "magic_moment": ["standing"],
    "solve_mystery": ["standing", "crouching"],
    "return_journey": ["walking"],

    "head_home": ["walking"],
    "share_stories": ["sitting"],
    "family_time": ["sitting", "standing"],
    "eat_dinner": ["sitting"],
    "relax": ["sitting", "resting"],
    "bath_time": ["sitting"],
    "bedtime_story": ["sitting", "lying down"],
    "goodnight": ["lying down"],
}
