"""
==========================================================
AI Publishing OS V7
Production Scene Planner
Version : 3.0
==========================================================
"""

from __future__ import annotations

from typing import Dict, List, Optional

from agents.engines.animal_engine import AnimalEngine
from agents.checkers.duplicate_checker import DuplicateChecker
from agents.data.subjects import get_subjects


class ScenePlanner:
    """
    Production Scene Planner

    Responsibilities
    ----------------
    • Load subjects from knowledge database
    • Rotate subjects automatically
    • Generate scenes using Animal Engine
    • Prevent duplicate prompts
    • Retry duplicate generations
    • Build page metadata
    • Generate statistics
    • Preview support
    • Export-ready output
    """

    MAX_RETRIES = 10

    def __init__(self):

        self.engine = AnimalEngine()

        self.duplicates = DuplicateChecker()

        self.reset()

    # --------------------------------------------------

    def reset(self):

        """
        Reset planner state.
        """

        self.subjects: List[str] = []

        self.generated: List[Dict] = []

        self.current_subject = 0

        self.duplicates.reset()

    # --------------------------------------------------

    def load_subjects(
        self,
        keyword: str,
    ) -> List[str]:

        keyword = keyword.lower().strip()

        subjects = get_subjects(keyword)

        if not subjects:
            subjects = [keyword]

        self.subjects = subjects

        return subjects

    # --------------------------------------------------

    def next_subject(self) -> str:

        if not self.subjects:
            return "animal"

        subject = self.subjects[self.current_subject]

        self.current_subject += 1

        if self.current_subject >= len(self.subjects):
            self.current_subject = 0

        return subject

    # --------------------------------------------------

    def generate_scene(
        self,
        subject: str,
        age_group: str,
        page: int,
        total_pages: int,
        story_mode: bool = False,
        character_profile: Dict = None,
    ) -> Dict:

        return self.engine.build(
            subject=subject,
            age_group=age_group,
            page_number=page,
            total_pages=total_pages,
            story_mode=story_mode,
            character_profile=character_profile,
        )

    # --------------------------------------------------

    def unique_scene(
        self,
        subject: str,
        age_group: str,
        page: int,
        total_pages: int,
        story_mode: bool = False,
        character_profile: Dict = None,
    ) -> Dict:

        retries = 0

        while retries < self.MAX_RETRIES:

            scene = self.generate_scene(
                subject,
                age_group,
                page,
                total_pages,
                story_mode,
                character_profile,
            )

            prompt = scene["positive"]

            if not self.duplicates.is_duplicate(prompt):

                self.duplicates.add_prompt(prompt)

                return scene

            retries += 1

        return scene
        # --------------------------------------------------

    def build_page(
        self,
        scene: Dict,
        page: int,
        niche: str,
    ) -> Dict:
        """
        Build a complete page object.
        """

        return {
            "page": page,
            "niche": niche,
            "subject": scene["subject"],

            "positive": scene["positive"],
            "negative": scene["negative"],

            "scene": scene["scene"],
            "background": scene["background"],
            "action": scene["action"],
            "pose": scene["pose"],
            "expression": scene["expression"],

            "props": scene["props"],
            "accessories": scene["accessories"],

            "complexity": scene["complexity"],
            "age_group": scene["age_group"],

            "chapter": scene.get("chapter"),
            "story_beat": scene.get("story_beat"),
            "mood_hint": scene.get("mood_hint"),
            "book_mode": scene.get("book_mode"),
        }

    # --------------------------------------------------

    def plan(
        self,
        keyword: str,
        total_pages: int,
        age_group: str = "kids",
        book_type: str = "niche",
        character_profile: Dict = None,
    ) -> List[Dict]:
        """
        Generate a complete book plan.

        book_type="niche": rotates through multiple subjects per page,
                          no story continuity (original behavior).
        book_type="story": single fixed subject for the whole book,
                          story_mode=True drives narrative continuity.
        """

        self.reset()

        keyword = keyword.lower().strip()

        self.load_subjects(keyword)

        story_mode = book_type == "story"

        if story_mode:
            fixed_subject = self.subjects[0] if self.subjects else keyword

        pages = []

        for page in range(1, total_pages + 1):

            subject = fixed_subject if story_mode else self.next_subject()

            scene = self.unique_scene(
                subject=subject,
                age_group=age_group,
                page=page,
                total_pages=total_pages,
                story_mode=story_mode,
                character_profile=character_profile,
            )

            page_data = self.build_page(
                scene=scene,
                page=page,
                niche=keyword,
            )

            pages.append(page_data)

            self.generated.append(page_data)

        return pages

    # --------------------------------------------------

    def statistics(self) -> Dict:
        """
        Planner statistics.
        """

        complexities = {}

        for page in self.generated:

            level = page["complexity"]

            complexities[level] = (
                complexities.get(level, 0) + 1
            )

        return {

            "pages": len(self.generated),

            "subjects_loaded": len(self.subjects),

            "unique_prompts":
                self.duplicates.total(),

            "duplicates_found":
                self.duplicates.duplicates(),

            "complexity_distribution":
                complexities,
        }

    # --------------------------------------------------

    def preview(
        self,
        keyword: str,
        pages: int = 5,
        age_group: str = "kids",
    ) -> List[Dict]:
        """
        Generate preview pages.
        """

        return self.plan(
            keyword=keyword,
            total_pages=pages,
            age_group=age_group,
        )
        # --------------------------------------------------

    def get_page(
        self,
        page: int,
    ) -> Optional[Dict]:
        """
        Return a page by number.
        """

        if page <= 0:
            return None

        if page > len(self.generated):
            return None

        return self.generated[page - 1]

    # --------------------------------------------------

    def pages(self) -> List[Dict]:
        """
        Return all generated pages.
        """

        return list(self.generated)

    # --------------------------------------------------

    def available_subjects(
        self,
        keyword: str,
    ) -> List[str]:
        """
        Return all subjects for a niche.
        """

        return get_subjects(
            keyword.lower().strip()
        )

    # --------------------------------------------------

    def subject_count(
        self,
        keyword: str,
    ) -> int:
        """
        Return number of subjects available.
        """

        return len(
            self.available_subjects(keyword)
        )

    # --------------------------------------------------

    def export(self) -> Dict:
        """
        Export planner output.
        """

        return {

            "pages": self.generated,

            "statistics": self.statistics(),

            "subjects": self.subjects,

            "duplicates": self.duplicates.statistics(),
        }

    # --------------------------------------------------

    def summary(self) -> Dict:
        """
        Small planner summary.
        """

        return {

            "total_pages": len(self.generated),

            "subjects_used": len(self.subjects),

            "unique_prompts":
                self.duplicates.total(),

            "duplicates_removed":
                self.duplicates.duplicates(),
        }

    # --------------------------------------------------

    def clear(self):
        """
        Clear planner state.
        """

        self.reset()

    # --------------------------------------------------

    def __len__(self):

        return len(self.generated)

    # --------------------------------------------------

    def __iter__(self):

        return iter(self.generated)

    # --------------------------------------------------

    def __repr__(self):

        return (
            f"<ScenePlanner "
            f"pages={len(self.generated)} "
            f"subjects={len(self.subjects)}>"
        )