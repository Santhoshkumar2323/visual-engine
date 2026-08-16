# Visual Engine

> Paste your numbers, get a publication-ready chart.

**Live app:** https://visual-engine.streamlit.app/

---

## Overview

Visual Engine is a Streamlit-based chart generator built for fast, consistent, branded data visualization — the kind of chart you'd drop into a report or a deck without opening a design tool. You paste labels and values, pick a chart style and theme, and get back a high-resolution PNG with a branded title bar, author credit, and source footer baked in.

Under the hood it's a small, deliberately linear pipeline: Streamlit collects input → a parsing layer validates and cleans it → a rendering layer (matplotlib) turns it into a fully composed figure → the figure is exported as PNG bytes, displayed inline, and offered as a download. There's no database, no session persistence, no backend service — every chart is generated fresh, in-memory, on each click of Generate.

---

## How input works

Labels and values are entered as two parallel lists — one label per line, one value per line — matched by position. Line 1 of labels pairs with line 1 of values, and so on. If the counts don't match, the app stops with a clear error before attempting to render anything.

Values are parsed by a dedicated cleanup routine that's built to tolerate messy, real-world pasted data rather than requiring clean numbers. Specifically, it handles:

- **Currency symbols** — ₹ and $ are stripped automatically
- **Comma-grouping** — both Western (`1,500`) and Indian (`1,50,000`) grouping styles
- **Decimals** — `45.678` parses as-is
- **Accounting-style negatives** — `(1500)` is read as `-1500`
- **Trailing-minus negatives** — `1500-` is read as `-1500`
- **Combinations of the above** — e.g. `(₹12,50,000)` correctly parses as `-1,250,000`, because symbol-stripping and negative-detection are applied independently before the number itself is extracted

Importantly, the *original text you typed* is preserved and used as the on-chart label — only the parsed numeric value drives the chart's math (bar length, axis scale, sort order). This means your typed formatting is what appears on the bar itself; values aren't reformatted for display.

---

## Chart types

Two chart types are available, and both are built on the same underlying pipeline — they diverge only in orientation and visual treatment:

**Ranked Bar** — horizontal bars, solid fill. Best for comparing a ranked list of values at a glance. When the dataset mixes positive and negative values, the axis auto-scales symmetrically around zero so both directions are visually balanced.

**Holo Bar** — vertical bars, unfilled outline-only styling for a more graphic, editorial look. Shares the exact same axis-scaling and sorting logic as Ranked Bar underneath — the difference is purely visual.

Sort order (Preserve Order / Ascending / Descending) applies identically to both chart types via a shared sorting step that runs before rendering.

---

## Themes

Three fixed color palettes, defined as static, immutable presets so every chart using the same theme looks pixel-consistent:

- **Obsidian (Dark Mode)** — near-black background, cyan accent
- **Midnight Gold (Luxury)** — deep navy background, gold accent
- **Swiss Clean (Light Mode)** — white background, blue accent

Themes are applied uniformly — there are no chart-type-specific color overrides, so switching themes never changes chart behavior, only appearance.

---

## Architecture

The codebase is split into four single-responsibility modules:

| Module | Responsibility |
|---|---|
| `parser.py` | Turns raw pasted text into validated numeric records. This is the only layer where bad input is caught — malformed numbers, mismatched label/value counts — before anything reaches the renderer. |
| `theme.py` | Defines the color palettes as frozen dataclasses. No logic, just data. |
| `renderer.py` | Owns all chart-generation logic: figure sizing, axis-range calculation, sort application, per-bar value labeling, the branded title/footer chrome, and final PNG export. |
| `app.py` | The Streamlit UI layer only — collects user input, calls `parse_input()`, dispatches to the appropriate render function, and displays the result. Contains no chart logic itself. |

**Request flow:** user input in the browser → `parse_input()` validates and structures it → `render_ranked_bar()` or `render_holo_bar()` builds the matplotlib figure and returns PNG bytes → the bytes are shown inline via `st.image()` and offered via a download button. Nothing is written to disk at any point.

---

## Built with

- [Streamlit](https://streamlit.io/) — UI and app framework
- [Matplotlib](https://matplotlib.org/) — chart rendering and PNG export