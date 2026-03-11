import streamlit as st

from models.generacion_electrica.finals._fct_emisiones_energia import fct_emisiones_energia

st.title("Data Contaminantes")

st.subheader("Analisis Exploratorio")

df_energia = fct_emisiones_energia()


df_energia["year"] = df_energia["fecha"].apply(lambda d: d.year if d else None)

pivot = (
    df_energia
    .groupby(["year", "nombre_central"])
    .agg(
        fechas_distintas=("fecha", "nunique"),
        fecha_min=("fecha", "min"),
        fecha_max=("fecha", "max"),
        n_rows=("fecha", "count"),
    )
    .reset_index()
    .sort_values(["year", "nombre_central"])
)

st.dataframe(pivot, use_container_width=True)