"""
==========================================================
AI Publishing OS V8
OpenAI Image Provider
==========================================================
"""

from __future__ import annotations

from typing import Dict

from .base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    OpenAI image generation provider.
    """

    NAME = "openai"

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
        Generate an image using OpenAI.
        """

        raise NotImplementedError(
            "OpenAI provider is not implemented yet."
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