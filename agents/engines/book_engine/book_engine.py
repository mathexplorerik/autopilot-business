from .niche_selector import NicheSelector
from .theme_planner import ThemePlanner
from .page_planner import PagePlanner
from .scene_planner import ScenePlanner
from .title_generator import TitleGenerator
from .subtitle_generator import SubtitleGenerator
from .blueprint_generator import BlueprintGenerator
from .quality_checker import QualityChecker
from agents.engines.generation_pipeline.generation_pipeline import GenerationPipeline

class BookEngine:

    def __init__(self):

        self.pipeline = GenerationPipeline()

        self.niche_selector = NicheSelector()

        self.theme_planner = ThemePlanner()

        self.page_planner = PagePlanner()

        self.scene_planner = ScenePlanner()

        self.title_generator = TitleGenerator()

        self.subtitle_generator = SubtitleGenerator()

        self.blueprint_generator = BlueprintGenerator()

        self.quality_checker = QualityChecker()

    def build(
    self,
    keyword: str,
    book_type: str,
    age_group: str,
    provider: str = "manual",
):

    # Step 1: Select Niche
        niche = self.niche_selector.select(
        keyword,
        book_type,
        age_group,
    )

    # Step 2: Plan Theme
        theme = self.theme_planner.plan(keyword)

    # Step 3: Plan Pages
        pages = self.page_planner.plan(
        book_type,
        age_group,
    )

    # Step 4: Plan Scenes
        scenes = self.scene_planner.plan(
        keyword=keyword,
        total_pages=pages["pages"],
        age_group=age_group,
    )

    # Step 5: Generate Title
        title = self.title_generator.generate(
        keyword,
        book_type,
    )

    # Step 6: Generate Subtitle
        subtitle = self.subtitle_generator.generate(
        keyword,
        age_group,
    )

    # Step 7: Build Blueprint
        blueprint = self.blueprint_generator.generate(
        title=title,
        subtitle=subtitle,
        keyword=keyword,
        theme=theme["theme"],
        pages=pages["pages"],
        scenes=scenes,
    )

    # Step 8: Quality Check
        quality = self.quality_checker.validate(
        blueprint
    )

        blueprint["quality"] = quality
        blueprint["trend"] = niche["trend_report"]

    # Step 9: Generate pages
        self.pipeline.configure(
        keyword=keyword,
        book_type=book_type,
        age_group=age_group,
        total_pages=pages["pages"],
        provider=provider,
    )

        generated_pages = self.pipeline.generate()

        blueprint["generated_pages"] = generated_pages

        return blueprint