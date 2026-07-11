"""
=========================================
Story Planner (with Story Beats)
=========================================
Decides the narrative shape of a multi-page book.
Each page maps to a "story beat" — a concrete event
(e.g. "wake_up", "meet_friend") with keywords the
engine can use to pick a matching action, plus a
fallback action_category and mood hint.

Does NOT pick specific actions/props/scenes —
that stays with AnimalEngine's existing selectors.
"""

BEATS = [
    # ---------- Introduction ----------
    {"chapter": "Introduction", "beat": "wake_up", "category": "daily_life", "keywords": ["wake", "morning"], "mood": "happy"},
    {"chapter": "Introduction", "beat": "stretch", "category": "movement", "keywords": ["stretch"], "mood": "calm"},
    {"chapter": "Introduction", "beat": "morning_routine", "category": "daily_life", "keywords": ["wash", "brush", "clean", "bath"], "mood": "happy"},
    {"chapter": "Introduction", "beat": "eat_breakfast", "category": "daily_life", "keywords": ["eat", "breakfast", "drink"], "mood": "happy"},
    {"chapter": "Introduction", "beat": "get_ready", "category": "daily_life", "keywords": ["ready", "dress", "pack"], "mood": "calm"},
    {"chapter": "Introduction", "beat": "leave_home", "category": "movement", "keywords": ["leave", "outside", "walk"], "mood": "happy"},
    {"chapter": "Introduction", "beat": "morning_walk", "category": "movement", "keywords": ["walk", "path"], "mood": "calm"},
    {"chapter": "Introduction", "beat": "say_hello", "category": "daily_life", "keywords": ["greet", "hello", "wave"], "mood": "happy"},

    # ---------- Exploration ----------
    {"chapter": "Exploration", "beat": "walk_to_park", "category": "movement", "keywords": ["walk", "path", "trail"], "mood": "curious"},
    {"chapter": "Exploration", "beat": "discover_nature", "category": "nature", "keywords": ["flower", "leaf", "tree", "garden"], "mood": "curious"},
    {"chapter": "Exploration", "beat": "meet_friend", "category": "play", "keywords": ["friend", "play"], "mood": "happy"},
    {"chapter": "Exploration", "beat": "learn_something", "category": "learning", "keywords": ["learn", "discover", "watch"], "mood": "curious"},
    {"chapter": "Exploration", "beat": "watch_animals", "category": "nature", "keywords": ["watch", "bird", "butterfly"], "mood": "curious"},
    {"chapter": "Exploration", "beat": "cross_path", "category": "movement", "keywords": ["bridge", "cross", "stream"], "mood": "curious"},
    {"chapter": "Exploration", "beat": "collect_things", "category": "nature", "keywords": ["collect", "gather", "pick"], "mood": "happy"},
    {"chapter": "Exploration", "beat": "rest_outdoors", "category": "nature", "keywords": ["rest", "shade", "sit"], "mood": "calm"},

    # ---------- Activities ----------
    {"chapter": "Activities", "beat": "play_sports", "category": "sports", "keywords": ["ball", "run", "race", "sport"], "mood": "excited"},
    {"chapter": "Activities", "beat": "paint_picture", "category": "creative", "keywords": ["paint", "draw", "color"], "mood": "playful"},
    {"chapter": "Activities", "beat": "celebrate", "category": "celebration", "keywords": ["celebrat", "party"], "mood": "excited"},
    {"chapter": "Activities", "beat": "play_game", "category": "play", "keywords": ["play", "game"], "mood": "playful"},
    {"chapter": "Activities", "beat": "music_time", "category": "celebration", "keywords": ["sing", "dance", "music"], "mood": "happy"},
    {"chapter": "Activities", "beat": "help_friend", "category": "daily_life", "keywords": ["help", "share"], "mood": "happy"},
    {"chapter": "Activities", "beat": "dance_party", "category": "celebration", "keywords": ["dance"], "mood": "excited"},
    {"chapter": "Activities", "beat": "build_something", "category": "creative", "keywords": ["build", "craft", "make"], "mood": "playful"},

    # ---------- Adventure ----------
    {"chapter": "Adventure", "beat": "start_adventure", "category": "adventure", "keywords": ["explore", "adventure"], "mood": "brave"},
    {"chapter": "Adventure", "beat": "find_treasure", "category": "adventure", "keywords": ["treasure", "find", "search"], "mood": "excited"},
    {"chapter": "Adventure", "beat": "cross_river", "category": "adventure", "keywords": ["river", "cross", "stream"], "mood": "brave"},
    {"chapter": "Adventure", "beat": "climb_high", "category": "adventure", "keywords": ["climb", "mountain", "hill"], "mood": "brave"},
    {"chapter": "Adventure", "beat": "discover_cave", "category": "adventure", "keywords": ["cave", "discover", "hidden"], "mood": "curious"},
    {"chapter": "Adventure", "beat": "magic_moment", "category": "fantasy", "keywords": ["magic", "fairy", "unicorn", "sparkl"], "mood": "excited"},
    {"chapter": "Adventure", "beat": "solve_mystery", "category": "adventure", "keywords": ["mystery", "secret", "hidden"], "mood": "curious"},
    {"chapter": "Adventure", "beat": "return_journey", "category": "adventure", "keywords": ["return", "back", "journey"], "mood": "happy"},

    # ---------- Wrap-up ----------
    {"chapter": "Wrap-up", "beat": "head_home", "category": "daily_life", "keywords": ["home", "return", "walk"], "mood": "calm"},
    {"chapter": "Wrap-up", "beat": "share_stories", "category": "celebration", "keywords": ["share", "tell", "story"], "mood": "happy"},
    {"chapter": "Wrap-up", "beat": "family_time", "category": "daily_life", "keywords": ["family", "together"], "mood": "happy"},
    {"chapter": "Wrap-up", "beat": "eat_dinner", "category": "daily_life", "keywords": ["eat", "dinner", "food"], "mood": "calm"},
    {"chapter": "Wrap-up", "beat": "relax", "category": "daily_life", "keywords": ["relax", "rest"], "mood": "calm"},
    {"chapter": "Wrap-up", "beat": "bath_time", "category": "daily_life", "keywords": ["bath", "wash", "clean"], "mood": "calm"},
    {"chapter": "Wrap-up", "beat": "bedtime_story", "category": "daily_life", "keywords": ["bed", "story", "sleep"], "mood": "calm"},
    {"chapter": "Wrap-up", "beat": "goodnight", "category": "daily_life", "keywords": ["sleep", "goodnight", "dream"], "mood": "calm"},
]


class StoryPlanner:
    """
    Maps a page number (out of total_pages) onto a
    fixed 40-beat story arc, scaled proportionally to
    any total_pages.
    """

    def __init__(self, beats=None):
        self.beats = beats or BEATS
        self.base_total = len(self.beats)

    def plan(self, page, total_pages):
        # Scale page (1..total_pages) onto beat index (0..len(beats)-1)
        ratio = (page - 1) / max(1, total_pages - 1) if total_pages > 1 else 0
        index = round(ratio * (self.base_total - 1))
        index = max(0, min(self.base_total - 1, index))

        beat = self.beats[index]

        return {
            "chapter": beat["chapter"],
            "story_beat": beat["beat"],
            "action_category": beat["category"],
            "keywords": beat["keywords"],
            "mood_hint": beat["mood"],
        }
