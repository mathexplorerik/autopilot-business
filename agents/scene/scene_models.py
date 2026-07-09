"""
==========================================================
AI Publishing OS V6
Scene Models
==========================================================
"""

from dataclasses import dataclass, field
from typing import List, Dict


# -------------------------------------------------------
# Scene Plan
# -------------------------------------------------------

@dataclass
class ScenePlan:

    level: str

    subjects: int = 1

    props: int = 1

    accessories: int = 0

    background: bool = False

    details: int = 2


# -------------------------------------------------------
# Scene
# -------------------------------------------------------

@dataclass
class Scene:

    subject: str

    action: str

    background: str

    props: List[str] = field(default_factory=list)

    accessories: List[str] = field(default_factory=list)

    plan: ScenePlan | None = None

    score: float = 100.0


# -------------------------------------------------------
# Scene Validation
# -------------------------------------------------------

@dataclass
class SceneValidation:

    valid: bool = True

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)


# -------------------------------------------------------
# Diversity Report
# -------------------------------------------------------

@dataclass
class DiversityReport:

    score: float

    subjects: Dict = field(default_factory=dict)

    actions: Dict = field(default_factory=dict)

    backgrounds: Dict = field(default_factory=dict)

    props: Dict = field(default_factory=dict)

    accessories: Dict = field(default_factory=dict)


# -------------------------------------------------------
# Scene Result
# -------------------------------------------------------

@dataclass
class SceneResult:

    scene: Scene

    validation: SceneValidation

    diversity: DiversityReport | None = None