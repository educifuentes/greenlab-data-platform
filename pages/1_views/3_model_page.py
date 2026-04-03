import streamlit as st

from helpers.utilities.model_catalog import build_global_model_registry
from helpers.ui_components.model_details_ui import render_model_details

st.title("Model Details")
st.markdown("Explore detailed information about registered models.")

# Obtener catálogo
df_catalog = build_global_model_registry("models")

if not df_catalog.empty:

    all_schemas = ["All"] + sorted(df_catalog["schema"].dropna().unique().tolist())
    all_stages = ["All"] + sorted(df_catalog["stage"].dropna().unique().tolist())

    col1, col2, col3 = st.columns([2, 1, 1])

    with col2:
        selected_schema = st.selectbox("Filter by Schema", options=all_schemas)
    with col3:
        selected_stage = st.selectbox("Filter by Stage", options=all_stages)

    df_filtered = df_catalog.copy()
    if selected_schema != "All":
        df_filtered = df_filtered[df_filtered["schema"] == selected_schema]
    if selected_stage != "All":
        df_filtered = df_filtered[df_filtered["stage"] == selected_stage]
        
    filtered_models = sorted(df_filtered["model"].dropna().unique().tolist())

    # Pre-select model from session state if it exists
    default_model = None
    if "selected_model" in st.session_state and st.session_state["selected_model"] in filtered_models:
        default_model = st.session_state["selected_model"]
        
    index = filtered_models.index(default_model) if default_model else 0

    with col1:
        selected_model = st.selectbox("Select Model", options=filtered_models, index=index if filtered_models else None)
        
    # Save the selected model back to session state so it persists
    if selected_model:
        st.session_state["selected_model"] = selected_model

    st.divider()

    if selected_model:
        render_model_details(selected_model)
    else:
        st.warning("No models found matching the selected filters.")

else:
    st.info("No schemas or models found in the directory.")