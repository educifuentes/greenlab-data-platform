import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_any_dtype,
)

def explorer_de_datos(df: pd.DataFrame, key_prefix: str = "") -> pd.DataFrame:
    """
    Data explorer widget.
    Allows filtering a dataframe with an English UI.
    """
    if not key_prefix:
        if "_explorer_counter" not in st.session_state:
            st.session_state._explorer_counter = 0
        st.session_state._explorer_counter += 1
        key_prefix = f"_explorer_{st.session_state._explorer_counter}"

    df = df.copy()

    with st.container():
        to_filter_columns = st.multiselect(
            "Filter dataframe on", 
            df.columns,
            placeholder="Choose columns...",
            key=f"{key_prefix}_columns"
        )
        
        for col in to_filter_columns:
            # Drop NAs to prevent errors when identifying types, min or max
            non_na_series = df[col].dropna()
            
            # Check if it's a category or has few unique values
            if isinstance(df[col].dtype, pd.CategoricalDtype) or non_na_series.nunique() < 10:
                selected = st.multiselect(
                    f"Values for {col}",
                    non_na_series.unique(),
                    default=list(non_na_series.unique()),
                    key=f"{key_prefix}_{col}_cat"
                )
                df = df[df[col].isin(selected)]
                
            # Numeric columns
            elif is_numeric_dtype(df[col]):
                if non_na_series.empty:
                    continue
                _min = float(non_na_series.min())
                _max = float(non_na_series.max())
                step = (_max - _min) / 100.0 if _max > _min else 1.0
                step = float(step)
                
                # Protect against sliders crashing on identical bounds
                if _min == _max:
                    _max += 0.01

                selected_range = st.slider(
                    f"Range for {col}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=f"{key_prefix}_{col}_num"
                )
                df = df[df[col].between(selected_range[0], selected_range[1])]
                
            # Date columns
            elif is_datetime64_any_dtype(df[col]):
                if non_na_series.empty:
                    continue
                    
                min_date = non_na_series.min()
                max_date = non_na_series.max()
                
                if pd.isna(min_date) or pd.isna(max_date):
                    continue
                    
                min_val = min_date.date() if hasattr(min_date, "date") else min_date
                max_val = max_date.date() if hasattr(max_date, "date") else max_date
                
                # Protect against identical bounds 
                if min_val == max_val:
                    selected_dates = st.date_input(
                        f"Date for {col}",
                        value=min_val,
                        key=f"{key_prefix}_{col}_date"
                    )
                    start = pd.to_datetime(selected_dates)
                    df = df[df[col] >= start]
                else:
                    selected_dates = st.date_input(
                        f"Date range for {col}",
                        value=(min_val, max_val),
                        min_value=min_val,
                        max_value=max_val,
                        key=f"{key_prefix}_{col}_date"
                    )
                    if len(selected_dates) == 2:
                        start, end = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
                        df = df[(df[col] >= start) & (df[col] <= end)]
            
            # Text / Other columns
            else:
                search_term = st.text_input(
                    f"Search pattern in {col}",
                    key=f"{key_prefix}_{col}_text"
                )
                if search_term:
                    df = df[df[col].astype(str).str.contains(search_term, case=False, na=False)]

    return df
