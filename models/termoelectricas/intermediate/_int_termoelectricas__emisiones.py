import pandas as pd
from models.termoelectricas.staging._stg_termoelectricas__emisiones import stg_termoelectricas__emisiones
from helpers.data_transformations.column_names_tosnakecase import to_snake_case
from helpers.build_model_lineage import build_model_lineage

def int_termoelectricas__emisiones():
    df = stg_termoelectricas__emisiones()
    df = to_snake_case(df)
    
    df.attrs.update(build_model_lineage())
    return df
