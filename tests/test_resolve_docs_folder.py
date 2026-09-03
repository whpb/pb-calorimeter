from functions.resolve_docs_folder import SEEDED, resolve_docs_folder


def test_lands_under_documents_and_is_created(docs_home):
    folder = resolve_docs_folder()
    assert folder == docs_home / "Documents" / "PBCal" / "docs" and folder.is_dir()


def test_seeds_every_file_the_operator_may_edit(docs_home):
    folder = resolve_docs_folder()
    assert {path.name for path in folder.iterdir()} == set(SEEDED)


def test_settings_are_seeded_from_the_shipped_default(docs_home):
    """settings.json is gitignored, so it can only ship under the default's name."""
    from functions.bundled_path import bundled_path

    seeded = (resolve_docs_folder() / "settings.json").read_text()
    assert seeded == bundled_path("settings.default.json").read_text()


def test_an_edited_file_is_never_overwritten(docs_home):
    """An upgrade must not throw away a curve or a template the operator has tuned."""
    edited = resolve_docs_folder() / "pb_cooling_capacity.csv"
    edited.write_text("mine")
    resolve_docs_folder()
    assert edited.read_text() == "mine"


def test_a_deleted_file_comes_back(docs_home):
    restored = resolve_docs_folder() / "report_template.typ"
    restored.unlink()
    assert resolve_docs_folder() and restored.is_file()


def test_asking_twice_is_harmless(docs_home):
    """Every load_settings call resolves it, so it must be cheap and idempotent."""
    assert resolve_docs_folder() == resolve_docs_folder()


def test_survives_a_missing_bundle(docs_home, monkeypatch, tmp_path):
    """Artwork and defaults may be absent; resolving the folder must still not raise."""
    from functions import bundled_path as anchor

    monkeypatch.setattr(anchor, "ROOT", tmp_path / "nothing-here")
    assert resolve_docs_folder().is_dir()
