"""
=========================================
Prompt Validator
=========================================
"""


class PromptValidator:

    def validate(self, parts):

        # Remove empty values
        parts = [p for p in parts if p]

        # Remove duplicate phrases
        seen = set()
        cleaned = []

        for part in parts:
            key = part.strip().lower()

            if key not in seen:
                seen.add(key)
                cleaned.append(part)

        return cleaned