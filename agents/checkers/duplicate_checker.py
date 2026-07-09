import hashlib


class DuplicateChecker:
    """
    Production Duplicate Checker

    Responsibilities
    ----------------
    • Detect exact duplicate prompts
    • Normalize prompts
    • Store hashes for fast lookup
    • Track statistics
    """

    def __init__(self):

        self.reset()

    # --------------------------------------------------

    def normalize(self, prompt: str) -> str:

        return " ".join(
            prompt.lower().strip().split()
        )

    # --------------------------------------------------

    def hash_prompt(self, prompt: str) -> str:

        normalized = self.normalize(prompt)

        return hashlib.md5(
            normalized.encode("utf-8")
        ).hexdigest()

    # --------------------------------------------------

    def is_duplicate(self, prompt: str) -> bool:

        prompt_hash = self.hash_prompt(prompt)

        duplicate = prompt_hash in self._hashes

        if duplicate:
            self.duplicate_count += 1

        return duplicate

    # --------------------------------------------------

    def add_prompt(self, prompt: str):

        normalized = self.normalize(prompt)

        prompt_hash = self.hash_prompt(prompt)

        self._hashes.add(prompt_hash)

        self._prompts.append(normalized)

    # --------------------------------------------------

    def add_many(self, prompts):

        for prompt in prompts:
            self.add_prompt(prompt)

    # --------------------------------------------------

    def contains(self, prompt: str):

        return self.is_duplicate(prompt)

    # --------------------------------------------------

    def total(self):

        return len(self._prompts)

    # --------------------------------------------------

    def duplicates(self):

        return self.duplicate_count

    # --------------------------------------------------

    def prompts(self):

        return list(self._prompts)

    # --------------------------------------------------

    def statistics(self):

        return {
            "unique_prompts": len(self._prompts),
            "duplicates_found": self.duplicate_count,
        }

    # --------------------------------------------------

    def reset(self):

        self._prompts = []

        self._hashes = set()

        self.duplicate_count = 0