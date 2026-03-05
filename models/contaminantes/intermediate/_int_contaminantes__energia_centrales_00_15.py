import pandas as pd

from models.contaminantes.staging._stg_contaminantes__energia_centrales_00_15 import stg_contaminantes__energia_centrales_00_15

def int_contaminantes__energia_centrales_00_15():
    df = stg_contaminantes__energia_centrales_00_15()

    rename_dict = {
        ""
    }
    return df.rename(columns=rename_dict)