"""
==========================================================
AI Publishing OS V8
Base Image Provider
==========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class BaseProvider(ABC):
    """
    Base interface for all image providers.
    """

    NAME = "base"

    VERSION = "1.0.0"

    @abstractmethod
    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
    ) -> Dict:
        """
        Generate an image.
        """
        raise NotImplementedError

    @abstractmethod
    def health(self) -> Dict:
        """
        Provider health.
        """
        raise NotImplementedError

    def provider_name(self) -> str:

        return self.NAME

    def version(self) -> str:

        return self.VERSION