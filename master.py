"""
==========================================================
AI Publishing OS V13
Master Command System
==========================================================
"""
import sys
import time
from datetime import datetime
from agents.utils.filename_sanitizer import sanitize_filename

# ✅ Colors
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


class MasterCommand:
    """
    One command — full pipeline.
    
    Usage:
        python3 master.py "diwali book"
        python3 master.py "jungle animals" --season christmas
        python3 master.py "dinosaurs" --pages 40 --age kids
    """

    COMMANDS = {
        "book":       "Generate complete book",
        "bundle":     "Generate 5 books from 1 niche",
        "tracing":    "Generate tracing book",
        "activity":   "Generate activity book",
        "help":       "Show help",
    }

    def __init__(self):
        self.start_time = time.time()

    def parse(self, args):
        """Parse command line arguments"""
        if not args:
            return self._show_help()

        # ✅ Extract niche (--portfolio/--dashboard are niche-less
        # commands, so the first arg may itself be a flag)
        niche = args[0].strip() if not args[0].startswith("--") else ""
        season  = None
        pages   = None
        age       = "kids"
        command   = "book"
        book_type = "coloring_books"

        # ✅ Parse flags
        i = 0 if args[0].startswith("--") else 1
        while i < len(args):
            if args[i] == "--season" and i+1 < len(args):
                season = args[i+1]
                i += 2
            elif args[i] == "--pages" and i+1 < len(args):
                pages = int(args[i+1])
                i += 2
            elif args[i] == "--age" and i+1 < len(args):
                age = args[i+1]
                i += 2
            elif args[i] == "--bundle":
                command = "bundle"
                i += 1
            elif args[i] == "--tracing":
                command = "tracing"
                i += 1
            elif args[i] == "--story":
                book_type = "story"
                i += 1
            elif args[i] == "--portfolio":
                command = "portfolio"
                i += 1
            elif args[i] == "--dashboard":
                command = "dashboard"
                i += 1
            else:
                i += 1

        return {
            "niche":     niche,
            "season":    season,
            "pages":     pages,
            "age":       age,
            "command":   command,
            "book_type": book_type,
        }

    def run(self, args=None):
        """Main entry point"""
        if args is None:
            args = sys.argv[1:]

        self._header()

        if not args or args[0] == "help":
            return self._show_help()

        # ✅ Parse
        config = self.parse(args)

        print(f"  📚 Niche   : {config['niche']}")
        print(f"  🎯 Command : {config['command']}")
        if config['season']:
            print(f"  🎄 Season  : {config['season']}")
        if config['pages']:
            print(f"  📄 Pages   : {config['pages']}")
        print(f"  👶 Age     : {config['age']}")
        print()

        # ✅ Execute
        if config['command'] == "bundle":
            return self._run_bundle(config)
        elif config['command'] == "tracing":
            return self._run_tracing(config)
        elif config['command'] == "portfolio":
            return self._run_portfolio(config)
        elif config['command'] == "dashboard":
            return self._run_dashboard(config)
        else:
            return self._run_book(config)

    def _run_portfolio(self, config):
        """Scan all known niches and rank them by opportunity + revenue potential"""
        print(f"{BOLD}{CYAN}▶ Running Portfolio Analysis...{RESET}\n")

        from agents.engines.research_engine import ResearchEngine
        from agents.engines.intelligence.portfolio_planner import PortfolioPlanner
        from agents.data.subjects import SUBJECTS

        engine = ResearchEngine()
        planner = PortfolioPlanner(engine)

        niches = list(SUBJECTS.keys())
        top_n = 5
        result = planner.top_n(niches, n=top_n, season=config.get("season", ""))

        print(f"{BOLD}Top {top_n} Niches by Portfolio Score{RESET}")
        print("-" * 55)
        for r in result:
            if "error" in r:
                print(f"  {r['niche']:20} ERROR: {r['error']}")
                continue
            print(
                f"  {r['niche']:20} score={r['portfolio_score']:5} "
                f"opp={r['opportunity_score']:3} "
                f"revenue=${r['estimated_monthly_revenue']}"
            )
        print("-" * 55)

        elapsed = time.time() - self.start_time
        print(f"\n{BOLD}{'=' * 55}{RESET}")
        print(f"{BOLD}{GREEN}   Done ({elapsed:.0f}s){RESET}")
        print(f"{BOLD}{'=' * 55}{RESET}\n")
        return result

    def _run_dashboard(self, config):
        """Generate a business-wide dashboard snapshot across all niches"""
        print(f"{BOLD}{CYAN}▶ Generating Business Dashboard...{RESET}\n")

        from agents.engines.research_engine import ResearchEngine
        from agents.engines.intelligence.pricing_intelligence import PricingIntelligence
        from agents.engines.intelligence.revenue_predictor import RevenuePredictor
        from agents.engines.intelligence.multi_market_optimizer import MultiMarketOptimizer
        from agents.engines.intelligence.portfolio_planner import PortfolioPlanner
        from agents.engines.intelligence.business_dashboard import BusinessDashboard
        from agents.data.subjects import SUBJECTS

        engine = ResearchEngine()
        pricing = PricingIntelligence()
        revenue = RevenuePredictor()
        mmo = MultiMarketOptimizer(pricing, revenue)
        portfolio = PortfolioPlanner(engine)
        dashboard = BusinessDashboard(engine, portfolio, mmo)

        niches = list(SUBJECTS.keys())
        snapshot = dashboard.generate(niches, season=config.get("season", ""), top_n=5)

        dashboard.print_summary(snapshot)
        saved_path = dashboard.save(snapshot)
        print(f"\n  📄 Saved: {saved_path}")

        elapsed = time.time() - self.start_time
        print(f"\n{BOLD}{'=' * 55}{RESET}")
        print(f"{BOLD}{GREEN}   Done ({elapsed:.0f}s){RESET}")
        print(f"{BOLD}{'=' * 55}{RESET}\n")
        return snapshot

    def _run_book(self, config):
        """Single book generate karo"""
        print(f"{BOLD}{CYAN}▶ Generating Book...{RESET}\n")

        # ✅ Import pipeline
        from agents.research_agent import ResearchAgent
        from agents.book_agent import BookAgent
        from agents.seo_agent import SEOAgent
        from agents.pdf_agent import PDFAgent
        from agents.cover_agent import CoverAgent
        from agents.marketing_agent import MarketingAgent
        from agents.publish_agent import PublishAgent
        from agents.analytics_agent import AnalyticsAgent

        results = {}

        # Research
        self._step("Research")
        research = ResearchAgent()
        report   = research.research(config['niche'], season=config.get('season', ''))
        results['research'] = '✅'

        # Book
        self._step("Book")
        book_agent = BookAgent()
        book = book_agent.create_book(
            keyword=report.niche,
            book_type=config.get("book_type", "coloring_books"),
            age_group=report.age_group,
            season=config.get("season"),
        )
        results['book'] = '✅'

        # Prompts
        self._step("Prompts")
        prompts = []
        if book.get("generated_pages"):
            prompts = [p.get("positive", "") for p in book["generated_pages"]]
            self._save_prompts(prompts, report.niche)
        results['prompts'] = '✅'

        # SEO
        self._step("SEO")
        seo_agent = SEOAgent()
        seo = seo_agent.generate(book)
        results['seo'] = '✅'

        # PDF
        self._step("PDF")
        pdf_agent = PDFAgent()
        pdf_path  = pdf_agent.build(book)
        if isinstance(pdf_path, dict):
            pdf_path = pdf_path.get("path", "")
        results['pdf'] = '✅'

        # Cover
        self._step("Cover")
        cover_agent = CoverAgent()
        cover_agent.create(book)
        results['cover'] = '✅'

        # Marketing
        self._step("Marketing")
        marketing_agent = MarketingAgent()
        marketing_agent.generate(book)
        results['marketing'] = '✅'

        # Publish
        self._step("Publish")
        publish_agent = PublishAgent()
        publish_agent.generate(book, seo)
        results['publish'] = '✅'

        # Analytics
        self._step("Analytics")
        analytics_agent = AnalyticsAgent()
        analytics_agent.generate(report, book)
        results['analytics'] = '✅'

        self._summary(config['niche'], book, pdf_path, results)
        return book

    def _run_bundle(self, config):
        """Bundle — 5 books ek saath"""
        print(f"{BOLD}{CYAN}▶ Generating Bundle (5 books)...{RESET}\n")

        book_types = [
            "coloring_books",
            "activity_book",
            "tracing_book",
            "maze_book",
            "dot_to_dot"
        ]

        results = []
        for i, book_type in enumerate(book_types, 1):
            print(f"\n{BOLD}📚 Book {i}/5 — {book_type}{RESET}")
            config['command'] = 'book'
            book = self._run_book({**config, 'command': 'book'})
            results.append(book)

        elapsed = time.time() - self.start_time
        print(f"\n{GREEN}🎉 Bundle Complete! 5 books in {elapsed:.0f}s{RESET}")
        return results

    def _run_tracing(self, config):
        """Tracing book generate karo"""
        print(f"{BOLD}{CYAN}▶ Generating Tracing Book...{RESET}\n")

        from agents.tracing_agent import TracingAgent
        agent  = TracingAgent()
        result = agent.generate({
            'niche':      config['niche'],
            'target_age': '3-6 Years',
            'title':      f'All-in-One Tracing Book for Kids'
        })

        print(f"\n{GREEN}✅ Tracing Book Complete!{RESET}")
        print(f"   PDF: {result['pdf_path']}")
        return result

    def _save_prompts(self, prompts, niche):
        """Prompts save karo"""
        import os
        safe  = sanitize_filename(niche)
        os.makedirs("output/prompts", exist_ok=True)
        with open(f"output/prompts/{safe}_simple.txt", "w") as f:
            f.write("\n".join(prompts))
        with open("output/prompts/prompts.txt", "w") as f:
            f.write("\n".join(prompts))

    def _step(self, name):
        print(f"  {GREEN}▶{RESET} {name}...")

    def _header(self):
        print(f"\n{BOLD}{'═'*55}{RESET}")
        print(f"{BOLD}{BLUE}   🚀 AI Publishing OS — Master Command{RESET}")
        print(f"{BOLD}{'═'*55}{RESET}")
        print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def _show_help(self):
        print(f"\n{BOLD}Usage:{RESET}")
        print(f"   python3 master.py <niche> [options]\n")
        print(f"{BOLD}Examples:{RESET}")
        print(f"   python3 master.py 'jungle animals'")
        print(f"   python3 master.py 'diwali' --season diwali")
        print(f"   python3 master.py 'dinosaurs' --pages 40")
        print(f"   python3 master.py 'animals' --bundle")
        print(f"   python3 master.py --tracing\n")
        print(f"{BOLD}Options:{RESET}")
        print(f"   --season  <name>   Season theme")
        print(f"   --pages   <num>    Page count")
        print(f"   --age     <group>  Age group")
        print(f"   --bundle           Generate 5 books")
        print(f"   --tracing          Tracing book\n")

    def _summary(self, niche, book, pdf_path, results):
        elapsed = time.time() - self.start_time
        print(f"\n{BOLD}{'═'*55}{RESET}")
        print(f"{BOLD}{GREEN}   🎉 COMPLETE!{RESET}")
        print(f"{BOLD}{'═'*55}{RESET}")
        print(f"   Niche  : {niche}")
        print(f"   Title  : {book.get('title', 'N/A')}")
        print(f"   Pages  : {book.get('total_pages', book.get('pages', 'N/A'))}")
        print(f"   PDF    : {pdf_path}")
        print(f"   Time   : {elapsed:.0f}s")
        print(f"{BOLD}{'═'*55}{RESET}\n")


if __name__ == "__main__":
    cmd = MasterCommand()
    cmd.run()
