import json
import shutil
from pathlib import Path

import typst

TEMPLATE = "report_template.typ"
ASSETS = "assets"


def compile_report(summary, save_path):
    """Render report_template.typ against a run's summary, returning the PDF path."""
    repo = Path(__file__).resolve().parent.parent
    root = save_path.parent.parent  # the results root: every run folder sits inside it
    source = save_path.with_suffix(".typ")
    shutil.copyfile(repo / TEMPLATE, source)
    if (repo / ASSETS).is_dir():
        # one shared copy at the root, reached as /assets/... - per run it would be 4.6 MB each
        shutil.copytree(repo / ASSETS, root / ASSETS, dirs_exist_ok=True)
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
