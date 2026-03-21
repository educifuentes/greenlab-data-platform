import streamlit as st
from helpers.utilities.model_catalog import build_global_model_registry
from helpers.utilities.find_model import find_model
from helpers.ui_components.render_model_lineage import render_model_lineage

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

    if selected_model:
        df_model = find_model(selected_model)
        if df_model is not None:
            render_model_lineage(df_model)

else:
    st.info("No se encontraron esquemas ni modelos registrados.")

st.subheader("Documentación")
st.info("Aquí se mostrará la documentación del schema seleccionado próximamente.")