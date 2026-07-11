"""
==========================================================
AI Publishing OS V7
Knowledge Source
Animals
==========================================================
"""

from agents.data.subjects import SUBJECTS


def get_all():
    """
    Return all available animal niches.
    """

    return SUBJECTS


def get_categories():

    return sorted(SUBJECTS.keys())


def get_subjects(category: str):

    return SUBJECTS.get(category.lower(), [])


def has_category(category: str):

    return category.lower() in SUBJECTS