import pandas as pd
from models.exposures.termoelectricas._exp_termoelectricas__emisiones_long import exp_termoelectricas__emisiones_long

def exp_termoelectricas__emisiones_by_hour():
    df = exp_termoelectricas__emisiones_long()
    
    df['fecha'] = pd.to_datetime(df['fecha']).dt.floor('h')
    
    group_cols = ['chimenea', 'fecha', 'contaminante', 'unidad', 'nombre_central']
    df_agg = df.groupby(group_cols, as_index=False)['concentracion'].sum()
    
    return df_agg
