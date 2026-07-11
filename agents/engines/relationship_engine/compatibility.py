"""
==========================================================
AI KDP AUTOPILOT V10
Relationship Compatibility
==========================================================
"""


class Compatibility:

    def is_valid(self, source, target):

        if not source or not target:
            return False

        source = source.lower()
        target = target.lower()

        # Forest actions should not use ocean scenes
        if "forest" in source and "ocean" in target:
            return False

        # Garden actions should not use classroom scenes
        if ("flower" in source or "garden" in source) and "classroom" in target:
            return False

        # River actions should not use desert scenes
        if ("river" in source or "lake" in source) and "desert" in target:
            return False

        return True