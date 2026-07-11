"""
AI Publishing OS V7
Prompt Rules
"""

PROMPT_RULES = {
    "positive": [
        "centered composition",
        "white background",
        "clean line art",
        "printable",
        "kids coloring book",
    ],
    "negative": [
        "shadow",
        "blur",
        "watermark",
        "text",
        "logo",
    ],
}


def positive():
    return PROMPT_RULES["positive"]


def negative():
    return PROMPT_RULES["negative"]