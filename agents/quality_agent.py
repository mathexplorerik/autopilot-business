import os
import json
from datetime import datetime

class QualityAgent:
    def check(self, book, report=None, prompts=None, seo=None):
        print("\n🔍 Quality Agent Running...\n")

        issues   = []
        warnings = []
        passed   = []

        # ✅ Book checks
        if not book.get("title"):
            issues.append("❌ Title missing")
        else:
            passed.append(f"✅ Title     : {book['title']}")

        if not book.get("pages"):
            issues.append("❌ Pages missing")
        else:
            passed.append(f"✅ Pages     : {book['pages']}")

        if not book.get("niche"):
            issues.append("❌ Niche missing")
        else:
            passed.append(f"✅ Niche     : {book['niche']}")

        # ✅ Prompts check
        if prompts:
            if book.get("pages") and len(prompts) != book["pages"]:
                warnings.append(
                    f"⚠️  Prompts {len(prompts)} != Pages {book['pages']}"
                )
            else:
                passed.append(f"✅ Prompts   : {len(prompts)} generated")

        # ✅ SEO check
        if seo:
            if not seo.get("title"):
                issues.append("❌ SEO title missing")
            else:
                passed.append(f"✅ SEO Title : {seo['title'][:40]}...")

            if not seo.get("description"):
                warnings.append("⚠️  SEO description missing")

        # ✅ Files check
        files_to_check = [
            ("output/books",   "Books folder"),
            ("output/prompts", "Prompts folder"),
        ]
        for path, name in files_to_check:
            if os.path.exists(path):
                passed.append(f"✅ {name} exists")
            else:
                warnings.append(f"⚠️  {name} not found")

        # ✅ Images check
        images_path = "output/images"
        if os.path.exists(images_path):
            images = [
                f for f in os.listdir(images_path)
                if f.endswith(".png") and f.startswith("page_")
            ]
            if images:
                passed.append(f"✅ Images    : {len(images)} found")
            else:
                warnings.append("⚠️  No images in output/images/")
        else:
            warnings.append("⚠️  Images folder not found")

        # ✅ Print results
        print("  " + "\n  ".join(passed))
        if warnings:
            print("\n  " + "\n  ".join(warnings))
        if issues:
            print("\n  " + "\n  ".join(issues))

        # ✅ Save report
        os.makedirs("output/reports", exist_ok=True)
        report_path = "output/reports/quality_report.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"QUALITY REPORT\n")
            f.write(f"{'='*40}\n")
            f.write(f"Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Niche   : {book.get('niche', 'N/A')}\n\n")
            f.write("PASSED:\n")
            for p in passed:
                f.write(f"  {p}\n")
            if warnings:
                f.write("\nWARNINGS:\n")
                for w in warnings:
                    f.write(f"  {w}\n")
            if issues:
                f.write("\nISSUES:\n")
                for i in issues:
                    f.write(f"  {i}\n")

        status = len(issues) == 0
        print(f"\n  {'='*40}")
        if status:
            print(f"  ✅ Quality Check PASSED!")
        else:
            print(f"  ❌ Quality Check FAILED — {len(issues)} issues")
        print(f"  📄 Report : {report_path}")

        return {"status": status, "issues": issues, "warnings": warnings}