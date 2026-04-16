import streamlit as st

from helpers.ui_components.render_docs import render_markdown_file
from helpers.ui_components.render_icon import render_icon

st.set_page_config(page_title="Guias de Uso", layout="wide")

# Page settings and header
st.title(f"{render_icon('guides')} Guias de Uso")
st.markdown("Essential information for developing and contributing to the Greenlab Data Platform.")

# Define the guides and their corresponding files
guides = {
    "Data Pipeline": "guides/1_data_pipeline.md",
    "Estructura de Carpetas": "guides/2_folder_structure_models.md",
    "Documentacion": "guides/3_documentacion_structure.md",
    # "Buenas Practicas": "guides/5_best_practices.md",
    # "Git Workflow": "guides/6_git_workflow.md",
    # "Development Setup": "guides/7_development_setup.md",
    # "Cloud Hosting": "guides/8_cloud_hosting.md"
}

# Create tabs
tabs = st.tabs(list(guides.keys()))

# Display content for each tab
for tab, (title, file_path) in zip(tabs, guides.items()):
    with tab:
        render_markdown_file(file_path)