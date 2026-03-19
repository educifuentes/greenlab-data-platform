import pandas as pd
from models.termoelectricas.intermediate._int_termoelectricas__emisiones import int_termoelectricas__emisiones

def fct_termoelectricas__emisiones():
    df = int_termoelectricas__emisiones()
    return df
