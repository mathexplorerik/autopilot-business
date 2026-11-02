import inspect
import os
import sys
import time

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)
sys.path.insert(0, os.path.join(root, "tests"))

import test_negative_cases as t

names = [n for n in dir(t) if n.startswith("test_") and inspect.isfunction(getattr(t, n))]
rows = []
for name in names:
    start = time.time()
    try:
        getattr(t, name)()
        status = "ok"
    except Exception as e:
        status = type(e).__name__
    rows.append((time.time() - start, name, status))

print()
rows.sort(reverse=True)
for seconds, name, status in rows:
    print(f"{seconds:7.2f}s  {status:12} {name}")
print("total:", round(sum(r[0] for r in rows), 1), "s")
