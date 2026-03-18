import streamlit as st

from helpers.set_lineage import set_lineage
from helpers.ui_components.render_lineage import render_lineage

from models.generacion_electrica.intermediate._int_generacion_electrica__energia_centrales import int_generacion_electrica__energia_centrales

st.title("Lineage")


df = int_generacion_electrica__energia_centrales()

df_lineage = set_lineage(df)

render_lineage(df_lineage)


