import os
import shutil
from PIL import Image

class ImageAgent:
    def prepare(self, prompts):
        print("\n🎨 Image Agent Running...\n")
        os.makedirs("output/images", exist_ok=True)
        checklist = []
        missing = []
        
        for i, prompt in enumerate(prompts, start=1):
            image_name = f"page_{i:03}.png"
            image_path = os.path.join("output/images", image_name)
            checklist.append(f"{image_name} -> {prompt}")
            if not os.path.exists(image_path):
                missing.append(image_name)

        checklist_path = os.path.join("output/images", "image_checklist.txt")
        with open(checklist_path, "w", encoding="utf-8") as f:
            f.write("\n".join(checklist))

        print("✅ Image checklist created.")
        print(f"📋 Total Images  : {len(checklist)}")
        print(f"✅ Ready         : {len(checklist) - len(missing)}")
        
        if missing:
            print(f"⚠️  Missing       : {len(missing)}")
        else:
            print("🎉 All images ready!")
            
        return checklist

    def import_images(self):
        print("\n📥 Importing Images...\n")
        os.makedirs("output/images", exist_ok=True)

        if not os.path.exists("downloads"):
            print("⚠️ downloads folder not found.")
            return

        files = sorted(
            f for f in os.listdir("downloads")
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        )

        if not files:
            print("⚠️ No images found in downloads.")
            return

        imported = 0
        skipped = 0

        for i, file in enumerate(files, start=1):
            src = os.path.join("downloads", file)
            dst = os.path.join("output/images", f"page_{i:03}.png")

            try:
                # ✅ Pro: Size check + KDP ke liye resize
                img = Image.open(src)
                w, h = img.size

                # KDP standard: 2550x3300 (8.5x11 @ 300 DPI)
                if w < 1000 or h < 1000:
                    print(f"⚠️  Skipped (too small): {file}")
                    skipped += 1
                    continue

                # PNG mein save karo
                img.save(dst, "PNG")
                print(f"✅ Imported: page_{i:03}.png ({w}x{h})")
                imported += 1

            except Exception as e:
                print(f"❌ Error: {file} — {e}")
                skipped += 1

        print(f"\n🎉 Done! Imported: {imported} | Skipped: {skipped}")