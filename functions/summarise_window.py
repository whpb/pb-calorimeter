import statistics


def summarise_window(samples, key, window):
    """Describe one selected zone: its extent, and the spread of `key` within it."""
    start, end = window
    values = [row[key] for row in samples
              if start <= row["Elapsed (min)"] <= end and row[key] is not None]
    if not values:
        raise ValueError(f"The {start:.2f}-{end:.2f} min window holds no {key} samples")
    return {
        "start_min": round(start, 3),
        "end_min": round(end, 3),
        "duration_min": round(end - start, 3),
        "samples": len(values),
        "mean": round(statistics.fmean(values), 3),
        # sd and spread are the "did I capture whole noise cycles?" read-out
        "sd": round(statistics.stdev(values), 3) if len(values) > 1 else 0.0,
        "spread": round(max(values) - min(values), 3),
    }
