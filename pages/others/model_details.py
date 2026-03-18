import streamlit as st

from helpers.find_model import find_model
from helpers.ui_components.render_model_lineage import render_model_lineage

# Retrieve query params from URL or session state (since st.switch_page drops query params)
model_name = st.query_params.get("model") or st.session_state.get("selected_model")

if model_name:
    st.header(f"Model: {model_name}")
    
    df = find_model(model_name)
    
    if df is not None:
        # 5. Render exact visualizations automatically
        render_model_lineage(df)
        
        st.subheader("Tabular Data Output")
        st.dataframe(df, use_container_width=True)
else:
    st.warning("No Model Selected.")