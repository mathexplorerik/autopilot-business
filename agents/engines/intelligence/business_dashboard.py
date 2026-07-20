"""
=========================================
Business Dashboard (V13)
=========================================
Consolidates every intelligence module into a
single business-level snapshot: top opportunity
niches, pricing/marketplace comparison for the
top pick, and overall portfolio revenue outlook.

This is the "one command, full picture" view for
deciding what to build next.
"""

import os
import json
from datetime import datetime


class BusinessDashboard:

    def __init__(self, research_engine, portfolio_planner, multi_market_optimizer):
        self.research_engine = research_engine
        self.portfolio_planner = portfolio_planner
        self.multi_market_optimizer = multi_market_optimizer

    def generate(self, niches: list, season: str = "", top_n: int = 5) -> dict:
        portfolio = self.portfolio_planner.analyze_portfolio(niches, season=season)
        top_niches = portfolio["ranked_niches"][:top_n]

        top_pick = portfolio["top_pick"]
        marketplace_comparison = None

        if top_pick and "error" not in top_pick:
            marketplace_comparison = self.multi_market_optimizer.compare_marketplaces(
                pages=40,
                demand_score=top_pick["demand_score"],
                competition_score=top_pick["competition_score"],
                opportunity_score=top_pick["opportunity_score"],
            )

        snapshot = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "niches_analyzed": portfolio["niches_analyzed"],
            "niches_with_errors": portfolio["niches_with_errors"],
            "top_niches": top_niches,
            "top_pick": top_pick,
            "top_pick_marketplace_comparison": marketplace_comparison,
            "total_estimated_monthly_revenue_if_all_built": portfolio["total_estimated_monthly_revenue_if_all_built"],
        }

        return snapshot

    def save(self, snapshot: dict, output_dir: str = "output/business_dashboard"):
        os.makedirs(output_dir, exist_ok=True)

        json_path = os.path.join(output_dir, "dashboard.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4, ensure_ascii=False)

        txt_path = os.path.join(output_dir, "dashboard.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("=" * 55 + "\n")
            f.write("   AI PUBLISHING OS - BUSINESS DASHBOARD\n")
            f.write("=" * 55 + "\n\n")
            f.write(f"  Generated: {snapshot['generated_at']}\n")
            f.write(f"  Niches analyzed: {snapshot['niches_analyzed']}\n\n")

            f.write("  TOP NICHES (by portfolio score)\n")
            f.write("  " + "-" * 40 + "\n")
            for i, n in enumerate(snapshot["top_niches"], 1):
                if "error" in n:
                    f.write(f"  {i}. {n['niche']}: ERROR - {n['error']}\n")
                    continue
                f.write(
                    f"  {i}. {n['niche']:20} score={n['portfolio_score']:5} "
                    f"opp={n['opportunity_score']:3} monthly_rev=${n['estimated_monthly_revenue']}\n"
                )

            if snapshot.get("top_pick_marketplace_comparison"):
                f.write("\n  BEST MARKETPLACE FOR TOP PICK\n")
                f.write("  " + "-" * 40 + "\n")
                f.write(f"  {snapshot['top_pick_marketplace_comparison']['recommendation']}\n")

            f.write(
                f"\n  Total estimated monthly revenue if ALL niches built: "
                f"${snapshot['total_estimated_monthly_revenue_if_all_built']}\n"
            )
            f.write("\n" + "=" * 55 + "\n")

        return {"json": json_path, "txt": txt_path}

    def print_summary(self, snapshot: dict):
        print()
        print("=" * 55)
        print("   BUSINESS DASHBOARD")
        print("=" * 55)
        print(f"  Niches analyzed: {snapshot['niches_analyzed']}")
        print()
        print("  TOP NICHES:")
        for i, n in enumerate(snapshot["top_niches"], 1):
            if "error" in n:
                print(f"    {i}. {n['niche']}: ERROR")
                continue
            print(f"    {i}. {n['niche']:20} score={n['portfolio_score']:5} monthly_rev=${n['estimated_monthly_revenue']}")
        if snapshot.get("top_pick_marketplace_comparison"):
            print()
            print("  " + snapshot["top_pick_marketplace_comparison"]["recommendation"])
        print()
        print(f"  Total monthly revenue potential (all niches): ${snapshot['total_estimated_monthly_revenue_if_all_built']}")
        print("=" * 55)
