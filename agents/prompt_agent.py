import os
import json
from agents.engines.prompt_engine import PromptEngine
from agents.data.subjects import SUBJECTS, get_subjects, get_age_group

class PromptAgent:
    def generate(self, report, season=None):
        print("\n✍️ Prompt Agent Running...\n")

        engine    = PromptEngine()
        niche     = report["niche"].lower()
        age_group = report.get("age_group", "kids")
        pages     = report.get("pages", 30)

        # ✅ Subjects dhundho
        subjects = get_subjects(niche)
        if not subjects:
            for key in SUBJECTS:
                if key in niche or niche in key:
                    subjects = get_subjects(key)
                    print(f"  🔍 Matched niche : '{key}'")
                    break

        if not subjects:
            subjects = [report["niche"]]
            print(f"  ⚠️  Unknown niche — using '{report['niche']}' as subject")
        else:
            print(f"  ✅ Subjects found : {len(subjects)}")

        if season:
            print(f"  🎄 Season        : {season}")

        print(f"  📄 Pages         : {pages}")
        print(f"  👶 Age Group     : {age_group}\n")

        # ✅ Prompts generate karo
        prompts       = []
        prompt_data   = []
        used_combos   = set()

        complexity_counts = {"simple": 0, "intermediate": 0, "advanced": 0, "pro": 0}

        for i in range(pages):
            subject = subjects[i % len(subjects)]

            # V3 Engine — full features
            result = engine.build_prompt(
                subject=subject,
                age_group=age_group,
                season=season,
                niche=niche,
                page_number=i + 1,
                total_pages=pages
            )

            positive = result["positive"]
            negative = result["negative"]
            complexity = result["complexity"]

            # Duplicate avoid karo
            attempts = 0
            while positive in used_combos and attempts < 5:
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
                attempts  += 1

            used_combos.add(positive)
            complexity_counts[complexity] += 1

            prompts.append(positive)
            prompt_data.append({
                "page":       i + 1,
                "subject":    subject,
                "complexity": complexity,
                "positive":   positive,
                "negative":   negative
            })

            print(f"  ✍️  Page {i+1:02}/{pages} [{complexity:8}] : {subject}")

        # ✅ Save — TXT
        os.makedirs("output/prompts", exist_ok=True)
        txt_path = "output/prompts/prompts.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            for p in prompt_data:
                f.write(f"=== Page {p['page']:02} | {p['subject']} | {p['complexity']} ===\n")
                f.write(f"POSITIVE: {p['positive']}\n")
                f.write(f"NEGATIVE: {p['negative']}\n\n")

        # ✅ Save — JSON
        json_path = "output/prompts/prompts.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "niche":      niche,
                "age_group":  age_group,
                "season":     season,
                "total":      len(prompts),
                "complexity": complexity_counts,
                "prompts":    prompt_data
            }, f, indent=2, ensure_ascii=False)

        # ✅ Summary
        print(f"\n  {'─'*40}")
        print(f"  ✅ Total Prompts : {len(prompts)}")
        print(f"  📊 🟢 Simple       : {complexity_counts['simple']}")
        print(f"  📊 🔵 Intermediate : {complexity_counts['intermediate']}")
        print(f"  📊 🟠 Advanced     : {complexity_counts['advanced']}")
        print(f"  📊 🔴 Pro          : {complexity_counts['pro']}")
        print(f"  📄 TXT           : {txt_path}")
        print(f"  📄 JSON          : {json_path}")

        return prompts