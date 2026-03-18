import streamlit as st

# Retrieve query params from URL
query_params = st.query_params
model_name = query_params.get("model", "No Model Selected")

st.header(f"Model: {model_name}")
st.markdown("description taml")

st.subheader("Lineage")



st.subheader("Data")