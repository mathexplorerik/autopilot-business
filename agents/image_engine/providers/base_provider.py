"""
==========================================================
AI Publishing OS V8
Base Image Provider
==========================================================
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict

from agents.image_engine.retry_wrapper import with_retry


class BaseProvider(ABC):
    """
    Base interface for all image providers.
    """
    NAME = "base"
    VERSION = "1.0.0"
    MAX_RETRY_ATTEMPTS = 3
    RETRY_BASE_DELAY_SECONDS = 2.0

    @abstractmethod
    def _generate_once(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
    ) -> Dict:
        """
        Subclasses implement the ACTUAL single-attempt image
        generation call here (the real API call). generate()
        below wraps this with retry/backoff automatically -
        subclasses should not implement their own retry logic.
        """
        raise NotImplementedError

    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        output_path: str,
    ) -> Dict:
        """
        Generate an image, with automatic retry/backoff on
        transient failures. Subclasses implement _generate_once()
        instead of overriding this method directly.
        """
        return with_retry(
            lambda: self._generate_once(prompt, negative_prompt, output_path),
            provider_name=self.NAME,
            max_attempts=self.MAX_RETRY_ATTEMPTS,
            base_delay_seconds=self.RETRY_BASE_DELAY_SECONDS,
        )

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
