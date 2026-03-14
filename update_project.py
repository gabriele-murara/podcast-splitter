import toml

with open("pyproject.toml", "r", encoding="utf-8") as f:
    pyproject = toml.load(f)

dependencies = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        elif line == '':
            continue
        elif line.startswith("#"):
            continue
        elif line.startswith("-"):
            continue

        dependencies.append(line)

pyproject.setdefault("project", {})
pyproject["project"]["dependencies"] = dependencies

with open("pyproject.toml", "w", encoding="utf-8") as f:
    toml.dump(pyproject, f)

print("pyproject.toml aggiornato con le dipendenze da requirements.txt")