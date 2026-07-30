"""
=========================================
Market Data Confidence Scorer (V13.20)
=========================================
Measures how much of a TrendEngine result is
supported by real external data versus fallback
or heuristic signals.

This score does NOT modify opportunity scores.
It is metadata describing evidence quality.
"""


class ConfidenceScorer:

    WEIGHTS = {
        "demand": 0.30,
        "competition": 0.20,
        "profit": 0.20,
        "evergreen": 0.10,
        "seasonal": 0.05,
        "marketplace": 0.15,
    }

    def analyze(self, provenance: dict) -> dict:
        real_weight = 0.0
        real_fields = []
        fallback_fields = []

        for field, weight in self.WEIGHTS.items():
            meta = provenance.get(field, {})
            mode = meta.get("mode")

            if mode == "real":
                real_weight += weight
                real_fields.append(field)
            else:
                fallback_fields.append(field)

        score = round(real_weight * 100)

        if score >= 70:
            level = "HIGH"
        elif score >= 35:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "score": score,
            "level": level,
            "real_fields": real_fields,
            "fallback_fields": fallback_fields,
            "real_field_count": len(real_fields),
            "total_field_count": len(self.WEIGHTS),
        }
