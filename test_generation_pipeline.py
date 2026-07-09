from agents.engines.generation_pipeline import GenerationPipeline

pipeline = GenerationPipeline()

pipeline.configure(
    keyword="jungle animals",
    book_type="coloring_books",
    age_group="kids",
    total_pages=10,
)

pages = pipeline.generate()

print("\nSUMMARY")
print(pipeline.summary())

print("\nSTATISTICS")
print(pipeline.statistics())

print("\nFIRST PAGE")
print(pages[0])