import os
import sys
import time
import json
import config
from datetime import datetime

from agents.research_agent import ResearchAgent
from agents.book_agent import BookAgent
from agents.prompt_agent import PromptAgent
from agents.download_agent import DownloadAgent
from agents.quality_agent import QualityAgent
from agents.pdf_agent import PDFAgent
from agents.cover_agent import CoverAgent
from agents.marketing_agent import MarketingAgent
from agents.publish_agent import PublishAgent
from agents.analytics_agent import AnalyticsAgent
from agents.seo_agent import SEOAgent
from agents.image_generator_agent import ImageGeneratorAgent

# ✅ Colors
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ═══════════════════════════════════════
# UI Helpers
# ═══════════════════════════════════════

def header():
    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}{BLUE}   🚀 AI KDP AUTOPILOT V3{RESET}")
    print(f"{BOLD}{'═'*60}{RESET}")
    print(f"   Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{BOLD}{'═'*60}{RESET}\n")

def step(number, total, name):
    print(f"\n{BOLD}{CYAN}[{number}/{total}] {name}{RESET}")
    print(f"{'─'*40}")

def success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def run_step(fn, step_name, optional=False):
    try:
        start  = time.time()
        result = fn()
        elapsed = time.time() - start
        success(f"{step_name} — {elapsed:.1f}s")
        return result
    except Exception as e:
        if optional:
            warning(f"{step_name} skipped: {e}")
            return None
        error(f"{step_name} failed: {e}")
        sys.exit(1)

def summary(niche, book, seo, pdf_path, start_time):
    elapsed = time.time() - start_time
    mins    = int(elapsed // 60)
    secs    = int(elapsed % 60)

    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}{GREEN}   🎉 AUTOPILOT COMPLETE!{RESET}")
    print(f"{BOLD}{'═'*60}{RESET}")
    print(f"   Niche     : {niche}")
    print(f"   Title     : {book.get('title', 'N/A')}")
    print(f"   Pages     : {book.get('pages', 'N/A')}")
    print(f"   PDF       : {pdf_path if pdf_path else 'N/A'}")

    keywords = seo.get("keywords", []) if seo else []
    if keywords:
        preview = keywords[:3] if isinstance(keywords, list) else []
        print(f"   Keywords  : {', '.join(preview)}...")

    print(f"   Time      : {mins}m {secs}s")
    print(f"{BOLD}{'═'*60}{RESET}\n")

def save_run_log(niche, book, seo, pdf_path, start_str):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path  = f"logs/run_{timestamp}.txt"

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("AI KDP AUTOPILOT — Run Log\n")
        f.write("="*40 + "\n")
        f.write(f"Niche    : {niche}\n")
        f.write(f"Title    : {book.get('title', 'N/A')}\n")
        f.write(f"Pages    : {book.get('pages', 'N/A')}\n")
        f.write(f"PDF      : {pdf_path}\n")
        f.write(f"Started  : {start_str}\n")
        f.write(f"Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        keywords = seo.get("keywords", []) if seo else []
        if keywords:
            f.write(f"Keywords : {', '.join(keywords[:7])}\n")

    success(f"Log saved : logs/run_{timestamp}.txt")
    return log_path

# ═══════════════════════════════════════
# Main Pipeline
# ═══════════════════════════════════════

def main():
    start_time = time.time()
    start_str  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    header()

    # ✅ Input
    niche = input(f"{BOLD}Enter Book Niche : {RESET}").strip()
    if not niche:
        error("Niche empty hai!")
        sys.exit(1)

    season = input(
        f"{BOLD}Season (christmas/halloween/easter/summer/winter/skip) : {RESET}"
    ).strip().lower()
    if season == "skip" or season == "":
        season = None

    print(f"\n{BOLD}Pipeline starting: {GREEN}{niche}{RESET}")
    if season:
        print(f"{BOLD}Season           : {GREEN}{season}{RESET}")

    TOTAL = 10

    # ─────────────────────────────
    # Step 1: Research
    # ─────────────────────────────
    step(1, TOTAL, "Research Agent")
    research_agent = ResearchAgent()
    report = run_step(
        lambda: research_agent.research(niche),
        "Research"
    )

    # ─────────────────────────────
    # Step 2: Book
    # ─────────────────────────────
    step(2, TOTAL, "Book Agent")
    book_agent = BookAgent()
    book = run_step(
        lambda: book_agent.create(report),
        "Book Created"
    )

    # ─────────────────────────────
    # Step 3: Prompts
    # ─────────────────────────────
    step(3, TOTAL, "Prompt Agent")
    prompt_agent = PromptAgent()
    prompts = run_step(
        lambda: prompt_agent.generate(report, season=season),
        "Prompts Generated"
    )

    # ─────────────────────────────
    # Step 4: Download Images
    # ─────────────────────────────
    step(4, TOTAL, "Download Agent")
    download_agent = DownloadAgent()
    images_ok = run_step(
        lambda: download_agent.import_images(book["pages"]),
        "Images Imported",
        optional=True
    )
    if not images_ok:
        warning("Images missing — PDF will have placeholders")

    # ─────────────────────────────
    # Step 5: Quality
    # ─────────────────────────────
    step(5, TOTAL, "Quality Agent")
    quality_agent = QualityAgent()
    quality = run_step(
        lambda: quality_agent.check(book),
        "Quality Check"
    )

    # ─────────────────────────────
    # Step 6: SEO
    # ─────────────────────────────
    step(6, TOTAL, "SEO Agent")
    seo_agent = SEOAgent()
    seo = run_step(
        lambda: seo_agent.generate(book),
        "SEO Generated"
    )

    # ─────────────────────────────
    # Step 7: PDF
    # ─────────────────────────────
    step(7, TOTAL, "PDF Agent")
    pdf_agent = PDFAgent()
    pdf_path = run_step(
        lambda: pdf_agent.build(book),
        "PDF Built"
    )
    # PDF path string ensure karo
    if isinstance(pdf_path, dict):
        pdf_path = pdf_path.get("path", "output/pdfs/book.pdf")

    # ─────────────────────────────
    # Step 8: Cover
    # ─────────────────────────────
    step(8, TOTAL, "Cover Agent")
    cover_agent = CoverAgent()
    cover = run_step(
        lambda: cover_agent.create(book),
        "Cover Created"
    )

    # ─────────────────────────────
    # Step 9: Marketing
    # ─────────────────────────────
    step(9, TOTAL, "Marketing Agent")
    marketing_agent = MarketingAgent()
    marketing = run_step(
        lambda: marketing_agent.generate(book),
        "Marketing Content Ready"
    )

    # ─────────────────────────────
    # Step 10: Publish + Analytics
    # ─────────────────────────────
    step(10, TOTAL, "Publish + Analytics")

    publish_agent = PublishAgent()
    publish = run_step(
        lambda: publish_agent.generate(book, seo),
        "Publish Files Ready"
    )

    analytics_agent = AnalyticsAgent()
    analytics = run_step(
        lambda: analytics_agent.generate(report, book),
        "Analytics Done"
    )

    # ─────────────────────────────
    # Summary + Log
    # ─────────────────────────────
    summary(niche, book, seo, pdf_path, start_time)
    save_run_log(niche, book, seo, pdf_path, start_str)

if __name__ == "__main__":
    main()