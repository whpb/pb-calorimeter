import csv
import os
from pathlib import Path


def rewrite_csv(rows, path):
    """Rewrite the results file in full, now that the derived columns exist."""
    temporary = Path(path).with_suffix(".csv.tmp")
    with open(temporary, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    # atomic, so a failure part way through cannot leave the run with half a results file
    os.replace(temporary, path)
