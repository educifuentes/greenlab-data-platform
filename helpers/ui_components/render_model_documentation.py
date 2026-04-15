import os
import streamlit as st
import yaml
from helpers.utilities.model_catalog import build_global_model_registry

def render_model_documentation(model_name: str):
    """
    Looks for a .yml file alongside the model and renders its description and column dictionary.
    """
    if not model_name:
        return
        
    df_catalog = build_global_model_registry()
    model_row = df_catalog[df_catalog["model"] == model_name]
    
    if not model_row.empty:
        schema = model_row.iloc[0]["schema"]
        stage = model_row.iloc[0]["stage"]
        
        # Build the expected path for the yaml configuration inside the exact same folder
        yml_path = os.path.join("models", stage, schema, f"{model_name}.yml")
        
        if os.path.exists(yml_path):
            try:
                with open(yml_path, 'r', encoding='utf-8') as f:
                    docs = yaml.safe_load(f)
                    
                if docs and "models" in docs:
                    for model_doc in docs["models"]:
                        if model_doc.get("name") == model_name:
                            desc = model_doc.get("description", "Sin descripción.")
                            st.write(desc)
                            
                            columns = model_doc.get("columns", [])
                            if columns:
                                st.markdown("#### Diccionario de Datos")
                                md_table = "| Columna | Descripción |\n|---|---|\n"
                                for col in columns:
                                    col_name = col.get("name", "")
                                    col_desc = col.get("description", "")
                                    md_table += f"| `{col_name}` | {col_desc} |\n"
                                st.markdown(md_table)
                            return
            except Exception as e:
                st.error(f"Error leyendo la documentación YAML: {e}")
                return
                
    st.info("No hay documentación (archivo .yml) disponible para este modelo.")
