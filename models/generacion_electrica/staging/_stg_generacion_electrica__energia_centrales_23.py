import pandas as pd

from helpers.load_source_from_excel import load_source_from_excel
from helpers.constants.nrows import NROWS


def stg_generacion_electrica__energia_centrales_23():
    df = load_source_from_excel("Generacion de Energia por Central - 2023", nrows=NROWS)

    return df
