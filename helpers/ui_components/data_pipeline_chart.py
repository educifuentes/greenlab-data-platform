import streamlit as st
from helpers.ui_components.render_icon import render_icon

def render_data_pipeline_chart():
    stages = ["sources", "staging", "intermediate", "marts", "exposures"]
    # Added empty outer padding columns to push elements closer together in the center.
    # The sequence is: [pad, stage, arrow, stage, arrow, stage, arrow, stage, arrow, stage, pad]
    cols = st.columns([1.5, 1, 0.5, 1, 0.5, 1, 0.5, 1, 0.5, 1, 1.5], vertical_alignment="center")

    for i, stage in enumerate(stages):
        # Stage container (shifted by +1 due to left padding)
        with cols[i * 2 + 1]:
            # Using native alignment as requested, removed border
            with st.container(border=False, horizontal_alignment="center"):
                st.markdown(f"# {render_icon(stage)}")
                st.markdown(f"**{stage.capitalize()}**")
        
        # Arrow (shifted by +1)
        if i < len(stages) - 1:
            with cols[i * 2 + 2]:
                # Applying standard markdown and letting vertical_alignment on cols do the work
                with st.container(horizontal_alignment="center"):
                    st.markdown("#### :material/arrow_forward:")
