from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ResearchReport:
    # Core
    niche: str
    resolved_niche: str

    # Book
    book_type: str = "coloring_book"
    language: str = "English"

    # Audience
    age_group: str = "kids"
    target_age: str = "4-8 Years"

    # Content
    pages: int = 40
    difficulty: str = "simple"

    # Theme
    theme: str = ""
    style: str = ""
    season: str = ""

    # Subjects
    subjects: List[str] = field(default_factory=list)

    # Scene rules
    scene_rules: Dict[str, Any] = field(default_factory=dict)

    # SEO
    keywords: List[str] = field(default_factory=list)
    backend_keywords: List[str] = field(default_factory=list)

    # Market
    category: str = ""
    competition: str = ""
    marketplace: str = "Amazon KDP"

    # Extra
    metadata: Dict[str, Any] = field(default_factory=dict)