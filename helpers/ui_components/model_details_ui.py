import streamlit as st

from helpers.utilities.find_model import find_model
from helpers.ui_components.render_model_lineage import render_model_lineage
from helpers.ui_components.render_model import render_model_ui
from helpers.ui_components.render_model_documentation import render_model_documentation

def render_model_details(model_name: str):
    if model_name:
        st.markdown(f"# Model: `{model_name}`")
        
        df = find_model(model_name)
        
        if df is not None:
            st.subheader("Documentacion")
            render_model_documentation(model_name)
            
            st.subheader("Dataframe")
            render_model_ui(df, table_name=model_name)

            # 5. Render exact visualizations automatically at the bottom
            render_model_lineage(df)
    else:
        st.warning("No Model Selected.")
