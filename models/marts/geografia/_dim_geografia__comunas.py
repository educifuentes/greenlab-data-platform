from models.staging.geografia._stg_geografia__codigos_comuna import stg_geografia__codigos_comuna

def dim_geografia__comunas():
    df = stg_geografia__codigos_comuna()
    return df
