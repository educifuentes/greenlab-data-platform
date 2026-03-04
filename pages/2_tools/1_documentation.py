import streamlit as st

from utilities.ui_components.render_docs import render_model_docs
from utilities.ui_components.icons import render_icon

st.set_page_config(page_title="Documentation", layout="wide")

# Page settings and header
st.title("Documentación")

# Create tabs for organization
tab1, tab2 = st.tabs([
    f"{render_icon('person')} personas",
    f"{render_icon('hogares')} hogares",
])

with tab1:
    render_model_docs("models/staging/censo_2024/_src_censo_2024.yml", target_name="personas")

with tab2:
    render_model_docs("models/staging/censo_2024/_src_censo_2024.yml", target_name="hogares")