import toml
from pathlib import Path

APP_NAME = "Podcast Splitter"

def get_version():
    # pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
    pyproject_file = Path(__file__).parent / "pyproject.toml"
    pyproject = toml.load(pyproject_file)
    return pyproject.get("project", {}).get("version", "0.0.0")


def get_app_name():
    return APP_NAME
