"""
=========================================
Filename Sanitization Utility
=========================================
Prevents path-traversal and invalid-filename
issues from user-supplied keywords/niches/titles
being used directly in file paths.
"""

import re


def sanitize_filename(text: str, max_length: int = 100) -> str:
    """
    Converts arbitrary text into a safe filename fragment:
    - lowercased
    - spaces -> underscores
    - path separators and traversal sequences stripped
    - only alphanumeric, underscore, hyphen kept
    - truncated to a sane max length
    - never returns an empty string
    """
    if not text:
        return "untitled"

    text = text.strip().lower()

    # Remove path separators and traversal sequences outright
    text = text.replace("..", "")
    text = text.replace("/", "_")
    text = text.replace("\\", "_")

    text = text.replace(" ", "_")

    # Keep only safe characters
    text = re.sub(r"[^a-z0-9_\-]", "", text)

    # Collapse repeated underscores
    text = re.sub(r"_+", "_", text).strip("_")

    text = text[:max_length]

    return text or "untitled"
