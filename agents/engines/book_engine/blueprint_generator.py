class BlueprintGenerator:
    """
    Builds the final book blueprint.
    """

    def __init__(self):
        pass

    def generate(
        self,
        title: str,
        subtitle: str,
        keyword: str,
        theme: str,
        pages: int,
        scenes: list,
    ) -> dict:

        return {
            "title": title,
            "subtitle": subtitle,
            "keyword": keyword,
            "theme": theme,
            "total_pages": pages,
            "scenes": scenes,
        }