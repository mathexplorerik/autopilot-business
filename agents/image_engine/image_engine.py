"""
==========================================================
AI Publishing OS V8
Image Engine
==========================================================
"""

from __future__ import annotations

from typing import Dict

from .image_metadata import ImageMetadata
from .image_saver import ImageSaver
from .image_validator import ImageValidator
from .provider_manager import ProviderManager


class ImageEngine:
    """
    Main image generation engine.
    """

    def __init__(self):

        self.providers = ProviderManager()

    def generate(
        self,
        metadata: ImageMetadata,
    ) -> Dict:
        """
        Generate an image.
        """

        # Validate input
        ImageValidator.validate(metadata)

        # Prepare output directory
        ImageSaver.prepare(metadata)

        # Select provider
        provider = self.providers.get(
            metadata.provider
        )

        # Generate image
        result = provider.generate(
            prompt=metadata.prompt,
            negative_prompt=metadata.negative_prompt,
            output_path=metadata.output_path,
        )

        # Save metadata
        ImageSaver.save_metadata(metadata)

        return result

    def providers(self):
        """
        List available providers.
        """

        return self.providers.providers()

    def health(self):
        """
        Provider health status.
        """

        return self.providers.health()