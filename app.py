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
# Defining the pages based on the directory structure
pages = {
    "Vistas": [
        st.Page("pages/1_views/1_home.py", title="Home", icon=render_icon("logo"), default=True),
        st.Page("pages/1_views/2_generacion_electrica.py", title="Generacion Electrica", icon=render_icon("co2")),
        st.Page("pages/1_views/3_lineage.py", title="Lineage", icon=render_icon("co2")),
    ],
    "Herramientas": [
        st.Page("pages/2_tools/1_catalog.py", title="Catalogo", icon=render_icon("catalog")),
        st.Page("pages/2_tools/2_documentation.py", title="Documentación", icon=render_icon("documentation"))
    ],
    "Desarrollo": [
        st.Page("pages/3_dev/1_staging.py", title="Staging", icon=render_icon("staging")),
        st.Page("pages/3_dev/2_intermediate.py", title="Intermediate", icon=render_icon("intermediate")),
        st.Page("pages/3_dev/3_finals.py", title="Finals", icon=render_icon("finals")),
        st.Page("pages/3_dev/4_bi_tables.py", title="BI Tables", icon=render_icon("bi_tables")),
    ],
}

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

# --- RUN NAVIGATION ---
pg.run()