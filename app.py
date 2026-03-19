import streamlit as st

from helpers.ui_components.icons import ICONS, render_icon
from helpers.get_version import get_git_version
from helpers.theme_manager import get_current_theme, set_theme

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
        st.Page("pages/1_views/2_catalog.py", title="Catalogo", icon=render_icon("catalog"), default=True),
        st.Page("pages/1_views/3_schemas.py", title="Schemas", icon=render_icon("projects")),
        st.Page("pages/1_views/4_how_to_use.py", title="Guias", icon=render_icon("documentation")),
        st.Page("pages/others/model_details.py", title="view Model", visibility="hidden")
    ],
}

# Only expose the development environment tabs locally
is_local = os.environ.get("ENVIRONMENT", "local").lower() == "local"
if is_local:
    pages["Desarrollo"] = [
        st.Page("pages/3_dev/1_staging.py", title="Staging", icon=render_icon("staging")),
        st.Page("pages/3_dev/2_intermediate.py", title="Intermediate", icon=render_icon("intermediate")),
        st.Page("pages/3_dev/3_marts.py", title="Marts", icon=render_icon("marts")),
        st.Page("pages/3_dev/4_exposures.py", title="BI Tables", icon=render_icon("exposures")),
    ]

# Only expose the development environment tabs locally



# --- SIDEBAR & BRANDING ---
with st.sidebar:
    st.markdown(f"# {render_icon('logo')} Greenlab")
    st.caption(f"{get_git_version()}")
    
    st.divider()
    
    # current_theme = get_current_theme()
    # is_light = current_theme == "light"
    
    # def on_theme_change():
    #     new_theme = "light" if st.session_state.theme_toggle else "dark"
    #     if new_theme != current_theme:
    #         set_theme(new_theme)
            
    # st.toggle("Modo Claro", value=is_light, key="theme_toggle", on_change=on_theme_change)

# --- NAVIGATION ---
pg = st.navigation(pages)

if "model" in st.query_params:
    st.session_state["selected_model"] = st.query_params["model"]
    if pg.title != "view Model":
        st.switch_page("pages/others/model_details.py")

# --- RUN NAVIGATION ---
pg.run()