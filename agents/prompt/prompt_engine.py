"""
==========================================================
AI Publishing OS V6
Prompt Engine — Complete
==========================================================
"""
from agents.data.knowledge.loader import KnowledgeLoader
from agents.engines.animal_engine import AnimalEngine
from agents.prompt.prompt_builder import PromptBuilder
from agents.prompt.prompt_formatter import PromptFormatter
from agents.prompt.prompt_scorer import PromptScorer
from agents.prompt.prompt_reporter import PromptReporter
from agents.prompt.prompt_saver import PromptSaver
from agents.prompt.prompt_templates import PromptTemplates
from agents.checkers.duplicate_engine import DuplicateEngine
from agents.data.subjects import get_subjects, SUBJECTS


class PromptEngine:

    VERSION = "V6"

    def __init__(self):

        self.knowledge = KnowledgeLoader()
        self.scene_engine = AnimalEngine()
        self.builder      = PromptBuilder()
        self.formatter    = PromptFormatter()
        self.scorer       = PromptScorer()
        self.reporter     = PromptReporter()
        self.saver        = PromptSaver()
        self.templates = PromptTemplates()
        self.duplicate    = DuplicateEngine()

    def build_prompt(self, niche, page, total_pages, style, line_weight, age_style, marketplace="amazon", product="coloring"):

        # ✅ Subject
        subjects = self._get_subjects(niche)
        subject  = subjects[(page - 1) % len(subjects)]

        # ✅ Complexity
        complexity = self._get_complexity(page, total_pages)
        label      = self._get_label(complexity)

        # ✅ Scene from AnimalEngine
        scene = self.scene_engine.build(
            subject=subject,
            age_group=age_style,
            page_number=page,
            total_pages=total_pages
        )

        # ✅ Template
        template = self._get_template(
            marketplace=marketplace,
            product=product
        )

        # ✅ Build prompt
        built = self.builder.build(
            scene=scene,
            style=style,
            line_weight=line_weight,
            age_style=age_style,
            complexity=complexity,
            template=template
        )

        # ✅ Score prompt
        scored = self.scorer.score({
            "positive": built["positive"]
        })

        # ✅ Metadata
        metadata = self.formatter.format_metadata(
            prompt_score=scored["score"],
            marketplace=marketplace,
            product_type=product
        )

        # ✅ Format final prompt
        return self.formatter.format(
            page=page,
            subject=subject,
            niche=niche,
            positive=built["positive"],
            negative=built["negative"],
            complexity=complexity,
            label=label,
            metadata=metadata
        )

    def build_batch(self, niche, pages, style, line_weight, age_style, marketplace="amazon", product="coloring"):
        print(f"\n  🔧 PromptEngine {self.VERSION}")
        print(f"  📚 Niche  : {niche}")
        print(f"  📄 Pages  : {pages}\n")

        prompts           = []
        skipped_duplicate = 0
        scores            = []

        for page in range(1, pages + 1):
            prompt = self.build_prompt(
                niche=niche,
                page=page,
                total_pages=pages,
                style=style,
                line_weight=line_weight,
                age_style=age_style,
                marketplace=marketplace,
                product=product
            )

            # ✅ Duplicate check
            dup = self.duplicate.validate(
                prompt=prompt["positive"],
                subject=prompt["subject"]
            )
            if not dup["valid"]:
                skipped_duplicate += 1
                continue

            self.duplicate.add(
                prompt=prompt["positive"],
                subject=prompt["subject"]
            )

            prompts.append(prompt)
            score = prompt["metadata"].get("prompt_score", 100)
            scores.append(score)

            grade = self.scorer.grade(score)
            print(f"  ✍️  Page {page:02}/{pages} [{prompt['complexity']:12}] {grade} : {prompt['subject']}")

        if skipped_duplicate:
            print(f"\n  🔁 Duplicates skipped: {skipped_duplicate}")

        # ✅ Report
        report = self.reporter.report(prompts)

        return {
            "prompts": prompts,
            "report":  report,
            "total":   len(prompts),
            "version": self.VERSION
        }

    def save_batch(self, prompts, niche, age_group, season=""):
        return self.saver.save(
            prompts=prompts,
            niche=niche,
            age_group=age_group,
            season=season
        )

    def _get_subjects(self, niche):
        subjects = get_subjects(niche)
        if subjects:
            return subjects
        for key in SUBJECTS:
            if key in niche or niche in key:
                s = get_subjects(key)
                if s:
                    return s
        return [niche]

    def _get_complexity(self, page, total):
        ratio = page / total
        if ratio <= 0.25:   return "simple"
        elif ratio <= 0.50: return "intermediate"
        elif ratio <= 0.75: return "advanced"
        return "pro"

    def _get_label(self, complexity):
        labels = {
            "simple":       "🟢 SIMPLE",
            "intermediate": "🔵 INTERMEDIATE",
            "advanced":     "🟠 ADVANCED",
            "pro":          "🔴 PRO"
        }
        return labels.get(complexity, complexity)
    
    def _get_template(
        self,
        marketplace="amazon",
        product="coloring"
    ):
        """
        Resolve prompt template.

        Priority:
        1. Knowledge database
        2. Built-in templates
        """

        prompt = self.knowledge.load_prompt("coloring_book")

        if prompt:
            return prompt["positive_template"]

        return self.templates.get(
            marketplace=marketplace,
            product=product
        )