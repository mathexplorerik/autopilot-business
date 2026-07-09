"""
==========================================================
AI Publishing OS V5
Prompt Agent — Pro Level
==========================================================
"""
import os
import json
from datetime import datetime
from agents.engines.prompt_engine import PromptEngine
from agents.data.subjects import SUBJECTS, get_subjects
from agents.models.prompt import Prompt
from agents.validators.prompt_validator import PromptValidator
from agents.checkers.duplicate_engine import DuplicateEngine


class PromptAgent:

    def generate(self, report, season=None):
        print("\n✍️  Prompt Agent Running...\n")

        engine           = PromptEngine()
        validator        = PromptValidator()
        duplicate_engine = DuplicateEngine()

        # ✅ ResearchReport object ya dict dono handle karo
        if hasattr(report, 'resolved_niche'):
            niche      = report.resolved_niche.lower()
            age_group  = report.age_group
            pages      = report.pages
            subjects   = report.subjects or []
            season     = season or report.season or None
        else:
            niche     = report.get("niche", "animals").lower()
            age_group = report.get("age_group", "kids")
            pages     = report.get("pages", 40)
            subjects  = report.get("subjects", [])

        safe_niche = niche.replace(" ", "_")

        # ✅ Subjects dhundho
        if not subjects:
            subjects = self._find_subjects(niche)

        print(f"  📚 Niche      : {niche}")
        print(f"  👶 Age Group  : {age_group}")
        print(f"  📄 Pages      : {pages}")
        if season:
            print(f"  🎄 Season     : {season}")
        print(f"  🐾 Subjects   : {len(subjects)} found")

        # ✅ Complexity distribution
        q = pages // 4
        print(f"\n  📊 Distribution:")
        print(f"     🟢 Simple       : {q} pages")
        print(f"     🔵 Intermediate : {q} pages")
        print(f"     🟠 Advanced     : {q} pages")
        print(f"     🔴 Pro          : {pages - q*3} pages\n")

        # ✅ Prompts generate karo
        prompt_data       = []
        used_combos       = set()
        skipped_invalid   = 0
        skipped_duplicate = 0
        complexity_counts = {
            "simple": 0, "intermediate": 0,
            "advanced": 0, "pro": 0
        }

        for i in range(pages):
            subject = subjects[i % len(subjects)]

            # Build prompt
            result = engine.build_prompt(
                subject=subject,
                age_group=age_group,
                season=season,
                niche=niche,
                page_number=i + 1,
                total_pages=pages
            )

            positive   = result["positive"]
            negative   = result["negative"]
            complexity = result["complexity"]
            label      = result.get("label", complexity)

            # ✅ Validate
            validation = validator.validate(positive, negative)
            if not validation["valid"]:
                skipped_invalid += 1
                continue

            # ✅ Duplicate avoid — regenerate
            attempts = 0
            while positive in used_combos and attempts < 5:
                result     = engine.build_prompt(
                    subject=subject,
                    age_group=age_group,
                    season=season,
                    niche=niche,
                    page_number=i + 1,
                    total_pages=pages
                )
                positive   = result["positive"]
                negative   = result["negative"]
                complexity = result["complexity"]
                attempts  += 1

            # ✅ Duplicate engine check
            dup_check = duplicate_engine.validate(
                prompt=positive,
                subject=subject
            )
            if not dup_check["valid"]:
                skipped_duplicate += 1
                continue

            # ✅ Add to tracker
            duplicate_engine.add(prompt=positive, subject=subject)
            used_combos.add(positive)
            complexity_counts[complexity] += 1

            prompt_data.append(
                Prompt(
                    page=i + 1,
                    subject=subject,
                    niche=niche,
                    complexity=complexity,
                    label=label,
                    positive=positive,
                    negative=negative
                )
            )

            print(f"  ✍️  Page {i+1:02}/{pages} {label:20} : {subject}")

        # ✅ Summary
        print(f"\n  {'─'*40}")
        print(f"  ✅ Generated      : {len(prompt_data)}/{pages}")
        if skipped_invalid:
            print(f"  ⚠️  Invalid        : {skipped_invalid}")
        if skipped_duplicate:
            print(f"  🔁 Duplicates     : {skipped_duplicate}")

        # ✅ Save
        prompts = self._save(
            prompt_data, niche, safe_niche,
            age_group, season, pages, complexity_counts
        )

        return prompts

    def _find_subjects(self, niche):
        """Niche ke subjects dhundho"""
        from agents.data.subjects import get_subjects, SUBJECTS

        subjects = get_subjects(niche)
        if subjects:
            return subjects

        for key in SUBJECTS:
            if key in niche or niche in key:
                subjects = get_subjects(key)
                if subjects:
                    print(f"  🔍 Matched: '{key}'")
                    return subjects

        print(f"  ⚠️  Fallback: '{niche}'")
        return [niche]

    def _save(self, prompt_data, niche, safe_niche, age_group, season, pages, complexity_counts):
        """Sab files save karo"""
        os.makedirs("output/prompts", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Convert Prompt objects to dict
        data = [
            p.to_dict() if isinstance(p, Prompt) else p
            for p in prompt_data
        ]

        # ✅ Niche specific TXT
        txt_path = f"output/prompts/{safe_niche}_prompts.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"PROMPTS FOR: {niche.upper()}\n")
            f.write(f"Generated : {timestamp}\n")
            f.write(f"Total     : {len(data)} prompts\n")
            f.write("="*60 + "\n\n")
            for p in data:
                f.write(f"--- Page {p['page']:02}/{pages} | {p['subject'].upper()} | {p['label']} ---\n")
                f.write(f"POSITIVE: {p['positive']}\n")
                f.write(f"NEGATIVE: {p['negative']}\n\n")

        # ✅ Niche specific JSON
        json_path = f"output/prompts/{safe_niche}_prompts.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "niche":      niche,
                "age_group":  age_group,
                "season":     season,
                "total":      len(data),
                "generated":  timestamp,
                "complexity": complexity_counts,
                "prompts":    data
            }, f, indent=2, ensure_ascii=False)

        # ✅ Simple TXT — ChatGPT ke liye
        simple_path = f"output/prompts/{safe_niche}_simple.txt"
        with open(simple_path, "w", encoding="utf-8") as f:
            for p in data:
                f.write(p['positive'] + "\n")

        # ✅ Backward compatibility
        with open("output/prompts/prompts.txt", "w", encoding="utf-8") as f:
            for p in data:
                f.write(p['positive'] + "\n")

        with open("output/prompts/prompts.json", "w", encoding="utf-8") as f:
            json.dump({
                "niche": niche, "age_group": age_group,
                "season": season, "total": len(data),
                "prompts": data
            }, f, indent=2, ensure_ascii=False)

        print(f"  🟢 Simple         : {complexity_counts['simple']}")
        print(f"  🔵 Intermediate   : {complexity_counts['intermediate']}")
        print(f"  🟠 Advanced       : {complexity_counts['advanced']}")
        print(f"  🔴 Pro            : {complexity_counts['pro']}")
        print(f"  📄 TXT            : {txt_path}")
        print(f"  📄 JSON           : {json_path}")
        print(f"  📄 Simple         : {simple_path}")
        print(f"  {'─'*40}")

        # Return positive prompts list
        return [p['positive'] for p in data]