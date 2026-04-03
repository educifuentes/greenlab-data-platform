import pandas as pd

from helpers.utilities.load_source import load_source
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.constants.nrows import NROWS
from helpers.utilities.build_model_lineage import build_model_lineage


def stg_geografia__codigos_provincia():
    file_path, sheet_name = get_source_metadata(
        "codigos_provincia",
        "models/sources/geografia/_src_geografia.yml"
    )
    df = load_source(file_path, format="csv", nrows=NROWS)

    df.attrs.update(build_model_lineage())

    return df
