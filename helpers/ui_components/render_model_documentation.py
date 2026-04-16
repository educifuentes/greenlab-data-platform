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
                                md_table = "| Columna | Descripción |\n|---|---|\n"
                                for col in columns:
                                    col_name = col.get("name", "")
                                    col_desc = col.get("description", "")
                                    md_table += f"| `{col_name}` | {col_desc} |\n"
                                st.markdown(md_table)
                            
                            metrics = model_doc.get("metrics", [])
                            if metrics:
                                st.markdown("#### Métricas Asociadas")
                                for m in metrics:
                                    st.write(f"- `{m}`")
                            return
            except Exception as e:
                st.error(f"Error leyendo la documentación YAML: {e}")
                return
                
    st.info("No hay documentación (archivo .yml) disponible para este modelo.")

def render_metrics_documentation(schema: str):
    """
    Looks for a <schema>_metrics.yml file inside models/metrics/<schema>/ 
    and renders the metrics documentation.
    """
    yml_path = os.path.join("models", "metrics", f"{schema}_metrics.yml")
    
    if os.path.exists(yml_path):
        try:
            with open(yml_path, 'r', encoding='utf-8') as f:
                docs = yaml.safe_load(f)
                
            if docs and "metrics" in docs:
                metrics_list = docs["metrics"]
                
                # Group metrics by group_name
                groups = {}
                for m in metrics_list:
                    g_name = m.get("group_name", "Métricas")
                    if g_name not in groups:
                        groups[g_name] = []
                    groups[g_name].append(m)
                
                for group_name, cols in groups.items():
                    with st.expander(f"{group_name}", expanded=True):
                        st.markdown("#### Detalles de las Métricas")
                        md_table = "| Métrica | Descripción | Cálculo | Unidad |\n|---|---|---|---|\n"
                        for col in cols:
                            col_name = col.get("name", "")
                            col_desc = col.get("description", "")
                            col_calc = col.get("calculation", "")
                            col_unit = col.get("unidad", "")
                            
                            md_table += f"| `{col_name}` | {col_desc} | {col_calc} | {col_unit} |\n"
                        st.markdown(md_table)
                return
        except Exception as e:
            st.error(f"Error leyendo la documentación YAML de métricas: {e}")
            return
            
    st.info("No hay documentación de métricas (archivo .yml) disponible para este esquema.")
