"""
==========================================================
AI Publishing OS V7
Knowledge Loader
==========================================================

Central loader for all knowledge resources.

Responsibilities
----------------
✓ Load JSON datasets
✓ Validate data
✓ Locate database files
✓ Future cache support

Version:
    7.0.0
"""

from __future__ import annotations

import json
from pathlib import Path

from agents.data.knowledge.schema.niche_schema import NicheSchema


class KnowledgeLoader:

    VERSION = "7.0.0"

    def __init__(self):

        self.root = Path(__file__).resolve().parent

        self.sources = self.root / "sources"
        self.cache = self.root / "cache"
        self.database = self.root / "database"

    # ==================================================
    # Paths
    # ==================================================

    def source_path(self, filename: str) -> Path:
        return self.sources / filename

    def cache_path(self, filename: str) -> Path:
        return self.cache / filename

    def database_path(self, *parts) -> Path:
        return self.database.joinpath(*parts)

    # ==================================================
    # Utilities
    # ==================================================

    def exists(self, filename: str) -> bool:
        return self.source_path(filename).exists()

    def load_json(self, path: Path):

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # ==================================================
    # Niche Database
    # ==================================================

    def available_niches(self):

        folder = self.database_path("niches")

        if not folder.exists():
            return []

        return sorted(
            file.stem
            for file in folder.glob("*.json")
        )

    def load_niche(self, niche_id: str):

        path = self.database_path(
            "niches",
            f"{niche_id}.json"
        )

        if not path.exists():
            return None

        data = self.load_json(path)

        if not NicheSchema.validate(data):

            raise ValueError(
                f"Invalid niche schema: {path.name}"
            )

        return data

    # ==================================================
    # Generic Loader
    # ==================================================

    def load_collection(
        self,
        collection: str
    ):

        folder = self.database_path(collection)

        if not folder.exists():
            return []

        results = []

        for file in sorted(folder.glob("*.json")):

            results.append(
                self.load_json(file)
            )

        return results

    # ==================================================
    # Information
    # ==================================================

    def info(self):

        return {

            "version": self.VERSION,

            "database": str(self.database),

            "sources": str(self.sources),

            "cache": str(self.cache),

        }
        # ==================================================
    # Prompt Database
    # ==================================================

    def load_prompt(self, prompt_id: str):

        path = self.database_path(
            "prompts",
            f"{prompt_id}.json"
        )

        if not path.exists():
            return None

        return self.load_json(path)