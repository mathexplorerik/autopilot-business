"""
=========================================
Recurring Motifs Generator
=========================================
Picks 2-3 fixed visual motifs for a book that
appear occasionally across pages (not every
page, to avoid repetition) to create a subtle
sense of a unified visual world.
"""

import random

MOTIF_POOL = [
    "butterfly", "rainbow", "shooting star", "ladybug",
    "dragonfly", "small cloud", "sparkle", "falling leaf",
    "little bird", "firefly",
]


class RecurringMotifsGenerator:
    def generate(self, count: int = 2) -> list:
        count = min(count, len(MOTIF_POOL))
        return random.sample(MOTIF_POOL, count)

    def should_appear(self, page: int, total_pages: int, frequency: int = 4) -> bool:
        """
        Motifs appear roughly every `frequency` pages,
        not on every page.
        """
        return page % frequency == 0
