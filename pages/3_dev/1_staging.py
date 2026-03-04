import streamlit as st

from models.staging.censo_2024._stg_censo_2024__personas import stg_censo_2024__personas
from models.staging.censo_2024._stg_censo_2024__hogares import stg_censo_2024__hogares
from models.staging.censo_2024._stg_censo_2024__viviendas import stg_censo_2024__viviendas

from models.staging.censo_2024._stg_censo_2024__codigos import (
    stg_censo_2024__codigos_regiones,
    stg_censo_2024__codigos_provincias,
    stg_censo_2024__codigos_comunas
)

from utilities.ui_components.render_model import render_model_ui
from utilities.ui_components.icons import render_icon

# Page settings and header
st.title("Staging")

# Create tabs for organization
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    f"{render_icon('person')} personas",
    f"{render_icon('hogares')} hogares",
    f"{render_icon('dashboard')} viviendas",
    f"{render_icon('map')} regiones", 
    f"{render_icon('map')} provincias",
    f"{render_icon('map')} comunas",
])

with tab1:
    personas_df = stg_censo_2024__personas()
    st.warning("Sample de 10k como input")
    
    render_model_ui(personas_df, table_name="Personas")

with tab2:
    hogares_df = stg_censo_2024__hogares()
    render_model_ui(hogares_df, table_name="Hogares")

with tab3:
    viviendas_df = stg_censo_2024__viviendas()
    render_model_ui(viviendas_df, table_name="Viviendas")

with tab4:
    regiones_df = stg_censo_2024__codigos_regiones()
    render_model_ui(regiones_df, table_name="Regiones")

with tab5:
    provincias_df = stg_censo_2024__codigos_provincias()
    render_model_ui(provincias_df, table_name="Provincias")

with tab6:
    comunas_df = stg_censo_2024__codigos_comunas()
    render_model_ui(comunas_df, table_name="Comunas")