from models.staging.geografia._stg_geografia__codigos_region import stg_geografia__codigos_region

def dim_geografia__regiones():
    df = stg_geografia__codigos_region()
    return df
