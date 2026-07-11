"""
==========================================================
 AI KDP AUTOPILOT V9
 Base Selector
==========================================================

Shared functionality for all selectors.
"""

import random


class BaseSelector:

    def __init__(self):
        self._history = set()

    def random_choice(self, items):
        """
        Return one random item.
        """
        if not items:
            return None

        return random.choice(items)

    def clear_history(self):
        self._history.clear()