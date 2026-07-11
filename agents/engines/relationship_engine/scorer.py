"""
==========================================================
AI KDP AUTOPILOT V10
Relationship Scorer
==========================================================
"""


class Scorer:

    class Scorer:

        def score(self, text, keywords):

            text = text.lower()

            score = 0

            for word in keywords:
                if word in text:
                    score += 10

            return score