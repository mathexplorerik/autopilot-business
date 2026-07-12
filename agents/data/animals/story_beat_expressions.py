"""
=========================================
Story Beat Expressions
=========================================
Beat-specific facial expressions that override
the generic category-level RELATIONSHIP_MATRIX
expression pool when story_mode is on.
"""

STORY_BEAT_EXPRESSIONS = {
    "wake_up": ["sleepy", "calm"],
    "stretch": ["calm", "happy"],
    "morning_routine": ["calm", "happy"],
    "eat_breakfast": ["happy"],
    "get_ready": ["calm", "happy"],
    "leave_home": ["happy", "excited"],
    "morning_walk": ["calm", "happy"],
    "say_hello": ["happy"],
    "walk_to_park": ["curious", "happy"],
    "discover_nature": ["curious"],
    "meet_friend": ["happy", "excited"],
    "learn_something": ["curious", "thoughtful"],
    "watch_animals": ["curious"],
    "cross_path": ["curious"],
    "collect_things": ["happy", "curious"],
    "rest_outdoors": ["calm"],
    "play_sports": ["excited"],
    "paint_picture": ["playful", "thoughtful"],
    "celebrate": ["excited", "happy"],
    "play_game": ["playful", "excited"],
    "music_time": ["happy", "excited"],
    "help_friend": ["happy"],
    "dance_party": ["excited", "playful"],
    "build_something": ["thoughtful", "playful"],
    "start_adventure": ["brave", "excited"],
    "find_treasure": ["excited", "surprised"],
    "cross_river": ["brave"],
    "climb_high": ["brave"],
    "discover_cave": ["curious", "surprised"],
    "magic_moment": ["surprised", "excited"],
    "solve_mystery": ["curious", "thoughtful"],
    "return_journey": ["happy"],
    "head_home": ["calm", "happy"],
    "share_stories": ["happy"],
    "family_time": ["happy", "calm"],
    "eat_dinner": ["calm", "happy"],
    "relax": ["calm"],
    "bath_time": ["calm"],
    "bedtime_story": ["calm", "sleepy"],
    "goodnight": ["sleepy", "calm"],
}
