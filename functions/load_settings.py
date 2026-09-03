import json

from functions.resolve_docs_folder import resolve_docs_folder


def load_settings():
    """Load and parse settings.json from the operator's docs folder, seeding it if absent."""
    path = resolve_docs_folder() / "settings.json"
    with open(path) as f:
        return json.load(f)
