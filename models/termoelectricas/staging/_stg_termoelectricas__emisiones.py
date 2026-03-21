import pandas as pd
from helpers.utilities.load_source import load_source
from helpers.utilities.get_source_metadata import get_source_metadata
from helpers.utilities.build_model_lineage import build_model_lineage

def stg_termoelectricas__emisiones():
    file_path, sheet_name = get_source_metadata(
        "Emisiones de centrales termoelectricas - 2020",
        "models/termoelectricas/sources/_src_termoelectricas.yml"
    )
    df = load_source(
        file_path,
        sheet_name=sheet_name,
        encoding="latin-1",
        sep=";"
    )
    df.attrs.update(build_model_lineage())

    return df
