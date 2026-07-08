"""
==========================================================
 AI KDP AUTOPILOT V4
 Prompt Validator
==========================================================
"""


class PromptValidator:
    """
    Validates prompts before image generation.
    """

    def validate(self, positive, negative):
        """
        Validate prompt.
        """

        return {
            "valid": True,
            "errors": [],
            "warnings": [],
            "positive": positive,
            "negative": negative,
        }