"""
Relationship Matcher
"""


class Matcher:

    def match(self, keywords, candidates):

        if not keywords:
            return candidates

        matched = []

        for item in candidates:

            text = item.lower()

            if any(word.lower() in text for word in keywords):
                matched.append(item)

        if matched:
            return matched

        return candidates