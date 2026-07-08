from agents.data.resolver import NicheResolver

class ResearchAgent:

    def research(self, niche):
        print("\n🔍 Research Agent Running...\n")

        # ✅ Resolver use karo
        resolver = NicheResolver()
        resolved = resolver.resolve(niche)

        niche    = resolved["niche"]
        subjects = resolved["subjects"]
        # ... baaki code same