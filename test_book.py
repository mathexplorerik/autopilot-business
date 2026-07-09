from agents.engines.book_engine import BookEngine

engine = BookEngine()

blueprint = engine.build(
    keyword="Animals",
    book_type="coloring_books",
    age_group="4-8",
)

print(blueprint)