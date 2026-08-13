def compute_layout(count: int, ratio: str):

    base_sizes = {
        "Landscape (16:9)": (13, 7),
        "Square (1:1)": (9, 9),
        "Vertical (9:16)": (7, 13)
    }

    width, height = base_sizes.get(ratio, (13, 7))

    if count > 8:
        height += (count - 8) * 0.4

    return width, height