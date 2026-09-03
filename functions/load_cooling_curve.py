import csv

from functions.resolve_docs_folder import resolve_docs_folder

CURVE_FILE = "pb_cooling_capacity.csv"


def load_cooling_curve():
    """Load the plate temperature / heating output calibration sweep, sorted by temperature."""
    path = resolve_docs_folder() / CURVE_FILE
    if not path.exists():
        raise FileNotFoundError(f"Cooling capacity curve not found at {path}")
    # the file carries a UTF-8 BOM and CRLF endings, hence utf-8-sig and newline=""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        # sorted by temperature because the sweep is recorded in heating-output order
        rows = sorted((float(temp), float(output)) for temp, output in reader if temp)
    if len(rows) < 2:
        raise ValueError(f"{CURVE_FILE} needs at least two points to interpolate between")
    print(f"Loaded {len(rows)} curve points spanning {rows[0][0]:.2f} to {rows[-1][0]:.2f} C")
    return [temp for temp, _ in rows], [output for _, output in rows]
