from agents.prompt.prompt_engine_v8 import PromptEngineV8
from agents.engines.animal_engine import AnimalEngine

scene = AnimalEngine().build(
    subject="lion",
    age_group="kids",
    page_number=1,
    total_pages=10,
)

engine = PromptEngineV8()

prompt = engine.build_final(
    page=1,
    keyword="jungle animals",
    subject="lion",
    scene=scene,
)

print("\nPROMPT")
print(prompt)

print("\nHEALTH")
print(engine.health())

print("\nSTATISTICS")
print(engine.statistics([prompt]))