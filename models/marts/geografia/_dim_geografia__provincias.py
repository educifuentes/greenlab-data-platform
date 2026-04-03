from models.staging.geografia._stg_geografia__codigos_provincia import stg_geografia__codigos_provincia

def dim_geografia__provincias():
    df = stg_geografia__codigos_provincia()
    return df
