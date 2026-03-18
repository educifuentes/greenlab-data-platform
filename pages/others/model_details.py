import streamlit as st

from helpers.model_catalog import build_global_model_registry
from helpers.ui_components.render_model_lineage import render_model_lineage

# Retrieve query params from URL
query_params = st.query_params
model_name = query_params.get("model", None)

if model_name:
    st.header(f"Model: {model_name}")
    
    from helpers.find_model import find_model
    
    df = find_model(model_name)
    
    if df is not None:
        # 5. Render exact visualizations automatically
        render_model_lineage(df)
        
        st.subheader("Tabular Data Output")
        st.dataframe(df, use_container_width=True)
else:
    st.warning("No Model Selected.")