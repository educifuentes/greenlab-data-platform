import streamlit as st

from utilities.ui_components.icons import ICONS, render_icon


st.title(f"{render_icon('logo')} Greenlab Data Platform")

st.header("Features")

st.markdown("- Catalogo de datos")
st.markdown("- Replicabilidad en trasnformciones en el data pipleline")
st.markdown("- Tranparencia gracias a Control de versiones (uso de git)")
st.markdown("- Podrorso y felxible: python para automatiuzar casi cualquier escensario")
st.markdown("- UI amigable y facil de usar")



st.subheader("Ejemplos")

st.page_link("pages/1_views/3_contaminantes.py", icon=":material/co2:")
