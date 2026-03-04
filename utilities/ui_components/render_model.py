import streamlit as st

def render_model_ui(df, source_name=None, table_name=None):
    """
    Renders a standard UI component for a data model summary.
    Includes shape, columns, and the dataframe.
    Optionally fetches and displays description from YAML config.
    """

    st.subheader(table_name)

    st.dataframe(df)

    col_count = len(df.columns)
    row_count = len(df)
    st.markdown(f"**Shape:** `{row_count:,} rows` × `{col_count} columns`")
    
    # Format dtypes: column_name : type (aligned)
    max_col_width = max(len(col) for col in df.columns)
    schema_str = "\n".join([f"{col.ljust(max_col_width)} : {dtype}" for col, dtype in df.dtypes.items()])
    
    with st.expander("View columns", expanded=True):
        st.code(schema_str, language="python")

    st.divider()