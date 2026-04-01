import pandas as pd

from helpers.utilities.load_source import load_source
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.constants.nrows import NROWS
from helpers.utilities.build_model_lineage import build_model_lineage


def stg_generacion_electrica__energia_centrales_20_22():
    file_path, sheet_name = get_source_metadata(
        "Generacion de Energia por Central - 2020 a 2022",
        "models/sources/generacion_electrica/_src_generacion_electrica.yml"
    )
    df = load_source(file_path, format="excel", sheet_name=sheet_name, nrows=NROWS)

    df.attrs.update(build_model_lineage())

    return df
