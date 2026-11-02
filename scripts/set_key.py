import getpass
import os
import sys

NAME = sys.argv[1] if len(sys.argv) > 1 else "STABILITY_API_KEY"
ENV_PATH = ".env"


def main():
    if not os.path.exists("master.py"):
        print("Run this from the project folder (the one that contains master.py).")
        return 1

    print("Go to your browser, copy the key, then paste it below.")
    print("Nothing is shown while you paste.")
    value = getpass.getpass(NAME + ": ").strip()

    problem = None
    if not value:
        problem = "nothing was entered"
    elif any(ch.isspace() for ch in value):
        problem = "it contains spaces or a line break, so it is not a key"
    elif value.lower().startswith(("export", "python", "http", "git ", "cat ")):
        problem = "it looks like a terminal command or a link, not a key"
    elif "/" in value or "." in value or "stability" in value.lower():
        problem = "it looks like a web address or page text (it has a slash, dot or the word stability), not a key"
    elif len(value) < 20:
        problem = "it is only " + str(len(value)) + " characters, too short for a key"
    if problem:
        print("NOT saved: " + problem + ".")
        return 1

    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            lines = f.read().splitlines()

    out = []
    replaced = False
    for line in lines:
        if line.startswith(NAME + "="):
            if not replaced:
                out.append(NAME + "=" + value)
                replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(NAME + "=" + value)

    with open(ENV_PATH, "w") as f:
        f.write("\n".join(out) + "\n")
    os.chmod(ENV_PATH, 0o600)

    print("Saved " + NAME + " | length " + str(len(value)) + " | starts with sk-: " + str(value.startswith("sk-")))
    return 0


sys.exit(main())
