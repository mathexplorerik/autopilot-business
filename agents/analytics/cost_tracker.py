"""
=========================================
Cost Tracker (V16 - Business Metrics)
=========================================
Tracks estimated API cost per book generation,
based on image-provider used and page count.
Without this, profit-margin calculation is
impossible at scale.

Cost estimates are industry-standard approximate
rates per image (as of early 2026) - update these
constants as actual provider pricing changes.
"""

import os
import json
from datetime import datetime


class CostTracker:

    COST_PER_IMAGE = {
        "manual": 0.0,
        "openai": 0.040,
        "flux": 0.025,
        "gemini": 0.020,
        "stability": 0.030,
    }

    def calculate_book_cost(self, provider: str, total_pages: int, images_generated: int = None) -> dict:
        provider_key = (provider or "manual").lower()
        cost_per_image = self.COST_PER_IMAGE.get(provider_key, self.COST_PER_IMAGE["manual"])

        actual_images = images_generated if images_generated is not None else total_pages

        estimated_cost = round(actual_images * cost_per_image, 4)

        return {
            "provider": provider_key,
            "total_pages": total_pages,
            "images_generated": actual_images,
            "cost_per_image": cost_per_image,
            "estimated_total_cost": estimated_cost,
        }

    def save_cost_record(self, book_title: str, cost_data: dict, output_dir: str = "output/analytics"):
        os.makedirs(output_dir, exist_ok=True)
        costs_path = os.path.join(output_dir, "costs.json")

        record = {
            "book_title": book_title,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        record.update(cost_data)

        history = []
        if os.path.exists(costs_path):
            try:
                with open(costs_path) as f:
                    history = json.load(f)
                if not isinstance(history, list):
                    history = [history]
            except (json.JSONDecodeError, ValueError):
                history = []

        history.append(record)

        with open(costs_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

        return costs_path

    def summarize_costs(self, output_dir: str = "output/analytics") -> dict:
        costs_path = os.path.join(output_dir, "costs.json")
        if not os.path.exists(costs_path):
            return {"total_books": 0, "total_estimated_cost": 0.0, "records": []}

        with open(costs_path) as f:
            history = json.load(f)

        total_cost = sum(r.get("estimated_total_cost", 0) for r in history)

        return {
            "total_books": len(history),
            "total_estimated_cost": round(total_cost, 4),
            "records": history,
        }
