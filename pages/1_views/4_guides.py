import streamlit as st

from helpers.ui_components.render_docs import render_model_docs
from helpers.ui_components.icons import render_icon

st.set_page_config(page_title="Guias de Uso", layout="wide")

# Page settings and header
st.title("User Guides")
st.markdown("Essential information for developing and contributing to the Greenlab Data Platform.")

# Define the guides and their corresponding files
guides = {
    "Setup": "guides/development_setup.md",
    "Git Workflow": "guides/git_workflow.md",
    "Data Architecture": "guides/data_architecture.md",
    "Naming Conventions": "guides/naming_conventions.md",
    "Best Practices": "guides/best_practices.md"
}

# Create tabs
tabs = st.tabs(list(guides.keys()))

# Display content for each tab
for tab, (title, file_path) in zip(tabs, guides.items()):
    with tab:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                st.markdown(content)
        except FileNotFoundError:
            st.error(f"Guide file not found: {file_path}")