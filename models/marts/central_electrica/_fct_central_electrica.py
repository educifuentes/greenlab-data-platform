import pandas as pd
from models.intermediate.central_electrica._int_central_electrica__energia_centrales import int_central_electrica__energia_centrales
from helpers.utilities.build_model_lineage import build_model_lineage

def fct_central_electrica():
    df = int_central_electrica__energia_centrales()
    
    col_map = {
        'nombre_central': 'power_plant_name',
        'llave_nombre': 'name_key',
        'fuente_tipo': 'source_type',
        'fuente_subtipo': 'source_subtype',
        'energia_tipo': 'energy_type',
        'factor_ernc': 'ernc_factor',
        'fecha': 'date'
    }
    df = df.rename(columns=col_map)
    
    id_vars = [
        'power_plant_name', 'name_key', 'source_type', 'source_subtype', 
        'region', 'energy_type', 'ernc_factor', 'date'
    ]
    hora_cols = [col for col in df.columns if col.startswith('hora_')]
    
    # Filter id_vars to only include those present in the dataframe
    id_vars = [col for col in id_vars if col in df.columns]
    
    df = df.melt(
        id_vars=id_vars,
        value_vars=hora_cols,
        var_name='hour',
        value_name='generated_energy'
    )
    
    # Clean up the 'hour' column to be an integer
    df['hour'] = df['hour'].astype(str).str.replace('hora_', '').astype(int)
    
    # Ensure final columns are in the requested order (preserving only those that exist)
    final_cols = [
        'power_plant_name', 'name_key', 'source_type', 'source_subtype', 
        'region', 'energy_type', 'ernc_factor', 'date', 'hour', 'generated_energy'
    ]
    final_cols = [c for c in final_cols if c in df.columns]
    df = df[final_cols]
    
    df.attrs.update(build_model_lineage())

    return df