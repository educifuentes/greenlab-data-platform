from models.contaminantes.intermediate._int_contaminantes__energia_centrales import int_contaminantes__energia_centrales

def fct_emisiones_energia():
    df = int_contaminantes__energia_centrales()
    return df