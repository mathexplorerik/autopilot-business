"""
Publish readiness (V16)
Decides whether a finished book is actually ready to upload, and says
exactly why not. READY only when there are no blockers.

The requirements here (7 keyword slots, a price, at least one category,
a cover file) are from memory of what KDP asks for and have not been
checked against the current KDP help pages.
"""

import os

from agents.safety.content_safety import check_text


class PublishReadiness:

    EXPECTED_KEYWORDS = 7
    WARN_BELOW_SEO_SCORE = 80

    def _text(self, value):
        return value.strip() if isinstance(value, str) else ""

    def _is_number(self, value):
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def _is_int(self, value):
        return isinstance(value, int) and not isinstance(value, bool)

    def _file_ok(self, path):
        return isinstance(path, str) and os.path.isfile(path) and os.path.getsize(path) > 0

    def _keywords(self, value):
        if isinstance(value, list):
            items = value
        elif isinstance(value, str):
            items = value.split(",")
        else:
            items = []
        return [k.strip() for k in items if isinstance(k, str) and k.strip()]

    def assess(self, seo, price, total_pages, images_found, cover_path, interior_pdf_path):
        blockers = []
        warnings = []
        seo = seo if isinstance(seo, dict) else {}

        if not self._file_ok(interior_pdf_path):
            blockers.append("interior PDF is missing or empty")

        if not self._is_int(total_pages) or total_pages <= 0:
            blockers.append("page count is missing or not a positive whole number")
        elif not self._is_int(images_found) or images_found < 0:
            blockers.append("the number of real images in the PDF is unknown")
        elif images_found == 0:
            blockers.append(
                "none of the " + str(total_pages) + " pages has a real image (all placeholders)"
            )
        elif images_found < total_pages:
            blockers.append(
                str(total_pages - images_found) + " of " + str(total_pages)
                + " pages are still placeholders"
            )
        elif images_found > total_pages:
            warnings.append("more images than pages was reported; check the page counts")

        if not self._file_ok(cover_path):
            blockers.append("cover file is missing or empty")

        for field in ("title", "subtitle", "description"):
            if not self._text(seo.get(field)):
                blockers.append(field + " is missing")

        keywords = self._keywords(seo.get("keywords"))
        if not keywords:
            blockers.append("no keywords")
        elif len(keywords) != self.EXPECTED_KEYWORDS:
            warnings.append(
                str(len(keywords)) + " keywords given (KDP has " + str(self.EXPECTED_KEYWORDS) + " slots)"
            )

        categories = seo.get("categories")
        has_category = isinstance(categories, list) and any(
            isinstance(c, str) and c.strip() for c in categories
        )
        if not has_category:
            blockers.append("no categories")

        if not self._is_number(price) or price <= 0:
            blockers.append("price is missing or not above zero")

        listing_text = " ".join([
            self._text(seo.get("title")),
            self._text(seo.get("subtitle")),
            self._text(seo.get("description")),
            ", ".join(keywords),
        ])
        safety = check_text(listing_text)
        if not safety["safe"]:
            found = ", ".join(sorted({phrase for phrase, category in safety["matches"]}))
            blockers.append("content safety: listing text contains " + found)

        score = seo.get("score")
        score_value = score.get("score") if isinstance(score, dict) else None
        if not self._is_number(score_value):
            warnings.append("no SEO score was calculated")
        elif score_value < self.WARN_BELOW_SEO_SCORE:
            warnings.append(
                "SEO score is " + str(score_value) + "/100 (below " + str(self.WARN_BELOW_SEO_SCORE) + ")"
            )

        ready = len(blockers) == 0
        return {
            "verdict": "READY" if ready else "NOT READY",
            "ready": ready,
            "blockers": blockers,
            "warnings": warnings,
        }
