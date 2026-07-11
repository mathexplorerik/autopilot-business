"""
==========================================================
AI Publishing OS V7
Knowledge Source
Publishing Niches
==========================================================
"""

from knowledge.models import NicheRecord


NICHES = [

    NicheRecord(
        id="jungle",
        name="Jungle Animals",
        category="Animals",
        audience="Kids 4-8",
        marketplace="Amazon KDP",
        description="Wild jungle animal coloring books."
    ),

    NicheRecord(
        id="dinosaurs",
        name="Dinosaurs",
        category="Prehistoric",
        audience="Kids 4-8",
        marketplace="Amazon KDP",
        description="Dinosaur coloring books."
    ),

    NicheRecord(
        id="ocean",
        name="Ocean Animals",
        category="Sea Life",
        audience="Kids 4-8",
        marketplace="Amazon KDP",
        description="Sea creatures and underwater life."
    ),

    NicheRecord(
        id="princess",
        name="Princess",
        category="Fantasy",
        audience="Kids 4-8",
        marketplace="Amazon KDP",
        description="Princess themed coloring books."
    ),

    NicheRecord(
        id="space",
        name="Space",
        category="Science",
        audience="Kids 4-8",
        marketplace="Amazon KDP",
        description="Planets, astronauts and rockets."
    ),
]


def get_all():

    return NICHES


def get_by_id(niche_id: str):

    for niche in NICHES:

        if niche.id == niche_id:

            return niche

    return None