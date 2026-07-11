"""
==========================================================
 AI KDP AUTOPILOT V9
 Selector Context
==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class SelectorContext:

    category: str
    subject: str

    age_group: str = "kids"

    page_number: int = 1

    total_pages: int = 40

    season: str | None = None

    action: str | None = None

    scene: str | None = None

    background: str | None = None

    pose: str | None = None

    expression: str | None = None

    props: list = field(default_factory=list)

    accessories: list = field(default_factory=list)