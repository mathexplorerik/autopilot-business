"""
Source-aware market-data value.

Adds provenance metadata without changing the existing
BaseMarketDataSource int-returning API.
"""

from dataclasses import dataclass
from typing import Literal


SourceMode = Literal["real", "heuristic", "fallback"]


@dataclass(frozen=True)
class SourceValue:
    value: int
    source: str
    mode: SourceMode

    def __post_init__(self):
        if isinstance(self.value, bool) or not isinstance(self.value, int):
            raise TypeError("value must be an int")
        if not 0 <= self.value <= 100:
            raise ValueError("value must be between 0 and 100")
        if not self.source or not self.source.strip():
            raise ValueError("source must not be empty")
        if self.mode not in ("real", "heuristic", "fallback"):
            raise ValueError(
                "mode must be 'real', 'heuristic', or 'fallback'"
            )

    def as_dict(self) -> dict:
        return {
            "value": self.value,
            "source": self.source,
            "mode": self.mode,
        }
