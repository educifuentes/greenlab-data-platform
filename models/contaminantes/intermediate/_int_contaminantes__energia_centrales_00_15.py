import pandas as pd

from models.contaminantes.staging._stg_contaminantes__energia_centrales_00_15 import stg_contaminantes__energia_centrales_00_15

from utilities.data_transformations.column_names_tosnakecase import to_snake_case

def int_contaminantes__energia_centrales_00_15():
    df = stg_contaminantes__energia_centrales_00_15()

    df = to_snake_case(df)

    return df