import streamlit as st
from helpers.ui_components.render_icon import render_icon

st.header("Data Modelling")

stages = ["sources", "staging", "intermediate", "marts", "exposures"]
# 5 columns for stages, 4 columns for arrows
cols = st.columns(9, vertical_alignment="center")

for i, stage in enumerate(stages):
    # Stage container
    with cols[i * 2]:
        # Using native alignment as requested, removed border
        with st.container(border=False, horizontal_alignment="center"):
            st.markdown(f"# {render_icon(stage)}")
            st.markdown(f"**{stage.capitalize()}**")
    
    # Arrow
    if i < len(stages) - 1:
        with cols[i * 2 + 1]:
            # Applying standard markdown and letting vertical_alignment on cols do the work
            # Adding an explicitly horizontally-centered container if it's visually better
            with st.container(horizontal_alignment="center", vertical_alignment="center"):
                st.markdown("#### :material/arrow_forward:")