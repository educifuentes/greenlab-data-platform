import pandas as pd
from helpers.load_source_from_csv import load_source_dataframe
from helpers.build_model_lineage import build_model_lineage

def stg_termoelectricas__emisiones():
    df = load_source_dataframe(
        "Emisiones de centrales termoelectricas - 2020",
        yaml_path="models/termoelectricas/sources/_src_termoelectricas.yml",
        encoding="latin-1",
        sep=";"
    )
    df.attrs.update(build_model_lineage())

    return df
