import os
import shutil
from PIL import Image

class DownloadAgent:
    # ✅ KDP Standard specs
    KDP_MIN_WIDTH  = 2550  # 8.5 inch @ 300 DPI
    KDP_MIN_HEIGHT = 3300  # 11 inch @ 300 DPI
    KDP_DPI        = 300
    VALID_FORMATS  = (".png", ".jpg", ".jpeg")

    def import_images(self, expected_pages):
        print("\n📥 Download Agent Running...\n")

        download_folder = "downloads"
        output_folder   = "output/images"
        report_path     = "output/images/import_report.txt"

        os.makedirs(output_folder, exist_ok=True)

        # ✅ Downloads folder check
        if not os.path.exists(download_folder):
            print(f"❌ '{download_folder}' folder nahi mila!")
            return False

        # ✅ Files sort karke lo
        files = sorted([
            f for f in os.listdir(download_folder)
            if f.lower().endswith(self.VALID_FORMATS)
        ])

        if not files:
            print(f"❌ No images found in {download_folder}/")
            return False

        print(f"  📁 Found     : {len(files)} images")
        print(f"  🎯 Expected  : {expected_pages} pages\n")

        # ✅ Stats tracking
        imported = []
        skipped  = []
        warnings = []

        for i, file in enumerate(files[:expected_pages], start=1):
            src = os.path.join(download_folder, file)
            dst = os.path.join(output_folder, f"page_{i:03}.png")

            try:
                img = Image.open(src)
                w, h = img.size

                # ✅ Size check
                if w < 800 or h < 800:
                    skipped.append(f"page_{i:03} — too small ({w}x{h})")
                    print(f"  ⚠️  Skipped  : {file} (too small: {w}x{h})")
                    continue

                # ✅ KDP warning
                if w < self.KDP_MIN_WIDTH or h < self.KDP_MIN_HEIGHT:
                    warnings.append(
                        f"page_{i:03} — low res ({w}x{h}) "
                        f"KDP needs {self.KDP_MIN_WIDTH}x{self.KDP_MIN_HEIGHT}"
                    )
                    print(f"  ⚠️  Low res  : {file} ({w}x{h}) — KDP quality low hogi")

                # ✅ RGB convert + PNG save
                if img.mode != "RGB":
                    img = img.convert("RGB")

                img.save(dst, "PNG", dpi=(self.KDP_DPI, self.KDP_DPI))
                imported.append(f"page_{i:03}.png ({w}x{h})")
                print(f"  ✅ Imported  : page_{i:03}.png ({w}x{h})")

            except Exception as e:
                skipped.append(f"{file} — error: {e}")
                print(f"  ❌ Error     : {file} — {e}")

        # ✅ Summary
        print(f"\n{'='*40}")
        print(f"  ✅ Imported  : {len(imported)}/{expected_pages}")
        print(f"  ⚠️  Warnings  : {len(warnings)}")
        print(f"  ❌ Skipped   : {len(skipped)}")

        missing = expected_pages - len(imported)
        if missing > 0:
            print(f"  📋 Missing   : {missing} images abhi banao")
        else:
            print(f"  🎉 All {expected_pages} images ready!")

        # ✅ Report save karo
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("IMPORT REPORT\n")
            f.write("="*40 + "\n\n")
            f.write(f"Expected : {expected_pages}\n")
            f.write(f"Imported : {len(imported)}\n")
            f.write(f"Skipped  : {len(skipped)}\n")
            f.write(f"Warnings : {len(warnings)}\n\n")

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

        print(f"\n  📄 Report    : {report_path}")
        print(f"{'='*40}\n")

        return len(imported) > 0