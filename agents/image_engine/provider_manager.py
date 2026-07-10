"""
==========================================================
AI Publishing OS V8
Provider Manager
==========================================================
"""

from __future__ import annotations

from .providers.manual_provider import ManualProvider
from .providers.openai_provider import OpenAIProvider
from .providers.flux_provider import FluxProvider
from .providers.gemini_provider import GeminiProvider
from .providers.stability_provider import StabilityProvider


class ProviderManager:

    def __init__(self):

        self._providers = {
            "manual": ManualProvider(),
            "openai": OpenAIProvider(),
            "flux": FluxProvider(),
            "gemini": GeminiProvider(),
            "stability": StabilityProvider(),
        }

    def get(self, provider: str):

        provider = provider.lower()

        if provider not in self._providers:
            raise ValueError(f"Unknown provider: {provider}")

        return self._providers[provider]

    def providers(self):

        return sorted(self._providers.keys())

    def health(self):

        return {
            name: provider.health()
            for name, provider in self._providers.items()
        }