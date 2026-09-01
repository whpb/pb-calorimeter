import csv

# the derived columns are deliberately dropped; a re-analysis recomputes them from scratch
RAW_COLUMNS = {"Timestamp": str, "Elapsed (min)": float, "Plate temperature (C)": float,
               "Master temperature (C)": float, "Heater utilisation (%)": float, "Q_abs (W)": float}
OPTIONAL = ("Master temperature (C)",)  # absent from files recorded before the probe existed


def load_samples(path):
    """Read a results CSV back into raw sample rows, ready to be analysed again."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"{path.name} holds no samples")
    missing = [name for name in RAW_COLUMNS if name not in rows[0] and name not in OPTIONAL]
    if missing:
        raise ValueError(f"{path.name} is not a results CSV; it is missing {missing}")
    # a missing column and a blank cell mean the same thing: no probe reading for this row
    return [{name: (None if not row.get(name) else convert(row[name]))
             for name, convert in RAW_COLUMNS.items()} for row in rows]
