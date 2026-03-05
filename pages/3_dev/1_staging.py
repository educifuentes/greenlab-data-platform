import streamlit as st

from models.contaminantes.staging._stg_contaminantes__energia_centrales_00_15 import stg_contaminantes__energia_centrales_00_15
from models.contaminantes.staging._stg_contaminantes__energia_centrales_16_19 import stg_contaminantes__energia_centrales_16_19
from models.contaminantes.staging._stg_contaminantes__energia_centrales_20_22 import stg_contaminantes__energia_centrales_20_22
from models.contaminantes.staging._stg_contaminantes__energia_centrales_23 import stg_contaminantes__energia_centrales_23
from models.contaminantes.staging._stg_contaminantes__energia_centrales_24 import stg_contaminantes__energia_centrales_24

from utilities.ui_components.render_model import render_model_ui
from utilities.ui_components.icons import render_icon

# Page settings and header
st.title("Staging")

st.header("Contaminantes")

render_model_ui(stg_contaminantes__energia_centrales_00_15(), 
                table_name="Energia 2000 al 2015")

render_model_ui(stg_contaminantes__energia_centrales_16_19(), 
                table_name="Energia 2016 al 2019")

render_model_ui(stg_contaminantes__energia_centrales_20_22(), 
                table_name="Energia 2020 al 2022")

render_model_ui(stg_contaminantes__energia_centrales_23(), 
                table_name="Energia 2023")

render_model_ui(stg_contaminantes__energia_centrales_24(), 
                table_name="Energia 2024")



st.code(stg_contaminantes__energia_centrales_24().columns)