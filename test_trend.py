from agents.trend_agent import TrendAgent

agent = TrendAgent()

report = agent.analyze(
    keyword="Animals",
    book_type="coloring_books",
    age_group="4-8",
)

print(report)