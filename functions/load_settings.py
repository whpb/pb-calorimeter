import json
from pathlib import Path


def load_settings():
    """Load and parse settings.json from the repo root."""
    path = Path(__file__).resolve().parent.parent / "settings.json"
    with open(path) as f:
        return json.load(f)
