import os
import json


class AnalyticsAgent:

    def generate(self, report, book):

        print("\n📊 Analytics Agent Running...\n")

        stats = {
            "niche": report["niche"],
            "pages": report["pages"],
            "target_age": report["target_age"],
            "difficulty": report["difficulty"],
            "title": book["title"],
            "status": "Ready for Publishing"
        }

        os.makedirs("output/analytics", exist_ok=True)

        with open("output/analytics/stats.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4)

        with open("output/analytics/dashboard.txt", "w", encoding="utf-8") as f:
            f.write("=== AI KDP DASHBOARD ===\n\n")
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")

        print("✅ Analytics files created.")

        return stats