"""
==========================================================
AI Publishing OS V6
Scene Planner
==========================================================
"""


class ScenePlanner:

    """
    Decide what each page should contain BEFORE
    the prompt is generated.
    """

    def plan(
        self,
        page: int,
        total_pages: int
    ):

        ratio = page / total_pages

        if ratio <= 0.25:

            return {

                "level": "simple",

                "subjects": 1,

                "props": 1,

                "accessories": 0,

                "background": False,

                "details": 2

            }

        elif ratio <= 0.50:

            return {

                "level": "intermediate",

                "subjects": 1,

                "props": 2,

                "accessories": 1,

                "background": True,

                "details": 4

            }

        elif ratio <= 0.75:

            return {

                "level": "advanced",

                "subjects": 1,

                "props": 3,

                "accessories": 2,

                "background": True,

                "details": 7

            }

        return {

            "level": "pro",

            "subjects": 2,

            "props": 4,

            "accessories": 2,

            "background": True,

            "details": 10

        }