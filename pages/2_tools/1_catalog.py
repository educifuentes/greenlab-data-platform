import streamlit as st
from helpers.model_catalog import build_global_model_registry
from helpers.ui_components.icons import render_icon

st.title(f"{render_icon('catalog')} Data Catalog")
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
        stages = sorted(df_catalog["stage"].unique().tolist())
        selected_stage = st.multiselect("Filter by Stage", options=stages)
        
    # Apply Filters
    df_filtered = df_catalog.copy()
    if selected_schema:
        df_filtered = df_filtered[df_filtered["schema"].isin(selected_schema)]
        
    if selected_stage:
        df_filtered = df_filtered[df_filtered["stage"].isin(selected_stage)]

    # Configure dataframe columns for proper Links
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "schema": st.column_config.TextColumn("Schema"),
            "stage": st.column_config.TextColumn("Stage"),
            "model": st.column_config.TextColumn("Model Name"),
            "link": st.column_config.LinkColumn("View Model", display_text="View Details ↗")
        }
    )
else:
    st.info("No models found in the models directory.")
