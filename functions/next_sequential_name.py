def next_sequential_name(folder, base, suffix=".csv"):
    """Return the next unused "{base} N" name in folder; suffix "" tests for a folder."""
    n = 1
    while (folder / f"{base} {n}{suffix}").exists():
        n += 1
    return f"{base} {n}"
