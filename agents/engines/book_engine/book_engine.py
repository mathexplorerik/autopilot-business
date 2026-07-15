from .niche_selector import NicheSelector
from .theme_planner import ThemePlanner
from .page_planner import PagePlanner
from .scene_planner import ScenePlanner
from .title_generator import TitleGenerator
from .subtitle_generator import SubtitleGenerator
from .blueprint_generator import BlueprintGenerator
from .quality_checker import QualityChecker
from .character_profile_generator import CharacterProfileGenerator
from .recurring_motifs_generator import RecurringMotifsGenerator
from agents.engines.generation_pipeline.generation_pipeline import GenerationPipeline
from agents.engines.education_engine.education_engine import EducationEngine
from agents.data.subjects import get_subjects
import random
from agents.data.animals.season_accessories import SEASON_ACCESSORIES


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
        self.character_profile_generator = CharacterProfileGenerator()
        self.recurring_motifs_generator = RecurringMotifsGenerator()
        self.education_engine = EducationEngine()

    def build(self, keyword, book_type, age_group, provider="manual", season=None, education_mode=None):

        if book_type == "educational":
            return self._build_educational_book(
                education_mode=education_mode,
                age_group=age_group,
            )

        niche = self.niche_selector.select(keyword, book_type, age_group)

        theme = self.theme_planner.plan(keyword)

        pages = self.page_planner.plan(book_type, age_group)

        character_profile = {}
        recurring_motifs = []
        resolved_subject = keyword
        if book_type == "story":
            candidate_subjects = get_subjects(keyword.lower().strip())
            resolved_subject = candidate_subjects[0] if candidate_subjects else keyword
            character_profile = self.character_profile_generator.generate(
                subject=resolved_subject,
                age_group=age_group,
            )
            recurring_motifs = self.recurring_motifs_generator.generate()

        season_accessory = None
        if season:
            options = SEASON_ACCESSORIES.get(season.lower())
            if options:
                season_accessory = random.choice(options)

        preview_page_count = min(3, pages["pages"])
        scenes_preview = self.scene_planner.plan(
            keyword=keyword,
            total_pages=preview_page_count,
            age_group=age_group,
            book_type=book_type,
            character_profile=character_profile,
            recurring_motifs=recurring_motifs,
            season=season,
            season_accessory=season_accessory,
        )

        title = self.title_generator.generate(keyword, book_type)

        subtitle = self.subtitle_generator.generate(keyword, age_group)

        blueprint = self.blueprint_generator.generate(
            title=title,
            subtitle=subtitle,
            keyword=keyword,
            theme=theme["theme"],
            pages=pages["pages"],
            scenes=scenes_preview,
            book_type=book_type,
            target_age=age_group,
            character_profile=character_profile,
            recurring_motifs=recurring_motifs,
        )

        blueprint["trend"] = niche["trend_report"]

        self.pipeline.configure(
            keyword=keyword,
            book_type=book_type,
            age_group=age_group,
            total_pages=pages["pages"],
            provider=provider,
            character_profile=character_profile,
            recurring_motifs=recurring_motifs,
            season=season,
            season_accessory=season_accessory,
        )

        generated_pages = self.pipeline.generate()
        blueprint["generated_pages"] = generated_pages

        quality = self.quality_checker.validate(blueprint)
        blueprint["quality"] = quality
        blueprint["status"] = "Ready for Publishing" if quality["valid"] else "Needs Review"

        return blueprint

    def _build_educational_book(self, education_mode, age_group):
        if not education_mode:
            raise ValueError("education_mode is required when book_type is educational")

        total_pages = self.education_engine.get_page_count(education_mode)

        generated_pages = []
        for page_number in range(1, total_pages + 1):
            page = self.education_engine.build(
                education_mode=education_mode,
                page_number=page_number,
                age_group=age_group,
            )
            page["page"] = page_number
            page["book_mode"] = "educational"
            generated_pages.append(page)

        title = education_mode.capitalize() + " Learning Coloring Book"
        subtitle = "A fun " + education_mode + " coloring book for kids"

        return {
            "title": title,
            "subtitle": subtitle,
            "keyword": education_mode,
            "niche": education_mode,
            "book_type": "educational",
            "education_mode": education_mode,
            "theme": education_mode.capitalize() + " Learning",
            "target_age": age_group,
            "total_pages": total_pages,
            "difficulty_curve": "consistent (educational content)",
            "chapters": [],
            "character_profile": {},
            "recurring_elements": [],
            "learning_objective": education_mode,
            "scenes": [],
            "generated_pages": generated_pages,
            "quality": {"valid": True, "issues": []},
            "status": "Ready for Publishing",
        }
