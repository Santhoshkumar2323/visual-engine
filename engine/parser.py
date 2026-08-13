import re


def clean_numeric(text):
    t = text.strip()

    negative = False

    if t.startswith("(") and t.endswith(")"):
        negative = True
        t = t[1:-1]

    if t.endswith("-"):
        negative = True
        t = t[:-1]

    if t.startswith("-"):
        negative = True
        t = t[1:]

    t = re.sub(r"[₹$,]", "", t)
    t = re.sub(r"\s+", " ", t)

    match = re.search(r"[-+]?\d*\.?\d+", t)
    if not match:
        raise ValueError(f"Invalid numeric value: {text}")

    number = float(match.group())

    if negative:
        number = -number

    return number


def parse_input(labels_text, values_text):
    labels = [l.strip() for l in labels_text.split("\n") if l.strip()]
    values = [v.strip() for v in values_text.split("\n") if v.strip()]

    if len(labels) != len(values):
        raise ValueError("Labels and values count mismatch.")

    data = []

    for label, raw in zip(labels, values):
        numeric = clean_numeric(raw)

        data.append({
            "label": label,
            "value": numeric,
            "display": raw.strip()
        })

    return data