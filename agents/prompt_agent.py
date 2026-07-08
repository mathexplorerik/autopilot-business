import os
import json
from datetime import datetime
from agents.engines.prompt_engine import PromptEngine
from agents.data.subjects import SUBJECTS, get_subjects, get_age_group
from agents.models.prompt import Prompt
from agents.validators.prompt_validator import PromptValidator

class PromptAgent:

    def generate(self, report, season=None):
        print("\n✍️  Prompt Agent Running...\n")

        engine    = PromptEngine()
        validator = PromptValidator()
        niche     = report["niche"].lower()
        age_group = report.get("age_group", "kids")
        pages     = report.get("pages", 30)
        safe_niche = niche.replace(" ", "_")

        # ✅ Subjects dhundho
        subjects = self._find_subjects(niche)

        print(f"  📚 Niche      : {niche}")
        print(f"  👶 Age Group  : {age_group}")
        print(f"  📄 Pages      : {pages}")
        if season:
            print(f"  🎄 Season     : {season}")
        print(f"  🐾 Subjects   : {len(subjects)} found\n")

        # ✅ Complexity distribution
        simple_count       = pages // 4
        intermediate_count = pages // 4
        advanced_count     = pages // 4
        pro_count          = pages - simple_count - intermediate_count - advanced_count

        print(f"  📊 Distribution:")
        print(f"     🟢 Simple       : {simple_count} pages")
        print(f"     🔵 Intermediate : {intermediate_count} pages")
        print(f"     🟠 Advanced     : {advanced_count} pages")
        print(f"     🔴 Pro          : {pro_count} pages\n")

        # ✅ Prompts generate karo
        prompts      = []
        prompt_data  = []
        used_combos  = set()
        complexity_counts = {
            "simple": 0,
            "intermediate": 0,
            "advanced": 0,
            "pro": 0
        }

        for i in range(pages):
            subject = subjects[i % len(subjects)]

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
            validation = validator.validate(
                positive,
                negative
            )

            if not validation["valid"]:
                print(f"⚠️ Invalid Prompt: {validation['errors']}")
                continue

            # ✅ Duplicate avoid karo
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

        # ✅ Save files
        self._save(prompt_data, prompts, niche, safe_niche, age_group, season, pages, complexity_counts)

        return prompts

    def _find_subjects(self, niche):
        """Niche ke subjects dhundho"""
        # Direct match
        subjects = get_subjects(niche)
        if subjects:
            return subjects

        # Partial match
        for key in SUBJECTS:
            if key in niche or niche in key:
                subjects = get_subjects(key)
                if subjects:
                    print(f"  🔍 Matched niche: '{key}'")
                    return subjects

        # Fallback
        print(f"  ⚠️  Unknown niche — using '{niche}' as subject")
        return [niche]

    def _save(self, prompt_data, prompts, niche, safe_niche, age_group, season, pages, complexity_counts):
        """Sab files save karo — niche specific naming"""
        os.makedirs("output/prompts", exist_ok=True)
        prompt_data = [
            p.to_dict() if isinstance(p, Prompt) else p
            for p in prompt_data
        ]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # ✅ 1. Niche specific TXT — ChatGPT/Redpanda ke liye
        txt_path = f"output/prompts/{safe_niche}_prompts.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"PROMPTS FOR: {niche.upper()}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Total: {pages} prompts\n")
            f.write("="*60 + "\n\n")
            for p in prompt_data:  
                f.write(f"--- Page {p['page']:02}/{pages} | {p['subject'].upper()} | {p['label']} ---\n")
                f.write(f"POSITIVE: {p['positive']}\n")
                f.write(f"NEGATIVE: {p['negative']}\n\n")

        # ✅ 2. Niche specific JSON — system ke liye
        json_path = f"output/prompts/{safe_niche}_prompts.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "niche":      niche,
                "age_group":  age_group,
                "season":     season,
                "total":      pages,
                "generated":  timestamp,
                "complexity": complexity_counts,
                "prompts":    prompt_data
            }, f, indent=2, ensure_ascii=False)

        # ✅ 3. Simple TXT — prompt viewer ke liye
        simple_path = f"output/prompts/{safe_niche}_simple.txt"
        with open(simple_path, "w", encoding="utf-8") as f:
            for p in prompt_data:
                f.write(p['positive'] + "\n")

        # ✅ 4. Latest prompts — backward compatibility
        with open("output/prompts/prompts.txt", "w", encoding="utf-8") as f:
            for p in prompt_data:
                f.write(p['positive'] + "\n")

        with open("output/prompts/prompts.json", "w", encoding="utf-8") as f:
            json.dump({
                "niche":      niche,
                "age_group":  age_group,
                "season":     season,
                "total":      pages,
                "prompts":    prompt_data
            }, f, indent=2, ensure_ascii=False)

        # ✅ Summary print
        print(f"\n  {'─'*40}")
        print(f"  ✅ Total Prompts  : {len(prompts)}")
        print(f"  🟢 Simple         : {complexity_counts['simple']}")
        print(f"  🔵 Intermediate   : {complexity_counts['intermediate']}")
        print(f"  🟠 Advanced       : {complexity_counts['advanced']}")
        print(f"  🔴 Pro            : {complexity_counts['pro']}")
        print(f"  📄 TXT            : {txt_path}")
        print(f"  📄 JSON           : {json_path}")
        print(f"  📄 Simple TXT     : {simple_path}")
        print(f"  {'─'*40}")