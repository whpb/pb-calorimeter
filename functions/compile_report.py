import json
import shutil
from pathlib import Path

import typst

TEMPLATE = "report_template.typ"
ASSETS = "assets"


def compile_report(summary, save_path):
    """Render report_template.typ against a run's summary, returning the PDF path."""
    repo = Path(__file__).resolve().parent.parent
    source = save_path.with_suffix(".typ")
    shutil.copyfile(repo / TEMPLATE, source)
    if (repo / ASSETS).is_dir():
        # the Typst root is the results folder, so repo-side images must travel with it
        shutil.copytree(repo / ASSETS, save_path.parent / ASSETS, dirs_exist_ok=True)
    data = save_path.with_suffix(".json")
    data.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    pdf = save_path.with_suffix(".pdf")
    try:
        # root is the results folder, so the template reaches its data and plot by name alone
        typst.compile(source, pdf, root=save_path.parent, sys_inputs={"data": data.name})
    except Exception as e:
        print(f"Typst failed; {source.name} and {data.name} are left in place to debug:\n{e}")
        return None
    return pdf
