"""
==========================================================
AI Publishing OS V8
Stability Image Provider
==========================================================
"""

from __future__ import annotations

from typing import Dict

from .base_provider import BaseProvider


class StabilityProvider(BaseProvider):
    """
    Stability AI image generation provider.
    """

    NAME = "stability"

    VERSION = "1.0.0"

    def __init__(self):
        pass

    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
    ) -> Dict:
        """
        Generate an image using Stability AI.
        """

        raise NotImplementedError(
            "Stability provider is not implemented yet."
        )

    def health(self) -> Dict:
        """
        Provider health status.
        """

        return {
            "provider": self.NAME,
            "version": self.VERSION,
            "status": "not_implemented",
        }