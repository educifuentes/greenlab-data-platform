import pandas as pd
from models.marts.central_electrica._fct_central_electrica import fct_central_electrica
from helpers.utilities.build_model_lineage import build_model_lineage

def exp_central_electrica_by_month():
    df = fct_central_electrica()
    
    # Identify the 24 hour columns
    hora_cols = [col for col in df.columns if col.startswith('hora_')]
    
    # Make sure we have numbers and fill NaNs
    df[hora_cols] = df[hora_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # Sum the hourly values to get the daily total energy
    df['total_energy'] = df[hora_cols].sum(axis=1)
    
    # Convert fecha to datetime to extract the month
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['month'] = df['fecha'].dt.to_period('M')
    
    # Group by month and nombre_central and sum
    final_df = df.groupby(['month', 'nombre_central'])['total_energy'].sum().reset_index()
    
    final_df.attrs.update(build_model_lineage())

    return final_df