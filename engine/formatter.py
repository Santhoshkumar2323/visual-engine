def format_value(value: float, unit: str):

    if unit == "percentage":
        return f"{value:.2f}%"

    if unit == "crore":
        return f"{value:,.0f} Cr"

    abs_n = abs(value)

    if abs_n >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f}B"
    if abs_n >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    if abs_n >= 1_000:
        return f"{value/1_000:.1f}K"

    return f"{value:.0f}"