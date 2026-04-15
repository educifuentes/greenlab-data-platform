import streamlit as st

from helpers.utilities.model_catalog import build_global_model_registry
from helpers.ui_components.render_model_documentation import render_model_documentation
from helpers.ui_components.icons import render_icon

st.set_page_config(page_title="Documentation", layout="wide")

st.title("Documentación")

# Get model catalog
df_catalog = build_global_model_registry()

# Filter only for marts
df_marts = df_catalog[df_catalog["stage"] == "marts"]

if not df_marts.empty:
    schemas = sorted(df_marts["schema"].unique())
    
    if schemas:
        tabs = st.tabs([schema.replace("_", " ").title() for schema in schemas])
        
        for tab, schema in zip(tabs, schemas):
            with tab:
                st.header(f"Esquema: {schema.replace('_', ' ').title()}")
                
                schema_models = df_marts[df_marts["schema"] == schema]
                
                for _, row in schema_models.iterrows():
                    model_name = row["model"]
                    with st.expander(f"Modelo: {model_name}", expanded=False):
                        render_model_documentation(model_name)
    else:
        st.info("No se encontraron esquemas en la etapa marts.")
else:
    st.info("No se encontraron modelos en la etapa marts.")