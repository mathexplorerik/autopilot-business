"""
==========================================================
AI Publishing OS V7
Generation Pipeline
Version : 1.0.0
==========================================================
"""

from __future__ import annotations
from typing import Dict, List, Optional

from agents.data.knowledge.engine import KnowledgeEngine
from agents.prompt.prompt_engine_v8 import PromptEngineV8
from agents.image_engine import (
    ImageEngine,
    ImageMetadata,
)

from agents.engines.animal_engine import AnimalEngine
from agents.checkers.duplicate_checker import DuplicateChecker


class GenerationPipeline:
    """
    Central AI Generation Pipeline.

    Responsibilities
    ----------------
    • Load knowledge
    • Select subjects
    • Generate prompts
    • Prevent duplicates
    • Build metadata
    • Export pages
    """

    MAX_RETRIES = 10

    def __init__(self):

        self.knowledge = KnowledgeEngine()

        self.animal_engine = AnimalEngine()

        self.prompt_engine = PromptEngineV8()

        self.image_engine = ImageEngine()

        self.duplicate_checker = DuplicateChecker()

        self.reset()

    # --------------------------------------------------

    def reset(self):

        self.pages: List[Dict] = []

        self.subjects: List[str] = []

        self.current_subject = 0

        self.keyword = ""

        self.book_type = ""

        self.age_group = "kids"

        self.total_pages = 0

        self.duplicate_checker.reset()

        self.character_profile = {}

    # --------------------------------------------------

    def configure(
        self,
        keyword: str,
        book_type: str,
        age_group: str,
        total_pages: int,
        provider: str = "manual",
        character_profile: dict = None,
    ):

        self.reset()

        self.keyword = keyword.lower().strip()

        self.book_type = book_type

        self.age_group = age_group

        self.total_pages = total_pages

        self.provider = provider.lower().strip()

        self.character_profile = character_profile or {}

    # --------------------------------------------------

    def load_subjects(self):
        """
        Load subjects from the Knowledge Engine.

        Supports both:
        - List[str]
        - Dict containing a "subjects" key
        """
        try:

            data = self.knowledge.subjects(
            self.keyword
        )

        except Exception:

            data = []

        # Case 1: Already a list
        if isinstance(data, list):

            self.subjects = data

        # Case 2: Dictionary
        elif isinstance(data, dict):

            self.subjects = data.get(
                "subjects",
                []
        )

        # Unknown format
        else:

            self.subjects = []

        # Final fallback
        if not self.subjects:

            self.subjects = [self.keyword]

        # ✅ Story mode uses a single fixed subject for continuity
        if self.book_type == "story" and self.subjects:
            self.subjects = [self.subjects[0]]

        return self.subjects
    
        # --------------------------------------------------

    def next_subject(self):
        """
        Return the next subject in rotation.
        """

        if not self.subjects:
            return self.keyword

        subject = self.subjects[self.current_subject]

        self.current_subject += 1

        if self.current_subject >= len(self.subjects):
            self.current_subject = 0

        return subject

        # --------------------------------------------------

    def generate_scene(
        self,
        subject: str,
        page: int,
    ) -> Dict:
        """
        Generate one scene using Animal Engine.
        """

        return self.animal_engine.build(
            subject=subject,
            age_group=self.age_group,
            page_number=page,
            total_pages=self.total_pages,
            story_mode=(self.book_type == "story"),
            character_profile=self.character_profile,
        )

    # --------------------------------------------------

    def validate_scene(
        self,
        scene: Dict,
    ) -> bool:
        """
        Basic validation.
        """

        required = [
            "positive",
            "negative",
            "scene",
            "background",
            "action",
            "pose",
            "expression",
            "subject",
        ]

        for field in required:

            if field not in scene:

                return False

            if scene[field] in ("", None):

                return False

        return True

    # --------------------------------------------------

    def generate_unique_scene(
        self,
        subject: str,
        page: int,
    ) -> Dict:
        """
        Retry until a unique prompt is generated.
        """

        retries = 0

        while retries < self.MAX_RETRIES:

            scene = self.generate_scene(
                subject,
                page,
            )

            if not self.validate_scene(scene):

                retries += 1

                continue

            prompt = scene["positive"]

            if self.duplicate_checker.is_duplicate(prompt):

                retries += 1

                continue

            self.duplicate_checker.add_prompt(prompt)

            return scene

        raise RuntimeError(
            f"Unable to generate unique scene after {self.MAX_RETRIES} retries."
        )

    # --------------------------------------------------

    def build_page(
        self,
        page: int,
        scene: Dict,
    ) -> Dict:
        """
        Convert scene into export-ready page.
        """
        prompt_data = self.prompt_engine.build_final(
            page=page,
            keyword=self.keyword,
            subject=scene["subject"],
            scene=scene,
        )

        prompt = prompt_data["positive"]

        metadata = ImageMetadata(
            provider=self.provider,
            prompt=prompt,
            output_path=f"output/{self.keyword}/page_{page:03d}",
        )

        result = self.image_engine.generate(metadata)

        return {

            "page": page,

            "keyword": self.keyword,

            "book_type": self.book_type,

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
		            
		    "prompt": prompt,

            "image": result,
        }
    
        # --------------------------------------------------

    def generate(self) -> List[Dict]:
        """
        Generate the complete book.
        """

        self.load_subjects()

        self.pages = []

        for page in range(1, self.total_pages + 1):

            subject = self.next_subject()

            scene = self.generate_unique_scene(
                subject=subject,
                page=page,
            )

            page_data = self.build_page(
                page=page,
                scene=scene,
            )

            self.generate_image(page_data)

            self.pages.append(page_data)

        return self.pages

    # --------------------------------------------------

    def total_generated(self) -> int:
        """
        Total generated pages.
        """

        return len(self.pages)

    # --------------------------------------------------

    def progress(self) -> Dict:
        """
        Current pipeline progress.
        """

        total = self.total_pages

        generated = len(self.pages)

        percent = 0

        if total:

            percent = round(
                (generated / total) * 100,
                2,
            )

        return {
            "generated": generated,
            "total": total,
            "progress": percent,
        }

    # --------------------------------------------------

    def statistics(self) -> Dict:
        """
        Generation statistics.
        """

        complexity = {}

        for page in self.pages:

            level = page["complexity"]

            complexity[level] = (
                complexity.get(level, 0) + 1
            )

        return {

            "pages": len(self.pages),

            "subjects_loaded": len(self.subjects),

            "unique_prompts":
                self.duplicate_checker.total(),

            "duplicates_removed":
                self.duplicate_checker.duplicates(),

            "complexity_distribution":
                complexity,
        }

    # --------------------------------------------------

    def summary(self) -> Dict:
        """
        Small generation summary.
        """

        return {

            "keyword": self.keyword,

            "book_type": self.book_type,

            "age_group": self.age_group,

            "pages": len(self.pages),

            "subjects": len(self.subjects),

            "duplicates":
                self.duplicate_checker.duplicates(),
        }
        # --------------------------------------------------

    def get_page(
        self,
        page: int,
    ) -> Optional[Dict]:
        """
        Return a page by page number.
        """

        if page < 1:
            return None

        if page > len(self.pages):
            return None

        return self.pages[page - 1]

    # --------------------------------------------------

    def preview(
        self,
        pages: int = 5,
    ) -> List[Dict]:
        """
        Return first N generated pages.
        """

        return self.pages[:pages]

    # --------------------------------------------------

    def find_subject(
        self,
        subject: str,
    ) -> List[Dict]:
        """
        Find all pages for a subject.
        """

        subject = subject.lower().strip()

        results = []

        for page in self.pages:

            if page["subject"].lower() == subject:

                results.append(page)

        return results

    # --------------------------------------------------

    def export(self) -> Dict:
        """
        Export complete pipeline result.
        """

        return {

            "keyword": self.keyword,

            "book_type": self.book_type,

            "age_group": self.age_group,

            "total_pages": self.total_pages,

            "subjects": self.subjects,

            "pages": self.pages,

            "statistics": self.statistics(),

            "summary": self.summary(),
        }

    # --------------------------------------------------

    def has_pages(self) -> bool:
        """
        True if pages have been generated.
        """

        return len(self.pages) > 0

    # --------------------------------------------------

    def clear(self):
        """
        Clear pipeline state.
        """

        self.reset()

    # --------------------------------------------------

    def first_page(self) -> Optional[Dict]:
        """
        Return first generated page.
        """

        if not self.pages:

            return None

        return self.pages[0]

    # --------------------------------------------------

    def last_page(self) -> Optional[Dict]:
        """
        Return last generated page.
        """

        if not self.pages:

            return None

        return self.pages[-1]

    # --------------------------------------------------

    def all_pages(self) -> List[Dict]:
        """
        Return all pages.
        """

        return list(self.pages)
        # --------------------------------------------------

    def available_subjects(self) -> List[str]:
        """
        Return loaded subjects.
        """

        return list(self.subjects)

    # --------------------------------------------------

    def duplicate_statistics(self) -> Dict:
        """
        Duplicate checker statistics.
        """

        return self.duplicate_checker.statistics()

    # --------------------------------------------------

    def reload(self):
        """
        Reload subjects from knowledge engine.
        """

        self.load_subjects()

    # --------------------------------------------------

    def regenerate_page(
        self,
        page: int,
    ) -> Optional[Dict]:
        """
        Regenerate a single page.
        """

        if page < 1 or page > self.total_pages:
            return None

        subject = self.subjects[
            (page - 1) % len(self.subjects)
        ]

        scene = self.generate_unique_scene(
            subject=subject,
            page=page,
        )

        page_data = self.build_page(
            page=page,
            scene=scene,
        )

        if page <= len(self.pages):
            self.pages[page - 1] = page_data
        else:
            self.pages.append(page_data)

        return page_data

    # --------------------------------------------------

    def health(self) -> Dict:
        """
        Pipeline health information.
        """

        return {

            "healthy": True,

            "knowledge_loaded": len(self.subjects) > 0,

            "pages_generated": len(self.pages),

            "duplicates": self.duplicate_checker.duplicates(),

            "unique_prompts": self.duplicate_checker.total(),
        }
    
    def generate_image(
        self,
        page: Dict,
    ) -> Dict:
        """
        Generate image for one page.
        """

        metadata = ImageMetadata(
            provider="manual",
            prompt=page["prompt"],
            negative_prompt=page["negative"],
            output_path=f"output/{self.keyword}/page_{page['page']:03d}",
        )

        return self.image_engine.generate(metadata)

    # --------------------------------------------------

    def __len__(self):

        return len(self.pages)

    # --------------------------------------------------

    def __iter__(self):

        return iter(self.pages)

    # --------------------------------------------------

    def __getitem__(self, index):

        return self.pages[index]

    # --------------------------------------------------

    def __contains__(self, subject):

        subject = str(subject).lower()

        return any(
            page["subject"].lower() == subject
            for page in self.pages
        )

    # --------------------------------------------------

    def __repr__(self):

        return (
            f"<GenerationPipeline "
            f"keyword='{self.keyword}' "
            f"pages={len(self.pages)} "
            f"subjects={len(self.subjects)}>"
        )

    # --------------------------------------------------

    def __str__(self):

        return (
            f"GenerationPipeline("
            f"keyword={self.keyword}, "
            f"pages={len(self.pages)})"
        )

    # --------------------------------------------------
    # Future Extension Hooks
    # --------------------------------------------------

    def apply_prompt_engine(self):
        """
        Future hook for Prompt Engine.
        """
        pass

    def apply_diversity_checker(self):
        """
        Future hook for Diversity Checker.
        """
        pass

    def apply_similarity_checker(self):
        """
        Future hook for Similarity Checker.
        """
        pass

    def apply_quality_checker(self):
        """
        Future hook for Quality Checker.
        """
        pass