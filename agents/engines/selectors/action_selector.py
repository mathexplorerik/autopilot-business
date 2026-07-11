"""
==========================================================
 AI KDP AUTOPILOT V9
 Universal Action Selector
==========================================================

Purpose:
    Select the best action based on context.

This class is intentionally lightweight.
Selection logic will be added gradually.
"""

class ActionSelector:

    def __init__(self):
        pass

    def pick(
        self,
        category,
        subject,
        age_group,
        page_number,
        total_pages,
        season=None
    ):
        """
        Returns one action for the given context.
        """
        raise NotImplementedError("Action selection not implemented yet.")