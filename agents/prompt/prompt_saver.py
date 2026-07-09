"""
==========================================================
AI Publishing OS V6
Prompt Saver
==========================================================
"""

import csv
import json
from pathlib import Path
from datetime import datetime


class PromptSaver:
    """
    Export prompt batches into multiple formats.

    Responsibilities
    ----------------
    ✓ TXT
    ✓ JSON
    ✓ CSV
    ✓ Markdown
    ✓ Latest Export

    Does NOT
    ----------
    ✗ Generate Prompts
    ✗ Validate
    ✗ Score
    """

    def __init__(self):

        self.output = Path("output/prompts")
        self.output.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        prompts,
        niche,
        age_group,
        season=""
    ):

        safe = niche.lower().replace(" ", "_")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        paths = {

            "txt":
                self._save_txt(
                    prompts,
                    safe,
                    timestamp
                ),

            "json":
                self._save_json(
                    prompts,
                    niche,
                    age_group,
                    season,
                    safe,
                    timestamp
                ),

            "csv":
                self._save_csv(
                    prompts,
                    safe,
                    timestamp
                ),

            "markdown":
                self._save_markdown(
                    prompts,
                    niche,
                    safe,
                    timestamp
                ),

            "latest":
                self._save_latest(
                    prompts
                )

        }

        return paths

    # --------------------------------------------------

    def _save_txt(
        self,
        prompts,
        safe,
        timestamp
    ):

        path = self.output / f"{safe}_{timestamp}.txt"

        with open(path, "w", encoding="utf-8") as f:

            for prompt in prompts:

                f.write(
                    f"Page {prompt['page']}\n"
                )

                f.write(
                    prompt["positive"] + "\n"
                )

                f.write(
                    prompt["negative"] + "\n\n"
                )

        return str(path)

    # --------------------------------------------------

    def _save_json(
        self,
        prompts,
        niche,
        age_group,
        season,
        safe,
        timestamp
    ):

        path = self.output / f"{safe}_{timestamp}.json"

        data = {

            "version": "V6",

            "generated_at": timestamp,

            "niche": niche,

            "age_group": age_group,

            "season": season,

            "total": len(prompts),

            "prompts": prompts

        }

        with open(path, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return str(path)

    # --------------------------------------------------

    def _save_csv(
        self,
        prompts,
        safe,
        timestamp
    ):

        path = self.output / f"{safe}_{timestamp}.csv"

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "Page",
                "Subject",
                "Complexity",
                "Positive",
                "Negative"
            ])

            for prompt in prompts:

                writer.writerow([

                    prompt["page"],

                    prompt["subject"],

                    prompt["complexity"],

                    prompt["positive"],

                    prompt["negative"]

                ])

        return str(path)

    # --------------------------------------------------

    def _save_markdown(
        self,
        prompts,
        niche,
        safe,
        timestamp
    ):

        path = self.output / f"{safe}_{timestamp}.md"

        with open(path, "w", encoding="utf-8") as f:

            f.write(f"# {niche}\n\n")

            for prompt in prompts:

                f.write(
                    f"## Page {prompt['page']}\n\n"
                )

                f.write(
                    f"**Subject:** {prompt['subject']}\n\n"
                )

                f.write(
                    f"**Positive:**\n\n{prompt['positive']}\n\n"
                )

                f.write(
                    f"**Negative:**\n\n{prompt['negative']}\n\n"
                )

        return str(path)

    # --------------------------------------------------

    def _save_latest(
        self,
        prompts
    ):

        path = self.output / "latest_prompts.json"

        with open(path, "w", encoding="utf-8") as f:

            json.dump(
                prompts,
                f,
                indent=4,
                ensure_ascii=False
            )

        return str(path)