"""
==========================================================
AI Publishing OS V8
Image Metadata
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime


@dataclass
class ImageMetadata:
    """
    Metadata for a generated image.
    """

    prompt: str

    negative_prompt: str = ""

    provider: str = ""

    model: str = ""

    style: str = ""

    width: int = 1024

    height: int = 1024

    seed: int = -1

    output_path: str = ""

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to dictionary.
        """

        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "provider": self.provider,
            "model": self.model,
            "style": self.style,
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "output_path": self.output_path,
            "created_at": self.created_at,
            "extra": self.extra,
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "ImageMetadata":
        """
        Create metadata from dictionary.
        """

        return cls(
            prompt=data.get("prompt", ""),
            negative_prompt=data.get("negative_prompt", ""),
            provider=data.get("provider", ""),
            model=data.get("model", ""),
            style=data.get("style", ""),
            width=data.get("width", 1024),
            height=data.get("height", 1024),
            seed=data.get("seed", -1),
            output_path=data.get("output_path", ""),
            created_at=data.get("created_at", ""),
            extra=data.get("extra", {}),
        )