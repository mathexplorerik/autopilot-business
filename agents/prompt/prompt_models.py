"""
==========================================================
AI Publishing OS V6
Prompt Models
==========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List


# -------------------------------------------------------
# Prompt Metadata
# -------------------------------------------------------

@dataclass
class PromptMetadata:

    marketplace: str = "Amazon KDP"

    generator: str = "Gemini"

    product_type: str = "Coloring Book"

    scene_score: float = 100.0

    prompt_score: float = 100.0

    diversity_score: float = 100.0

    version: str = "V6"

    extra: Dict = field(default_factory=dict)


# -------------------------------------------------------
# Prompt
# -------------------------------------------------------

@dataclass
class Prompt:

    page: int

    subject: str

    niche: str

    complexity: str

    label: str

    positive: str

    negative: str

    metadata: PromptMetadata | None = None

    def to_dict(self):

        return {

            "page": self.page,

            "subject": self.subject,

            "niche": self.niche,

            "complexity": self.complexity,

            "label": self.label,

            "positive": self.positive,

            "negative": self.negative,

            "metadata": (
                self.metadata.__dict__
                if self.metadata
                else {}
            )

        }


# -------------------------------------------------------
# Prompt Batch
# -------------------------------------------------------

@dataclass
class PromptBatch:

    niche: str

    age_group: str

    season: str = ""

    prompts: List[Prompt] = field(default_factory=list)

    created_at: str = ""

    def total(self):

        return len(self.prompts)

    def to_dict(self):

        return {

            "niche": self.niche,

            "age_group": self.age_group,

            "season": self.season,

            "created_at": self.created_at,

            "total": self.total(),

            "prompts": [

                p.to_dict()

                for p in self.prompts

            ]

        }


# -------------------------------------------------------
# Prompt Score
# -------------------------------------------------------

@dataclass
class PromptScore:

    score: float

    grade: str

    issues: List[str] = field(default_factory=list)

    regenerate: bool = False