from pathlib import Path

from agents.data.animals.actions import ACTIONS

output = Path("agents/data/animals/action_index.py")

lines = []

lines.append('"""')
lines.append("Auto-generated file.")
lines.append("DO NOT EDIT MANUALLY.")
lines.append('"""')
lines.append("")
lines.append("ACTION_INDEX = {")
lines.append("")

for category, actions in ACTIONS.items():

    for action in actions:

        lines.append(f'    "{action}": "{category}",')

    lines.append("")

lines.append("}")

output.write_text("\n".join(lines), encoding="utf-8")

print("===================================")
print("Action Index Generated Successfully")
print("===================================")
print(f"Categories : {len(ACTIONS)}")
print(f"Total Actions : {sum(len(v) for v in ACTIONS.values())}")
print(f"Saved : {output}")