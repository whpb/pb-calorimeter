import json
import shutil

import typst

from functions.bundled_path import bundled_path
from functions.resolve_docs_folder import resolve_docs_folder

TEMPLATE = "report_template.typ"
ASSETS = "assets"


def compile_report(summary, save_path):
    """Render report_template.typ against a run's summary, returning the PDF path."""
    root = save_path.parent.parent  # the results root: every run folder sits inside it
    source = save_path.with_suffix(".typ")
    # the operator's copy, so the page can be re-laid-out without a rebuild
    shutil.copyfile(resolve_docs_folder() / TEMPLATE, source)
    assets = bundled_path(ASSETS)
    if assets.is_dir():
        # one shared copy at the root, reached as /assets/... - per run it would be 6.5 MB each
        shutil.copytree(assets, root / ASSETS, dirs_exist_ok=True)
    data = save_path.with_suffix(".json")
    data.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    pdf = save_path.with_suffix(".pdf")
    try:
        # root bounds what the template may read; paths in it stay relative to the run folder
        typst.compile(source, pdf, root=root, sys_inputs={"data": data.name})
    except Exception as e:
        print(f"Typst failed; {source.name} and {data.name} are left in place to debug:\n{e}")
        return None
    return pdf
