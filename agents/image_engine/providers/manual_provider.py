"""
==========================================================
AI Publishing OS V8
Manual Image Provider
==========================================================
"""

from __future__ import annotations

import json
from pathlib import Path

from .base_provider import BaseProvider


class ManualProvider(BaseProvider):

    NAME = "manual"

    VERSION = "1.0.0"

    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
    ):

        output = Path(output_path)

        output.mkdir(parents=True, exist_ok=True)

        (output / "prompt.txt").write_text(
            prompt,
            encoding="utf-8",
        )

        metadata = {
            "provider": self.NAME,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }

        (output / "metadata.json").write_text(
            json.dumps(metadata, indent=4),
            encoding="utf-8",
        )

        return {
            "success": True,
            "provider": self.NAME,
            "folder": str(output),
        }

    def health(self):

        return {
            "provider": self.NAME,
            "status": "ok",
        }