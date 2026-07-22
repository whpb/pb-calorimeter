import json
from pathlib import Path


def load_settings():
    path = Path(__file__).resolve().parent.parent / "settings.json"
    with open(path) as f:
        return json.load(f)
