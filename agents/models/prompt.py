"""
==========================================================
AI KDP AUTOPILOT V4
Prompt Model
==========================================================

Single Prompt Object
Used by:
- Prompt Engine
- Prompt Validator
- Duplicate Detector
- Image Generator
- Quality Agent
- PDF Agent
==========================================================
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Prompt:

    # Identity
    page: int
    subject: str
    niche: str

    # Prompt
    positive: str
    negative: str

    # Metadata
    complexity: str
    label: str

    # Animal Engine
    scene: Optional[str] = None
    background: Optional[str] = None
    action: Optional[str] = None
    pose: Optional[str] = None
    expression: Optional[str] = None

    props: List[str] = field(default_factory=list)
    accessories: List[str] = field(default_factory=list)

    # Validation
    valid: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    # Quality
    score: float = 100.0

    # Image
    image_path: Optional[str] = None
    image_generated: bool = False

    # Trace
    seed: Optional[int] = None

    def has_errors(self):
        return len(self.errors) > 0

    def add_error(self, message):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message):
        self.warnings.append(message)

    def to_dict(self):
        return {
            "page": self.page,
            "subject": self.subject,
            "niche": self.niche,
            "positive": self.positive,
            "negative": self.negative,
            "complexity": self.complexity,
            "label": self.label,
            "scene": self.scene,
            "background": self.background,
            "action": self.action,
            "pose": self.pose,
            "expression": self.expression,
            "props": self.props,
            "accessories": self.accessories,
            "valid": self.valid,
            "warnings": self.warnings,
            "errors": self.errors,
            "score": self.score,
            "image_path": self.image_path,
            "image_generated": self.image_generated,
            "seed": self.seed,
        }