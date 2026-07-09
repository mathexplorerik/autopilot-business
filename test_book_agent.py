from agents.book_agent import BookAgent

agent = BookAgent()

book = agent.create_book(
    keyword="jungle animals",
    book_type="coloring_books",
    age_group="kids",
)

print("\nBOOK SUMMARY")
print(agent.summary())

print("\nSTATISTICS")
print(agent.statistics())

print("\nHEALTH")
print(agent.health())

path = agent.save()

print("\nSAVED TO")
print(path)