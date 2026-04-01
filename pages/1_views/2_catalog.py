import streamlit as st
import pandas as pd

from helpers.utilities.model_catalog import build_global_model_registry
from helpers.ui_components.icons import render_icon
from helpers.ui_components.dataframe_column_display import dataframe_column_display


st.title(f"{render_icon('logo')} Greenlab Data Platform")

st.markdown(
    "Bienvenido a la plataforma central de gobierno de datos de Greenlab! \n\n"
    "Explora y descubre nuestro ecosistema de información, diseñado para asegurar "
    "la trazabilidad, calidad y transparencia en cada capa de nuestros modelos analíticos."
)



st.subheader(f"{render_icon('catalog')} Catalog")
st.markdown("Browse and search across all multi-schema models registered in the codebase.")

# Generate Catalog data dynamically
df_catalog = build_global_model_registry("models")

if not df_catalog.empty:
    
    # Place filters side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        schemas = sorted(df_catalog["schema"].unique().tolist())
        selected_schema = st.multiselect("Filter by Schema", options=schemas)
        
    with col2:
        expected_order = ["exposures", "marts", "intermediate", "staging", "sources"]
        stages = sorted(df_catalog["stage"].unique().tolist(), key=lambda x: expected_order.index(x) if x in expected_order else len(expected_order))
        selected_stage = st.multiselect("Filter by Stage", options=stages)
        
    # Apply Filters
    df_filtered = df_catalog.copy()

    # Apply Custom Sorting: first by schema (alphabetical), then by stage (custom order)
    stage_order = ["exposures", "marts", "intermediate", "staging", "sources"]
    df_filtered["stage"] = pd.Categorical(df_filtered["stage"], categories=stage_order, ordered=True)
    df_filtered = df_filtered.sort_values(["schema", "stage"])

    if selected_schema:
        df_filtered = df_filtered[df_filtered["schema"].isin(selected_schema)]
        
    if selected_stage:
        df_filtered = df_filtered[df_filtered["stage"].isin(selected_stage)]

    # Prepare the stage column for st.column_config.MultiselectColumn (expects a list)
    df_filtered["stage"] = df_filtered["stage"].astype(object).apply(lambda x: [x])

    # Configure dataframe columns for proper Links
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "schema": st.column_config.TextColumn("Schema"),
            "stage": st.column_config.MultiselectColumn(
                "Stage",
                options=[
                    "exposures",
                    "marts",
                    "intermediate",
                    "staging",
                    "sources",
                ],
                # Colors correspond sequentially to the options list above
                color=["#dc3545", "#ffc107", "#007bff", "#28a745", "#6c757d"]
            ),
            "model": st.column_config.TextColumn("Model Name"),
            "link": st.column_config.LinkColumn("View Model", display_text="View Details ↗")
        }
    )
else:
    st.info("No models found in the models directory.")
