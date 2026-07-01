import os


class QualityAgent:

    def check(self, report, prompts, seo, book):

        print("\n🔍 Quality Agent Running...\n")

        issues = []

        if report["pages"] != len(prompts):
            issues.append("Page count and prompts count do not match.")

        if not seo["title"]:
            issues.append("Missing title.")

        if not seo["description"]:
            issues.append("Missing description.")

        if not os.path.exists("output/books/book.json"):
            issues.append("book.json not found.")

        if len(issues) == 0:
            print("✅ Quality Check Passed")

            with open("output/reports/quality_report.txt", "w") as f:
                f.write("QUALITY CHECK PASSED\n")

            return True

        print("❌ Quality Issues Found")

        with open("output/reports/quality_report.txt", "w") as f:
            for issue in issues:
                f.write(issue + "\n")

        return False