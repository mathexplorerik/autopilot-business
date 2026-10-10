"""
==========================================================
AI Publishing OS V16
Stability AI Image Provider (REAL implementation)
==========================================================
Uses Stability AI's REST API (stable-image/generate/core
endpoint) to generate real images for coloring-book pages.

Requires STABILITY_API_KEY environment variable.
Get a key at: https://platform.stability.ai/account/keys

IMPORTANT: This code has NOT been tested with a live API
key in this environment (network access is disabled here).
Test it on your own machine with a real key before relying
on it for production book generation.
"""

from __future__ import annotations

import os
from typing import Dict

import requests

from .base_provider import BaseProvider


class StabilityProvider(BaseProvider):
    """
    Stability AI image generation provider.
    """

    NAME = "stability"
    VERSION = "2.0.0"

    API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def __init__(self):
        self.api_key = os.environ.get("STABILITY_API_KEY")

    def health(self) -> Dict:
        return {
            "provider": self.NAME,
            "version": self.VERSION,
            "status": "ready" if self.api_key else "missing_api_key",
            "api_key_configured": bool(self.api_key),
        }

    def _generate_once(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
    ) -> Dict:
        if not self.api_key:
            raise ValueError(
                "STABILITY_API_KEY environment variable is not set. "
                "Get a key at https://platform.stability.ai/account/keys "
                "and run: export STABILITY_API_KEY=your_key_here"
            )

        os.makedirs(output_path, exist_ok=True)
        image_file_path = os.path.join(output_path, "image.png")

        response = requests.post(
            self.API_URL,
            headers={
                "authorization": f"Bearer {self.api_key}",
                "accept": "image/*",
            },
            files={"none": ""},
            data={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "output_format": "png",
                "aspect_ratio": "4:5",  # close to 8.5x11 book-page ratio
            },
            timeout=60,
        )

        if response.status_code in (400, 401, 402, 403, 404, 422):
            # Permanent client-side errors (bad key, no credits, invalid
            # request): retrying cannot fix these, so fail fast.
            raise ValueError(
                f"Stability API rejected the request ({response.status_code}): {response.text[:300]}"
            )
        if response.status_code != 200:
            # Raise a plain Exception (not ValueError/NotImplementedError)
            # so the retry wrapper treats this as a transient failure
            # worth retrying (rate limits, server errors, etc.)
            raise Exception(
                f"Stability API error {response.status_code}: {response.text[:300]}"
            )

        with open(image_file_path, "wb") as f:
            f.write(response.content)

        return {
            "success": True,
            "provider": self.NAME,
            "image_path": image_file_path,
            "folder": output_path,
        }
