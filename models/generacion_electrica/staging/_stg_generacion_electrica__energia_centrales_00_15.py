import pandas as pd

from helpers.utilities.load_source import load_source
from helpers.constants.nrows import NROWS
from helpers.utilities.build_model_lineage import build_model_lineage


def stg_generacion_electrica__energia_centrales_00_15():
    df = load_source("Generacion de Energia por Central - 2000 a 2015", format="excel", nrows=NROWS)

    df.attrs.update(build_model_lineage())

    return df