"""
Niche Resolver System
User jo bhi type kare — sahi niche find karo
"""

from agents.data.subjects import SUBJECTS

# ✅ Aliases — shortcut names
ALIASES = {
    # Animals
    "jungle":       "jungle animals",
    "safari":       "jungle animals",
    "wild animals": "jungle animals",
    "africa":       "jungle animals",
    "forest animals": "jungle animals",

    "ocean":        "ocean animals",
    "sea":          "ocean animals",
    "marine":       "ocean animals",
    "underwater":   "ocean animals",
    "sea animals":  "ocean animals",

    "farm":         "farm animals",
    "countryside":  "farm animals",

    "dino":         "dinosaurs",
    "dinos":        "dinosaurs",
    "prehistoric":  "dinosaurs",

    "butterfly":    "butterflies",
    "insects":      "butterflies",

    "space":        "space",
    "galaxy":       "space",
    "astronaut":    "space",
    "planets":      "space",

    "princess":     "princess",
    "fairy":        "princess",
    "unicorn":      "princess",
    "mermaid":      "princess",

    "vehicles":     "vehicles",
    "cars":         "vehicles",
    "trucks":       "vehicles",
    "transport":    "vehicles",

    # Festivals
    "diwali":       "diwali",
    "deepawali":    "diwali",
    "deepavali":    "diwali",

    "holi":         "holi",
    "colours":      "holi",
    "colors":       "holi",

    "eid":          "eid",
    "ramadan":      "eid",
    "eid ul fitr":  "eid",

    "bakra eid":    "bakra eid",
    "eid ul adha":  "bakra eid",
    "qurbani":      "bakra eid",

    "christmas":    "christmas",
    "xmas":         "christmas",
    "x-mas":        "christmas",
    "santa":        "christmas",

    "dussehra":     "dussehra",
    "dasara":       "dussehra",
    "vijayadashami":"dussehra",

    "navratri":     "navratri",
    "garba":        "navratri",
    "dandiya":      "navratri",

    "ganesh":       "ganesh chaturthi",
    "ganesha":      "ganesh chaturthi",
    "ganapati":     "ganesh chaturthi",

    "sankranti":    "makar sankranti",
    "kite festival":"makar sankranti",
    "uttarayan":    "makar sankranti",

    "onam":         "onam",
    "kerala":       "onam",

    "rakhi":        "raksha bandhan",
    "rakshabandhan":"raksha bandhan",

    # Special days
    "mothers day":  "mothers day",
    "mother":       "mothers day",
    "mom":          "mothers day",
    "mummy":        "mothers day",

    "fathers day":  "fathers day",
    "father":       "fathers day",
    "dad":          "fathers day",
    "papa":         "fathers day",

    "doctors day":  "doctors day",
    "doctor":       "doctors day",
    "medical":      "doctors day",
}


class NicheResolver:

    def __init__(self):
        self.subjects  = SUBJECTS
        self.aliases   = ALIASES
        self.all_niches = list(SUBJECTS.keys())

    def resolve(self, user_input: str) -> dict:
        """
        User input se sahi niche find karo.
        Returns: {
            "niche": str,
            "matched": str,
            "method": str,
            "confidence": float,
            "subjects": list
        }
        """
        raw = user_input.strip().lower()
        EXACT_MATCH = 1.00
        ALIAS_MATCH = 0.95
        ALIAS_CONTAINS = 0.90
        PARTIAL_MATCH = 0.80
        WORD_MATCH = 0.60
        FALLBACK_MATCH = 0.10

        # ✅ Method 1 — Exact match
        if raw in self.subjects:
            return self._result(raw, raw, "exact", 1.0)

        # ✅ Method 2 — Alias match
        if raw in self.aliases:
            niche = self.aliases[raw]
            return self._result(niche, raw, "alias", 0.95)
        
        # ✅ Method 2.5 — Alias contains match
        for alias, niche in self.aliases.items():
          if alias in raw:
            return self._result(niche, raw, "alias_contains", 0.90)

        # ✅ Method 3 — Partial match in subjects
        for niche in self.all_niches:
            if raw in niche or niche in raw:
                return self._result(niche, raw, "partial", 0.80)

        # ✅ Method 4 — Alias partial match
        for alias, niche in self.aliases.items():
            if raw in alias or alias in raw:
                return self._result(niche, raw, "alias_partial", 0.70)
                
        # ✅ Method 5 — Word match
        raw_words = set(raw.split())
        best_match = None
        best_score = 0

        for niche in self.all_niches:
            niche_words = set(niche.split())
            common      = raw_words & niche_words
            if common:
                score = len(common) / max(len(raw_words), len(niche_words))
                if score > best_score:
                    best_score  = score
                    best_match  = niche

        if best_match and best_score > 0.3:
           return self._result(best_match, raw, "word_match", WORD_MATCH) 
        
        # ✅ Fallback — use as is
        return self._result("animals", raw, "fallback", 0.1)

    def _result(self, niche, input_str, method, confidence):
        subjects = []
        if niche in self.subjects:
            subjects = self.subjects[niche].get("subjects", [niche])

        print(f"  🔍 Resolver: '{input_str}' → '{niche}' [{method}] ({confidence:.0%})")

        return {
            "niche":      niche,
            "matched":    input_str,
            "method":     method,
            "confidence": confidence,
            "subjects":   subjects
        }

    def suggest(self, user_input: str, limit=5) -> list:
        """Similar niches suggest karo"""
        raw = user_input.strip().lower()
        suggestions = []

        for niche in self.all_niches:
            if raw in niche or any(w in niche for w in raw.split()):
                suggestions.append(niche)

        return suggestions[:limit]

    def list_all(self) -> list:
        """Sab available niches list karo"""
        return sorted(self.all_niches)