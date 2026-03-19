import streamlit as st
from helpers.model_catalog import build_global_model_registry

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
    
    # Renderizar el df con links
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "schema": st.column_config.TextColumn("Schema"),
            "stage": st.column_config.MultiselectColumn(
                "Stage",
                options=[
                    "staging",
                    "intermediate",
                    "marts",
                    "exposures",
                ],
                color=["#28a745", "#007bff", "#ffc107", "#dc3545"]
            ),
            "model": st.column_config.TextColumn("Model Name"),
            "link": st.column_config.LinkColumn("View Model", display_text="View Details ↗")
        }
    )
else:
    st.info("No se encontraron esquemas ni modelos registrados.")

st.subheader("Documentación")
st.info("Aquí se mostrará la documentación del schema seleccionado próximamente.")