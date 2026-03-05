import pandas as pd

from utilities.load_source_from_excel import load_source_from_excel


def stg_contaminantes__energia_centrales_00_15():
    df = load_source_from_excel("Generacion de Energia por Central - 2000 a 2015")

    # sample 500 rows
    df = df.head(10)

    return df