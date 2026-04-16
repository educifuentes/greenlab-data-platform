import pandas as pd
from models.intermediate.termoelectricas._int_termoelectricas__emisiones import int_termoelectricas__emisiones
from helpers.utilities.build_model_lineage import build_model_lineage

def fct_termoelectricas__emisiones():
    df = int_termoelectricas__emisiones()

    # reshape to long

        
    id_vars = ['chimenea', 'fecha', 'nombre_central']
    
    col_mapping = {
        'concentracion_nox_ppm': ('nox', 'ppm'),
        'concentracion_nox_mg_nm3': ('nox', 'mg_nm3'),
        'concentracion_nox_mg_mwh': ('nox', 'mg_mwh'),
        'concentracion_so2_ppm': ('so2', 'ppm'),
        'concentracion_so2_mg_nm3': ('so2', 'mg_nm3'),
        'concentracion_so2_mg_mwh': ('so2', 'mg_mwh'),
        'concentracion_porcentaje_co2': ('co2', 'porcentaje'),
        'concentracion_co2_ton_mwh': ('co2', 'ton_mwh'),
        'oxigeno_porcentaje_base_seca': ('o2', 'porcentaje'), 
    }
    
    # Parse dates safely to handle variations in original raw string format
    df['fecha'] = pd.to_datetime(df['fecha'], format='mixed', dayfirst=True)
    
    # Filter the df to only keep the id vars plus the value vars to map
    df = df[id_vars + list(col_mapping.keys())]
    
    # Unpivot to long format
    df_long = pd.melt(
        df, 
        id_vars=id_vars, 
        value_vars=list(col_mapping.keys()),
        var_name='original_column',
        value_name='concentracion'
    )
    
    # Force numeric concentration and drop NAs
    df_long['concentracion'] = pd.to_numeric(df_long['concentracion'], errors='coerce')
    df_long = df_long.dropna(subset=['concentracion'])
    
    # Infer 'contaminante' and 'unidad' from the mapping
    df_long['contaminante'] = df_long['original_column'].map(lambda x: col_mapping[x][0])
    df_long['unidad'] = df_long['original_column'].map(lambda x: col_mapping[x][1])
    
    # Remove surrogate column
    df_long = df_long.drop(columns=['original_column'])
    
    # Reorder columns exactly as requested by user
    final_columns = [
        'chimenea',
        'fecha',
        'contaminante',
        'concentracion',
        'unidad',
        'nombre_central'
    ]
    df_long = df_long[final_columns]
    

    df.attrs.update(build_model_lineage())

    return df
