import pandas as pd

from models.marts.termoelectricas._fct_termoelectricas__emisiones import fct_termoelectricas__emisiones

def exp_termoelectricas__emisiones_por_dia():
    df = fct_termoelectricas__emisiones()
    
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
