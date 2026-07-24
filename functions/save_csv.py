import csv

from functions.resolve_save_path import resolve_save_path


def save_csv(row, settings):
    """Write a single result row to a new CSV file at the resolved save path."""
    path = resolve_save_path(settings)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)
    print(f"Saved results to {path}")
