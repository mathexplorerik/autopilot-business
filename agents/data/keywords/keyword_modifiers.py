"""
=========================================
Keyword Modifiers
=========================================
Proven KDP/Etsy search-pattern modifiers,
each with a relative popularity weight and
a relative competition weight (both 0-100,
based on general marketplace search behavior
patterns, not live API data).
"""

KEYWORD_MODIFIERS = [
    {"pattern": "{niche} coloring book",            "popularity": 95, "competition_delta": 0},
    {"pattern": "{niche} coloring pages",            "popularity": 85, "competition_delta": -5},
    {"pattern": "{niche} coloring book for kids",    "popularity": 90, "competition_delta": -5},
    {"pattern": "{niche} activity book",             "popularity": 70, "competition_delta": -10},
    {"pattern": "{niche} coloring book for toddlers","popularity": 65, "competition_delta": -15},
    {"pattern": "{niche} coloring book for adults",  "popularity": 60, "competition_delta": -10},
    {"pattern": "printable {niche} coloring pages",  "popularity": 55, "competition_delta": -20},
    {"pattern": "{niche} coloring book large print", "popularity": 40, "competition_delta": -25},
    {"pattern": "cute {niche} coloring book",        "popularity": 50, "competition_delta": -15},
    {"pattern": "{niche} coloring book gift",        "popularity": 35, "competition_delta": -20},
    {"pattern": "{niche} coloring pages pdf",        "popularity": 45, "competition_delta": -20},
    {"pattern": "{niche} activity book for kids ages 4-8", "popularity": 55, "competition_delta": -18},
    {"pattern": "{niche} coloring workbook",         "popularity": 30, "competition_delta": -22},
    {"pattern": "easy {niche} coloring book",        "popularity": 40, "competition_delta": -18},
    {"pattern": "{niche} coloring and activity book","popularity": 45, "competition_delta": -12},
]
