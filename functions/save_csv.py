import csv
from pathlib import Path


def save_csv(row, path):
    """Append a single result row to the CSV file at path, writing a header if new."""
    is_new = not Path(path).exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if is_new:
            writer.writeheader()
        writer.writerow(row)
    print(f"Saved results to {path}")
