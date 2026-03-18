import streamlit as st
from helpers.widgets.generate_mermaid import generate_mermaid

def render_lineage(final_df, models_registry):
    """
    Renders the Mermaid diagram and provides an expander for raw metadata.
    """
    st.subheader("Data Lineage")
    
    mermaid_code = generate_mermaid(final_df, models_registry)
    
    st.markdown(f"```mermaid\n{mermaid_code}\n```")
    
    with st.expander("Raw Metadata"):
        st.write(final_df.attrs)
