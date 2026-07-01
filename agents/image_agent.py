import os
import shutil


class ImageAgent:

    def prepare(self, prompts):

        print("\n🎨 Image Agent Running...\n")

        os.makedirs("output/images", exist_ok=True)

        checklist = []
        missing = []

        for i, prompt in enumerate(prompts, start=1):

            image_name = f"page_{i:03}.png"
            image_path = f"output/images/{image_name}"

            checklist.append(f"{image_name} -> {prompt}")

            if not os.path.exists(image_path):
                missing.append(image_name)

        with open("output/images/image_checklist.txt", "w", encoding="utf-8") as f:
            for item in checklist:
                f.write(item + "\n")

        print("✅ Image checklist created.")
        print(f"📋 Total: {len(checklist)} images needed")

        if missing:
            print(f"⚠️ Missing: {len(missing)} images abhi download karo")
        else:
            print("🎉 Sab images ready hain!")

        return checklist

    def import_images(self):

        print("\n📥 Importing Images...\n")

        os.makedirs("output/images", exist_ok=True)

        files = sorted(
            [
                f for f in os.listdir("downloads")
                if f.lower().endswith(".png")
            ]
        )

        for i, file in enumerate(files, start=1):

            src = os.path.join("downloads", file)
            dst = os.path.join(
                "output/images",
                f"page_{i:03}.png"
            )

            shutil.copy(src, dst)

            print(f"Copied -> {dst}")

        print("\n✅ Images imported.")