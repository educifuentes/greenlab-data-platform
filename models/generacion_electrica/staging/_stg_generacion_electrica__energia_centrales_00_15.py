import pandas as pd

from utilities.load_source_from_excel import load_source_from_excel
from utilities.constants.nrows import NROWS


def stg_generacion_electrica__energia_centrales_00_15():
    df = load_source_from_excel("Generacion de Energia por Central - 2000 a 2015", nrows=NROWS)

    return df