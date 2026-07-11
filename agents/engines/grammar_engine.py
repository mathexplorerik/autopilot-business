"""
=========================================
Grammar Engine
=========================================
Handles a/an article selection based on
the phonetic sound of the following word.
"""


def get_article(word: str) -> str:
    if not word:
        return "a"

    word_lower = word.strip().lower()

    consonant_sound_exceptions = (
        "unicorn", "unicycle", "user", "uniform", "europe",
        "european", "one", "once",
    )

    vowel_sound_exceptions = (
        "hour", "honest", "honor", "heir",
    )

    first_word = word_lower.split()[0]

    if first_word in consonant_sound_exceptions:
        return "a"

    if first_word in vowel_sound_exceptions:
        return "an"

    if word_lower[0] in "aeiou":
        return "an"

    return "a"


def with_article(word: str) -> str:
    return f"{get_article(word)} {word}"