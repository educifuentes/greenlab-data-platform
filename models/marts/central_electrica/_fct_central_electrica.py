from models.intermediate.central_electrica._int_central_electrica__energia_centrales import int_central_electrica__energia_centrales
from helpers.utilities.build_model_lineage import build_model_lineage

def fct_central_electrica():
    df = int_central_electrica__energia_centrales()
    df.attrs.update(build_model_lineage())

    return df