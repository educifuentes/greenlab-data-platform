import pandas as pd
from models.intermediate.central_electrica._int_central_electrica__energia_centrales import int_central_electrica__energia_centrales
from helpers.utilities.build_model_lineage import build_model_lineage

def fct_central_electrica():
    df = int_central_electrica__energia_centrales()
    
    id_vars = [
        'nombre_central', 'llave_nombre', 'fuente_tipo', 'fuente_subtipo', 
        'region', 'energia_tipo', 'factor_ernc', 'fecha'
    ]
    hora_cols = [col for col in df.columns if col.startswith('hora_')]
    
    # Filter id_vars to only include those present in the dataframe
    id_vars = [col for col in id_vars if col in df.columns]
    
    df = df.melt(
        id_vars=id_vars,
        value_vars=hora_cols,
        var_name='hora',
        value_name='energia_generada'
    )
    
    # Clean up the 'hora' column to be an integer
    df['hora'] = df['hora'].astype(str).str.replace('hora_', '').astype(int)
    
    # Ensure final columns are in the requested order (preserving only those that exist)
    final_cols = [
        'nombre_central', 'llave_nombre', 'fuente_tipo', 'fuente_subtipo', 
        'region', 'energia_tipo', 'factor_ernc', 'fecha', 'hora', 'energia_generada'
    ]
    final_cols = [c for c in final_cols if c in df.columns]
    df = df[final_cols]
    
    df.attrs.update(build_model_lineage())

    return df