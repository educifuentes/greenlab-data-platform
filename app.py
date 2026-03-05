import streamlit as st

from utilities.ui_components.icons import ICONS, render_icon
from utilities.get_version import get_git_version

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
        st.Page("pages/1_views/1_overview.py", title="Overview", icon=render_icon("dashboard")),
        st.Page("pages/1_views/2_query_builder_semantic_models.py", title="Query Builder", icon=render_icon("query")),
        st.Page("pages/1_views/3_contaminantes.py", title="Contaminantes", icon=render_icon("co2")),
    ],
    "Herramientas": [
        st.Page("pages/2_tools/1_documentation.py", title="Documentación", icon=render_icon("documentation")),
        st.Page("pages/2_tools/2_validations.py", title="Validaciones de Datos", icon=render_icon("check")),
        st.Page("pages/2_tools/3_explorer.py", title="Explorador de Datos", icon=render_icon("search")),
        st.Page("pages/2_tools/4_catalog.py", title="Catalogo", icon=render_icon("catalog")),
    ],
    "Desarrollo": [
        st.Page("pages/3_dev/1_staging.py", title="Staging", icon=render_icon("staging")),
        st.Page("pages/3_dev/2_intermediate.py", title="Intermediate", icon=render_icon("intermediate")),
        st.Page("pages/3_dev/3_finals.py", title="Finals", icon=render_icon("finals")),
        st.Page("pages/3_dev/4_bi_tables.py", title="BI Tables", icon=render_icon("bi_tables")),
    ],
}

# --- NAVIGATION ---
pg = st.navigation(pages)

# --- SIDEBAR & BRANDING ---
with st.sidebar:
    st.markdown(f"# {render_icon('logo')} Greenlab")
    st.caption(f"{get_git_version()}")
    st.markdown("---")

# --- RUN NAVIGATION ---
pg.run()