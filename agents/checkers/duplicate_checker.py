class DuplicateChecker:
    """
    Tracks generated prompts and prevents exact duplicates.
    """

    def __init__(self):
        self.prompts = set()

    def is_duplicate(self, prompt: str) -> bool:
        return prompt.strip().lower() in self.prompts

    def add_prompt(self, prompt: str):
        self.prompts.add(prompt.strip().lower())

    def reset(self):
        self.prompts.clear()