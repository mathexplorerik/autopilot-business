"""
==========================================================
AI Publishing OS V6
Subject Provider
==========================================================
"""

import random
from typing import List


class SubjectProvider:
    """
    Provides subjects for prompt generation.

    Responsibilities
    ----------------
    ✓ Store subjects
    ✓ Sequential selection
    ✓ Random selection
    ✓ Unique selection
    """

    def __init__(self, subjects: List[str] | None = None):

        self.subjects = subjects or []

        self.used = set()

    # --------------------------------------------------

    def load(self, subjects: List[str]):

        """Load subjects."""

        self.subjects = list(subjects)

        self.used.clear()

    # --------------------------------------------------

    def all(self) -> List[str]:

        """Return all subjects."""

        return self.subjects

    # --------------------------------------------------

    def total(self) -> int:

        return len(self.subjects)

    # --------------------------------------------------

    def get(self, index: int) -> str:

        """Sequential subject."""

        if not self.subjects:
            raise ValueError("No subjects loaded.")

        return self.subjects[index % len(self.subjects)]

    # --------------------------------------------------

    def random(self) -> str:

        """Random subject."""

        if not self.subjects:
            raise ValueError("No subjects loaded.")

        return random.choice(self.subjects)

    # --------------------------------------------------

    def unique(self) -> str:

        """
        Return a subject that has not been used.
        Resets automatically after all subjects are used.
        """

        available = [
            s for s in self.subjects
            if s not in self.used
        ]

        if not available:

            self.used.clear()

            available = self.subjects.copy()

        subject = random.choice(available)

        self.used.add(subject)

        return subject

    # --------------------------------------------------

    def reset(self):

        """Reset used subjects."""

        self.used.clear()