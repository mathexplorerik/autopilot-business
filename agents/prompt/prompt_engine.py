"""
==========================================================
AI Publishing OS V6
Prompt Engine — Fixed
==========================================================
"""
from agents.engines.animal_engine import AnimalEngine
from agents.prompt.prompt_builder import PromptBuilder
from agents.prompt.prompt_formatter import PromptFormatter
from agents.prompt.prompt_scorer import PromptScorer
from agents.prompt.prompt_reporter import PromptReporter
from agents.prompt.prompt_saver import PromptSaver
from agents.checkers.duplicate_engine import DuplicateEngine
from agents.data.subjects import get_subjects, SUBJECTS


class PromptEngine:

    VERSION = "V6"

    def __init__(self):
        self.scene_engine = AnimalEngine()
        self.builder      = PromptBuilder()
        self.formatter    = PromptFormatter()
        self.scorer       = PromptScorer()
        self.reporter     = PromptReporter()
        self.saver        = PromptSaver()
        self.duplicate    = DuplicateEngine()

    def build_prompt(self, niche, page, total_pages, style, line_weight, age_style, marketplace="amazon", product="coloring"):

        # ✅ Subject
        subjects = self._get_subjects(niche)
        subject  = subjects[(page - 1) % len(subjects)]

        # ✅ Complexity
        complexity = self._get_complexity(page, total_pages)

        # ✅ Scene from AnimalEngine
        scene = self.scene_engine.build(
            subject=subject,
            age_group=age_style,
            page_number=page,
            total_pages=total_pages
        )

        # ✅ Template
        template = (
            "Cute {expression} {subject} {action} {background}, "
            "{props}, {accessories}, "
            "kids coloring book page, "
            "{style}, {line_weight}, "
            "{age_style}, {complexity}, "
            "white background, centered composition, "
            "no shading, printable"
        )

        # ✅ Build prompt
        result = self.builder.build(
            scene=scene,
            style=style,
            line_weight=line_weight,
            age_style=age_style,
            complexity=complexity,
            template=template
        )

        return {
            "positive":   result["positive"],
            "negative":   result["negative"],
            "subject":    subject,
            "niche":      niche,
            "complexity": complexity,
            "page":       page,
            "scene":      scene
        }

    def build_batch(self, niche, pages, style, line_weight, age_style, marketplace="amazon", product="coloring"):
        """Complete prompt batch generate karo"""
        print(f"\n  🔧 PromptEngine {self.VERSION}")
        print(f"  📚 Niche  : {niche}")
        print(f"  📄 Pages  : {pages}\n")

        prompts = []

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
                continue

            self.duplicate.add(
                prompt=prompt["positive"],
                subject=prompt["subject"]
            )

            prompts.append(prompt)
            print(f"  ✍️  Page {page:02}/{pages} [{prompt['complexity']:12}] : {prompt['subject']}")

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