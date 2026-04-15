import pandas as pd
from models.exposures.termoelectricas._exp_termoelectricas__emisiones_long import exp_termoelectricas__emisiones_long

def exp_termoelectricas__emisiones_by_day():
    df = exp_termoelectricas__emisiones_long()
    
    df['fecha'] = pd.to_datetime(df['fecha']).dt.floor('D')
    
    group_cols = ['chimenea', 'fecha', 'contaminante', 'unidad', 'nombre_central']
    df_agg = df.groupby(group_cols, as_index=False)['concentracion'].sum()
    
    # Métricas Demostrativas (según termoelectricas_metrics.yml)
    df_agg['emisiones_co2_totales'] = df_agg.apply(
        lambda row: row['concentracion'] if row['contaminante'] == 'CO2' else 0, axis=1
    )
    df_agg['emisiones_mp_totales'] = df_agg.apply(
        lambda row: row['concentracion'] if row['contaminante'] == 'MP' else 0, axis=1
    )
    
    return df_agg
