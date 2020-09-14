from pathlib import Path

for i in Path("cogs/").iterdir():
    print(i.stem)

def f(*x):
    print(" ".join(x))
f("test test test")