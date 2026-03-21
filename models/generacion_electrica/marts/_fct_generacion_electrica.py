from models.generacion_electrica.intermediate._int_generacion_electrica__energia_centrales import int_generacion_electrica__energia_centrales
from helpers.build_model_lineage import build_model_lineage

def fct_generacion_electrica():
    df = int_generacion_electrica__energia_centrales()
    df.attrs.update(build_model_lineage())

    return df