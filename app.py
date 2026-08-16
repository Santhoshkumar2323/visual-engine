import streamlit as st

from engine.theme import THEMES
from engine.parser import parse_input
from engine.renderer import (
    render_ranked_bar,
    render_holo_bar
)

st.set_page_config(page_title="Visual Engine", layout="centered")

st.title("VISUAL ENGINE")

title = st.text_input("Title")
labels = st.text_area("Labels (one per line)")
values = st.text_area("Values (one per line)")

chart_type = st.selectbox("Chart Type", [
    "Ranked Bar",
    "Holo Bar"
])

sort_mode = st.selectbox("Sort Mode", [
    "Preserve Order",
    "Descending",
    "Ascending"
])

theme_choice = st.selectbox("Theme", list(THEMES.keys()))

author = st.text_input("Author")
footer = st.text_input("Source")

if st.button("Generate"):
    try:
        data = parse_input(labels, values)
        theme = THEMES[theme_choice]

        if chart_type == "Ranked Bar":
            img = render_ranked_bar(
                data, theme, title, footer, author, sort_mode
            )
            
        else:
            img = render_holo_bar(
                data, theme, title, footer, author, sort_mode
            )

        st.image(img, use_container_width=True)

        st.download_button(
            "Download PNG",
            img,
            file_name="chart.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(str(e))