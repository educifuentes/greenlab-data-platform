import streamlit as st

from models.contaminantes.staging._stg_contaminantes__energia_centrales_00_15 import stg_contaminantes__energia_centrales_00_15
from models.contaminantes.staging._stg_contaminantes__energia_centrales_16_19 import stg_contaminantes__energia_centrales_16_19
from models.contaminantes.staging._stg_contaminantes__energia_centrales_20_23 import stg_contaminantes__energia_centrales_20_23
from models.contaminantes.staging._stg_contaminantes__energia_centrales_24 import stg_contaminantes__energia_centrales_24

from utilities.ui_components.render_model import render_model_ui
from utilities.ui_components.icons import render_icon

# Page settings and header
st.title("Staging")

st.header("Contaminantes")

render_model_ui(stg_contaminantes__energia_centrales_00_15(), 
                table_name="Energia 2000 al 2015")

# render_model_ui(stg_contaminantes__energia_centrales_16_19(), 
#                 table_name="Energia 2016 al 2019")

# render_model_ui(stg_contaminantes__energia_centrales_20_23(), 
#                 table_name="Energia 2020 al 2023")

# render_model_ui(stg_contaminantes__energia_centrales_24(), 
#                 table_name="Energia 2024")


# # Create tabs for organization
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#     f"{render_icon('person')} personas",
#     f"{render_icon('hogares')} hogares",
#     f"{render_icon('dashboard')} viviendas",
#     f"{render_icon('map')} regiones", 
#     f"{render_icon('map')} provincias",
#     f"{render_icon('map')} comunas",
# ])

# with tab1:
#     personas_df = stg_censo_2024__personas()
#     st.warning("Sample de 10k como input")
    
#     render_model_ui(personas_df, table_name="Personas")

# with tab2:
#     hogares_df = stg_censo_2024__hogares()
#     render_model_ui(hogares_df, table_name="Hogares")

# with tab3:
#     viviendas_df = stg_censo_2024__viviendas()
#     render_model_ui(viviendas_df, table_name="Viviendas")

# with tab4:
#     regiones_df = stg_censo_2024__codigos_regiones()
#     render_model_ui(regiones_df, table_name="Regiones")

# with tab5:
#     provincias_df = stg_censo_2024__codigos_provincias()
#     render_model_ui(provincias_df, table_name="Provincias")

# with tab6:
#     comunas_df = stg_censo_2024__codigos_comunas()
#     render_model_ui(comunas_df, table_name="Comunas")