import os
from agents.engines.prompt_engine import PromptEngine
from agents.data.subjects import SUBJECTS, get_subjects, get_age_group

class PromptAgent:
    def generate(self, report):
        print("\n✍️ Prompt Agent Running...\n")

        engine = PromptEngine()
        niche = report["niche"].lower()
        age_group = report.get("age_group", "kids")
        pages = report.get("pages", 30)

        # ✅ Subjects dhundho
        subjects = get_subjects(niche)
        if not subjects:
            # Partial match try karo
            for key in SUBJECTS:
                if key in niche or niche in key:
                    subjects = get_subjects(key)
                    print(f"  🔍 Matched niche: '{key}'")
                    break

        # Fallback
        if not subjects:
            subjects = [report["niche"]]
            print(f"  ⚠️  Unknown niche — using '{report['niche']}' as subject")
        else:
            print(f"  ✅ Subjects found : {len(subjects)}")

        # ✅ Prompts generate karo
        prompts = []
        used_combos = set()

        for i in range(pages):
            subject = subjects[i % len(subjects)]
            prompt = engine.build_prompt(subject, age_group=age_group)

            # Duplicate avoid karo
            attempts = 0
            while prompt in used_combos and attempts < 5:
                prompt = engine.build_prompt(subject, age_group=age_group)
                attempts += 1

            used_combos.add(prompt)
            prompts.append(prompt)
            print(f"  ✍️  Prompt {i+1:02}/{pages} : {subject}")

        # ✅ Save karo
        os.makedirs("output/prompts", exist_ok=True)
        txt_path = "output/prompts/prompts.txt"
        json_path = "output/prompts/prompts.json"

        # TXT file
        with open(txt_path, "w", encoding="utf-8") as f:
            for prompt in prompts:
                f.write(prompt + "\n")

        # JSON file — image agent ke liye useful
        import json
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "niche": niche,
                "age_group": age_group,
                "total": len(prompts),
                "prompts": prompts
            }, f, indent=2)

        print(f"\n  ✅ {len(prompts)} prompts created")
        print(f"  📄 TXT  : {txt_path}")
        print(f"  📄 JSON : {json_path}")

        return prompts