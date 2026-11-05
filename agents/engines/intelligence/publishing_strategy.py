"""
Bundle suggestions and publishing strategy (V16)

Reads the rows PortfolioPlanner already produces and turns them into
(1) groups of related niches that could be published as a bundle or
series, and (2) a launch order with a reason for every step.

This is a planning aid built on heuristic scores, not market research.
The niche groups below are my own grouping, not data from any source.
"""

NICHE_GROUPS = {
    "animals": ["animals", "farm animals", "ocean animals", "jungle animals", "dinosaurs", "butterflies"],
    "festivals": ["diwali", "holi", "dussehra", "navratri", "raksha bandhan", "christmas",
                  "eid", "bakra eid", "ganesh chaturthi", "makar sankranti", "onam"],
    "family days": ["mothers day", "fathers day", "doctors day"],
    "fantasy and play": ["space", "princess", "vehicles"],
}

SEASONAL_GROUPS = ("festivals", "family days")
HIGH_COMPETITION = 75
LEVEL_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}

DISCLAIMER = (
    "Built on heuristic portfolio scores, not on real market data. "
    "Treat it as a way to organise a plan, and check each niche yourself before investing."
)


def _num(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _usable(rows):
    out = []
    if not isinstance(rows, list):
        return out
    for row in rows:
        if not isinstance(row, dict) or "error" in row:
            continue
        niche = row.get("niche")
        if not isinstance(niche, str) or not niche.strip():
            continue
        if not _num(row.get("portfolio_score")):
            continue
        out.append(row)
    out.sort(key=lambda r: r["portfolio_score"], reverse=True)
    return out


def _level(row):
    level = row.get("confidence_level")
    return level if level in LEVEL_RANK else "LOW"


def _revenue(row):
    value = row.get("estimated_monthly_revenue")
    return value if _num(value) else 0


def _group_of(niche):
    key = niche.strip().lower()
    for group, members in NICHE_GROUPS.items():
        if key in members:
            return group
    return None


class BundlePlanner:

    def suggest(self, ranked_niches, max_per_bundle=3):
        rows = _usable(ranked_niches)
        by_group = {}
        ungrouped = []
        for row in rows:
            group = _group_of(row["niche"])
            if group is None:
                ungrouped.append(row["niche"])
            else:
                by_group.setdefault(group, []).append(row)

        bundles = []
        for group, members in by_group.items():
            chosen = members[:max(max_per_bundle, 1)]
            if len(chosen) < 2:
                continue
            weakest = min((_level(r) for r in chosen), key=lambda lv: LEVEL_RANK[lv])
            bundles.append({
                "group": group,
                "niches": [r["niche"] for r in chosen],
                "combined_monthly_revenue_estimate": round(sum(_revenue(r) for r in chosen), 2),
                "weakest_confidence": weakest,
                "seasonal": group in SEASONAL_GROUPS,
                "note": "Publish as a series with one shared look. Revenue is an estimate, not a forecast.",
            })
        bundles.sort(key=lambda b: b["combined_monthly_revenue_estimate"], reverse=True)

        return {"bundles": bundles, "ungrouped": ungrouped, "disclaimer": DISCLAIMER}


class PublishingStrategy:

    def plan(self, ranked_niches, marketplace_comparison=None):
        rows = _usable(ranked_niches)
        total = len(rows)
        launch_order = []

        for position, row in enumerate(rows, 1):
            level = _level(row)
            reasons = ["ranked " + str(position) + " of " + str(total) + " by portfolio score"]

            if level == "LOW":
                action = "test small"
                reasons.append("confidence is LOW: the numbers are mostly fallback guesses, so try one book before more")
            else:
                action = "build"
                reasons.append("confidence is " + level)

            competition = row.get("competition_score")
            if _num(competition) and competition >= HIGH_COMPETITION:
                reasons.append("competition score is " + str(competition) + ": needs a clear angle, not a copy of what exists")

            if _group_of(row["niche"]) in SEASONAL_GROUPS:
                reasons.append("seasonal: check the real date and publish a few months ahead (rule of thumb, not data)")

            launch_order.append({
                "order": position,
                "niche": row["niche"],
                "action": action,
                "portfolio_score": row["portfolio_score"],
                "confidence": level,
                "reasons": reasons,
            })

        first_marketplace = None
        notes = []
        if isinstance(marketplace_comparison, dict) and isinstance(marketplace_comparison.get("best_marketplace"), str):
            first_marketplace = marketplace_comparison["best_marketplace"]
            notes.append(
                "First marketplace is chosen by estimated royalty per sale only. Etsy and Gumroad sell "
                "digital downloads and Amazon KDP sells print, and the royalty rates are assumptions, "
                "so traffic and product type are not part of this choice."
            )

        return {
            "launch_order": launch_order,
            "first_marketplace": first_marketplace,
            "notes": notes,
            "disclaimer": DISCLAIMER,
        }
