import streamlit as st

from helpers.constants.icons import ICONS
from helpers.ui_components.render_icon import render_icon
from helpers.utilities.get_version import get_git_version
from helpers.utilities.theme_manager import get_current_theme, set_theme

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Greenlab Censos | Dashboard",
    page_icon=render_icon("logo"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PAGE SETUP ---
import os

# Defining the pages based on the directory structure
pages = {
    "Vistas": [
        st.Page("pages/1_views/1_catalog.py", title="Catálogo", icon=render_icon("catalog"), default=True),
        st.Page("pages/1_views/2_model_details.py", title="Modelos", icon=render_icon("projects")),
        st.Page("pages/1_views/3_documentation.py", title="Documentación", icon=render_icon("documentation")),
        st.Page("pages/1_views/4_guides.py", title="Guias de Uso", icon=render_icon("lineage"))
        # st.Page("pages/1_views/5_demo.py", title="Demo", icon=render_icon("demo")),
    ],
}

# Only expose the development environment tabs locally
is_local = os.environ.get("ENVIRONMENT", "local").lower() == "local"
if is_local:
    pages["Desarrollo"] = [
        st.Page("pages/2_dev/1_staging.py", title="Staging", icon=render_icon("staging")),
        st.Page("pages/2_dev/2_intermediate.py", title="Intermediate", icon=render_icon("intermediate")),
        st.Page("pages/2_dev/3_marts.py", title="Marts", icon=render_icon("marts")),
        st.Page("pages/2_dev/4_exposures.py", title="Exposures", icon=render_icon("exposures")),
    ]




# --- SIDEBAR & BRANDING ---
with st.sidebar:
    st.markdown(f"# {render_icon('logo')} Greenlab")
    st.caption(f"{get_git_version()}")
    st.markdown("[Source Code](https://github.com/educifuentes/greenlab-data-platform)")
    
    st.divider()

# --- NAVIGATION ---
pg = st.navigation(pages)

if "model" in st.query_params:
    st.session_state["selected_model"] = st.query_params["model"]
    if pg.title != "view Model":
        st.switch_page("pages/1_views/2_model_details.py")

# --- RUN NAVIGATION ---
pg.run()