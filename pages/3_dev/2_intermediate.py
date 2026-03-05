import streamlit as st

from models.contaminantes.intermediate._int_contaminantes__energia_centrales import int_contaminantes__energia_centrales

from utilities.ui_components.render_model import render_model_ui
from utilities.ui_components.icons import render_icon

st.title("Intermediate")

render_model_ui(int_contaminantes__energia_centrales(), table_name="Energia centrales por fecha y hora")

