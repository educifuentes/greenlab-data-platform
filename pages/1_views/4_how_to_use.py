import streamlit as st

from helpers.ui_components.render_docs import render_model_docs
from helpers.ui_components.icons import render_icon

st.set_page_config(page_title="Documentation", layout="wide")

# Page settings and header
st.title("Guias de Uso")

# pone ren tabs files de guides