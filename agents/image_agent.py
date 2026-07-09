"""
==========================================================
AI Publishing OS V6
Image Agent — Pro Level
==========================================================
"""
import os
import json
import shutil
from PIL import Image
from datetime import datetime
from pathlib import Path


class ImageAgent:

    # ✅ KDP Standard
    KDP_WIDTH    = 2550
    KDP_HEIGHT   = 3300
    KDP_DPI      = 300
    MIN_WIDTH    = 1000
    MIN_HEIGHT   = 1000
    VALID_EXTS   = (".png", ".jpg", ".jpeg", ".webp")

    def prepare(self, prompts):
        print("\n🎨 Image Agent Running...\n")
        os.makedirs("output/images", exist_ok=True)

        checklist = []
        missing   = []
        ready     = []

        for i, prompt in enumerate(prompts, start=1):
            image_name = f"page_{i:03}.png"
            image_path = os.path.join("output/images", image_name)

            # Prompt string ya dict handle karo
            if isinstance(prompt, dict):
                positive = prompt.get("positive", str(prompt))
            else:
                positive = str(prompt)

            checklist.append({
                "page":     i,
                "name":     image_name,
                "path":     image_path,
                "prompt":   positive,
                "exists":   os.path.exists(image_path)
            })

            if os.path.exists(image_path):
                ready.append(image_name)
            else:
                missing.append(image_name)

        # ✅ Save checklist
        os.makedirs("output/images", exist_ok=True)
        checklist_path = "output/images/image_checklist.txt"
        json_path      = "output/images/image_checklist.json"

        with open(checklist_path, "w", encoding="utf-8") as f:
            f.write("IMAGE CHECKLIST\n")
            f.write("="*50 + "\n\n")
            for item in checklist:
                status = "✅" if item["exists"] else "⬜"
                f.write(f"{status} {item['name']}\n")
                f.write(f"   Prompt: {item['prompt'][:80]}...\n\n")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "total":   len(checklist),
                "ready":   len(ready),
                "missing": len(missing),
                "items":   checklist
            }, f, indent=2, ensure_ascii=False)

        # ✅ Summary
        print(f"  📋 Total    : {len(checklist)}")
        print(f"  ✅ Ready    : {len(ready)}")
        print(f"  ⬜ Missing  : {len(missing)}")
        print(f"  📄 Checklist: {checklist_path}")

        if not missing:
            print(f"\n  🎉 All images ready!")
        else:
            print(f"\n  ⚠️  {len(missing)} images needed")
            print(f"  💡 Run prompt_viewer.py to generate")

        return [item["prompt"] for item in checklist]

    def import_images(self, expected=None):
        print("\n📥 Image Import Running...\n")

        src_folder = "downloads"
        dst_folder = "output/images"
        os.makedirs(dst_folder, exist_ok=True)

        # ✅ Downloads folder check
        if not os.path.exists(src_folder):
            print(f"  ⚠️  '{src_folder}' folder nahi mila!")
            return False

        # ✅ Files sort karke lo
        files = sorted([
            f for f in os.listdir(src_folder)
            if f.lower().endswith(self.VALID_EXTS)
        ])

        if not files:
            print(f"  ⚠️  No images in {src_folder}/")
            return False

        print(f"  📁 Found    : {len(files)} images")
        if expected:
            print(f"  🎯 Expected : {expected} pages")

        imported  = []
        skipped   = []
        warnings  = []
        limit     = expected or len(files)

        for i, file in enumerate(files[:limit], start=1):
            src = os.path.join(src_folder, file)
            dst = os.path.join(dst_folder, f"page_{i:03}.png")

            try:
                img  = Image.open(src)
                w, h = img.size

                # ✅ Too small check
                if w < self.MIN_WIDTH or h < self.MIN_HEIGHT:
                    skipped.append(f"{file} (too small: {w}x{h})")
                    print(f"  ❌ Skipped : {file} — too small ({w}x{h})")
                    continue

                # ✅ KDP quality warning
                if w < self.KDP_WIDTH or h < self.KDP_HEIGHT:
                    warnings.append(f"page_{i:03}.png — low res ({w}x{h})")
                    print(f"  ⚠️  Low res : {file} ({w}x{h})")

                # ✅ RGB convert
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # ✅ Save with DPI
                img.save(dst, "PNG", dpi=(self.KDP_DPI, self.KDP_DPI))
                imported.append(f"page_{i:03}.png ({w}x{h})")
                print(f"  ✅ Imported : page_{i:03}.png ({w}x{h})")

            except Exception as e:
                skipped.append(f"{file} — {e}")
                print(f"  ❌ Error    : {file} — {e}")

        # ✅ Save report
        self._save_report(imported, skipped, warnings, limit)

        # ✅ Summary
        print(f"\n  {'='*40}")
        print(f"  ✅ Imported : {len(imported)}/{limit}")
        print(f"  ⚠️  Warnings : {len(warnings)}")
        print(f"  ❌ Skipped  : {len(skipped)}")

        missing = limit - len(imported)
        if missing > 0:
            print(f"  📋 Missing  : {missing} — banao aur dobara chalao")
        else:
            print(f"  🎉 All {limit} images ready!")

        return len(imported) > 0

    def _save_report(self, imported, skipped, warnings, expected):
        """Import report save karo"""
        os.makedirs("output/images", exist_ok=True)
        report_path = "output/images/import_report.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("IMAGE IMPORT REPORT\n")
            f.write("="*40 + "\n")
            f.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Expected  : {expected}\n")
            f.write(f"Imported  : {len(imported)}\n")
            f.write(f"Skipped   : {len(skipped)}\n")
            f.write(f"Warnings  : {len(warnings)}\n\n")

            if imported:
                f.write("✅ IMPORTED:\n")
                for item in imported:
                    f.write(f"  {item}\n")

            if warnings:
                f.write("\n⚠️  WARNINGS:\n")
                for w in warnings:
                    f.write(f"  {w}\n")

            if skipped:
                f.write("\n❌ SKIPPED:\n")
                for s in skipped:
                    f.write(f"  {s}\n")

        print(f"  📄 Report   : {report_path}")