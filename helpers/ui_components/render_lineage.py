import streamlit as st
import streamlit_mermaid as st_mm
from helpers.widgets.generate_mermaid import generate_mermaid

def render_lineage(df):
    """
    Renders the Mermaid diagram and provides an expander for raw metadata.
    """
    st.subheader("Data Lineage")
    
    mermaid_code = generate_mermaid(df)
    
    st_mm.st_mermaid(mermaid_code, height=400)
    
    with st.expander("Raw Metadata"):
        st.write(df.attrs)


