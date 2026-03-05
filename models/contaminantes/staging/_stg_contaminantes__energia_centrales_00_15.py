import pandas as pd


def stg_contaminantes__energia_centrales_00_15():
    df = pd.read_csv("models/contaminantes/staging/energia/2000 al 2015 - SIC-Table 1.csv")
    return df

    