import pandas as pd

from models.marts.central_electrica._fct_central_electrica import fct_central_electrica
from models.marts.geografia._dim_geografia__regiones import dim_geografia__regiones


from helpers.utilities.build_model_lineage import build_model_lineage

def exp_central_electrica_generado_por_mes_region():
    df = fct_central_electrica()
    
    # Make sure we have numbers and fill NaNs
    df['energia_generada'] = pd.to_numeric(df['energia_generada'], errors='coerce').fillna(0)
    
    # Convert fecha to datetime to extract the month
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['month'] = df['fecha'].dt.to_period('M')
    
    # Generación Renovable (ERNC) calculation
    df['is_ernc'] = df.get('energia_tipo', 'Otro') == 'ERNC'
    df['generacion_renovable_ernc'] = df['energia_generada'] * df['is_ernc']

    # save attrs before grouping/merging removes them
    fct_attrs = df.attrs.copy()

    # join wirh regiones
    regiones = dim_geografia__regiones()
    df = df.merge(regiones, left_on='region', right_on='region_nombre_completo', how='left')
    
    # Group by month and nombre_central and calculate metric aggregations
    df = df.groupby(['month', 'id_region', 'region_corto']).agg(
        energia_total_generada=('energia_generada', 'sum'),
        plantas_en_operacion=('nombre_central', 'nunique')
    ).reset_index()
    
    # Restore original general attributes (withouenergia_generadat wiping out lineage logic)
    df.attrs.update(fct_attrs)
    df.attrs.update(regiones.attrs)
    
    # Rebuild complete lineage (will automatically find fct_attrs and regiones from locals)
    df.attrs.update(build_model_lineage())

    return df