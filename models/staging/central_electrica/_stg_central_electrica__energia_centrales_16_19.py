import pandas as pd

from helpers.utilities.load_source import load_source
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.constants.nrows import NROWS
from helpers.utilities.build_model_lineage import build_model_lineage


def stg_central_electrica__energia_centrales_16_19():
    file_path, sheet_name = get_source_metadata(
        "Generacion de Energia por Central - 2016 a 2019",
        "models/sources/central_electrica/_src_central_electrica.yml"
    )
    df = load_source(file_path, format="excel", sheet_name=sheet_name, nrows=NROWS)

    df.attrs.update(build_model_lineage())

    return df
