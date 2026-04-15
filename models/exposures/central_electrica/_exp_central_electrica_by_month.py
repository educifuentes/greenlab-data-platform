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
    df['energia_total_generada'] = df[hora_cols].sum(axis=1)
    
    # Convert fecha to datetime to extract the month
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['month'] = df['fecha'].dt.to_period('M')
    
    # Generación Renovable (ERNC) calculation
    df['is_ernc'] = df.get('energia_tipo', 'Otro') == 'ERNC'
    df['generacion_renovable_ernc'] = df['energia_total_generada'] * df['is_ernc']
    
    # Group by month and nombre_central and calculate metric aggregations
    final_df = df.groupby(['month', 'nombre_central']).agg(
        energia_total_generada=('energia_total_generada', 'sum'),
        generacion_renovable_ernc=('generacion_renovable_ernc', 'sum'),
        plantas_en_operacion=('nombre_central', 'nunique')
    ).reset_index()
    
    final_df.attrs.update(build_model_lineage())

    return final_df