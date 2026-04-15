import streamlit as st

from helpers.widgets.generate_lineage_chart import generate_lineage_chart
from helpers.ui_components.render_mermaid import render_mermaid

def render_model_lineage(df):
    """
    Renders the Mermaid diagram and provides an expander for raw metadata.
    """
    st.subheader("Data Lineage")
    
    mermaid_code = generate_lineage_chart(df)
    
    render_mermaid(mermaid_code, height=400)
    
    with st.expander("Raw Metadata"):
        st.write(df.attrs)


