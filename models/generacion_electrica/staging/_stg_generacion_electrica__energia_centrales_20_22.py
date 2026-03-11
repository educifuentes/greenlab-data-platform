import pandas as pd

from utilities.load_source_from_excel import load_source_from_excel
from utilities.constants.nrows import NROWS


def stg_generacion_electrica__energia_centrales_20_22():
    df = load_source_from_excel("Generacion de Energia por Central - 2020 a 2022", nrows=NROWS)

    return df
