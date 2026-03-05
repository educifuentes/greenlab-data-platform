import pandas as pd
from utilities.load_source import load_source_dataframe


def stg_contaminantes__energia_centrales_00_15():
    df = load_source_dataframe("Generacion de Energia por Central - 2000 al 2015")
    return df