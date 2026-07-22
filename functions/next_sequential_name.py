def next_sequential_name(folder, base):
    n = 1
    while (folder / f"{base} {n}.csv").exists():
        n += 1
    return f"{base} {n}"
