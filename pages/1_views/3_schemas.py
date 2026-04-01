import streamlit as st

from helpers.utilities.model_catalog import build_global_model_registry
from helpers.ui_components.model_details_ui import render_model_details

st.title("Schemas")
st.markdown("Directorio de schemas")

# Obtener catálogo
df_catalog = build_global_model_registry("models")

if not df_catalog.empty:
    # 1. Selectbox con los schemas
    schemas = sorted(df_catalog["schema"].unique().tolist())
    selected_schema = st.selectbox("Seleccione un schema", options=schemas)
    
    st.subheader(f"Modelos - {selected_schema}")
    
    # 2. Filtrar el dataframe por el schema seleccionado
    df_filtered = df_catalog[df_catalog["schema"] == selected_schema]
    
    models = sorted(df_filtered["model"].dropna().unique().tolist())
    selected_model = st.selectbox("Seleccione un modelo", options=models)

    render_model_details(selected_model)

else:
    st.info("No se encontraron esquemas ni modelos registrados.")