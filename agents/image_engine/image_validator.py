"""
==========================================================
AI Publishing OS V8
Image Validator
==========================================================
"""

from __future__ import annotations

from pathlib import Path

from .image_metadata import ImageMetadata


class ImageValidator:
    """
    Validates image generation requests.
    """

    MIN_SIZE = 256
    MAX_SIZE = 4096

    @classmethod
    def validate(
        cls,
        metadata: ImageMetadata,
    ) -> None:
        """
        Validate image metadata.
        """

        if not metadata.prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        if metadata.width < cls.MIN_SIZE:
            raise ValueError(
                f"Width must be at least {cls.MIN_SIZE}."
            )

        if metadata.width > cls.MAX_SIZE:
            raise ValueError(
                f"Width cannot exceed {cls.MAX_SIZE}."
            )

        if metadata.height < cls.MIN_SIZE:
            raise ValueError(
                f"Height must be at least {cls.MIN_SIZE}."
            )

        if metadata.height > cls.MAX_SIZE:
            raise ValueError(
                f"Height cannot exceed {cls.MAX_SIZE}."
            )

        if metadata.output_path.strip():
            output = Path(metadata.output_path)

            if output.suffix.lower() not in {
                ".png",
                ".jpg",
                ".jpeg",
                ".webp",
            }:
                
                if metadata.provider == "manual":
                    return

                raise ValueError(
                    "Unsupported output image format."
                )

    @classmethod
    def is_valid(
        cls,
        metadata: ImageMetadata,
    ) -> bool:
        """
        Return True if metadata is valid.
        """

        try:
            cls.validate(metadata)
            return True
        except Exception:
            return False