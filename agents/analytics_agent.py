"""
==========================================================
AI Publishing OS V5
Analytics Agent — Pro Level
==========================================================
"""
import os
import json
from datetime import datetime


class AnalyticsAgent:

    def generate(self, report, book):
        print("\n📊 Analytics Agent Running...\n")

        # ✅ ResearchReport object ya dict dono handle karo
        if hasattr(report, 'resolved_niche'):
            niche      = report.resolved_niche
            pages      = report.pages
            target_age = report.target_age
            difficulty = report.difficulty
            age_group  = report.age_group
            keywords   = report.keywords or []
            competition = report.competition or "Unknown"
        else:
            niche      = report.get("niche", "unknown")
            pages      = report.get("pages", 40)
            target_age = report.get("target_age", "4-8 Years")
            difficulty = report.get("difficulty", "Easy")
            age_group  = report.get("age_group", "kids")
            keywords   = report.get("keywords", [])
            competition = report.get("competition", "Unknown")

        # ✅ Book data
        if hasattr(book, 'get'):
            title    = book.get("title", "Unknown")
            subtitle = book.get("subtitle", "")
        else:
            title    = getattr(book, 'title', "Unknown")
            subtitle = getattr(book, 'subtitle', "")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Stats
        stats = {
            "timestamp":   timestamp,
            "niche":       niche,
            "title":       title,
            "subtitle":    subtitle,
            "pages":       pages,
            "target_age":  target_age,
            "age_group":   age_group,
            "difficulty":  difficulty,
            "competition": competition,
            "keywords":    keywords[:7] if keywords else [],
            "status":      "Ready for Publishing",
            "next_steps": [
                "Upload to Amazon KDP",
                "Create Pinterest pins",
                "Upload to Gumroad",
                "Share on Instagram"
            ]
        }

        # ✅ Save files
        os.makedirs("output/analytics", exist_ok=True)

        # JSON
        json_path = "output/analytics/stats.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)

        # Dashboard TXT
        dash_path = "output/analytics/dashboard.txt"
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write("="*50 + "\n")
            f.write("   AI KDP AUTOPILOT — DASHBOARD\n")
            f.write("="*50 + "\n\n")
            f.write(f"  Generated : {timestamp}\n\n")
            f.write(f"  📚 BOOK INFO\n")
            f.write(f"  {'─'*30}\n")
            f.write(f"  Niche      : {niche}\n")
            f.write(f"  Title      : {title}\n")
            f.write(f"  Pages      : {pages}\n")
            f.write(f"  Age Group  : {target_age}\n")
            f.write(f"  Difficulty : {difficulty}\n\n")
            f.write(f"  🔑 KEYWORDS\n")
            f.write(f"  {'─'*30}\n")
            for kw in keywords[:7]:
                f.write(f"  • {kw}\n")
            f.write(f"\n  📈 MARKET\n")
            f.write(f"  {'─'*30}\n")
            f.write(f"  Competition : {competition}\n")
            f.write(f"  Status      : Ready for Publishing\n\n")
            f.write(f"  ✅ NEXT STEPS\n")
            f.write(f"  {'─'*30}\n")
            for step in stats["next_steps"]:
                f.write(f"  → {step}\n")
            f.write("\n" + "="*50 + "\n")

        print(f"  📚 Niche     : {niche}")
        print(f"  📖 Title     : {title}")
        print(f"  📄 Pages     : {pages}")
        print(f"  🎯 Status    : Ready for Publishing")
        print(f"  📄 JSON      : {json_path}")
        print(f"  📄 Dashboard : {dash_path}")
        print(f"  ✅ Analytics Complete!")

        return stats