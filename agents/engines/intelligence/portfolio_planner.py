"""
=========================================
Portfolio Planner (V13)
=========================================
Given a list of candidate niches (each with demand/
competition scores), suggests a balanced portfolio
allocation - mixing safe, proven bets with a smaller number
of higher-risk/higher-reward niches.
"""


class PortfolioPlanner:

    SAFE_BET_SHARE = 0.5
    GROWTH_SHARE = 0.35
    SPECULATIVE_SHARE = 0.15

    def _opportunity(self, niche: dict) -> float:
        if "opportunity_score" in niche and niche["opportunity_score"] is not None:
            return niche["opportunity_score"]
        demand = niche.get("demand_score", 50) or 50
        competition = niche.get("competition_score", 50) or 50
        return demand - competition

    def _classify(self, niche: dict) -> str:
        demand = max(0, min(100, niche.get("demand_score", 50) or 50))
        competition = max(0, min(100, niche.get("competition_score", 50) or 50))

        if demand >= 70 and competition <= 50:
            return "safe_bet"
        if demand >= 50 and competition <= 75:
            return "growth"
        return "speculative"

    def plan(self, niches: list, target_book_count: int = 10) -> dict:
        if not niches:
            return {
                "allocation": [],
                "summary": {"safe_bet": 0, "growth": 0, "speculative": 0},
                "note": "No niches supplied - nothing to allocate.",
            }

        target_book_count = max(1, target_book_count or 1)

        classified = []
        for niche in niches:
            tier = self._classify(niche)
            classified.append({
                "niche": niche.get("niche", "unknown"),
                "tier": tier,
                "opportunity_score": round(self._opportunity(niche), 1),
                "demand_score": niche.get("demand_score"),
                "competition_score": niche.get("competition_score"),
            })

        by_tier = {"safe_bet": [], "growth": [], "speculative": []}
        for entry in classified:
            by_tier[entry["tier"]].append(entry)
        for tier in by_tier:
            by_tier[tier].sort(key=lambda e: e["opportunity_score"], reverse=True)

        target_counts = {
            "safe_bet": round(target_book_count * self.SAFE_BET_SHARE),
            "growth": round(target_book_count * self.GROWTH_SHARE),
            "speculative": round(target_book_count * self.SPECULATIVE_SHARE),
        }

        allocation = []
        summary = {"safe_bet": 0, "growth": 0, "speculative": 0}
        for tier, target in target_counts.items():
            picks = by_tier[tier][:target]
            allocation.extend(picks)
            summary[tier] = len(picks)

        return {
            "allocation": allocation,
            "summary": summary,
            "target_book_count": target_book_count,
            "note": (
                "Allocation favors safe_bet niches by default "
                f"({int(self.SAFE_BET_SHARE*100)}% target share). "
                "Tiers with too few qualifying niches are simply "
                "under-filled rather than padded with weak picks."
            ),
        }
