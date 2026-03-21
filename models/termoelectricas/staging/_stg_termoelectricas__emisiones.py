import pandas as pd
from helpers.utilities.load_source import load_source
from helpers.build_model_lineage import build_model_lineage

def stg_termoelectricas__emisiones():
    df = load_source(
        "Emisiones de centrales termoelectricas - 2020",
        yaml_path="models/termoelectricas/sources/_src_termoelectricas.yml",
        encoding="latin-1",
        sep=";"
    )
    df.attrs.update(build_model_lineage())

    return df
