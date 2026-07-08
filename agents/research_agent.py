from data.resolver import NicheResolver


class ResearchAgent:

    def __init__(self):
        self.resolver = NicheResolver()

    def research(self, niche):
        print("\n🔍 Research Agent Running...\n")

        resolved = self.resolver.resolve(niche)

        report = {
            "niche": resolved["niche"],
            "subjects": resolved["subjects"],

            "pages": 40,
            "age_group": "kids",
            "target_age": "4-8 Years",
            "difficulty": "Easy",

            "title": "",
            "keywords": [],
            "kdp_category": ""
        }

        print("Research Complete ✅")

        return report