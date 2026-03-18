import streamlit as st

from helpers.ui_components.render_model_lineage import render_model_lineage
from models.generacion_electrica.intermediate._int_generacion_electrica__energia_centrales import int_generacion_electrica__energia_centrales

st.title("Lineage")

df = int_generacion_electrica__energia_centrales()
render_model_lineage(df)

