import streamlit as st

from models.intermediate._int_censo_2024__personas import int_censo_2024__personas
from models.intermediate._int_censo_2024__hogares import int_censo_2024__hogares

# from models.staging.censo_2024._int_censo_2024__viviendas import int_censo_2024__viviendas

from utilities.ui_components.render_model import render_model_ui
from utilities.ui_components.icons import render_icon

# Page settings and header
st.title("Intermediate")

# Create tabs for organization
tab1, tab2, tab3 = st.tabs([
    f"{render_icon('person')} personas",
    f"{render_icon('hogares')} hogares",
    f"{render_icon('dashboard')} viviendas",
])

with tab1:
    personas_df = int_censo_2024__personas()
    render_model_ui(personas_df, table_name="Personas")

with tab2:
    hogares_df = int_censo_2024__hogares()
    render_model_ui(hogares_df, table_name="Hogares")

# with tab3:
#     viviendas_df = stg_censo_2024__viviendas()
#     render_model_ui(viviendas_df, table_name="Viviendas")