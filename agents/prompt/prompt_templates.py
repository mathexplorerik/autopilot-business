"""
==========================================================
AI Publishing OS V6
Prompt Templates
==========================================================
"""


class PromptTemplates:
    """
    Central template repository.

    Future Support
    --------------
    ✓ Coloring Books
    ✓ Activity Books
    ✓ Tracing Books
    ✓ Worksheets
    ✓ Story Books

    ✓ Amazon KDP
    ✓ Etsy
    ✓ Gumroad
    """

    DEFAULT = (
        "Cute {expression} {subject} "
        "{action} "
        "{background}, "
        "{props}, "
        "{accessories}, "
        "kids coloring book page, "
        "{style}, "
        "{line_weight}, "
        "{complexity}, "
        "{age_style}, "
        "black and white line art, "
        "white background, "
        "printable, "
        "centered composition"
    )

    AMAZON_KDP = DEFAULT

    ETSY = (
        DEFAULT +
        ", high resolution printable, "
        "premium coloring page"
    )

    GUMROAD = (
        DEFAULT +
        ", premium printable bundle quality"
    )

    ACTIVITY_BOOK = (
        "Kids activity page featuring "
        "{subject}, "
        "{action}, "
        "{background}, "
        "{props}, "
        "{accessories}, "
        "{style}"
    )

    TRACING_BOOK = (
        "Large simple outline of "
        "{subject}, "
        "{action}, "
        "{background}, "
        "extra thick lines, "
        "easy tracing practice"
    )

    STORY_BOOK = (
        "{subject} "
        "{action} "
        "{background}, "
        "children's storybook illustration, "
        "{style}"
    )

    def get(
        self,
        marketplace="amazon",
        product="coloring"
    ):

        marketplace = marketplace.lower()
        product = product.lower()

        # Product-specific templates

        if product == "activity":
            return self.ACTIVITY_BOOK

        if product == "tracing":
            return self.TRACING_BOOK

        if product == "story":
            return self.STORY_BOOK

        # Marketplace-specific templates

        if marketplace == "etsy":
            return self.ETSY

        if marketplace == "gumroad":
            return self.GUMROAD

        return self.AMAZON_KDP
