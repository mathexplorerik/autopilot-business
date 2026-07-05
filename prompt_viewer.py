import os
import json
import subprocess

def main():
    json_path = "output/prompts/prompts.json"
    if not os.path.exists(json_path):
        print("❌ Pehle python3 main.py chalao")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    prompts = data.get("prompts", [])
    total   = len(prompts)

    print(f"\n{'='*60}")
    print(f"  🎨 PROMPT VIEWER — {total} prompts")
    print(f"  Ek ek prompt dikhega — image banao phir Enter dabaao")
    print(f"{'='*60}\n")

    os.makedirs("downloads", exist_ok=True)
    subprocess.run(["open", "downloads/"])

    done = len([f for f in os.listdir("downloads") if f.endswith(".png")])
    start_from = done + 1

    if done > 0:
        print(f"  ✅ Already done: {done} images")
        print(f"  ▶️  Starting from: Prompt {start_from}\n")

    for i, prompt_data in enumerate(prompts, start=1):
        if i < start_from:
            continue

        positive   = prompt_data.get("positive", "") if isinstance(prompt_data, dict) else prompt_data
        complexity = prompt_data.get("complexity", "simple") if isinstance(prompt_data, dict) else "simple"
        subject    = prompt_data.get("subject", "") if isinstance(prompt_data, dict) else ""

        print(f"\n{'─'*60}")
        print(f"  📄 Page      : {i}/{total}")
        print(f"  🐾 Subject   : {subject}")
        print(f"  📊 Complexity: {complexity}")
        print(f"{'─'*60}")
        print(f"\n  📋 PROMPT:\n")
        print(f"  {positive}")
        print(f"\n{'─'*60}")
        print(f"  1. Prompt copy karo")
        print(f"  2. Redpanda AI pe paste karo")
        print(f"  3. Image banao aur downloads/ mein save karo")
        print(f"{'─'*60}")

        user_input = input(f"\n  Enter=Next | s=Skip | q=Quit: ").strip().lower()

        if user_input == 'q':
            print(f"\n  👋 Quit — {i-1} done")
            break
        elif user_input == 's':
            print(f"  ⏭️  Skipped {i}")
            continue
        else:
            current = len([f for f in os.listdir("downloads") if f.endswith(".png")])
            print(f"  📁 Downloads: {current} images")

    final = len([f for f in os.listdir("downloads") if f.endswith(".png")])
    print(f"\n{'='*60}")
    print(f"  🎉 Total: {final}/{total} images")
    if final >= total:
        print(f"  ✅ Sab ready! Ab python3 main.py chalao")
    else:
        print(f"  ⚠️  {total - final} baaki hain")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
