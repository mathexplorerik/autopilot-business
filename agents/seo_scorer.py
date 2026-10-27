"""
SEO Scorer (V16)
Checklist score (0-100) for whether a book listing follows common KDP
good practice. It does NOT predict ranking or sales.

The limits below (title 200, keyword 50, description 4000, 7 keyword
slots) are from memory of KDP guidelines and could not be verified in
the build environment. Check them against the current KDP help pages
and edit the constants if they have changed.
"""

import re


class SEOScorer:

    MIN_TITLE_CHARS = 30
    MAX_TITLE_CHARS = 200
    TITLE_KEYWORD_WINDOW = 60
    MIN_DESCRIPTION_CHARS = 300
    MAX_DESCRIPTION_CHARS = 4000
    KEYWORD_SLOTS = 7
    MAX_KEYWORD_CHARS = 50

    AGE_RANGE = re.compile(r"[0-9]+ *- *[0-9]+")
    WORDS = re.compile(r"[a-z0-9]+")

    def _text(self, value):
        return value.strip() if isinstance(value, str) else ""

    def _keywords(self, value):
        if isinstance(value, list):
            items = value
        elif isinstance(value, str):
            items = value.split(",")
        else:
            items = []
        return [k.strip() for k in items if isinstance(k, str) and k.strip()]

    def _mentions_age(self, text):
        lower = text.lower()
        if self.AGE_RANGE.search(lower):
            return True
        words = self.WORDS.findall(lower)
        return "age" in words or "ages" in words

    def score(self, seo, niche=""):
        seo = seo if isinstance(seo, dict) else {}
        title = self._text(seo.get("title"))
        subtitle = self._text(seo.get("subtitle"))
        description = self._text(seo.get("description"))
        keywords = self._keywords(seo.get("keywords"))
        niche_l = self._text(niche).lower()
        n_kw = len(keywords)

        checks = []

        def add(name, max_points, passed, detail):
            checks.append({
                "name": name,
                "max_points": max_points,
                "points": max_points if passed else 0,
                "passed": bool(passed),
                "detail": detail,
            })

        add(
            "title_length", 15,
            self.MIN_TITLE_CHARS <= len(title) <= self.MAX_TITLE_CHARS,
            "title is " + str(len(title)) + " characters (want "
            + str(self.MIN_TITLE_CHARS) + "-" + str(self.MAX_TITLE_CHARS) + ")",
        )

        if niche_l:
            window = title.lower()[:self.TITLE_KEYWORD_WINDOW]
            add(
                "niche_in_title_start", 15, niche_l in window,
                "niche keyword should appear in the first "
                + str(self.TITLE_KEYWORD_WINDOW) + " characters of the title",
            )
        else:
            add("niche_in_title_start", 15, False, "no niche was given, cannot check")

        add("subtitle_present", 5, len(subtitle) > 0, "subtitle is empty")

        add(
            "age_range_mentioned", 10,
            self._mentions_age(title + " " + subtitle),
            "title or subtitle should state the age range (for example Ages 4-8)",
        )

        add(
            "description_min_length", 15,
            len(description) >= self.MIN_DESCRIPTION_CHARS,
            "description is " + str(len(description)) + " characters (want at least "
            + str(self.MIN_DESCRIPTION_CHARS) + ")",
        )

        add(
            "description_max_length", 5,
            0 < len(description) <= self.MAX_DESCRIPTION_CHARS,
            "description should be 1-" + str(self.MAX_DESCRIPTION_CHARS) + " characters",
        )

        add(
            "keyword_slots_used", 15, n_kw == self.KEYWORD_SLOTS,
            str(n_kw) + " keywords given (want exactly " + str(self.KEYWORD_SLOTS) + ")",
        )

        lowered = [k.lower() for k in keywords]
        add(
            "no_duplicate_keywords", 5,
            n_kw > 0 and len(set(lowered)) == n_kw,
            "keywords contain duplicates (ignoring upper/lower case) or none were given",
        )

        add(
            "keyword_length", 5,
            n_kw > 0 and all(len(k) <= self.MAX_KEYWORD_CHARS for k in keywords),
            "every keyword must be at most " + str(self.MAX_KEYWORD_CHARS) + " characters",
        )

        if niche_l and n_kw > 0:
            with_niche = sum(1 for k in lowered if niche_l in k)
            add(
                "niche_in_keywords", 10, with_niche * 2 >= n_kw,
                str(with_niche) + " of " + str(n_kw) + " keywords contain the niche (want at least half)",
            )
        else:
            add("niche_in_keywords", 10, False, "no niche or no keywords, cannot check")

        total = sum(c["points"] for c in checks)
        return {
            "score": total,
            "max_score": 100,
            "checks": checks,
            "failed": [c["name"] + ": " + c["detail"] for c in checks if not c["passed"]],
        }
