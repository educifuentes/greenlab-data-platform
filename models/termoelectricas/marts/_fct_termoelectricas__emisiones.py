import pandas as pd
from models.termoelectricas.intermediate._int_termoelectricas__emisiones import int_termoelectricas__emisiones
from helpers.utilities.build_model_lineage import build_model_lineage

def fct_termoelectricas__emisiones():
    df = int_termoelectricas__emisiones()
    df.attrs.update(build_model_lineage())

    return df
