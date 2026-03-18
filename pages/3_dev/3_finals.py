import streamlit as st

from models.generacion_electrica.finals._fct_generacion_electrica import fct_generacion_electrica

from helpers.ui_components.render_model import render_model_ui
from helpers.ui_components.icons import render_icon

st.title("Finals")

render_model_ui(fct_generacion_electrica(), table_name="Generacion Electrica")