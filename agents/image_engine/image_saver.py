"""
==========================================================
AI Publishing OS V8
Image Saver
==========================================================
"""

from __future__ import annotations

import json
from pathlib import Path

from .image_metadata import ImageMetadata


class ImageSaver:
    """
    Saves image metadata and prepares output paths.
    """

    @staticmethod
    def ensure_directory(
        output_path: str,
    ) -> Path:
        """
        Create output directory if needed.
        """

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    @staticmethod
    def save_metadata(
        metadata: ImageMetadata,
    ) -> Path:
        """
        Save metadata beside the image.
        """

        image_path = Path(metadata.output_path)

        metadata_path = image_path.with_suffix(".json")

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                metadata.to_dict(),
                f,
                indent=4,
                ensure_ascii=False,
            )

        return metadata_path

    @staticmethod
    def prepare(
        metadata: ImageMetadata,
    ) -> None:
        """
        Prepare output directory.
        """

        ImageSaver.ensure_directory(
            metadata.output_path
        )