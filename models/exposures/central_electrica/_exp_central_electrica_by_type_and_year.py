import pandas as pd
from models.marts.central_electrica._fct_central_electrica import fct_central_electrica
from helpers.utilities.build_model_lineage import build_model_lineage

def exp_central_electrica_by_type_and_year():
    df = fct_central_electrica()
    
    # Identify the 24 hour columns
    hora_cols = [col for col in df.columns if col.startswith('hora_')]
    
    # Make sure we have numbers and fill NaNs
    df[hora_cols] = df[hora_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # Sum the hourly values to get the daily total energy
    df['total_energy'] = df[hora_cols].sum(axis=1)
    
    # Convert fecha to datetime to extract the year
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['year'] = df['fecha'].dt.year
    
    # Pivot by year and energia_tipo, summing total_energy
    final_df = df.pivot_table(index='year', columns='energia_tipo', values='total_energy', aggfunc='sum').reset_index()
    
    # Clean up column names (optional, removes the axis name 'energia_tipo')
    final_df.columns.name = None
    
    final_df.attrs.update(build_model_lineage())

    return final_df