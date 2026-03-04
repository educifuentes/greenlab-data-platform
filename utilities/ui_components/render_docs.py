import streamlit as st
import yaml
import os

def get_simple_type(t):
    if not t: return "---"
    t = str(t).lower()
    if any(x in t for x in ["str", "varchar", "text", "string"]): return "Texto"
    if any(x in t for x in ["int", "float", "number", "numeric", "decimal"]): return "Número"
    if "bool" in t: return "Booleano"
    if any(x in t for x in ["date", "time", "stamp"]): return "Fecha"
    return "Otro"

def render_model_docs(yaml_path, kind="table", target_name=None):
    """
    Lee un archivo YAML de documentación (formato dbt/sources/semantic) y lo renderiza
    con un diseño limpio y profesional en Streamlit.
    """
    if not os.path.exists(yaml_path):
        st.error(f"⚠️ Archivo no encontrado: `{yaml_path}`")
        return

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo YAML: {e}")
        return

    if not data:
        st.warning("El archivo YAML está vacío.")
        return

    # Extract items to display based on keywords
    items = []
    
    # 1. Check for standard dbt models/metrics
    items.extend(data.get('models', []))
    items.extend(data.get('metrics', []))
    
    # 2. Check for dbt sources
    sources_data = data.get('sources', {})
    if isinstance(sources_data, list):
        for src in sources_data:
            items.extend(src.get('tables', []))
    elif isinstance(sources_data, dict):
        # Handle the custom structure in _src_censos.yml
        for source_name, source_content in sources_data.items():
            if isinstance(source_content, dict):
                items.extend(source_content.get('tables', []))

    # 3. Check for semantic models (Semantic Layer)
    items.extend(data.get('semantic_models', []))

    # Filter by name if requested
    if target_name:
        items = [item for item in items if item.get('name') == target_name]

    if not items:
        if target_name:
            st.warning(f"No se encontró información para '{target_name}' en el archivo.")
        else:
            st.warning("No se encontró información de modelos, fuentes o métricas en el archivo.")
        return

    for item in items:
        name = item.get('name', 'Sin Nombre')
        description = item.get('description', 'Sin descripción disponible.')
        
        with st.container():
            if kind == "metrics" or 'measures' in item:
                st.subheader(f"Métrica: {name}")
            else:
                st.subheader(f"Tabla: {name}")
            
            st.info(description)
            
            # Display columns if present
            if 'columns' in item:
                st.markdown("**Columnas:**")
                table_content = "| Columna | Descripción | Tipo |\n| :--- | :--- | :--- |\n"
                
                for col in item['columns']:
                    col_name = f"`{col.get('name', '')}`"
                    col_desc = col.get('description', '---')
                    raw_type = col.get('data_type') or col.get('type', '')
                    tipo = get_simple_type(raw_type)
                    table_content += f"| {col_name} | {col_desc} | {tipo} |\n"
                
                st.markdown(table_content)

            # Display measures if present (Semantic layer)
            if 'measures' in item:
                st.markdown("**Medidas:**")
                measures_content = "| Medida | Tipo | Descripción |\n| :--- | :--- | :--- |\n"
                for m in item.get('measures', []):
                    m_name = f"`{m.get('name', '')}`"
                    m_type = m.get('type', '---')
                    m_desc = m.get('description', '---')
                    measures_content += f"| {m_name} | {m_type} | {m_desc} |\n"
                st.markdown(measures_content)

            # Display entities if present (Semantic layer)
            if 'entities' in item:
                with st.expander("Ver Entidades"):
                    for e in item.get('entities', []):
                        st.write(f"- **{e.get('name', '')}** ({e.get('type', '')})")

            st.divider()
