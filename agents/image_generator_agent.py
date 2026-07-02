import os
import time
import json
from datetime import datetime
from google import genai
import config

class ImageGeneratorAgent:

    # ✅ KDP Standard
    KDP_WIDTH  = 2550  # 8.5 inch @ 300 DPI
    KDP_HEIGHT = 3300  # 11 inch @ 300 DPI

    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

    def generate(self, prompts, niche="book"):
        print("\n🖼️  Image Generator Agent Running...\n")
        print(f"  📚 Niche   : {niche}")
        print(f"  📄 Total   : {len(prompts)} images\n")

        os.makedirs("output/images", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        # ✅ Stats
        success  = []
        failed   = []
        skipped  = []
        start    = time.time()

        for i, prompt_data in enumerate(prompts, start=1):

            # Prompt string ya dict dono handle karo
            if isinstance(prompt_data, dict):
                positive   = prompt_data.get("positive", "")
                complexity = prompt_data.get("complexity", "simple")
            else:
                positive   = prompt_data
                complexity = "simple"

            filename = f"page_{i:03}.png"
            filepath = os.path.join("output/images", filename)

            # ✅ Already exist? Skip karo
            if os.path.exists(filepath):
                skipped.append(filename)
                print(f"  ⏭️  [{i:02}/{len(prompts)}] {filename} — already exists, skipped")
                continue

            print(f"  🎨 [{i:02}/{len(prompts)}] {filename} [{complexity}]")
            print(f"       Prompt: {positive[:60]}...")

            try:
                response = self.client.models.generate_images(
                    model="gemini-2.5-flash-image-preview",
                    prompt=positive
                )

                saved = False
                for part in response.generated_images:
                    part.image.save(filepath)
                    saved = True
                    break

                if saved:
                    size = os.path.getsize(filepath)
                    success.append(filename)
                    print(f"  ✅ Saved — {size/1024:.1f} KB")
                else:
                    failed.append(filename)
                    print(f"  ❌ No image returned")

            except Exception as e:
                failed.append(filename)
                print(f"  ❌ Failed: {e}")

                # Rate limit error → wait karo
                if "429" in str(e) or "quota" in str(e).lower():
                    print(f"  ⏳ Rate limit — waiting 30s...")
                    time.sleep(30)
                    continue

            time.sleep(2)

        # ✅ Summary
        elapsed = time.time() - start
        mins    = int(elapsed // 60)
        secs    = int(elapsed % 60)

        print(f"\n  {'='*40}")
        print(f"  ✅ Success  : {len(success)}/{len(prompts)}")
        print(f"  ⏭️  Skipped  : {len(skipped)}")
        print(f"  ❌ Failed   : {len(failed)}")
        print(f"  ⏱️  Time     : {mins}m {secs}s")

        if failed:
            print(f"\n  ❌ Failed images:")
            for f in failed:
                print(f"     {f}")

        # ✅ Report save karo
        report = {
            "niche":     niche,
            "total":     len(prompts),
            "success":   len(success),
            "skipped":   len(skipped),
            "failed":    len(failed),
            "time":      f"{mins}m {secs}s",
            "generated": success,
            "failed_list": failed,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        report_path = "output/images/generation_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"  📄 Report   : {report_path}")
        print(f"  {'='*40}\n")

        return success