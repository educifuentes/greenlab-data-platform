from models.staging.geografia._stg_geografia__codigos_pais import stg_geografia__codigos_pais

def dim_geografia__paises():
    df = stg_geografia__codigos_pais()
    return df
