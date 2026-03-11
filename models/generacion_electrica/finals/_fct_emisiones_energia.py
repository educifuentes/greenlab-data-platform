from models.generacion_electrica.intermediate._int_generacion_electrica__energia_centrales import int_generacion_electrica__energia_centrales

def fct_emisiones_energia():
    df = int_generacion_electrica__energia_centrales()
    return df