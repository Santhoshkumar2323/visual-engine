import matplotlib.pyplot as plt
import numpy as np
import io

LEFT = 0.10
RIGHT = 0.95
BOTTOM = 0.18
TOP = 0.88

def base_figure(theme, width=13, height=7):
    fig = plt.figure(figsize=(width, height), dpi=140)
    fig.patch.set_facecolor(theme.background)

    ax = fig.add_axes([LEFT, BOTTOM, RIGHT - LEFT, TOP - BOTTOM])
    ax.set_facecolor(theme.background)

    return fig, ax


def compute_axis(values):
    min_v = min(values)
    max_v = max(values)

    if min_v < 0 and max_v > 0:
        max_abs = max(abs(min_v), abs(max_v))
        pad = max_abs * 0.10
        return -max_abs - pad, max_abs + pad

    if min_v >= 0:
        pad = max_v * 0.10
        return 0, max_v + pad

    pad = abs(min_v) * 0.10
    return min_v - pad, 0


def apply_sort(data, mode):
    if mode == "Descending":
        return sorted(data, key=lambda x: x["value"], reverse=True)
    if mode == "Ascending":
        return sorted(data, key=lambda x: x["value"])
    return data


def finalize(fig, theme, title, footer, author):
    fig.add_artist(plt.Line2D(
        [0.02, 0.98], [0.93, 0.93],
        transform=fig.transFigure,
        color=theme.grid,
        linewidth=1.2
    ))

    fig.text(
        0.5,
        0.955,
        title.upper(),
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color=theme.text_main
    )

    fig.add_artist(plt.Line2D(
        [0.02, 0.98], [0.11, 0.11],
        transform=fig.transFigure,
        color=theme.grid,
        linewidth=1.2
    ))

    fig.text(
        0.02,
        0.065,
        author,
        ha="left",
        va="center",
        fontsize=11,
        fontweight="bold",
        color=theme.text_main
    )

    fig.text(
        0.98,
        0.065,
        footer,
        ha="right",
        va="center",
        fontsize=10,
        color=theme.text_sub
    )


def export(fig):
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf


def render_ranked_bar(data, theme, title, footer, author, sort_mode):

    data = apply_sort(data, sort_mode)

    height = max(5, len(data) * 0.8 + 2)
    fig, ax = base_figure(theme, 13, height)

    labels = [d["label"] for d in data]
    values = [d["value"] for d in data]

    y = np.arange(len(data))

    colors = [
        theme.hero if v >= 0 else theme.negative
        for v in values
    ]

    bars = ax.barh(y, values, height=0.55, color=colors)

    lower, upper = compute_axis(values)
    ax.set_xlim(lower, upper)

    ax.axvline(0, color=theme.grid, linewidth=1)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, color=theme.text_main)
    ax.tick_params(axis="x", colors=theme.text_sub)

    offset_scale = max(abs(lower), abs(upper)) * 0.02

    for bar, d in zip(bars, data):
        val = d["value"]
        offset = offset_scale

        x = val + offset if val >= 0 else val - offset

        ax.text(
            x,
            bar.get_y() + bar.get_height() / 2,
            d["display"],
            va="center",
            ha="left" if val >= 0 else "right",
            fontsize=12,
            fontweight="bold",
            color=theme.text_main
        )

    finalize(fig, theme, title, footer, author)
    return export(fig)


def render_holo_bar(data, theme, title, footer, author, sort_mode):

    data = apply_sort(data, sort_mode)

    height = max(6, len(data) * 1.0 + 3)
    fig, ax = base_figure(theme, 13, height)

    labels = [d["label"] for d in data]
    values = [d["value"] for d in data]

    x = np.arange(len(data))

    edge_colors = [
        theme.hero if v >= 0 else theme.negative
        for v in values
    ]

    bars = ax.bar(
        x,
        values,
        width=0.6,
        color="none",
        edgecolor=edge_colors,
        linewidth=3
    )

    lower, upper = compute_axis(values)
    ax.set_ylim(lower, upper)

    ax.axhline(0, color=theme.grid, linewidth=1)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, color=theme.text_main)

    ax.tick_params(axis="y", colors=theme.text_sub)

    offset_scale = max(abs(lower), abs(upper)) * 0.02

    for i, (bar, d) in enumerate(zip(bars, data)):
        val = d["value"]
        offset = offset_scale

        y_pos = val + offset if val >= 0 else val - offset

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_pos,
            d["display"],
            ha="center",
            va="bottom" if val >= 0 else "top",
            fontsize=12,
            fontweight="bold",
            color=edge_colors[i]
        )

    finalize(fig, theme, title, footer, author)
    return export(fig)


def render_pie(data, theme, title, footer, author):

    values = [d["value"] for d in data]

    if any(v < 0 for v in values):
        raise ValueError("Pie chart cannot contain negative values.")

    fig, ax = base_figure(theme, 8, 8)

    colors = [theme.hero] + [theme.muted] * (len(values) - 1)

    wedges, _ = ax.pie(
        values,
        colors=colors,
        startangle=90,
        wedgeprops=dict(edgecolor=theme.background)
    )

    ax.set_aspect("equal")

    legend_labels = [
        f"{d['label']} — {d['display']}"
        for d in data
    ]

    ax.legend(
        wedges,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        frameon=False,
        labelcolor=theme.text_main
    )

    finalize(fig, theme, title, footer, author)
    return export(fig)