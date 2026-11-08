"""
Command parser (V16)
Turns a plain request such as "50 page dinosaurs story book for ages 4-6
for christmas" into the arguments master.py understands.

Rule-based, not an AI model. It understands the patterns listed below and
nothing else. Every flag master.py ignores today (--pages, --age) produces a
warning, so a request never silently asks for something it will not get.
"""

import re
import shlex

from agents.data.subjects import list_niches


class CommandParser:

    SEASONS = ("christmas", "halloween", "easter", "diwali", "holi", "eid")
    PROVIDERS = ("manual", "stability", "flux", "gemini", "openai")
    MAX_TEXT = 500
    MAX_NICHE_CHARS = 60
    MIN_PAGES = 1
    MAX_PAGES = 300

    AGE_WORDS = {
        "toddler": "toddler", "toddlers": "toddler",
        "teen": "teens", "teens": "teens", "teenager": "teens", "teenagers": "teens",
        "adult": "adults", "adults": "adults",
        "kid": "kids", "kids": "kids", "child": "kids", "children": "kids",
    }

    FILLER = {
        "make", "create", "generate", "build", "produce", "write", "show", "display",
        "run", "see", "give", "list", "rank", "plan", "me", "please", "a", "an", "the",
        "of", "about", "on", "for", "with", "using", "via", "and", "to", "in", "my", "new",
        "book", "books", "coloring", "colouring", "color", "colour", "page", "pages", "pg", "pgs",
        "story", "kids", "kid", "children", "child", "toddler", "toddlers", "teen", "teens",
        "teenager", "teenagers", "adult", "adults", "age", "ages", "year", "years", "yr", "yrs",
        "old", "provider", "bundle", "portfolio", "dashboard", "business", "overview", "report",
        "strategy", "launch", "all", "niche", "niches",
        "banao", "bana", "do", "dena", "ki", "ka", "ke", "ek", "aur", "wali", "wala",
        "mujhe", "chahiye", "kitab", "kitaab", "dikhao",
    }

    PAGES_A = re.compile(r"(?<!\d)(\d{1,6})\s*-?\s*(?:pages?|pgs?)\b")
    PAGES_B = re.compile(r"\bpages?\s*[:=]?\s*(\d{1,6})\b")
    AGE_RANGE_A = re.compile(r"\bages?\s*(\d{1,2})\s*(?:-|to|\u2013)\s*(\d{1,2})\b")
    AGE_RANGE_B = re.compile(r"\b(\d{1,2})\s*(?:-|to|\u2013)\s*(\d{1,2})\s*(?:years?|yrs?|yo)\b")
    AGE_SINGLE_A = re.compile(r"\bages?\s*(\d{1,2})\b")
    AGE_SINGLE_B = re.compile(r"\b(\d{1,2})\s*(?:years?|yrs?)\s*old\b")
    PROVIDER = re.compile(r"\b(?:using|with|via|provider)\s+(manual|stability|flux|gemini|openai)\b")
    TOKEN = re.compile(r"[a-z][a-z'\-]*")

    def _cut(self, text, match):
        return text[:match.start()] + " " + text[match.end():]

    def _age_group(self, number):
        if number < 4:
            return "toddler"
        if number <= 8:
            return "kids"
        if number <= 15:
            return "teens"
        return "adults"

    def parse(self, text):
        result = {
            "ok": False,
            "text": text if isinstance(text, str) else None,
            "command": None, "niche": None, "book_type": None, "season": None,
            "pages": None, "age": None, "provider": None,
            "argv": [], "command_line": "",
            "warnings": [], "errors": [], "notes": [],
        }
        warnings, errors, notes = result["warnings"], result["errors"], result["notes"]

        if not isinstance(text, str) or not text.strip():
            errors.append("nothing to parse: write a request such as 'story book about lion for christmas'")
            return result

        t = text.strip().lower()
        if len(t) > self.MAX_TEXT:
            t = t[:self.MAX_TEXT]
            notes.append("the request was longer than " + str(self.MAX_TEXT) + " characters; only the first " + str(self.MAX_TEXT) + " were read")

        match = self.PROVIDER.search(t)
        if match:
            result["provider"] = match.group(1)
            t = self._cut(t, match)

        pages = None
        match = self.PAGES_A.search(t) or self.PAGES_B.search(t)
        if match:
            pages = int(match.group(1))
            t = self._cut(t, match)
        result["pages"] = pages

        age = None
        for pattern, kind in (
            (self.AGE_RANGE_A, "range"), (self.AGE_RANGE_B, "range"),
            (self.AGE_SINGLE_A, "single"), (self.AGE_SINGLE_B, "single"),
        ):
            match = pattern.search(t)
            if match:
                if kind == "range":
                    value = (int(match.group(1)) + int(match.group(2))) / 2
                else:
                    value = int(match.group(1))
                age = self._age_group(value)
                t = self._cut(t, match)
                break

        tokens = self.TOKEN.findall(t)
        if age is None:
            for word in tokens:
                if word in self.AGE_WORDS:
                    age = self.AGE_WORDS[word]
                    break
        result["age"] = age

        words = set(tokens)
        command_words = [c for c in ("dashboard", "portfolio", "bundle") if c in words]
        command = command_words[0] if command_words else "book"
        if len(command_words) > 1:
            notes.append("more than one command word found (" + ", ".join(command_words) + "); using " + command)
        result["command"] = command
        result["book_type"] = "story" if "story" in words else "coloring_books"

        season_found = next((w for w in tokens if w in self.SEASONS), None)
        content = [w for w in tokens if w not in self.FILLER]
        phrase = " ".join(content)
        known = set(list_niches())

        niche = None
        season = None
        if command in ("dashboard", "portfolio"):
            season = season_found
            leftover = [w for w in content if w not in self.SEASONS]
            if leftover:
                notes.append("words ignored for a " + command + " request: " + ", ".join(leftover))
        elif phrase in known:
            niche = phrase
        else:
            without_season = [w for w in content if w not in self.SEASONS]
            if without_season:
                niche = " ".join(without_season)
                season = season_found
            elif season_found:
                niche = season_found
                notes.append("'" + season_found + "' was the only subject, so it is used as the niche and no season is set")
        result["niche"] = niche
        result["season"] = season

        if command in ("book", "bundle"):
            if not niche:
                errors.append("no niche found: say what the book is about, for example 'lion' or 'dinosaurs'")
            elif len(niche) > self.MAX_NICHE_CHARS:
                errors.append("the niche is too long (more than " + str(self.MAX_NICHE_CHARS) + " characters)")
            elif niche in known:
                notes.append("'" + niche + "' is a known niche")
            else:
                notes.append("'" + niche + "' is not one of the known niches; research will map it to a close one and may fall back to a generic one")

        if pages is not None:
            if pages < self.MIN_PAGES or pages > self.MAX_PAGES:
                errors.append("pages must be between " + str(self.MIN_PAGES) + " and " + str(self.MAX_PAGES) + " (got " + str(pages) + ")")
            else:
                warnings.append("pages=" + str(pages) + " will be ignored: master.py builds the book with its default page count")
        if age and age != "kids":
            warnings.append("age=" + age + " will be ignored: the age comes from the niche research")
        provider = result["provider"]
        if provider and provider != "manual":
            warnings.append("provider " + provider + " needs a valid API key in .env; images from a real provider have not been verified yet")
        if command == "bundle":
            warnings.append("bundle is unverified: it has not been checked that it makes 5 different books (an early version repeated the same one)")

        if not errors:
            if command in ("dashboard", "portfolio"):
                argv = ["--" + command]
                if season:
                    argv += ["--season", season]
            else:
                argv = [niche]
                if result["book_type"] == "story":
                    argv.append("--story")
                if season:
                    argv += ["--season", season]
                if pages is not None:
                    argv += ["--pages", str(pages)]
                if age and age != "kids":
                    argv += ["--age", age]
                if provider:
                    argv += ["--provider", provider]
                if command == "bundle":
                    argv.append("--bundle")
            result["argv"] = argv
            result["command_line"] = "python3 master.py " + " ".join(shlex.quote(a) for a in argv)

        result["ok"] = not errors
        return result
