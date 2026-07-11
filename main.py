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

# ═══════════════════════════════════════
# Colors
# ═══════════════════════════════════════
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
MAGENTA= "\033[95m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

TOTAL_STEPS = 11

# ═══════════════════════════════════════
# UI Helpers
# ═══════════════════════════════════════

def header():
    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}{BLUE}   🚀 AI KDP AUTOPILOT V4{RESET}")
    print(f"{BOLD}{BLUE}   Coloring Book Generator — Full Pipeline{RESET}")
    print(f"{BOLD}{'═'*60}{RESET}")
    print(f"   Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Steps    : {TOTAL_STEPS} agents")
    print(f"{BOLD}{'═'*60}{RESET}\n")

def step(number, name):
    print(f"\n{BOLD}{CYAN}[{number:02}/{TOTAL_STEPS}] {name}{RESET}")
    print(f"{'─'*40}")

def success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def info(msg):
    print(f"{MAGENTA}ℹ️  {msg}{RESET}")

def run_step(fn, step_name, optional=False):
    try:
        start   = time.time()
        result  = fn()
        elapsed = time.time() - start
        success(f"{step_name} — {elapsed:.1f}s")
        return result
    except Exception as e:
        if optional:
            warning(f"{step_name} skipped: {e}")
            return None
        error(f"{step_name} failed: {e}")
        sys.exit(1)

def print_summary(niche, book, seo, pdf_path, start_time, results):
    elapsed = time.time() - start_time
    mins    = int(elapsed // 60)
    secs    = int(elapsed % 60)

    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}{GREEN}   🎉 AUTOPILOT COMPLETE!{RESET}")
    print(f"{BOLD}{'═'*60}{RESET}")
    print(f"   Niche     : {niche}")
    print(f"   Title     : {book.get('title', 'N/A')}")
    print(f"   Pages     : {book.get('pages') or book.get('total_pages', 'N/A')}")
    print(f"   Age Group : {book.get('target_age') or book.get('age_group', 'N/A')}")
    print(f"   PDF       : {pdf_path or 'N/A'}")

    keywords = seo.get("keywords", []) if seo else []
    if keywords:
        kw = keywords[:3] if isinstance(keywords, list) else []
        print(f"   Keywords  : {', '.join(kw)}...")

    print(f"   Time      : {mins}m {secs}s")
    print(f"{BOLD}{'─'*60}{RESET}")

    # Steps summary
    print(f"\n   {'Step':<25} {'Status'}")
    print(f"   {'─'*35}")
    for name, status in results.items():
        icon = "✅" if status == "ok" else "⚠️ " if status == "skipped" else "❌"
        print(f"   {name:<25} {icon}")

    print(f"{BOLD}{'═'*60}{RESET}\n")

def save_run_log(niche, book, seo, pdf_path, start_str, results):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path  = f"logs/run_{timestamp}.txt"

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("AI KDP AUTOPILOT V4 — Run Log\n")
        f.write("="*40 + "\n")
        f.write(f"Niche    : {niche}\n")
        f.write(f"Title    : {book.get('title', 'N/A')}\n")
        f.write(f"Pages    : {book.get('pages') or book.get('total_pages', 'N/A')}\n")
        f.write(f"PDF      : {pdf_path}\n")
        f.write(f"Started  : {start_str}\n")
        f.write(f"Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        keywords = seo.get("keywords", []) if seo else []
        if keywords:
            f.write(f"Keywords : {', '.join(keywords[:7])}\n\n")

        f.write("STEPS:\n")
        for name, status in results.items():
            f.write(f"  {name}: {status}\n")

    success(f"Log saved : {log_path}")
    return log_path

# ═══════════════════════════════════════
# Input Helper
# ═══════════════════════════════════════

def get_input():
    niche = input(f"{BOLD}📚 Enter Book Niche : {RESET}").strip()
    if not niche:
        error("Niche empty hai!")
        sys.exit(1)

    print(f"\n{BOLD}🎄 Season Options:{RESET} christmas / halloween / easter / summer / winter / skip")
    season = input(f"{BOLD}   Enter Season    : {RESET}").strip().lower()
    if season in ("skip", ""):
        season = None

    print(f"\n{BOLD}🖼️  Image Options:{RESET}")
    print(f"   1 — Manual (downloads/ folder se)")
    print(f"   2 — AI Generate (Gemini API)")
    print(f"   3 — Skip images")
    image_mode = input(f"{BOLD}   Choose [1/2/3]   : {RESET}").strip()

    return niche, season, image_mode

# ═══════════════════════════════════════
# Main Pipeline
# ═══════════════════════════════════════

def main():
    start_time = time.time()
    start_str  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results    = {}

    header()

    # ✅ Input
    niche, season, image_mode = get_input()

    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}  Pipeline : {GREEN}{niche}{RESET}")
    if season:
        print(f"{BOLD}  Season   : {GREEN}{season}{RESET}")
    print(f"{BOLD}  Images   : {GREEN}{'Manual' if image_mode=='1' else 'AI Generate' if image_mode=='2' else 'Skip'}{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

    # ─────────────────────────────
    # Step 1: Research
    # ─────────────────────────────
    step(1, "Research Agent")
    research_agent = ResearchAgent()
    report = run_step(lambda: research_agent.research(niche), "Research")
    results["Research"] = "ok"

    # ─────────────────────────────
    # Step 2: Book
    # ─────────────────────────────
    step(2, "Book Agent")
    book_agent = BookAgent()
    book = run_step(lambda: book_agent.create_book(
        keyword=report.resolved_niche if hasattr(report, 'resolved_niche') else report.get("niche", "animals"),
        book_type="coloring_books",
        age_group=report.age_group if hasattr(report, 'age_group') else report.get("age_group", "kids")
    ), "Book Created")
    results["Book"] = "ok"

    # ─────────────────────────────
    # Step 3: Prompts
    # ─────────────────────────────
    step(3, "Prompt Agent")
    prompt_agent = PromptAgent()
    prompts = run_step(
        lambda: prompt_agent.generate(report, season=season),
        "Prompts Generated"
    )
    results["Prompts"] = "ok"

    # ─────────────────────────────
    # Step 4: Images
    # ─────────────────────────────
    step(4, "Image Agent")

    if image_mode == "1":
        # Manual — downloads/ se
        info("Manual mode — downloads/ folder se images import ho rahi hain")
        download_agent = DownloadAgent()
        images_ok = run_step(
            lambda: download_agent.import_images(book["pages"]),
            "Images Imported",
            optional=True
        )
        results["Images"] = "ok" if images_ok else "skipped"
        if not images_ok:
            warning("Images missing — PDF mein placeholders honge")

    elif image_mode == "2":
        # AI Generate — Gemini
        info("AI mode — Gemini se images generate ho rahi hain")
        image_agent = ImageGeneratorAgent()
        generated = run_step(
            lambda: image_agent.generate(prompts, niche=niche),
            "Images Generated",
            optional=True
        )
        results["Images"] = "ok" if generated else "skipped"

    else:
        # Skip
        warning("Images skipped — PDF mein placeholders honge")
        results["Images"] = "skipped"

    # ─────────────────────────────
    # Step 5: Quality
    # ─────────────────────────────
    step(5, "Quality Agent")
    quality_agent = QualityAgent()
    quality = run_step(lambda: quality_agent.check(book), "Quality Check")
    results["Quality"] = "ok"

    # ─────────────────────────────
    # Step 6: SEO
    # ─────────────────────────────
    step(6, "SEO Agent")
    seo_agent = SEOAgent()
    seo = run_step(lambda: seo_agent.generate(book), "SEO Generated")
    results["SEO"] = "ok"

    # ─────────────────────────────
    # Step 7: PDF
    # ─────────────────────────────
    step(7, "PDF Agent")
    pdf_agent = PDFAgent()
    pdf_path = run_step(lambda: pdf_agent.build(book), "PDF Built")
    if isinstance(pdf_path, dict):
        pdf_path = pdf_path.get("path", "output/pdfs/book.pdf")
    results["PDF"] = "ok"

    # ─────────────────────────────
    # Step 8: Cover
    # ─────────────────────────────
    step(8, "Cover Agent")
    cover_agent = CoverAgent()
    cover = run_step(lambda: cover_agent.create(book), "Cover Created")
    results["Cover"] = "ok"

    # ─────────────────────────────
    # Step 9: Marketing
    # ─────────────────────────────
    step(9, "Marketing Agent")
    marketing_agent = MarketingAgent()
    marketing = run_step(
        lambda: marketing_agent.generate(book),
        "Marketing Content Ready"
    )
    results["Marketing"] = "ok"

    # ─────────────────────────────
    # Step 10: Publish
    # ─────────────────────────────
    step(10, "Publish Agent")
    publish_agent = PublishAgent()
    publish = run_step(
        lambda: publish_agent.generate(book, seo),
        "Publish Files Ready"
    )
    results["Publish"] = "ok"

    # ─────────────────────────────
    # Step 11: Analytics
    # ─────────────────────────────
    step(11, "Analytics Agent")
    analytics_agent = AnalyticsAgent()
    analytics = run_step(
        lambda: analytics_agent.generate(report, book),
        "Analytics Done"
    )
    results["Analytics"] = "ok"

    # ─────────────────────────────
    # Summary + Log
    # ─────────────────────────────
    print_summary(niche, book, seo, pdf_path, start_time, results)
    save_run_log(niche, book, seo, pdf_path, start_str, results)

if __name__ == "__main__":
    main()