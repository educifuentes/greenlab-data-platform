import streamlit as st
import os
import re

from helpers.ui_components.render_docs import render_model_docs
from helpers.ui_components.icons import render_icon

st.set_page_config(page_title="Guias de Uso", layout="wide")

# Page settings and header
st.title(f"{render_icon('guides')} Guias de Uso")
st.markdown("Essential information for developing and contributing to the Greenlab Data Platform.")

# Define the guides and their corresponding files
guides = {
    "Data Pipeline": "guides/1_data_pipeline.md",
    "Folder and File Structure": "guides/2_folder_structure_models.md",
    "Documentacion": "guides/3_documentacion_structure.md",
    "Buenas Practicas": "guides/5_best_practices.md",
    "Git Workflow": "guides/6_git_workflow.md",
    "Development Setup": "guides/7_development_setup.md",
    "Cloud Hosting": "guides/8_cloud_hosting.md"
}

# Create tabs
tabs = st.tabs(list(guides.keys()))

# Display content for each tab
for tab, (title, file_path) in zip(tabs, guides.items()):
    with tab:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Parse markdown to support local images via st.image()
                pattern = r"!\[(.*?)\]\((.*?)\)"
                last_idx = 0
                for match in re.finditer(pattern, content):
                    start, end = match.span()
                    
                    # Render markdown before image
                    text_before = content[last_idx:start]
                    if text_before.strip():
                        st.markdown(text_before)
                        
                    # Extract and check image
                    alt_text = match.group(1)
                    img_path = match.group(2)
                    if os.path.exists(img_path):
                        st.image(img_path, caption=alt_text, width=400)
                    else:
                        st.markdown(match.group(0)) # Render as text if missing
                        
                    last_idx = end
                    
                # Render remaining markdown
                remaining_text = content[last_idx:]
                if remaining_text.strip():
                    st.markdown(remaining_text)
        except FileNotFoundError:
            st.error(f"Guide file not found: {file_path}")