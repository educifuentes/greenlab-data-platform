import pandas as pd

from helpers.utilities.load_source import load_source
from helpers.constants.nrows import NROWS
from helpers.utilities.build_model_lineage import build_model_lineage


def stg_generacion_electrica__energia_centrales_20_22():
    df = load_source("Generacion de Energia por Central - 2020 a 2022", format="excel", nrows=NROWS)

    df.attrs.update(build_model_lineage())

    return df
