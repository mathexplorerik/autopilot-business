"""
==========================================================
AI Publishing OS V7
Knowledge Package
==========================================================

Central knowledge system for AI Publishing OS.

This package is responsible for:

• Loading knowledge sources
• Managing datasets
• Validating knowledge
• Providing data to AI engines

Version:
    V7
"""

from .engine import KnowledgeEngine
from .loader import KnowledgeLoader

__version__ = "7.0.0"

__all__ = [
    "KnowledgeEngine",
    "KnowledgeLoader",
]