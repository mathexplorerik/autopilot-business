import config
from agents.research_agent import ResearchAgent
from agents.prompt_agent import PromptAgent
from agents.seo_agent import SEOAgent
from agents.book_agent import BookAgent
from agents.quality_agent import QualityAgent
from agents.pdf_agent import PDFAgent
from agents.cover_agent import CoverAgent
from agents.marketing_agent import MarketingAgent
from agents.publish_agent import PublishAgent
from agents.analytics_agent import AnalyticsAgent
from agents.image_agent import ImageAgent
print("=" * 60)
print("🚀 AI KDP AUTOPILOT")
print("=" * 60)

niche = input("\nEnter Book Niche : ")

research = ResearchAgent()

report = research.research(niche)

print("\n========== REPORT ==========")

for key, value in report.items():
    print(f"{key} : {value}")

prompt_agent = PromptAgent()

prompts = prompt_agent.generate(report)
image_agent = ImageAgent()

image_agent.prepare(prompts)
image_agent.import_images()


print("\n========== FIRST 5 PROMPTS ==========\n")

for prompt in prompts[:5]:
    print(prompt)

seo_agent = SEOAgent()

seo = seo_agent.generate(report)

print("\n========== SEO ==========\n")

print("Title:")
print(seo["title"])

print("\nSubtitle:")
print(seo["subtitle"])

book_agent = BookAgent()

book = book_agent.build(report, seo)

print("\n========== BOOK ==========\n")

print(book["title"])
print(f"Pages : {book['pages']}")
quality_agent = QualityAgent()

quality_agent.check(
    report,
    prompts,
    seo,
    book
)
pdf_agent = PDFAgent()

pdf_file = pdf_agent.build(book)

print("\n========== PDF ==========\n")
print(pdf_file)
cover_agent = CoverAgent()

cover = cover_agent.generate(book)

print("\n========== COVER ==========\n")

print("Title :", cover["title"])
print("Size  :", cover["size"])
marketing_agent = MarketingAgent()

marketing = marketing_agent.generate(book)

print("\n========== MARKETING ==========\n")

print("Pinterest:")
print(marketing["pinterest"])

print("\nInstagram:")
print(marketing["instagram"])
publish_agent = PublishAgent()

publish = publish_agent.generate(book, seo)

print("\n========== PUBLISH ==========\n")

print("Title:")
print(publish["title"])

print("\nPages:")
print(publish["pages"])
analytics_agent = AnalyticsAgent()

analytics = analytics_agent.generate(report, book)

print("\n========== ANALYTICS ==========\n")

print("Status:")
print(analytics["status"])

print("\nNiche:")
print(analytics["niche"])